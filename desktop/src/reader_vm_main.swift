import Foundation
import Virtualization
import Darwin
import CryptoKit

// Unreleased entry candidate. No caller-provided path, identity, or nonce is
// accepted as proof of the helper, assets, guest, or owning Work.
private enum ReaderPlatformError: Error {
    case unavailable
    case unverifiedOwnership
}

// Candidate only: the caller must first authenticate and retain the directory,
// disk descriptor, fixed digest and Work. Existing or incomplete claims are
// never overwritten or removed; an error after creation remains UNKNOWN.
private func persistOriginalWorkClaim(directoryFD: Int32, diskFD: Int32,
                                      expectedDiskDigest: Data, binding: Data) throws {
    guard directoryFD >= 0, diskFD >= 0, expectedDiskDigest.count == 32,
          !binding.isEmpty, binding.count <= 4096 else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    var directory = stat()
    var disk = stat()
    guard fstat(directoryFD, &directory) == 0,
          (directory.st_mode & S_IFMT) == S_IFDIR,
          directory.st_uid == geteuid(), (directory.st_mode & 0o077) == 0,
          fstat(diskFD, &disk) == 0, (disk.st_mode & S_IFMT) == S_IFREG,
          disk.st_uid == geteuid(), disk.st_nlink == 1, disk.st_size > 0 else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    var hasher = SHA256()
    var offset: off_t = 0
    var buffer = [UInt8](repeating: 0, count: 1024 * 1024)
    while offset < disk.st_size {
        let wanted = min(buffer.count, Int(disk.st_size - offset))
        let count = buffer.withUnsafeMutableBytes { bytes in
            pread(diskFD, bytes.baseAddress!, wanted, offset)
        }
        if count < 0 && errno == EINTR { continue }
        guard count > 0 else { throw ReaderPlatformError.unverifiedOwnership }
        hasher.update(data: Data(buffer.prefix(count)))
        offset += off_t(count)
    }
    var hashedDisk = stat()
    guard Data(hasher.finalize()) == expectedDiskDigest,
          fstat(diskFD, &hashedDisk) == 0, hashedDisk.st_dev == disk.st_dev,
          hashedDisk.st_ino == disk.st_ino, hashedDisk.st_size == disk.st_size else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    let claimFD = openat(directoryFD, "work.claim", O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC, 0o600)
    guard claimFD >= 0 else { throw ReaderPlatformError.unverifiedOwnership }
    var claimClosed = false
    defer { if !claimClosed { _ = close(claimFD) } }
    var frame = Data("CURIS-READER-CLAIM/1\n".utf8)
    frame.append(Data("\(disk.st_dev):\(disk.st_ino):\(disk.st_size)\n".utf8))
    frame.append(expectedDiskDigest)
    frame.append(contentsOf: SHA256.hash(data: binding))
    var written = 0
    while written < frame.count {
        let count = frame.withUnsafeBytes { bytes in
            write(claimFD, bytes.baseAddress!.advanced(by: written), frame.count - written)
        }
        if count < 0 && errno == EINTR { continue }
        guard count > 0 else { throw ReaderPlatformError.unverifiedOwnership }
        written += count
    }
    var after = stat()
    guard fstat(diskFD, &after) == 0, after.st_dev == disk.st_dev,
          after.st_ino == disk.st_ino, after.st_size == disk.st_size,
          fsync(claimFD) == 0, fsync(directoryFD) == 0 else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    let closeResult = close(claimFD)
    claimClosed = true
    guard closeResult == 0 else { throw ReaderPlatformError.unverifiedOwnership }
}

private func readerProbeReply(frame: Data, role: Character) throws -> Data {
    guard role == "C" || role == "S", frame.count == 59,
          let text = String(data: frame, encoding: .ascii),
          text.hasPrefix("PROBE/1 \(role) "), text.hasSuffix("\n") else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    let nonce = text.dropFirst(10).dropLast()
    guard nonce.utf8.count == 48,
          nonce.utf8.allSatisfy({ (48...57).contains($0) || (97...102).contains($0) }) else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    return Data("READY/1 \(role) \(nonce)\n".utf8)
}

