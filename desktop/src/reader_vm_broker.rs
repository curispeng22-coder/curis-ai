//! Fixture-only local broker candidate. No production entry or automatic spawn.
//!
//! A path hash, PID, nonce, or caller assertion is not a child identity. The
//! fixture pin and the actual live-process/FD verifier are not yet available;
//! the only entry point rejects before opening a process or a channel.

use std::fs::OpenOptions;
use std::io::{Read, Write};
use std::os::fd::{AsRawFd, OwnedFd};
use std::os::unix::fs::{MetadataExt, OpenOptionsExt};
use std::os::unix::net::{UnixListener, UnixStream};
use std::os::unix::ffi::OsStrExt;
use std::os::unix::fs::{DirBuilderExt, PermissionsExt};
use std::path::PathBuf;
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::sync::atomic::{AtomicBool, Ordering};

#[repr(C)]
#[derive(Clone, Copy, PartialEq, Eq)]
struct AuditToken { words: [u32; 8] }

#[link(name = "bsm")]
extern "C" {
    fn audit_token_to_pid(token: AuditToken) -> libc::pid_t;
    fn audit_token_to_pidversion(token: AuditToken) -> libc::c_int;
}

#[link(name = "System")]
extern "C" {
    fn CC_SHA256(data: *const libc::c_void, len: u32, md: *mut u8) -> *mut u8;
    fn proc_pidinfo(pid: libc::c_int, flavor: libc::c_int, arg: u64,
                    buffer: *mut libc::c_void, size: libc::c_int) -> libc::c_int;
}

type CFRef = *const libc::c_void;

#[link(name = "CoreFoundation", kind = "framework")]
extern "C" {
    static kCFTypeDictionaryKeyCallBacks: libc::c_void;
    static kCFTypeDictionaryValueCallBacks: libc::c_void;
    fn CFNumberCreate(allocator: CFRef, number_type: i64, value: *const libc::c_void) -> CFRef;
    fn CFDictionaryCreate(allocator: CFRef, keys: *const CFRef, values: *const CFRef,
                          count: isize, key_callbacks: *const libc::c_void,
                          value_callbacks: *const libc::c_void) -> CFRef;
    fn CFDictionaryGetValue(dictionary: CFRef, key: CFRef) -> CFRef;
    fn CFGetTypeID(value: CFRef) -> usize;
    fn CFDataGetTypeID() -> usize;
    fn CFDataGetLength(data: CFRef) -> isize;
    fn CFDataGetBytePtr(data: CFRef) -> *const u8;
    fn CFRelease(value: CFRef);
}

#[link(name = "Security", kind = "framework")]
extern "C" {
    static kSecGuestAttributePid: CFRef;
    static kSecCodeInfoUnique: CFRef;
    fn SecCodeCopyGuestWithAttributes(host: CFRef, attributes: CFRef, flags: u32, guest: *mut CFRef) -> i32;
    fn SecCodeCopyStaticCode(code: CFRef, flags: u32, static_code: *mut CFRef) -> i32;
    fn SecCodeCheckValidity(code: CFRef, flags: u32, requirement: CFRef) -> i32;
    fn SecCodeCopySigningInformation(code: CFRef, flags: u32, information: *mut CFRef) -> i32;
    fn SecRandomCopyBytes(random: CFRef, count: usize, bytes: *mut u8) -> i32;
}

struct OwnedCF(CFRef);
impl Drop for OwnedCF {
    fn drop(&mut self) { if !self.0.is_null() { unsafe { CFRelease(self.0) } } }
}

fn live_cd_hash(pid: u32) -> Result<Vec<u8>, &'static str> {
    if pid <= 1 || pid > i32::MAX as u32 { return Err("child PID invalid"); }
    let pid_value = pid as i32;
    unsafe {
        let number = OwnedCF(CFNumberCreate(std::ptr::null(), 3, (&pid_value as *const i32).cast()));
        if number.0.is_null() { return Err("PID number unavailable"); }
        let key = kSecGuestAttributePid;
        let dictionary = OwnedCF(CFDictionaryCreate(std::ptr::null(), &key, &number.0, 1,
            &kCFTypeDictionaryKeyCallBacks, &kCFTypeDictionaryValueCallBacks));
        if dictionary.0.is_null() { return Err("code attributes unavailable"); }
        let mut code = std::ptr::null();
        if SecCodeCopyGuestWithAttributes(std::ptr::null(), dictionary.0, 0, &mut code) != 0 || code.is_null() {
            return Err("live child code identity unavailable");
        }
        let code = OwnedCF(code);
        if SecCodeCheckValidity(code.0, 0, std::ptr::null()) != 0 {
            return Err("live child code validity unavailable");
        }
        let mut static_code = std::ptr::null();
        if SecCodeCopyStaticCode(code.0, 0, &mut static_code) != 0 || static_code.is_null() {
            return Err("child static code unavailable");
        }
        let static_code = OwnedCF(static_code);
        let mut information = std::ptr::null();
        if SecCodeCopySigningInformation(static_code.0, 2, &mut information) != 0 || information.is_null() {
            return Err("live child signing information unavailable");
        }
        let information = OwnedCF(information);
        let data = CFDictionaryGetValue(information.0, kSecCodeInfoUnique);
        if data.is_null() || CFGetTypeID(data) != CFDataGetTypeID() { return Err("live child CDHash unavailable"); }
        let len = CFDataGetLength(data);
        let bytes = CFDataGetBytePtr(data);
        if len <= 0 || len > 64 || bytes.is_null() { return Err("live child CDHash invalid"); }
        Ok(std::slice::from_raw_parts(bytes, len as usize).to_vec())
    }
}

