import Foundation
import XCTest

final class ReaderVMLocalIdentityTests: XCTestCase {
    func testInvalidProcessCannotBeAReaderOwner() {
        XCTAssertThrowsError(try readerLocalCodeIdentity(pid: 0))
        XCTAssertThrowsError(try readerLocalCodeIdentity(pid: 1))
    }
}