private func readerExchangeProbe(fd: Int32, role: Character) throws {
    // Caller must already own the intended inherited endpoint. This exchange
    // tests protocol consistency; it cannot authenticate a process or FD.
    guard (role == "C" && fd == 0) || (role == "S" && fd == 2) else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    let flags = fcntl(fd, F_GETFL)
    var suppress: Int32 = 1
    guard flags >= 0, fcntl(fd, F_SETFL, flags | O_NONBLOCK) == 0,
          setsockopt(fd, SOL_SOCKET, SO_NOSIGPIPE, &suppress, socklen_t(MemoryLayout<Int32>.size)) == 0 else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    let deadline = DispatchTime.now().uptimeNanoseconds + 3_000_000_000
    func wait(_ event: Int16) throws {
        while true {
            let now = DispatchTime.now().uptimeNanoseconds
            guard now < deadline else { throw ReaderPlatformError.unverifiedOwnership }
            let remaining = Int32(min((deadline - now + 999_999) / 1_000_000, UInt64(Int32.max)))
            var descriptor = pollfd(fd: fd, events: event, revents: 0)
            let result = poll(&descriptor, 1, remaining)
            if result < 0 && errno == EINTR { continue }
            guard result > 0, descriptor.revents & event != 0 else {
                throw ReaderPlatformError.unverifiedOwnership
            }
            return
        }
    }
    var request = Data()
    while !request.contains(10) {
        try wait(Int16(POLLIN))
        var bytes = [UInt8](repeating: 0, count: 60 - request.count)
        let count = read(fd, &bytes, bytes.count)
        if count < 0 && (errno == EAGAIN || errno == EINTR) { continue }
        guard count > 0 else { throw ReaderPlatformError.unverifiedOwnership }
        request.append(contentsOf: bytes.prefix(count))
        guard request.count <= 59 else { throw ReaderPlatformError.unverifiedOwnership }
    }
    let reply = try readerProbeReply(frame: request, role: role)
    var sent = 0
    while sent < reply.count {
        try wait(Int16(POLLOUT))
        let count = reply.withUnsafeBytes { buffer in
            write(fd, buffer.baseAddress!.advanced(by: sent), buffer.count - sent)
        }
        if count < 0 && (errno == EAGAIN || errno == EINTR) { continue }
        guard count > 0 else { throw ReaderPlatformError.unverifiedOwnership }
        sent += count
    }
}

@available(macOS 13.0, *)
private struct VerifiedReaderAssets {
    let diskURL: URL
    let variableStoreURL: URL
    let identity: ReaderVMController.Identity
    let nonce: String

    private init(diskURL: URL, variableStoreURL: URL,
                 identity: ReaderVMController.Identity, nonce: String) {
        self.diskURL = diskURL
        self.variableStoreURL = variableStoreURL
        self.identity = identity
        self.nonce = nonce
    }

    static func resolveFromOwnedChannel() throws -> VerifiedReaderAssets {
        // No signing anchor, peer verifier, or authenticated asset resolver is
        // available yet. Keep the entry closed until those are implemented.
        throw ReaderPlatformError.unverifiedOwnership
    }

    func requireExclusiveOriginalWork() throws {
        // A persistent disk and EFI ownership/disposition gate does not exist.
        // Do not reuse either across Work or erase them after stop.
        throw ReaderPlatformError.unverifiedOwnership
    }
}

@available(macOS 13.0, *)
private func makeOwnedController(_ assets: VerifiedReaderAssets) throws -> ReaderVMController {
    try assets.requireExclusiveOriginalWork()
    let boot = VZEFIBootLoader()
    boot.variableStore = VZEFIVariableStore(url: assets.variableStoreURL)
    let disk = try VZDiskImageStorageDeviceAttachment(url: assets.diskURL, readOnly: false)
    let configuration = VZVirtualMachineConfiguration()
    configuration.bootLoader = boot
    configuration.cpuCount = 2
    configuration.memorySize = 4 * 1024 * 1024 * 1024
    configuration.storageDevices = [VZVirtioBlockDeviceConfiguration(attachment: disk)]
    configuration.socketDevices = [VZVirtioSocketDeviceConfiguration()]
    configuration.networkDevices = []
    configuration.directorySharingDevices = []
    return try ReaderVMController(configuration: configuration, identity: assets.identity, nonce: assets.nonce)
}