fn verify_owned_child(child: &mut Child, fixed: &FixedFixture) -> Result<ProcessIdentity, &'static str> {
    let before = owned_child_start(child)?;
    let hash = live_cd_hash(before.0)?;
    let after = owned_child_start(child)?;
    if before != after || hash != fixed.cd_hash { return Err("live child identity changed"); }
    Ok(ProcessIdentity { pid: before.0, start_seconds: before.1, start_microseconds: before.2, cd_hash: hash })
}

fn kernel_peer_token(stream: &UnixStream) -> Result<(AuditToken, libc::pid_t, libc::c_int), &'static str> {
    let mut token = AuditToken { words: [0; 8] };
    let mut length = std::mem::size_of::<AuditToken>() as libc::socklen_t;
    let rc = unsafe { libc::getsockopt(stream.as_raw_fd(), libc::SOL_LOCAL, libc::LOCAL_PEERTOKEN,
        (&mut token as *mut AuditToken).cast(), &mut length) };
    if rc != 0 || length as usize != std::mem::size_of::<AuditToken>() {
        return Err("workspace peer token is UNKNOWN");
    }
    let pid = unsafe { audit_token_to_pid(token) };
    let version = unsafe { audit_token_to_pidversion(token) };
    if pid <= 1 || version < 0 { return Err("workspace peer token is invalid"); }
    Ok((token, pid, version))
}

fn workspace_process_info(pid: libc::pid_t) -> Result<(u32, u64, u64), &'static str> {
    let mut info: ProcBsdInfo = unsafe { std::mem::zeroed() };
    let len = std::mem::size_of::<ProcBsdInfo>() as libc::c_int;
    if unsafe { proc_pidinfo(pid, 3, 0, (&mut info as *mut ProcBsdInfo).cast(), len) } != len
        || info.pid != pid as u32 || info.ppid <= 1 || info.start_seconds == 0 || info.start_microseconds >= 1_000_000 {
        return Err("workspace process identity is UNKNOWN");
    }
    Ok((info.ppid, info.start_seconds, info.start_microseconds))
}

fn verify_workspace_peer(stream: &UnixStream, guardian: &mut Child,
                         guardian_pin: &FixedFixture, workspace_cd_hash: &[u8]) -> Result<(), &'static str> {
    if workspace_cd_hash.is_empty() { return Err("workspace code identity is unavailable"); }
    let parent_before = verify_owned_child(guardian, guardian_pin)?;
    let peer_before = kernel_peer_token(stream)?;
    let process_before = workspace_process_info(peer_before.1)?;
    if process_before.0 != parent_before.pid as u32
        || (process_before.1, process_before.2) < (parent_before.start_seconds, parent_before.start_microseconds)
        || live_cd_hash(peer_before.1 as u32)? != workspace_cd_hash {
        return Err("workspace peer identity mismatch");
    }
    let process_after = workspace_process_info(peer_before.1)?;
    let peer_after = kernel_peer_token(stream)?;
    let parent_after = verify_owned_child(guardian, guardian_pin)?;
    if peer_before != peer_after || process_before != process_after || parent_before != parent_after {
        return Err("workspace peer identity changed");
    }
    Ok(())
}

