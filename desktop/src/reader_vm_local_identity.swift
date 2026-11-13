import Foundation
import Security

// These primitives only observe a process. The fixture broker must compare
// the result with its own retained child handle and independently fixed build.
enum ReaderLocalIdentityError: Error {
    case unavailable
    case invalidCodeIdentity
}

struct ReaderLocalCodeIdentity: Equatable {
    let pid: pid_t
    let cdHash: Data
}

func readerLocalCodeIdentity(pid: pid_t) throws -> ReaderLocalCodeIdentity {
    guard pid > 1 else { throw ReaderLocalIdentityError.unavailable }
    let attributes = [kSecGuestAttributePid as String: NSNumber(value: pid)] as CFDictionary
    var code: SecCode?
    guard SecCodeCopyGuestWithAttributes(nil, attributes, SecCSFlags(), &code) == errSecSuccess,
          let code = code else { throw ReaderLocalIdentityError.unavailable }
    var staticCode: SecStaticCode?
    guard SecCodeCopyStaticCode(code, SecCSFlags(), &staticCode) == errSecSuccess,
          let staticCode = staticCode else { throw ReaderLocalIdentityError.unavailable }
    var info: CFDictionary?
    guard SecCodeCopySigningInformation(staticCode, SecCSFlags(rawValue: kSecCSSigningInformation), &info) == errSecSuccess,
          let values = info as? [String: Any],
          let hash = values[kSecCodeInfoUnique as String] as? Data,
          !hash.isEmpty else { throw ReaderLocalIdentityError.invalidCodeIdentity }
    return ReaderLocalCodeIdentity(pid: pid, cdHash: hash)
}