@available(macOS 13.0, *)
private func readerWorkBindingFrame(assets: VerifiedReaderAssets) throws -> Data {
    var expected = Data("BIND/1\n".utf8)
    for value in [assets.identity.tenantID, assets.identity.companyID, assets.identity.workRef,
                  assets.identity.taskID, assets.identity.employeeID, assets.identity.bindingRef, assets.nonce] {
        let bytes = Data(value.utf8)
        guard !bytes.isEmpty, bytes.count <= 512 else { throw ReaderPlatformError.unverifiedOwnership }
        expected.append(UInt8(bytes.count >> 8))
        expected.append(UInt8(bytes.count & 0xff))
        expected.append(bytes)
    }
    guard expected.count <= 4096 else { throw ReaderPlatformError.unverifiedOwnership }
    return expected
}

@available(macOS 13.0, *)
private func readerWorkBindingReply(frame: Data, assets: VerifiedReaderAssets) throws -> Data {
    // This parser is not a peer authenticator; the caller must already own and
    // verify the control channel and the asset/Work binding.
    guard frame == (try readerWorkBindingFrame(assets: assets)) else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    return Data("BOUND \(assets.nonce)\n".utf8)
}

@available(macOS 13.0, *)
private func readerReadBindingFrame(fd: Int32, assets: VerifiedReaderAssets) throws -> Data {
    let expectedCount = try readerWorkBindingFrame(assets: assets).count
    let flags = fcntl(fd, F_GETFL)
    guard fd >= 0, flags >= 0, fcntl(fd, F_SETFL, flags | O_NONBLOCK) == 0 else {
        throw ReaderPlatformError.unverifiedOwnership
    }
    let deadline = DispatchTime.now().uptimeNanoseconds + 3_000_000_000
    var received = Data()
    while received.count < expectedCount {
        let now = DispatchTime.now().uptimeNanoseconds
        guard now < deadline else { throw ReaderPlatformError.unverifiedOwnership }
        let remaining = Int32(min((deadline - now + 999_999) / 1_000_000, UInt64(Int32.max)))
        var descriptor = pollfd(fd: fd, events: Int16(POLLIN), revents: 0)
        let ready = poll(&descriptor, 1, remaining)
        if ready < 0 && errno == EINTR { continue }
        guard ready > 0, descriptor.revents & Int16(POLLIN) != 0 else {
            throw ReaderPlatformError.unverifiedOwnership
        }
        var chunk = [UInt8](repeating: 0, count: min(4096, expectedCount + 1 - received.count))
        let count = read(fd, &chunk, chunk.count)
        if count < 0 && (errno == EAGAIN || errno == EINTR) { continue }
        guard count > 0 else { throw ReaderPlatformError.unverifiedOwnership }
        received.append(contentsOf: chunk.prefix(count))
        guard received.count <= expectedCount else { throw ReaderPlatformError.unverifiedOwnership }
    }
    return try readerWorkBindingReply(frame: received, assets: assets)
}

private func readerWriteBindingReply(fd: Int32, reply: Data) throws {
    let deadline = DispatchTime.now().uptimeNanoseconds + 3_000_000_000
    var sent = 0
    while sent < reply.count {
        let now = DispatchTime.now().uptimeNanoseconds
        guard now < deadline else { throw ReaderPlatformError.unverifiedOwnership }
        let remaining = Int32(min((deadline - now + 999_999) / 1_000_000, UInt64(Int32.max)))
        var descriptor = pollfd(fd: fd, events: Int16(POLLOUT), revents: 0)
        let ready = poll(&descriptor, 1, remaining)
        if ready < 0 && errno == EINTR { continue }
        guard ready > 0, descriptor.revents & Int16(POLLOUT) != 0 else {
            throw ReaderPlatformError.unverifiedOwnership
        }
        let count = reply.withUnsafeBytes { buffer in
            write(fd, buffer.baseAddress!.advanced(by: sent), reply.count - sent)
        }
        if count < 0 && (errno == EAGAIN || errno == EINTR) { continue }
        guard count > 0 else { throw ReaderPlatformError.unverifiedOwnership }
        sent += count
    }
}

private func requireAtomicWorkAdmission() throws {
    // Two separate descriptor streams do not establish the order of Work
    // admission and owner revocation. A platform owner must supply that proof.
    throw ReaderPlatformError.unverifiedOwnership
}

@available(macOS 13.0, *)
private final class ReaderOwnedStopChannel {
    private let source: DispatchSourceRead
    private let queue: DispatchQueue
    private let completion: (ReaderVMController.State) -> Void
    private let startLock = NSLock()
    private var started = false
    private var pending = Data()
    private var finished = false
    private var partialDeadlineScheduled = false