fn bind_workspace_listener(app_data: &std::path::Path) -> Result<UnixListener, &'static str> {
    fn private_directory(path: &std::path::Path) -> Result<(), &'static str> {
        let meta = std::fs::symlink_metadata(path).map_err(|_| "IPC directory is unavailable")?;
        if !meta.is_dir() || meta.file_type().is_symlink() || meta.uid() != unsafe { libc::geteuid() }
            || meta.permissions().mode() & 0o077 != 0 {
            return Err("IPC directory is not private");
        }
        Ok(())
    }
    let base = std::fs::symlink_metadata(app_data).map_err(|_| "App data directory is unavailable")?;
    if !base.is_dir() || base.file_type().is_symlink() || base.uid() != unsafe { libc::geteuid() } {
        return Err("App data directory identity is invalid");
    }
    let reader = app_data.join("reader");
    match std::fs::DirBuilder::new().mode(0o700).create(&reader) {
        Ok(()) => (),
        Err(error) if error.kind() == std::io::ErrorKind::AlreadyExists => (),
        Err(_) => return Err("Reader directory is unavailable"),
    }
    private_directory(&reader)?;
    let ipc = reader.join("ipc");
    // Never reuse an existing socket directory or remove an uncertain one.
    std::fs::DirBuilder::new().mode(0o700).create(&ipc).map_err(|_| "IPC directory already exists or is unavailable")?;
    private_directory(&ipc)?;
    let path = ipc.join("workspace.sock");
    if path.as_os_str().as_bytes().len() >= 104 { return Err("IPC path is too long"); }
    let listener = UnixListener::bind(&path).map_err(|_| "workspace IPC bind is UNKNOWN")?;
    std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o600))
        .map_err(|_| "workspace IPC permission is UNKNOWN")?;
    Ok(listener)
}

#[repr(C)]
struct ProcBsdInfo {
    flags: u32, status: u32, xstatus: u32, pid: u32, ppid: u32,
    uid: u32, gid: u32, ruid: u32, rgid: u32, svuid: u32, svgid: u32, reserved: u32,
    command: [u8; 16], name: [u8; 32], nfiles: u32, pgid: u32, pjobc: u32,
    tdev: u32, tpgid: u32, nice: i32, start_seconds: u64, start_microseconds: u64,
}

fn owned_child_start(child: &mut Child) -> Result<(u32, u64, u64), &'static str> {
    if child.try_wait().map_err(|_| "child status unavailable")?.is_some() {
        return Err("owned child already exited");
    }
    let pid = child.id();
    if pid <= 1 || pid > i32::MAX as u32 { return Err("child PID invalid"); }
    let mut info: ProcBsdInfo = unsafe { std::mem::zeroed() };
    let size = std::mem::size_of::<ProcBsdInfo>();
    let result = unsafe { proc_pidinfo(pid as i32, 3, 0, (&mut info as *mut ProcBsdInfo).cast(), size as i32) };
    if result != size as i32 || info.pid != pid || info.ppid != std::process::id()
        || info.start_seconds == 0 || info.start_microseconds >= 1_000_000 {
        return Err("owned child kernel identity unavailable");
    }
    if child.try_wait().map_err(|_| "child status unavailable")?.is_some() {
        return Err("owned child exited during identity check");
    }
    Ok((pid, info.start_seconds, info.start_microseconds))
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct ProcessIdentity {
    pid: u32,
    start_seconds: u64,
    start_microseconds: u64,
    cd_hash: Vec<u8>,
}

struct OwnedFixtureBroker {
    child: Child,
    identity: ProcessIdentity,
    control: UnixStream,
    stop: Arc<FixtureStop>,
    work: WorkBinding,
    fixed: FixedFixture,
}

struct FixtureStop {
    channel: Mutex<UnixStream>,
    used: AtomicBool,
    work: WorkBinding,
}

#[derive(Default)]
enum AdmissionState {
    #[default]
    Empty,
    Active(WorkBinding),
    Revoking(WorkBinding),
}

#[derive(Default)]
pub(crate) struct FixtureControl {
    cancelled: AtomicBool,
    expected: Mutex<Option<WorkBinding>>,
    admission: Mutex<AdmissionState>,
    stop: Mutex<Option<Arc<FixtureStop>>>,
}

impl FixtureControl {
    fn request_stop(&self, work: &WorkBinding) -> Result<(), &'static str> {
        let expected = self.expected.try_lock().map_err(|_| "stop Work identity is UNKNOWN")?;
        if !work.complete() || expected.as_ref() != Some(work) { return Err("stop Work mismatch or not admitted"); }
        drop(expected);
        self.cancelled.store(true, Ordering::Release);
        // Revocation is not acknowledged if an enqueue is holding this lock.
        // The caller can retry; the independent stop path still runs below.
        if let Ok(mut admission) = self.admission.try_lock() {
            if matches!(&*admission, AdmissionState::Active(active) if active == work) {
                *admission = AdmissionState::Revoking(work.clone());
            }
        }
        let guard = self.stop.try_lock().map_err(|_| "stop registration is UNKNOWN")?;
        match guard.as_ref() {
            Some(stop) => stop.request(work),
            None => Err("stop pending platform ownership; state remains UNKNOWN"),
        }
    }
}

impl FixtureStop {
    fn request(&self, work: &WorkBinding) -> Result<(), &'static str> {
        if !work.complete() || work != &self.work { return Err("stop Work mismatch"); }
        if self.used.swap(true, Ordering::AcqRel) { return Err("stop channel is unavailable; state remains UNKNOWN"); }
        let mut stream = self.channel.try_lock().map_err(|_| "stop delivery is UNKNOWN")?;
        disable_sigpipe(&stream).map_err(|_| "stop delivery is UNKNOWN")?;
        stream.set_nonblocking(true).map_err(|_| "stop delivery is UNKNOWN")?;
        stream.write_all(b"STOP\n").map_err(|_| "stop delivery is UNKNOWN")?;
        Err("stop requested; VM and resource state remain UNKNOWN")
    }
}

