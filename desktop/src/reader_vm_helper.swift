import Foundation
import Virtualization

// Unwired candidate. Configuration authenticity and owned process identity must be
// established by a separate verified platform adapter before any integration.
@available(macOS 12.0, *)
final class ReaderVMController: NSObject, VZVirtualMachineDelegate {
    struct Identity: Equatable {
        let tenantID: String
        let companyID: String
        let workRef: String
        let taskID: String
        let employeeID: String
        let bindingRef: String

        var complete: Bool {
            [tenantID, companyID, workRef, taskID, employeeID, bindingRef]
                .allSatisfy { !$0.isEmpty }
        }
    }

    enum State: String {
        case cold, starting, running, stopRequested, frameworkStopObserved, unknown
    }

    enum ControllerError: Error { case invalidBinding }

    private let queue: DispatchQueue
    private let machine: VZVirtualMachine
    private let identity: Identity
    private let nonce: String
    private var state: State = .cold
    private var cancelAfterStart = false
    private var startCallbackSeen = false
    private var stopCallbackSeen = false
    private var vmFailureObserved = false

    init(configuration: VZVirtualMachineConfiguration, identity: Identity, nonce: String) throws {
        guard identity.complete, nonce.utf8.count == 48,
              nonce.utf8.allSatisfy({ (48...57).contains($0) || (97...102).contains($0) }) else {
            throw ControllerError.invalidBinding
        }
        try configuration.validate()
        let vmQueue = DispatchQueue(label: "com.curis.reader.vm.controller")
        self.queue = vmQueue
        self.machine = VZVirtualMachine(configuration: configuration, queue: vmQueue)
        self.identity = identity
        self.nonce = nonce
        super.init()
        vmQueue.sync { self.machine.delegate = self }
    }

    private func deliver(_ result: State, to completion: @escaping (State) -> Void) {
        DispatchQueue.global(qos: .userInitiated).async { completion(result) }
    }

    func start(identity: Identity, nonce: String, completion: @escaping (State) -> Void) {
        queue.async {
            guard identity == self.identity, nonce == self.nonce, self.state == .cold else {
                self.deliver(.unknown, to: completion)
                return
            }
            self.state = .starting
            var delivered = false
            func finish(_ value: State) {
                guard !delivered else { return }
                delivered = true
                self.deliver(value, to: completion)
            }
            self.queue.asyncAfter(deadline: .now() + 90) {
                guard !delivered else { return }
                self.cancelAfterStart = true
                self.state = .unknown
                finish(.unknown)
            }
            self.machine.start { result in
                let started: Bool
                switch result {
                case .success: started = true
                case .failure: started = false
                }
                guard !self.startCallbackSeen else { return }
                self.startCallbackSeen = true
                if self.cancelAfterStart {
                    if started && (self.machine.state == .running || self.machine.state == .paused) {
                        self.queue.asyncAfter(deadline: .now() + 90) {
                            if !self.stopCallbackSeen {
                                self.state = .unknown
                            }
                        }
                        self.machine.stop { stopError in
                            guard !self.stopCallbackSeen else { return }
                            self.stopCallbackSeen = true
                            self.state = !self.vmFailureObserved && stopError == nil && self.machine.state == .stopped
                                ? .frameworkStopObserved : .unknown
                        }
                    } else {
                        self.state = .unknown
                    }
                    finish(.unknown)
                    return
                }
                guard self.state == .starting else {
                    self.state = .unknown
                    finish(.unknown)
                    return
                }
                self.state = started ? .running : .unknown
                finish(self.state)
            }
        }
    }

    func stop(identity: Identity, nonce: String, completion: @escaping (State) -> Void) {
        queue.async {
            guard identity == self.identity, nonce == self.nonce else {
                self.deliver(.unknown, to: completion)
                return
            }
            if self.state == .cold {
                // A stop admitted before start prevents a later queued start.
                // No VM or guest termination is asserted by this transition.
                self.state = .stopRequested
                self.deliver(.unknown, to: completion)
                return
            }
            if self.state == .starting {
                self.cancelAfterStart = true
                self.state = .stopRequested
                self.deliver(.unknown, to: completion)
                return
            }
            guard self.state == .running else {
                self.deliver(self.state == .frameworkStopObserved ? .frameworkStopObserved : .unknown, to: completion)
                return
            }
            self.state = .stopRequested
            var delivered = false
            func finish(_ value: State) {
                guard !delivered else { return }
                delivered = true
                self.deliver(value, to: completion)
            }
            self.queue.asyncAfter(deadline: .now() + 90) {
                guard !delivered else { return }
                self.state = .unknown
                finish(.unknown)
            }
            self.machine.stop { error in
                guard !self.stopCallbackSeen else { return }
                self.stopCallbackSeen = true
                self.state = !self.vmFailureObserved && error == nil && self.machine.state == .stopped
                    ? .frameworkStopObserved : .unknown
                finish(self.state)
            }
        }
    }

    func stopFromOwnedChannel(frame: Data, identity: Identity, nonce: String,
                              completion: @escaping (State) -> Void) {
        // Only the separately verified stop channel may call this method.
        guard frame == Data("STOP\n".utf8) else {
            deliver(.unknown, to: completion)
            return
        }
        stop(identity: identity, nonce: nonce, completion: completion)
    }

    func observe(identity: Identity, nonce: String, completion: @escaping (State) -> Void) {
        queue.async {
            guard identity == self.identity, nonce == self.nonce else {
                self.deliver(.unknown, to: completion)
                return
            }
            self.deliver(self.state, to: completion)
        }
    }

    func guestDidStop(_ virtualMachine: VZVirtualMachine) {
        guard virtualMachine === machine else { return }
        if state != .stopRequested && state != .frameworkStopObserved {
            cancelAfterStart = true
            state = .unknown
        }
    }

    func virtualMachine(_ virtualMachine: VZVirtualMachine, didStopWithError error: Error) {
        guard virtualMachine === machine else { return }
        vmFailureObserved = true
        cancelAfterStart = true
        state = .unknown
    }
}