    // The caller must have independently verified and exclusively transferred
    // ownership of fd; this class cannot authenticate a descriptor itself.
    // On init failure the caller retains fd. A complete first frame is the
    // one-shot request; bytes arriving later are not observed after cancellation.
    init(fd: Int32, controller: ReaderVMController, identity: ReaderVMController.Identity,
         nonce: String, completion: @escaping (ReaderVMController.State) -> Void) throws {
        guard fd == 2 else { throw ReaderPlatformError.unverifiedOwnership }
        let flags = fcntl(fd, F_GETFL)
        guard flags >= 0, fcntl(fd, F_SETFL, flags | O_NONBLOCK) == 0 else {
            throw ReaderPlatformError.unverifiedOwnership
        }
        queue = DispatchQueue(label: "com.curis.reader.vm.stop-channel")
        self.completion = completion
        source = DispatchSource.makeReadSource(fileDescriptor: fd, queue: queue)
        source.setEventHandler { [weak self] in
            guard let self = self, !self.finished else { return }
            var bytes = [UInt8](repeating: 0, count: 6)
            let count = read(fd, &bytes, bytes.count)
            if count < 0 && (errno == EAGAIN || errno == EINTR) { return }
            if count == 0 {
                // Loss of the already-verified owner channel requests the same
                // bounded stop; it does not prove VM or guest termination.
                self.finished = true
                self.source.cancel()
                controller.stop(identity: identity, nonce: nonce, completion: completion)
                return
            }
            guard count > 0 else {
                self.finished = true
                self.source.cancel()
                controller.stop(identity: identity, nonce: nonce, completion: completion)
                return
            }
            self.pending.append(contentsOf: bytes.prefix(count))
            guard self.pending.count <= 5 else {
                self.finished = true
                self.source.cancel()
                controller.stop(identity: identity, nonce: nonce, completion: completion)
                return
            }
            if self.pending.count == 5 {
                self.finished = true
                self.source.cancel()
                if self.pending == Data("STOP\n".utf8) {
                    controller.stopFromOwnedChannel(frame: self.pending, identity: identity,
                                                    nonce: nonce, completion: completion)
                } else {
                    controller.stop(identity: identity, nonce: nonce, completion: completion)
                }
            } else if !self.partialDeadlineScheduled {
                self.partialDeadlineScheduled = true
                self.queue.asyncAfter(deadline: .now() + 5) { [weak self] in
                    guard let self = self, !self.finished else { return }
                    self.finished = true
                    self.source.cancel()
                    controller.stop(identity: identity, nonce: nonce, completion: completion)
                }
            }
        }
        source.setCancelHandler { _ = close(fd) }
    }

    func start() throws {
        startLock.lock()
        guard !started else {
            startLock.unlock()
            throw ReaderPlatformError.unverifiedOwnership
        }
        started = true
        source.resume()
        startLock.unlock()
    }

    deinit {
        startLock.lock()
        if !started {
            started = true
            source.resume()
        }
        source.cancel()
        startLock.unlock()
    }
}

@main
private enum ReaderVMMain {
    static func main() {
        do {
            guard #available(macOS 13.0, *) else {
                throw ReaderPlatformError.unavailable
            }
            guard CommandLine.arguments.count == 2, CommandLine.arguments[1] == "--fixture" else {
                throw ReaderPlatformError.unverifiedOwnership
            }
            // Fixture probes carry only random challenges. They do not grant
            // Work, disk, guest, network, or VM access.
            try readerExchangeProbe(fd: 0, role: "C")
            try readerExchangeProbe(fd: 2, role: "S")
            let assets = try VerifiedReaderAssets.resolveFromOwnedChannel()
            let controller = try makeOwnedController(assets)
            let stopChannel = try ReaderOwnedStopChannel(fd: 2, controller: controller,
                identity: assets.identity, nonce: assets.nonce) { _ in
                // The callback is only framework-local evidence. Guest and
                // external effects remain unknown until separately verified.
            }
            try stopChannel.start()
            let reply = try readerReadBindingFrame(fd: 0, assets: assets)
            try requireAtomicWorkAdmission()
            try readerWriteBindingReply(fd: 0, reply: reply)
            controller.start(identity: assets.identity, nonce: assets.nonce) { _ in }
            withExtendedLifetime(stopChannel) { dispatchMain() }
        } catch {
            // Descriptor 2 is reserved for the private stop channel.
            exit(1)
        }
    }
}