// A created child and both parent channels must stay together until an owner
// independently verifies or safely resolves them. Dropping Child is not reap.
#[must_use = "retain the pending child and channels until a verified supervisor resolves them"]
struct PendingFixture {
    child: Child,
    control: UnixStream,
    stop: UnixStream,
    handshake_attempted: bool,
    challenge_attempted: bool,
}

// App must retain this object while any child remains UNKNOWN. No PID or FD
// recovered from storage may be adopted or signalled by this supervisor.
pub(crate) struct FixtureSupervisor {
    bundle_resources: PathBuf,
    active: Option<OwnedFixtureBroker>,
    unresolved: Vec<PendingFixture>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct WorkBinding {
    tenant_id: String,
    company_id: String,
    work_ref: String,
    task_id: String,
    employee_id: String,
    binding_ref: String,
    nonce: String,
}

fn wait_channel(fd: libc::c_int, events: i16, deadline: std::time::Instant) -> Result<(), &'static str> {
    loop {
        let remaining = deadline.checked_duration_since(std::time::Instant::now()).ok_or("handshake timed out")?;
        if remaining.is_zero() { return Err("handshake timed out"); }
        let timeout = remaining.as_millis().max(1).min(i32::MAX as u128) as i32;
        let mut descriptor = libc::pollfd { fd, events, revents: 0 };
        let result = unsafe { libc::poll(&mut descriptor, 1, timeout) };
        if result > 0 && descriptor.revents & events != 0 { return Ok(()); }
        if result == 0 { return Err("handshake timed out"); }
        if result < 0 && std::io::Error::last_os_error().kind() == std::io::ErrorKind::Interrupted { continue; }
        return Err("handshake channel failed");
    }
}

fn disable_sigpipe(stream: &UnixStream) -> Result<(), &'static str> {
    let enabled: libc::c_int = 1;
    let status = unsafe { libc::setsockopt(stream.as_raw_fd(), libc::SOL_SOCKET, libc::SO_NOSIGPIPE,
        (&enabled as *const libc::c_int).cast(), std::mem::size_of_val(&enabled) as libc::socklen_t) };
    if status != 0 { return Err("socket signal suppression unavailable"); }
    Ok(())
}

impl PendingFixture {
    fn close_channels_and_reap(mut self) -> Result<(), Self> {
        use std::net::Shutdown;
        let _ = self.control.shutdown(Shutdown::Both);
        let _ = self.stop.shutdown(Shutdown::Both);
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(3);
        loop {
            match self.child.try_wait() {
                Ok(Some(_)) => return Ok(()),
                Ok(None) if std::time::Instant::now() < deadline => {
                    std::thread::sleep(std::time::Duration::from_millis(10));
                }
                _ => return Err(self),
            }
        }
    }

    fn bind_verified(mut self, fixed: FixedFixture, work: WorkBinding, control: &FixtureControl)
        -> Result<OwnedFixtureBroker, (Self, FixedFixture, &'static str)>
    {
        if !work.complete() { return Err((self, fixed, "original Work binding invalid")); }
        let before = match verify_owned_child(&mut self.child, &fixed) {
            Ok(identity) => identity,
            Err(reason) => return Err((self, fixed, reason)),
        };
        // PID/CDHash alone do not establish that these FDs are the child's
        // exclusive endpoints. Do not send Work data until that proof exists.
        if verify_private_channels(&mut self).is_err() {
            return Err((self, fixed, "private channel ownership is UNKNOWN"));
        }
        if self.handshake_attempted {
            return Err((self, fixed, "Work channel handshake cannot be retried"));
        }
        self.handshake_attempted = true;
        let admission = match control.admission.try_lock() {
            Ok(guard) => guard,
            Err(_) => return Err((self, fixed, "Work admission is UNKNOWN")),
        };
        if control.cancelled.load(Ordering::Acquire)
            || !matches!(&*admission, AdmissionState::Active(active) if active == &work) {
            return Err((self, fixed, "Work was revoked or remains UNKNOWN"));
        }
        if verify_atomic_work_admission_available().is_err() {
            return Err((self, fixed, "atomic Work admission and revocation are unavailable"));
        }
        // Fixed field order and 16-bit lengths leave no duplicate-key syntax.
        let mut request = b"BIND/1\n".to_vec();
        for value in [&work.tenant_id, &work.company_id, &work.work_ref, &work.task_id,
                      &work.employee_id, &work.binding_ref, &work.nonce] {
            request.extend_from_slice(&(value.len() as u16).to_be_bytes());
            request.extend_from_slice(value.as_bytes());
        }
        let expected = format!("BOUND {}\n", work.nonce);
        if disable_sigpipe(&self.control).is_err() || self.control.set_nonblocking(true).is_err() {
            return Err((self, fixed, "Work channel unavailable"));
        }
        let deadline = std::time::Instant::now() + std::time::Duration::from_secs(3);
        let mut sent = 0;
        while sent < request.len() {
            if wait_channel(self.control.as_raw_fd(), libc::POLLOUT, deadline).is_err() {
                return Err((self, fixed, "Work channel send is UNKNOWN"));
            }
            match self.control.write(&request[sent..]) {
                Ok(0) => return Err((self, fixed, "Work channel send is UNKNOWN")),
                Ok(count) => sent += count,
                Err(error) if error.kind() == std::io::ErrorKind::WouldBlock
                    || error.kind() == std::io::ErrorKind::Interrupted => continue,
                Err(_) => return Err((self, fixed, "Work channel send is UNKNOWN")),
            }
        }
        drop(admission);
        let mut reply = Vec::new();
        while !reply.contains(&b'\n') {
            if wait_channel(self.control.as_raw_fd(), libc::POLLIN, deadline).is_err() {
                return Err((self, fixed, "Work channel reply timed out"));
            }
            let mut chunk = [0u8; 128];
            match self.control.read(&mut chunk) {
                Ok(0) => return Err((self, fixed, "Work channel reply is UNKNOWN")),
                Ok(count) => reply.extend_from_slice(&chunk[..count]),
                Err(error) if error.kind() == std::io::ErrorKind::WouldBlock
                    || error.kind() == std::io::ErrorKind::Interrupted => continue,
                Err(_) => return Err((self, fixed, "Work channel reply is UNKNOWN")),
            }
            if reply.len() > 128 { return Err((self, fixed, "Work channel reply too large")); }
        }
        if reply != expected.as_bytes() { return Err((self, fixed, "Work channel reply mismatch")); }
        let after = match verify_owned_child(&mut self.child, &fixed) {
            Ok(identity) => identity,
            Err(reason) => return Err((self, fixed, reason)),
        };
        if before != after { return Err((self, fixed, "child identity changed")); }
        let stop = Arc::new(FixtureStop { channel: Mutex::new(self.stop), used: AtomicBool::new(false), work: work.clone() });
        Ok(OwnedFixtureBroker { child: self.child, identity: after, control: self.control, stop, work, fixed })
    }
}

impl FixtureSupervisor {
    pub(crate) fn new(bundle_resources: PathBuf) -> Self {
        Self { bundle_resources, active: None, unresolved: Vec::new() }
    }

    fn start_background(owner: Arc<Mutex<Self>>, control: Arc<FixtureControl>, work: WorkBinding)
        -> Result<std::sync::mpsc::Receiver<Result<(), &'static str>>, &'static str>
    {
        let (tx, rx) = std::sync::mpsc::channel();
        std::thread::Builder::new().name("reader-fixture-owner".into()).spawn(move || {
            let result = match owner.lock() {
                Ok(mut supervisor) => supervisor.start(work, &control),
                Err(_) => Err("fixture owner state is UNKNOWN"),
            };
            let _ = tx.send(result);
        }).map_err(|_| "fixture owner worker unavailable")?;
        Ok(rx)
    }

    // Call only from a background worker. The future App-facing stop path must
    // not wait on a lock held by this bounded but synchronous startup path.
    fn start(&mut self, work: WorkBinding, control: &FixtureControl) -> Result<(), &'static str> {
        if control.cancelled.load(Ordering::Acquire) || !work.complete() || self.active.is_some() || !self.unresolved.is_empty() {
            return Err("fixture Work is invalid or a child remains UNKNOWN");
        }
        let lock = verify_bundled_reader_lock(&self.bundle_resources)?;
        let fixed = FixedFixture::load_owner_pin(&self.bundle_resources, &lock)?;
        fixed.verify_file()?;
        verify_live_platform_available()?;
        {
            let mut expected = control.expected.try_lock().map_err(|_| "fixture Work admission is UNKNOWN")?;
            if expected.is_some() { return Err("fixture Work is already admitted or UNKNOWN"); }
            *expected = Some(work.clone());
        }
        {
            let mut admission = control.admission.try_lock().map_err(|_| "fixture Work admission is UNKNOWN")?;
            if control.cancelled.load(Ordering::Acquire) || !matches!(&*admission, AdmissionState::Empty) {
                return Err("fixture Work was revoked or remains UNKNOWN");
            }
            *admission = AdmissionState::Active(work.clone());
        }
        let pending = OwnedFixtureBroker::spawn_with_fixed_fixture(&fixed)?;
        match pending.bind_verified(fixed, work.clone(), control) {
            Ok(owned) => {
                let stop = Arc::clone(&owned.stop);
                self.active = Some(owned);
                // Only the background owner waits here. Stop itself never waits
                // for this lock and records cancellation before trying it.
                let mut slot = control.stop.lock().unwrap_or_else(|poisoned| poisoned.into_inner());
                *slot = Some(Arc::clone(&stop));
                drop(slot);
                if control.cancelled.load(Ordering::Acquire) {
                    let _ = stop.request(&work);
                    return Err("fixture cancellation and stop remain UNKNOWN");
                }
                Ok(())
            },
            Err((pending, _, reason)) => {
                if let Err(pending) = pending.close_channels_and_reap() {
                    self.unresolved.push(pending);
                    return Err("fixture child and resources remain UNKNOWN");
                }
                Err(reason)
            }
        }
    }

    fn unresolved_count(&self) -> usize { self.unresolved.len() }

    fn observe_active(&mut self) -> &'static str {
        match self.active.as_mut() {
            None if self.unresolved.is_empty() => "NO_OWNED_CHILD",
            None => "CHILD_OR_RESOURCES_UNKNOWN",
            Some(active) => match active.child.try_wait() {
                Ok(Some(_)) => "CHILD_EXITED_RESOURCES_UNKNOWN",
                Ok(None) => "CHILD_RUNNING_RESOURCES_UNKNOWN",
                Err(_) => "CHILD_OR_RESOURCES_UNKNOWN",
            },
        }
    }

    fn observe_pending(&mut self) -> usize {
        // try_wait only observes/reaps the actual Child returned by spawn;
        // failures and still-running processes remain retained as UNKNOWN.
        self.unresolved.retain_mut(|pending| !matches!(pending.child.try_wait(), Ok(Some(_))));
        self.unresolved.len()
    }
}

fn random_challenge() -> Result<String, &'static str> {
    let mut bytes = [0u8; 24];
    if unsafe { SecRandomCopyBytes(std::ptr::null(), bytes.len(), bytes.as_mut_ptr()) } != 0 {
        return Err("private channel challenge unavailable");
    }
    Ok(bytes.iter().map(|value| format!("{value:02x}")).collect())
}

fn exchange_challenge(stream: &mut UnixStream, role: &str, challenge: &str) -> Result<(), &'static str> {
    disable_sigpipe(stream)?;
    stream.set_nonblocking(true).map_err(|_| "private channel unavailable")?;
    let request = format!("PROBE/1 {role} {challenge}\n");
    let expected = format!("READY/1 {role} {challenge}\n");
    let deadline = std::time::Instant::now() + std::time::Duration::from_secs(3);
    let mut sent = 0;
    while sent < request.len() {
        wait_channel(stream.as_raw_fd(), libc::POLLOUT, deadline)?;
        match stream.write(&request.as_bytes()[sent..]) {
            Ok(0) => return Err("private channel send failed"),
            Ok(count) => sent += count,
            Err(error) if error.kind() == std::io::ErrorKind::WouldBlock
                || error.kind() == std::io::ErrorKind::Interrupted => continue,
            Err(_) => return Err("private channel send failed"),
        }
    }
    let mut response = Vec::new();
    while !response.contains(&b'\n') {
        wait_channel(stream.as_raw_fd(), libc::POLLIN, deadline)?;
        let mut chunk = [0u8; 128];
        match stream.read(&mut chunk) {
            Ok(0) => return Err("private channel response missing"),
            Ok(count) => response.extend_from_slice(&chunk[..count]),
            Err(error) if error.kind() == std::io::ErrorKind::WouldBlock
                || error.kind() == std::io::ErrorKind::Interrupted => continue,
            Err(_) => return Err("private channel response invalid"),
        }
        if response.len() > 128 { return Err("private channel response too large"); }
    }
    if response != expected.as_bytes() { return Err("private channel challenge mismatch"); }
    Ok(())
}

fn verify_private_channels(pending: &mut PendingFixture) -> Result<(), &'static str> {
    if pending.challenge_attempted { return Err("private channel challenge cannot be retried"); }
    pending.challenge_attempted = true;
    let control = random_challenge()?;
    let stop = random_challenge()?;
    if control == stop { return Err("private channel challenges unexpectedly match"); }
    exchange_challenge(&mut pending.control, "C", &control)?;
    exchange_challenge(&mut pending.stop, "S", &stop)?;
    // Under the Owner's local threat model this checks protocol consistency;
    // it does not prove that no process inherited or received either FD.
    Ok(())
}

impl WorkBinding {
    fn complete(&self) -> bool {
        [&self.tenant_id, &self.company_id, &self.work_ref, &self.task_id,
         &self.employee_id, &self.binding_ref].iter().all(|value| !value.is_empty() && value.len() <= 512)
            && self.nonce.len() == 48
            && self.nonce.bytes().all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c))
    }
}

struct FixedFixture {
    executable: PathBuf,
    sha256: [u8; 32],
    cd_hash: Vec<u8>,
}

fn verify_bundled_reader_lock(resources: &std::path::Path) -> Result<serde_json::Value, &'static str> {
    // This pin is the existing incomplete lock, not an authorization to run.
    // A future approved release must update the source pin and verify its full
    // asset/owner closure before either of the other gates can be released.
    const PIN: &str = "c4e90e387378cfc6b266f20f11eaee74891ffe4cf65420b533b72f5840b89d34";
    let path = resources.join("runtime/workspace/_internal/backend/app/reader_runtime_lock.json");
    let mut file = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW)
        .open(path).map_err(|_| "bundled reader lock is unavailable")?;
    let before = file.metadata().map_err(|_| "bundled reader lock is unavailable")?;
    if !before.is_file() || before.nlink() != 1 || before.len() == 0 || before.len() > 65536 {
        return Err("bundled reader lock is invalid");
    }
    let mut bytes = Vec::new();
    std::io::Read::by_ref(&mut file).take(65537).read_to_end(&mut bytes).map_err(|_| "bundled reader lock is unavailable")?;
    let after = file.metadata().map_err(|_| "bundled reader lock is unavailable")?;
    if before.dev() != after.dev() || before.ino() != after.ino() || before.len() != after.len()
        || before.mtime() != after.mtime() || before.mtime_nsec() != after.mtime_nsec()
        || before.ctime() != after.ctime() || before.ctime_nsec() != after.ctime_nsec()
        || bytes.len() as u64 != before.len() {
        return Err("bundled reader lock changed");
    }
    let mut digest = [0u8; 32];
    if unsafe { CC_SHA256(bytes.as_ptr().cast(), bytes.len() as u32, digest.as_mut_ptr()) }.is_null()
        || digest.iter().map(|byte| format!("{byte:02x}")).collect::<String>() != PIN {
        return Err("bundled reader lock identity mismatch");
    }
    let lock: serde_json::Value = serde_json::from_slice(&bytes).map_err(|_| "bundled reader lock is invalid")?;
    if lock.get("schemaVersion").and_then(|v| v.as_u64()) != Some(1)
        || lock.get("mode").and_then(|v| v.as_str()) != Some("PUBLIC_READ_ONLY_READER")
        || lock.get("complete").and_then(|v| v.as_bool()) != Some(true)
        || lock.get("executionAuthorized").and_then(|v| v.as_bool()) != Some(true) {
        return Err("bundled reader runtime is not authorized");
    }
    Ok(lock)
}

impl FixedFixture {
    fn load_owner_pin(resources: &std::path::Path, lock: &serde_json::Value) -> Result<Self, &'static str> {
        // Proposed fields are meaningful only inside the single pinned,
        // separately authorized reader lock. No caller supplies a path or pin.
        let closure = lock.get("hostHelperClosure").and_then(|v| v.as_object())
            .ok_or("fixed helper closure is unavailable")?;
        if closure.get("path").and_then(|v| v.as_str()) != Some("reader/ReaderVMHelper") {
            return Err("fixed helper path is invalid");
        }
        fn hex(value: Option<&str>, length: usize) -> Result<Vec<u8>, &'static str> {
            let text = value.ok_or("fixed helper identity is unavailable")?;
            if text.len() != length * 2 || !text.bytes().all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b)) {
                return Err("fixed helper identity is invalid");
            }
            (0..length).map(|i| u8::from_str_radix(&text[i * 2..i * 2 + 2], 16)
                .map_err(|_| "fixed helper identity is invalid")).collect()
        }
        let sha = hex(closure.get("sha256").and_then(|v| v.as_str()), 32)?;
        let cd_hash = hex(closure.get("cdHash").and_then(|v| v.as_str()), 20)?;
        let mut sha256 = [0u8; 32];
        sha256.copy_from_slice(&sha);
        Ok(Self { executable: resources.join("runtime/reader/ReaderVMHelper"), sha256, cd_hash })
    }

    fn verify_file(&self) -> Result<(), &'static str> {
        let mut file = OpenOptions::new().read(true).custom_flags(libc::O_NOFOLLOW)
            .open(&self.executable).map_err(|_| "fixture helper unavailable")?;
        let before = file.metadata().map_err(|_| "fixture metadata unavailable")?;
        if !before.is_file() || before.nlink() != 1 || before.len() == 0 || before.len() > 64 * 1024 * 1024 {
            return Err("fixture helper is invalid");
        }
        let mut bytes = Vec::new();
        std::io::Read::by_ref(&mut file).take(64 * 1024 * 1024 + 1).read_to_end(&mut bytes)
            .map_err(|_| "fixture helper read failed")?;
        let after = file.metadata().map_err(|_| "fixture metadata unavailable")?;
        if before.dev() != after.dev() || before.ino() != after.ino()
            || before.len() != after.len() || before.mtime() != after.mtime()
            || before.mtime_nsec() != after.mtime_nsec() || before.ctime() != after.ctime()
            || before.ctime_nsec() != after.ctime_nsec() || bytes.len() as u64 != before.len() {
            return Err("fixture helper changed during verification");
        }
        let mut digest = [0u8; 32];
        if unsafe { CC_SHA256(bytes.as_ptr().cast(), bytes.len() as u32, digest.as_mut_ptr()) }.is_null()
            || digest != self.sha256 || self.cd_hash.is_empty() {
            return Err("fixture build identity mismatch");
        }
        Ok(())
    }
}

fn verify_live_platform_available() -> Result<(), &'static str> {
    // No independently verified PID/starttime/CDHash and private-FD proof yet.
    Err("live process and control-channel verification unavailable")
}

fn verify_atomic_work_admission_available() -> Result<(), &'static str> {
    // A future platform owner must make Work admission and revocation atomic.
    // Checking a local cancellation flag before writing cannot establish it.
    Err("atomic Work admission and revocation are unavailable")
}

impl OwnedFixtureBroker {
    fn open() -> Result<Self, &'static str> {
        // The legacy no-context entry cannot supply a verified bundled lock.
        // Production admission above requires resources plus the pinned lock.
        Err("owned fixture supervisor is unavailable")
    }

    fn spawn_with_fixed_fixture(fixed: &FixedFixture) -> Result<PendingFixture, &'static str> {
        // Keep even internal calls closed until the live platform verifier exists.
        verify_live_platform_available()?;
        let (control, control_child) = UnixStream::pair().map_err(|_| "control channel unavailable")?;
        let (stop, stop_child) = UnixStream::pair().map_err(|_| "stop channel unavailable")?;
        let fds = [control.as_raw_fd(), control_child.as_raw_fd(), stop.as_raw_fd(), stop_child.as_raw_fd()];
        if fds.iter().any(|fd| {
            let flags = unsafe { libc::fcntl(*fd, libc::F_GETFD) };
            *fd <= 2 || flags < 0 || flags & libc::FD_CLOEXEC == 0
        })
            || fds.iter().enumerate().any(|(i, fd)| fds[..i].contains(fd)) {
            return Err("private channels lack exclusive close-on-exec descriptors");
        }
        let child_control: OwnedFd = control_child.into();
        let child_stop: OwnedFd = stop_child.into();
        let mut command = Command::new(&fixed.executable);
        command.arg("--fixture");
        // Delegate standard descriptor mapping to Command; do not overwrite
        // a descriptor that its spawn implementation might use internally.
        command.env_clear().stdin(Stdio::from(child_control)).stdout(Stdio::null())
            .stderr(Stdio::from(child_stop));
        // The live-platform gate above still rejects: this path cannot start
        // until target-platform FD inheritance and child ownership are verified.
        let child = command.spawn().map_err(|_| "fixture helper spawn failed")?;
        Ok(PendingFixture { child, control, stop, handshake_attempted: false, challenge_attempted: false })
    }

    fn identity(&self) -> &ProcessIdentity {
        &self.identity
    }

}

#[cfg(test)]
mod tests {
    use super::OwnedFixtureBroker;

    #[test]
    fn fixture_entry_is_closed_without_independent_process_proof() {
        assert!(OwnedFixtureBroker::open().is_err());
    }

    #[test]
    fn work_binding_requires_complete_identity_and_lowercase_nonce() {
        let mut binding = super::WorkBinding { tenant_id: "t".into(), company_id: "c".into(),
            work_ref: "w".into(), task_id: "task".into(), employee_id: "e".into(),
            binding_ref: "b".into(), nonce: "a".repeat(48) };
        assert!(binding.complete());
        binding.nonce = "A".repeat(48);
        assert!(!binding.complete());
        binding.nonce = "a".repeat(48);
        binding.work_ref.clear();
        assert!(!binding.complete());
    }

    #[test]
    fn revocation_is_scoped_to_the_original_generation() {
        let work = super::WorkBinding { tenant_id: "t".into(), company_id: "c".into(),
            work_ref: "w".into(), task_id: "task".into(), employee_id: "e".into(),
            binding_ref: "b".into(), nonce: "a".repeat(48) };
        let control = super::FixtureControl::default();
        *control.expected.lock().unwrap() = Some(work.clone());
        *control.admission.lock().unwrap() = super::AdmissionState::Active(work.clone());
        let mut other = work.clone();
        other.nonce = "b".repeat(48);
        assert!(control.request_stop(&other).is_err());
        assert!(matches!(&*control.admission.lock().unwrap(), super::AdmissionState::Active(active) if active == &work));
        // An absent remote owner remains UNKNOWN even when local admission is revoked.
        assert!(control.request_stop(&work).is_err());
        assert!(matches!(&*control.admission.lock().unwrap(), super::AdmissionState::Revoking(active) if active == &work));
    }
}
