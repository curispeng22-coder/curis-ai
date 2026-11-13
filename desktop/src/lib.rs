// Curis Local Desktop — packaged Tauri runtime.
//
// The shell owns only the local process boundary. Product state remains in the
// packaged Workspace Runtime and the single user data database; the WebView
// talks to the fixed loopback Trusted Gateway on :8080.

#[cfg(target_os = "macos")]
mod reader_vm_broker;

use std::fs::{create_dir_all, File, OpenOptions};
use std::io::{Read, Write};
use std::os::fd::AsRawFd;
use std::os::unix::fs::MetadataExt;
use std::os::unix::process::CommandExt;
use std::net::{SocketAddr, TcpStream};
use std::path::{Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::{Duration, Instant};

use tauri::{Manager, State};

struct Sidecars {
    workspace: Mutex<Option<Child>>,
    gateway: Mutex<Option<Child>>,
    frontend: Mutex<Option<Child>>,
}

struct InstanceLock {
    _file: File,
}

struct OperationFence(Arc<AtomicBool>);
struct FenceGuard(Arc<AtomicBool>);
impl Drop for FenceGuard {
    fn drop(&mut self) { self.0.store(false, Ordering::Release); }
}
fn enter_operation(fence: &OperationFence) -> Result<FenceGuard, String> {
    fence.0.compare_exchange(false, true, Ordering::AcqRel, Ordering::Acquire)
        .map_err(|_| "另一个本机数据操作尚未结束。".to_string())?;
    Ok(FenceGuard(fence.0.clone()))
}

struct RecoveryState {
    root: PathBuf,
    preview: Mutex<Option<RecoveryPreview>>,
}
struct RecoveryPreview {
    id: String,
    archive: PathBuf,
    archive_sha: String,
    generation: String,
    root_device: u64,
    root_inode: u64,
    archive_device: u64,
    archive_inode: u64,
    archive_size: u64,
    archive_mtime_ns: i128,
    expires: Instant,
}

fn recovery_requires_safe_mode(status: &serde_json::Value) -> bool {
    matches!(status["status"].as_str(), Some("UNKNOWN" | "RECOVERY_HOLD" | "RECOVERY_REQUIRED"))
}

fn recovery_helper(app: &tauri::AppHandle, root: &Path, lock: &InstanceLock, operation: &str, args: &[&str]) -> Result<serde_json::Value, String> {
    let executable = runtime_path(app, "recovery/curis-recovery")?;
    let mut command = Command::new(executable);
    command.env("CURIS_DESKTOP_VERSION", env!("CARGO_PKG_VERSION"));
    command.arg(operation).arg("--data-root").arg(root).arg("--app-lock-fd").arg("3");
    for arg in args { command.arg(arg); }
    let original = lock._file.as_raw_fd();
    unsafe {
        command.pre_exec(move || {
            if libc::dup2(original, 3) < 0 { return Err(std::io::Error::last_os_error()); }
            if libc::fcntl(3, libc::F_SETFD, 0) < 0 { return Err(std::io::Error::last_os_error()); }
            Ok(())
        });
    }
    let output = command.stdin(Stdio::null()).output().map_err(|_| "无法启动本机恢复工具。".to_string())?;
    if !output.status.success() || output.stdout.len() > 64 * 1024 {
        return Err("本机数据操作未完成；原数据与恢复点已保留，请查看诊断状态。".into());
    }
    serde_json::from_slice(&output.stdout).map_err(|_| "恢复工具回证无法核验。".to_string())
}

fn recovery_origin(window: &tauri::WebviewWindow) -> Result<(), String> {
    let url = window.url().map_err(|_| "无法确认当前窗口。".to_string())?;
    if !trusted_writing_origin(window.label(), url.scheme(), url.host_str(), url.port()) {
        return Err("备份恢复只能由当前本机主窗口操作。".into());
    }
    Ok(())
}

fn recovery_token() -> Result<String, String> {
    let mut random = [0_u8; 32];
    File::open("/dev/urandom").and_then(|mut source| source.read_exact(&mut random))
        .map_err(|_| "无法生成恢复确认。".to_string())?;
    Ok(random.iter().map(|byte| format!("{byte:02x}")).collect())
}

fn archive_identity(path: &Path) -> Result<(u64, u64, u64, i128), String> {
    let metadata = std::fs::symlink_metadata(path).map_err(|_| "所选备份已不可读取。".to_string())?;
    if !metadata.is_file() || metadata.file_type().is_symlink() || metadata.nlink() != 1 {
        return Err("所选备份不是普通文件。".into());
    }
    Ok((metadata.dev(), metadata.ino(), metadata.len(), metadata.mtime_nsec() as i128 + metadata.mtime() as i128 * 1_000_000_000))
}

fn root_identity(path: &Path) -> Result<(u64, u64), String> {
    let metadata = std::fs::symlink_metadata(path).map_err(|_| "数据目录不可用。".to_string())?;
    if !metadata.is_dir() || metadata.file_type().is_symlink() { return Err("数据目录不安全。".into()); }
    Ok((metadata.dev(), metadata.ino()))
}

fn runtime_path(app: &tauri::AppHandle, relative: &str) -> Result<PathBuf, String> {
    app.path()
        .resource_dir()
        .map_err(|error| format!("resource directory unavailable: {error}"))
        .map(|root| root.join("runtime").join(relative))
}

fn application_data(app: &tauri::AppHandle) -> Result<PathBuf, String> {
    let root = std::env::var_os("CURIS_DESKTOP_DATA_ROOT")
        .filter(|value| !value.is_empty())
        .map(PathBuf::from)
        .map(Ok)
        .unwrap_or_else(|| {
            app.path()
                .app_data_dir()
                .map_err(|error| format!("application data directory unavailable: {error}"))
        })?;
    create_dir_all(root.join("data")).map_err(|error| format!("create data directory: {error}"))?;
    create_dir_all(root.join("logs")).map_err(|error| format!("create log directory: {error}"))?;
    Ok(root)
}

fn acquire_instance_lock(app: &tauri::AppHandle) -> Result<InstanceLock, String> {
    let root = application_data(app)?;
    let path = root.join("curis-desktop.lock");
    let file = OpenOptions::new()
        .create(true)
        .read(true)
        .write(true)
        .open(&path)
        .map_err(|error| format!("open instance lock {}: {error}", path.display()))?;
    let result = unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) };
    if result != 0 {
        return Err("Curis 已经在运行；请切换到现有窗口。".to_string());
    }
    Ok(InstanceLock { _file: file })
}

fn log_file(root: &Path, name: &str) -> Result<std::fs::File, String> {
    std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(root.join("logs").join(name))
        .map_err(|error| format!("open {name} log: {error}"))
}

fn spawn_guarded(
    app: &tauri::AppHandle,
    data_root: &Path,
    name: &str,
    target: PathBuf,
    args: &[PathBuf],
    envs: &[(&str, &str)],
) -> Result<Child, String> {
    let guardian = runtime_path(app, "guardian/curis-guardian")?;
    let stdout = log_file(data_root, &format!("{name}.log"))?;
    let stderr = log_file(data_root, &format!("{name}.err.log"))?;
    let mut command = Command::new(guardian);
    command
        .arg("--parent-pid")
        .arg(std::process::id().to_string())
        .arg("--target")
        .arg(target);
    for argument in args {
        command.arg(argument);
    }
    for (key, value) in envs {
        command.env(key, value);
    }
    command
        .current_dir(data_root)
        .stdin(Stdio::piped())
        .stdout(Stdio::from(stdout))
        .stderr(Stdio::from(stderr))
        .spawn()
        .map_err(|error| format!("启动 {name} sidecar 失败: {error}"))
        .and_then(|process| attach_parent_channel(process, name))
}

fn attach_parent_channel(mut process: Child, name: &str) -> Result<Child, String> {
    let result = (|| -> std::io::Result<()> {
        let channel = process.stdin.as_mut().ok_or_else(|| {
            std::io::Error::other("guardian lifecycle pipe missing")
        })?;
        // Child owns this write end. It must not survive any unrelated exec.
        let flags = unsafe { libc::fcntl(channel.as_raw_fd(), libc::F_GETFD) };
        if flags < 0 {
            return Err(std::io::Error::last_os_error());
        }
        if flags & libc::FD_CLOEXEC == 0 {
            return Err(std::io::Error::other("guardian lifecycle pipe is inheritable"));
        }
        writeln!(channel, "curis-guardian/v1 {}", std::process::id())
    })();
    if let Err(error) = result {
        kill_child(&mut Some(process));
        return Err(format!("启动 {name} guardian 生命周期监督失败: {error}"));
    }
    // Keep stdin inside Child for the full lifetime of the owning shell.
    Ok(process)
}

fn spawn_workspace(app: &tauri::AppHandle, data_root: &Path) -> Result<Child, String> {
    let executable = runtime_path(app, "workspace/curis-workspace")?;
    let db = data_root.join("data/curis.sqlite");
    let db_string = db.to_string_lossy().to_string();
    let data_root_string = data_root.to_string_lossy().to_string();
    spawn_guarded(
        app,
        data_root,
        "workspace",
        executable,
        &[],
        &[
            ("CURIS_DESKTOP_DATA_ROOT", &data_root_string),
            ("CURIS_DB", &db_string),
            ("CURIS_DB_PATH", &db_string),
            ("CURIS_WORKSPACE_DB", &db_string),
            ("CURIS_ENV", "local"),
            ("CURIS_PACKAGED_RUNTIME", "1"),
            ("CURIS_CREDENTIAL_BACKEND", "macos-keychain"),
            ("CURIS_PRODUCT", "workspace"),
            ("CURIS_WORKSPACE_ENVIRONMENT", "development"),
            ("CURIS_IDENTITY_MODE", "selfuse"),
            ("CURIS_LOCAL_OWNER_ENABLED", "1"),
            ("CURIS_TENANT_ID", "selfuse"),
            ("CURIS_CEO_ID", "selfuse-ceo"),
            ("PYTHONUNBUFFERED", "1"),
            ("CURIS_WORKSPACE_PORT", "8002"),
        ],
    )
}

fn spawn_gateway(app: &tauri::AppHandle, data_root: &Path) -> Result<Child, String> {
    let executable = runtime_path(app, "gateway/curis-gateway")?;
    spawn_guarded(
        app,
        data_root,
        "gateway",
        executable,
        &[],
        &[("CURIS_WORKSPACE_PORT", "8002"), ("CURIS_GATEWAY_PORT", "8080")],
    )
}

fn frontend_cache_path(relative: &Path) -> bool {
    relative.starts_with(Path::new(".next").join("cache"))
}

fn frontend_prohibited_name(name: &str) -> bool {
    let base = name.strip_suffix("-wal").or_else(|| name.strip_suffix("-shm")).or_else(|| name.strip_suffix("-journal")).unwrap_or(name);
    name == ".env" || name.starts_with(".env.") || [".db", ".sqlite", ".sqlite3"].iter().any(|suffix| base.ends_with(suffix))
}

fn frontend_files(root: &Path, relative: &Path, source: bool, files: &mut Vec<PathBuf>) -> Result<(), String> {
    let path = root.join(relative);
    let metadata = std::fs::symlink_metadata(&path).map_err(|error| format!("inspect frontend {}: {error}", path.display()))?;
    if metadata.file_type().is_symlink() {
        return Err(format!("frontend link is not allowed: {}", path.display()));
    }
    if source && frontend_cache_path(relative) {
        return Ok(());
    }
    if metadata.is_dir() {
        for entry in std::fs::read_dir(&path).map_err(|error| format!("read frontend directory: {error}"))? {
            let entry = entry.map_err(|error| format!("read frontend entry: {error}"))?;
            frontend_files(root, &relative.join(entry.file_name()), source, files)?;
        }
    } else if metadata.is_file() {
        let name = path.file_name().and_then(|value| value.to_str()).ok_or("invalid frontend filename")?;
        if frontend_prohibited_name(name) {
            return Err(format!("frontend environment/database file is not allowed: {}", path.display()));
        }
        files.push(relative.to_path_buf());
    } else {
        return Err(format!("non-regular frontend entry: {}", path.display()));
    }
    Ok(())
}

#[cfg(test)]
mod frontend_materialization_tests {
    use super::*;
    use std::os::unix::fs::symlink;

    fn fixture(name: &str) -> (PathBuf, PathBuf) {
        let root = Path::new("/private/tmp/curis-business-catalog-cache-tests-20261009-01").join(format!("{}-{name}", std::process::id()));
        assert!(!root.exists(), "retained fixture must not be overwritten");
        let source = root.join("frontend");
        let data = root.join("data-root");
        create_dir_all(source.join(".next/server")).unwrap();
        create_dir_all(source.join("node_modules/next")).unwrap();
        create_dir_all(source.join("node_modules/react")).unwrap();
        create_dir_all(source.join("node_modules/react-dom")).unwrap();
        create_dir_all(&data).unwrap();
        for file in ["server.js", "node_modules/next/package.json", "node_modules/react/package.json", "node_modules/react-dom/package.json"] {
            std::fs::write(source.join(file), b"original fixture bytes").unwrap();
        }
        std::fs::write(source.join(".next/BUILD_ID"), b"safe_BUILD-06\n").unwrap();
        (source, data)
    }

    #[test]
    fn copies_inside_data_root_without_mutating_bundle_or_copying_source_cache() {
        let (source, data) = fixture("immutable-copy");
        create_dir_all(source.join(".next/cache/images")).unwrap();
        std::fs::write(source.join(".next/cache/images/source-cache"), b"do not deploy").unwrap();
        let before = std::fs::read(source.join("server.js")).unwrap();
        let server = materialize_frontend(&source, &data).unwrap();
        assert!(server.starts_with(&data));
        assert_eq!(std::fs::read(&server).unwrap(), before);
        assert_eq!(std::fs::read(source.join("server.js")).unwrap(), before);
        assert!(!server.parent().unwrap().join(".next/cache").exists());
    }

    #[test]
    fn same_build_refreshes_current_dependency_bytes_and_retains_owned_cache() {
        let (source, data) = fixture("same-build-refresh");
        let server = materialize_frontend(&source, &data).unwrap();
        let deployed = server.parent().unwrap();
        create_dir_all(deployed.join(".next/cache/images")).unwrap();
        std::fs::write(deployed.join(".next/cache/images/user-cache"), b"retain cache").unwrap();
        std::fs::write(source.join("node_modules/next/package.json"), b"new dependency version bytes").unwrap();
        materialize_frontend(&source, &data).unwrap();
        assert_eq!(std::fs::read(deployed.join("node_modules/next/package.json")).unwrap(), b"new dependency version bytes");
        assert_eq!(std::fs::read(deployed.join(".next/cache/images/user-cache")).unwrap(), b"retain cache");
    }

    #[test]
    fn rejects_source_and_destination_links_without_following_inside_fixture_targets() {
        let (source, data) = fixture("source-link");
        let target = source.parent().unwrap().join("link-target");
        std::fs::write(&target, b"fixture target untouched").unwrap();
        symlink(&target, source.join("linked.txt")).unwrap();
        assert!(materialize_frontend(&source, &data).is_err());
        assert_eq!(std::fs::read(&target).unwrap(), b"fixture target untouched");
        let (source, data) = fixture("destination-link");
        let target = data.parent().unwrap().join("linked-directory");
        create_dir_all(&target).unwrap();
        symlink(&target, data.join("runtime")).unwrap();
        assert!(materialize_frontend(&source, &data).is_err());
        assert_eq!(std::fs::read_dir(target).unwrap().count(), 0);
    }

    #[test]
    fn refuses_unsafe_identity_missing_entries_and_unknown_destination_files() {
        let (source, data) = fixture("unsafe-id");
        std::fs::write(source.join(".next/BUILD_ID"), b"../escape").unwrap();
        assert!(materialize_frontend(&source, &data).is_err());
        let (source, data) = fixture("missing-entry");
        let incomplete = source.join("incomplete");
        create_dir_all(&incomplete).unwrap();
        assert!(materialize_frontend(&incomplete, &data).is_err());
        let (source, data) = fixture("unknown-file");
        let server = materialize_frontend(&source, &data).unwrap();
        let unknown = server.parent().unwrap().join("unknown-user-file");
        std::fs::write(&unknown, b"must not sweep").unwrap();
        assert!(materialize_frontend(&source, &data).is_err());
        assert_eq!(std::fs::read(unknown).unwrap(), b"must not sweep");
    }

    #[test]
    fn rejects_environment_database_names_and_caches_destination_links() {
        for name in [".env", ".env.local", "fixture.sqlite", "fixture.sqlite-wal", "fixture.db-shm"] {
            assert!(frontend_prohibited_name(name));
        }
        assert!(!frontend_prohibited_name("package.json"));
        let (source, data) = fixture("environment-file");
        std::fs::write(source.join(".env"), b"synthetic fixture only").unwrap();
        assert!(materialize_frontend(&source, &data).is_err());
        let (source, data) = fixture("cache-link");
        let server = materialize_frontend(&source, &data).unwrap();
        let target = source.parent().unwrap().join("cache-target");
        create_dir_all(&target).unwrap();
        symlink(target, server.parent().unwrap().join(".next/cache")).unwrap();
        assert!(materialize_frontend(&source, &data).is_err());
    }
}

fn frontend_directory(root: &Path, relative: &Path) -> Result<PathBuf, String> {
    let mut current = root.to_path_buf();
    for part in relative.components() {
        if !matches!(part, std::path::Component::Normal(_)) {
            return Err("frontend deployment path must remain inside data root".to_string());
        }
        current.push(part);
        match std::fs::symlink_metadata(&current) {
            Ok(metadata) if metadata.is_dir() && !metadata.file_type().is_symlink() => {}
            Ok(_) => return Err(format!("frontend destination is not a regular directory: {}", current.display())),
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => std::fs::create_dir(&current).map_err(|error| format!("create frontend directory: {error}"))?,
            Err(error) => return Err(format!("inspect frontend destination: {error}")),
        }
    }
    Ok(current)
}

fn materialize_frontend(source: &Path, data_root: &Path) -> Result<PathBuf, String> {
    let metadata = std::fs::symlink_metadata(data_root).map_err(|error| format!("inspect data root: {error}"))?;
    if metadata.file_type().is_symlink() || !metadata.is_dir() {
        return Err("frontend data root must be a regular directory".to_string());
    }
    let mut files = Vec::new();
    frontend_files(source, Path::new(""), true, &mut files)?;
    for required in ["server.js", ".next/BUILD_ID", "node_modules/next/package.json", "node_modules/react/package.json", "node_modules/react-dom/package.json"] {
        if !files.contains(&PathBuf::from(required)) {
            return Err(format!("frontend resource missing: {required}"));
        }
    }
    if !source.join(".next/server").is_dir() {
        return Err("frontend server resources missing".to_string());
    }
    let build_id = std::fs::read_to_string(source.join(".next/BUILD_ID")).map_err(|error| format!("read frontend build identity: {error}"))?;
    let build_id = build_id.trim();
    if build_id.is_empty() || build_id.len() > 128 || !build_id.bytes().all(|value| value.is_ascii_alphanumeric() || value == b'-' || value == b'_') {
        return Err("unsafe frontend build identity".to_string());
    }
    let destination = frontend_directory(data_root, &Path::new("runtime/frontend").join(build_id))?;
    let expected: std::collections::HashSet<_> = files.iter().collect();
    let mut existing = Vec::new();
    frontend_files(&destination, Path::new(""), false, &mut existing)?;
    for relative in existing {
        if !frontend_cache_path(&relative) && !expected.contains(&relative) {
            return Err(format!("unknown frontend deployment file retained; startup refused: {}", relative.display()));
        }
    }
    for relative in files {
        let parent = relative.parent().ok_or("frontend file has no parent")?;
        frontend_directory(&destination, parent)?;
        let target = destination.join(&relative);
        if std::fs::symlink_metadata(&target).is_ok_and(|metadata| metadata.file_type().is_symlink()) {
            return Err("frontend target link is not allowed".to_string());
        }
        let bytes = std::fs::read(source.join(&relative)).map_err(|error| format!("read frontend resource: {error}"))?;
        std::fs::write(&target, &bytes).map_err(|error| format!("refresh frontend resource: {error}"))?;
        if std::fs::read(&target).map_err(|error| format!("verify frontend resource: {error}"))? != bytes {
            return Err("frontend deployment bytes differ".to_string());
        }
    }
    Ok(destination.join("server.js"))
}

fn spawn_frontend(app: &tauri::AppHandle, data_root: &Path) -> Result<Child, String> {
    let node = runtime_path(app, "node")?;
    let server = materialize_frontend(&runtime_path(app, "frontend")?, data_root)?;
    spawn_guarded(
        app,
        data_root,
        "frontend",
        node,
        &[server],
        &[
            ("NODE_ENV", "production"),
            ("HOSTNAME", "127.0.0.1"),
            ("PORT", "3010"),
            ("NEXT_TELEMETRY_DISABLED", "1"),
        ],
    )
}

fn kill_child(child: &mut Option<Child>) {
    if let Some(process) = child.as_mut() {
        // Closing the lifeline also covers a failed/ignored guardian TERM signal.
        drop(process.stdin.take());
        unsafe {
            libc::kill(process.id() as libc::pid_t, libc::SIGTERM);
        }
        // Guardian has its own three-second target grace, then reaps the child.
        let deadline = Instant::now() + Duration::from_secs(4);
        while Instant::now() < deadline {
            if process.try_wait().ok().flatten().is_some() {
                *child = None;
                return;
            }
            std::thread::sleep(Duration::from_millis(50));
        }
        let _ = process.kill();
        let _ = process.wait();
    }
    *child = None;
}

fn kill_sidecars(app: &tauri::AppHandle) {
    if let Some(state) = app.try_state::<Sidecars>() {
        kill_child(&mut state.workspace.lock().expect("workspace state lock"));
        kill_child(&mut state.gateway.lock().expect("gateway state lock"));
        kill_child(&mut state.frontend.lock().expect("frontend state lock"));
    }
}

fn stop_for_recovery(child: &mut Option<Child>) -> Result<(), String> {
    let Some(process) = child.as_mut() else { return Ok(()); };
    drop(process.stdin.take());
    unsafe { libc::kill(process.id() as libc::pid_t, libc::SIGTERM); }
    let deadline = Instant::now() + Duration::from_secs(8);
    while Instant::now() < deadline {
        if process.try_wait().map_err(|_| "无法核实受控服务停止。".to_string())?.is_some() {
            *child = None;
            return Ok(());
        }
        std::thread::sleep(Duration::from_millis(50));
    }
    Err("受控服务未在限定时间内停止；本次数据操作已取消。".into())
}

#[derive(Clone, Copy)]
struct BusinessRunState { workspace: bool, gateway: bool }

fn readiness_or_cleanup<F>(sidecars: &Sidecars, started_workspace: bool, started_gateway: bool,
    readiness: F) -> Result<(), String>
where F: FnOnce() -> Result<(), String> {
    if let Err(error) = readiness() {
        if started_gateway {
            let mut gateway = sidecars.gateway.lock().map_err(|_| "服务状态不可用。")?;
            kill_child(&mut gateway);
        }
        if started_workspace {
            let mut workspace = sidecars.workspace.lock().map_err(|_| "服务状态不可用。")?;
            kill_child(&mut workspace);
        }
        return Err(error);
    }
    Ok(())
}

fn verified_backup_receipt(mut value: serde_json::Value, destination: &Path) -> Result<serde_json::Value, String> {
    if value["status"] != "BACKUP_VERIFIED" { return Err("备份回证尚未通过。".into()); }
    // Return only to the authenticated main-window caller, never to diagnostics.
    value["localDestination"] = serde_json::json!(destination.to_string_lossy().to_string());
    Ok(value)
}

fn resume_owned_business(app: &tauri::AppHandle, root: &Path, prior: BusinessRunState) -> Result<(), String> {
    let state: State<Sidecars> = app.state();
    let mut started_workspace = false;
    let mut started_gateway = false;
    if prior.workspace {
        let mut workspace = state.workspace.lock().map_err(|_| "服务状态不可用。")?;
        if workspace.is_none() {
            *workspace = Some(spawn_workspace(app, root)?);
            started_workspace = true;
        }
    }
    if prior.gateway {
        let mut gateway = state.gateway.lock().map_err(|_| "服务状态不可用。")?;
        if gateway.is_none() {
            match spawn_gateway(app, root) {
                Ok(value) => { *gateway = Some(value); started_gateway = true; },
                Err(error) => {
                    drop(gateway);
                    if started_workspace {
                        let mut workspace = state.workspace.lock().map_err(|_| "服务状态不可用。")?;
                        kill_child(&mut workspace);
                    }
                    return Err(format!("恢复后业务服务未启动：{error}"));
                }
            }
        }
    }
    if prior.workspace && prior.gateway {
        readiness_or_cleanup(&state, started_workspace, started_gateway,
            || wait_for_ready(90).map_err(|_| "数据已保留，但业务服务尚未就绪。".to_string()))?;
    }
    Ok(())
}

fn quiesce_business(app: &tauri::AppHandle, root: &Path) -> Result<BusinessRunState, String> {
    let state: State<Sidecars> = app.state();
    let prior = BusinessRunState {
        workspace: state.workspace.lock().map_err(|_| "服务状态不可用。")?.is_some(),
        gateway: state.gateway.lock().map_err(|_| "服务状态不可用。")?.is_some(),
    };
    let stopped = (|| -> Result<(), String> {
      {
        let mut gateway = state.gateway.lock().map_err(|_| "服务状态不可用。")?;
        stop_for_recovery(&mut gateway)?;
      }
      {
        let mut workspace = state.workspace.lock().map_err(|_| "服务状态不可用。")?;
        stop_for_recovery(&mut workspace)?;
      }
      for port in [8002_u16, 8080] {
        if TcpStream::connect_timeout(&SocketAddr::from(([127, 0, 0, 1], port)), Duration::from_millis(250)).is_ok() {
            return Err("业务服务仍在运行；未读取或替换数据。".into());
        }
      }
      let db = root.join("data/curis.sqlite");
      let output = Command::new("/usr/sbin/lsof").arg("-t").arg("--").arg(&db)
        .output().map_err(|_| "无法核实数据库写入者。".to_string())?;
      if !output.stdout.is_empty() || !matches!(output.status.code(), Some(1)) {
        return Err("数据库仍被其他进程使用；未继续数据操作。".into());
      }
      for file in [root.join("data/curis.sqlite-wal"), root.join("data/curis.sqlite-shm")] {
          if file.exists() {
              let opened = Command::new("/usr/sbin/lsof").arg("-t").arg("--").arg(&file)
                  .output().map_err(|_| "无法核实数据库附属文件。".to_string())?;
              if !opened.stdout.is_empty() || !matches!(opened.status.code(), Some(1)) {
                  return Err("数据库附属文件仍被使用；未继续数据操作。".into());
              }
          }
      }
      let package_store = std::env::var_os("CURIS_WORKSPACE_PACKAGE_STORE")
          .map(PathBuf::from).unwrap_or_else(|| root.join("data/workspace-packages"));
      for directory in [root.join("data/assets/employee-avatars"), package_store, root.join("export")] {
          if directory.is_dir() {
              let opened = Command::new("/usr/sbin/lsof").arg("-t").arg("+D").arg(&directory)
                  .output().map_err(|_| "无法核实托管文件使用者。".to_string())?;
              if !opened.stdout.is_empty() || !matches!(opened.status.code(), Some(1)) {
                  return Err("托管文件仍被其他进程使用；未继续数据操作。".into());
              }
          }
      }
      Ok(())
    })();
    if let Err(error) = stopped {
        let resumed = resume_owned_business(app, root, prior);
        return Err(resumed.err().unwrap_or(error));
    }
    Ok(prior)
}

fn restart_business(app: &tauri::AppHandle, root: &Path, prior: BusinessRunState) -> Result<(), String> {
    resume_owned_business(app, root, prior)
}

#[cfg(target_os = "macos")]
async fn recovery_panel(window: &tauri::WebviewWindow, save: bool) -> Result<Option<PathBuf>, String> {
    recovery_origin(window)?;
    let app = window.app_handle().clone();
    let current = window.clone();
    let (sender, receiver) = std::sync::mpsc::channel();
    app.run_on_main_thread(move || {
        use objc2::MainThreadMarker;
        use objc2_app_kit::{NSOpenPanel, NSSavePanel, NSModalResponseOK, NSModalResponseCancel};
        use objc2_foundation::{NSArray, NSString};
        let selected = (|| -> Result<Option<PathBuf>, String> {
            recovery_origin(&current)?;
            let marker = MainThreadMarker::new().ok_or("无法打开本机文件选择窗口。")?;
            let path = if save {
                let panel = NSSavePanel::savePanel(marker);
                panel.setMessage(Some(&NSString::from_str("完整备份包含敏感经营数据，未加密；请选择本机保存位置。")));
                panel.setNameFieldStringValue(&NSString::from_str("curis-full-backup.zip"));
                #[allow(deprecated)]
                panel.setAllowedFileTypes(Some(&NSArray::from_retained_slice(&[NSString::from_str("zip")])));
                let response = panel.runModal();
                if response == NSModalResponseCancel { return Ok(None); }
                if response != NSModalResponseOK { return Err("未选择备份位置。".into()); }
                panel.URL().and_then(|url| url.path()).map(|value| PathBuf::from(value.to_string()))
            } else {
                let panel = NSOpenPanel::openPanel(marker);
                panel.setMessage(Some(&NSString::from_str("选择要预检的 Curis 完整备份。")));
                panel.setCanChooseFiles(true);
                panel.setCanChooseDirectories(false);
                #[allow(deprecated)]
                panel.setAllowedFileTypes(Some(&NSArray::from_retained_slice(&[NSString::from_str("zip")])));
                let response = panel.runModal();
                if response == NSModalResponseCancel { return Ok(None); }
                if response != NSModalResponseOK { return Err("未选择备份文件。".into()); }
                panel.URL().and_then(|url| url.path()).map(|value| PathBuf::from(value.to_string()))
            };
            Ok(path)
        })();
        let _ = sender.send(selected);
    }).map_err(|_| "无法打开本机文件选择窗口。".to_string())?;
    tauri::async_runtime::spawn_blocking(move || receiver.recv()).await
        .map_err(|_| "文件选择未返回。".to_string())?
        .map_err(|_| "文件选择窗口已关闭。".to_string())?
}

fn focus_existing_instance() {
    #[cfg(target_os = "macos")]
    {
        // Launch Services delivers the open event to the already-running
        // bundle, bringing its window back to the foreground.
        let _ = Command::new("/usr/bin/open")
            .args(["-b", "com.curis.desktop"])
            .status();
    }
}

fn http_status(address: SocketAddr, path: &str) -> Option<u16> {
    http_status_with_headers(address, path, &[])
}

fn http_status_with_headers(address: SocketAddr, path: &str, headers: &[(&str, &str)]) -> Option<u16> {
    let mut stream = TcpStream::connect_timeout(&address, Duration::from_millis(350)).ok()?;
    stream.set_read_timeout(Some(Duration::from_millis(700))).ok()?;
    let extra_headers = headers
        .iter()
        .map(|(key, value)| format!("{key}: {value}\r\n"))
        .collect::<String>();
    let request = format!(
        "GET {path} HTTP/1.1\r\nHost: 127.0.0.1\r\n{extra_headers}Connection: close\r\n\r\n"
    );
    stream.write_all(request.as_bytes()).ok()?;
    let mut response = [0_u8; 128];
    let size = stream.read(&mut response).ok()?;
    let line = std::str::from_utf8(&response[..size]).ok()?.lines().next()?;
    line.split_whitespace().nth(1)?.parse().ok()
}

fn wait_for_ready(timeout_seconds: u64) -> Result<(), String> {
    let deadline = Instant::now() + Duration::from_secs(timeout_seconds);
    let gateway = "127.0.0.1:8080".parse::<SocketAddr>().expect("gateway address");
    let frontend = "127.0.0.1:3010".parse::<SocketAddr>().expect("frontend address");
    while Instant::now() < deadline {
        let gateway_ok = matches!(http_status(gateway, "/health"), Some(200));
        let runtime_ok = matches!(
            http_status_with_headers(
                gateway,
                "/api/workspace/runtime/foundation/companies",
                &[("X-Curis-Tenant", "selfuse"), ("X-Curis-CEO", "selfuse-ceo")]
            ),
            Some(200)
        );
        // `/ceo-office` is a real product route; any non-5xx response proves
        // the standalone server is accepting requests (redirects included).
        let frontend_ok = matches!(http_status(frontend, "/ceo-office"), Some(status) if status < 500);
        if gateway_ok && runtime_ok && frontend_ok {
            return Ok(());
        }
        std::thread::sleep(Duration::from_millis(250));
    }
    Err("Curis 启动超时：Trusted Gateway 或 Frontend 未就绪。".to_string())
}

fn open_recovery_settings(app: &tauri::AppHandle) -> Result<(), String> {
    let address = "127.0.0.1:3010".parse::<SocketAddr>().expect("frontend address");
    let route = "/ceo-office/settings?tab=data";
    let deadline = Instant::now() + Duration::from_secs(90);
    while Instant::now() < deadline {
        if matches!(http_status(address, route), Some(status) if status < 500) {
            let window = app.get_webview_window("main").ok_or("无法打开恢复设置窗口。")?;
            let url = tauri::Url::parse("http://127.0.0.1:3010/ceo-office/settings?tab=data")
                .map_err(|_| "恢复设置地址无效。")?;
            window.navigate(url).map_err(|_| "无法打开恢复设置窗口。")?;
            return Ok(());
        }
        std::thread::sleep(Duration::from_millis(250));
    }
    Err("恢复设置页面尚未就绪；业务服务保持停止。".into())
}


struct WritingExportRoot {
    root: PathBuf,
    saving: std::sync::atomic::AtomicBool,
}
struct WritingSaveGuard<'a>(&'a std::sync::atomic::AtomicBool);
impl Drop for WritingSaveGuard<'_> {
    fn drop(&mut self) { self.0.store(false, std::sync::atomic::Ordering::Release); }
}

#[derive(serde::Serialize)]
struct WritingSaveOutcome {
    status: &'static str,
    path: Option<String>,
    bytes: usize,
    verified: bool,
}

fn validate_writing_export(bytes: &[u8], scope: &serde_json::Value, package_ref: &str, formal_ref: &str) -> Result<(), String> {
    if bytes.is_empty() || bytes.len() > 2 * 1024 * 1024 {
        return Err("发布包文件为空或超过允许大小。".into());
    }
    let package: serde_json::Value = serde_json::from_slice(bytes).map_err(|_| "发布包不是合法 JSON。")?;
    if package["schema_version"] != "writing.local-package/v1" || package["metadata"]["target"] != "LOCAL_DOWNLOAD"
        || package["external_publication"] != "NOT_PUBLISHED" || package["scope"] != *scope
        || package_ref.is_empty() || formal_ref.is_empty()
        || package["package_ref"] != package_ref || package["formal_ref"] != formal_ref {
        return Err("发布包或原正式稿来源不一致。".into());
    }
    for field in ["tenant_id", "company_id", "workspace_id", "instance_id", "book_ref", "chapter_ref", "package_id", "package_version", "package_digest"] {
        if !scope[field].as_str().is_some_and(|value| !value.is_empty() && value.len() <= 256) {
            return Err("发布包缺少明确的原对象来源。".into());
        }
    }
    Ok(())
}

// Legacy S2/D4 export has no company/tenant fields. Bind its exact projection to
// the explicitly selected, scoped UI record; never invent scope claims in bytes.
fn validate_cg_export(bytes: &[u8], selection: &serde_json::Value) -> Result<(), &'static str> {
    if bytes.is_empty() || bytes.len() > 2 * 1024 * 1024 { return Err("CG_BYTES_INVALID"); }
    let package: serde_json::Value = serde_json::from_slice(bytes).map_err(|_| "CG_JSON_INVALID")?;
    let fields = ["verification_ref", "title", "body", "format", "platform", "account", "checks",
        "connection_status", "verification", "source"];
    if !selection.as_object().is_some_and(|object| object.len() == fields.len() && fields.iter().all(|key| object.contains_key(*key)))
        || !package.as_object().is_some_and(|object| object.len() == fields.len() + 3
            && fields.iter().all(|key| object.contains_key(*key)) && ["package_type", "exported_at", "notice"].iter().all(|key| object.contains_key(*key))) {
        return Err("CG_SHAPE_INVALID");
    }
    if package["package_type"] != "curis.cg.local-verification-export/1"
        || package["notice"] != "本地核验导出，不构成发布；平台连接不存在。"
        || package["verification"] != "UNVERIFIED" || package["source"] != "CEO_MANUAL"
        || package["connection_status"] != "NOT_CONNECTED" {
        return Err("CG_TRUTH_INVALID");
    }
    if fields.iter().any(|key| package[*key] != selection[*key]) { return Err("CG_SELECTION_MISMATCH"); }
    let text = |value: &serde_json::Value, max: usize, nonempty: bool| value.as_str().is_some_and(|s| s.chars().count() <= max && (!nonempty || !s.is_empty()));
    if !text(&package["verification_ref"], 256, true) || !package["verification_ref"].as_str().unwrap().starts_with("cg-verify-")
        || !text(&package["exported_at"], 128, true)
        || ["title", "body", "format"].iter().any(|key| !package[*key].is_string()) {
        return Err("CG_FIELDS_INVALID");
    }
    for key in ["account", "platform"] {
        let item = &package[key];
        if !item.as_object().is_some_and(|object| object.len() == 2 && object.contains_key("ref") && object.contains_key("name"))
            || !text(&item["ref"], 256, true) || !text(&item["name"], 2000, true) { return Err("CG_FIELDS_INVALID"); }
    }
    if !package["account"]["ref"].as_str().unwrap().starts_with("cg-account-")
        || !matches!(package["platform"]["ref"].as_str(), Some("xhs" | "douyin" | "wechat_oa" | "tiktok" | "youtube" | "bilibili")) {
        return Err("CG_FIELDS_INVALID");
    }
    let checks = package["checks"].as_array().ok_or("CG_CHECKS_INVALID")?;
    if checks.is_empty() || checks.len() > 64 { return Err("CG_CHECKS_INVALID"); }
    let mut keys = std::collections::HashSet::new();
    for item in checks {
        if !item.as_object().is_some_and(|object| object.len() == 4 && ["key", "label", "checked", "note"].iter().all(|key| object.contains_key(*key)))
            || !text(&item["key"], 256, true) || !text(&item["label"], 2000, true)
            || !item["checked"].is_boolean() || !text(&item["note"], 2000, false)
            || !keys.insert(item["key"].as_str().unwrap()) { return Err("CG_CHECKS_INVALID"); }
    }
    Ok(())
}

fn writing_export_system_path(path: &Path) -> PathBuf {
    // Accept only these system spellings, never an arbitrary selected symlink.
    // The writer still verifies canonical paths and held directory identities.
    #[cfg(target_os = "macos")]
    for (alias, canonical) in [("/tmp", "/private/tmp"), ("/var", "/private/var")] {
        if let Ok(relative) = path.strip_prefix(alias) { return Path::new(canonical).join(relative); }
    }
    path.to_path_buf()
}

fn writing_export_relative(root: &Path, destination: &Path) -> Result<PathBuf, &'static str> {
    use std::path::Component;
    use std::os::unix::ffi::OsStrExt;
    if !destination.is_absolute() || destination.as_os_str().as_bytes().split(|byte| *byte == b'/')
        .any(|part| part == b"." || part == b".." || part.contains(&0)) {
        return Err("PATH_INVALID");
    }
    let destination = writing_export_system_path(destination);
    let relative = destination.strip_prefix(writing_export_system_path(root).join("export")).map_err(|_| "OUTSIDE_EXPORT_ROOT")?;
    if relative.components().any(|part| !matches!(part, Component::Normal(_)))
        || relative.file_name().is_none()
        || relative.extension().and_then(|value| value.to_str()) != Some("json")
        || relative.file_name().is_some_and(|name| name.as_bytes().starts_with(b".")) {
        return Err("FILE_NAME_INVALID");
    }
    Ok(relative.to_path_buf())
}

fn open_writing_directory(parent: &File, name: &std::ffi::OsStr, create: bool) -> Result<File, &'static str> {
    use std::os::unix::ffi::OsStrExt;
    use std::os::fd::FromRawFd;
    let name = std::ffi::CString::new(name.as_bytes()).map_err(|_| "DIRECTORY_NAME_INVALID")?;
    if create {
        let result = unsafe { libc::mkdirat(parent.as_raw_fd(), name.as_ptr(), 0o700) };
        if result != 0 && std::io::Error::last_os_error().raw_os_error() != Some(libc::EEXIST) {
            return Err("DIRECTORY_CREATE_FAILED");
        }
    }
    let descriptor = unsafe { libc::openat(parent.as_raw_fd(), name.as_ptr(), libc::O_RDONLY | libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC) };
    if descriptor < 0 { return Err("DIRECTORY_OPEN_FAILED"); }
    Ok(unsafe { File::from_raw_fd(descriptor) })
}

fn open_writing_root(root: &Path) -> Result<File, &'static str> {
    use std::os::unix::fs::OpenOptionsExt;
    OpenOptions::new().read(true).custom_flags(libc::O_DIRECTORY | libc::O_NOFOLLOW | libc::O_CLOEXEC)
        .open(root).map_err(|_| "ROOT_OPEN_FAILED")
}

fn writing_export_root_path(root: &Path, held: &File) -> Result<PathBuf, &'static str> {
    use std::os::unix::fs::MetadataExt;
    let canonical = root.canonicalize().map_err(|_| "ROOT_RESOLVE_FAILED")?;
    let selected = std::fs::symlink_metadata(&canonical).map_err(|_| "ROOT_RESOLVE_FAILED")?;
    let opened = held.metadata().map_err(|_| "ROOT_METADATA_FAILED")?;
    if canonical != writing_export_system_path(root) || !selected.is_dir()
        || selected.dev() != opened.dev() || selected.ino() != opened.ino() {
        return Err("ROOT_PATH_OR_IDENTITY_CHANGED");
    }
    Ok(canonical)
}

fn write_writing_export(root: &Path, destination: &Path, bytes: &[u8]) -> Result<WritingSaveOutcome, &'static str> {
    use std::os::fd::FromRawFd;
    use std::os::unix::ffi::OsStrExt;
    use std::os::unix::fs::MetadataExt;
    let relative = writing_export_relative(root, destination)?;
    let root_file = open_writing_root(root)?;
    writing_export_root_path(root, &root_file)?;
    let mut directory = open_writing_directory(&root_file, std::ffi::OsStr::new("export"), true)?;
    if let Some(parent) = relative.parent() {
        for part in parent.components() { directory = open_writing_directory(&directory, part.as_os_str(), true)?; }
    }
    let expected_parent = destination.parent().ok_or("PARENT_MISSING")?;
    let parent_path = expected_parent.canonicalize().map_err(|_| "PARENT_RESOLVE_FAILED")?;
    let parent_metadata = std::fs::symlink_metadata(expected_parent).map_err(|_| "PARENT_RESOLVE_FAILED")?;
    let held_metadata = directory.metadata().map_err(|_| "DIRECTORY_METADATA_FAILED")?;
    if parent_path != writing_export_system_path(expected_parent) || !parent_metadata.is_dir()
        || parent_metadata.dev() != held_metadata.dev() || parent_metadata.ino() != held_metadata.ino() {
        return Err("PARENT_PATH_OR_IDENTITY_CHANGED");
    }
    // Every traversal and final creation is anchored to held directory FDs, never a followed path.
    let name = std::ffi::CString::new(relative.file_name().unwrap().as_bytes()).map_err(|_| "FILE_NAME_INVALID")?;
    let descriptor = unsafe { libc::openat(directory.as_raw_fd(), name.as_ptr(), libc::O_RDWR | libc::O_CREAT | libc::O_EXCL | libc::O_NOFOLLOW | libc::O_CLOEXEC, 0o600) };
    if descriptor < 0 {
        return Err(if std::io::Error::last_os_error().raw_os_error() == Some(libc::EEXIST) {
            "DESTINATION_EXISTS"
        } else { "FILE_CREATE_FAILED" });
    }
    let mut output = unsafe { File::from_raw_fd(descriptor) };
    output.write_all(bytes).map_err(|_| "FILE_WRITE_FAILED")?;
    output.sync_all().map_err(|_| "FILE_SYNC_FAILED")?;
    directory.sync_all().map_err(|_| "DIRECTORY_SYNC_FAILED")?;
    use std::io::{Seek, SeekFrom};
    output.seek(SeekFrom::Start(0)).map_err(|_| "FILE_SEEK_FAILED")?;
    let mut readback = Vec::new(); output.read_to_end(&mut readback).map_err(|_| "FILE_READBACK_FAILED")?;
    if readback != bytes { return Err("READBACK_MISMATCH"); }
    // A replaced parent/name must not be reported as a successful file at the selected location.
    let selected = std::fs::symlink_metadata(destination).map_err(|_| "DESTINATION_METADATA_FAILED")?;
    let actual = output.metadata().map_err(|_| "FILE_METADATA_FAILED")?;
    if !selected.is_file() || selected.dev() != actual.dev() || selected.ino() != actual.ino() {
        return Err("DESTINATION_IDENTITY_CHANGED");
    }
    let canonical_parent = destination.parent().ok_or("PARENT_MISSING")?.canonicalize().map_err(|_| "POSTWRITE_PARENT_RESOLVE_FAILED")?;
    if canonical_parent != writing_export_system_path(destination.parent().unwrap()) { return Err("POSTWRITE_PARENT_CHANGED"); }
    Ok(WritingSaveOutcome { status: "SAVED", path: Some(canonical_parent.join(relative.file_name().unwrap()).to_string_lossy().into()), bytes: bytes.len(), verified: true })
}

fn trusted_writing_origin(label: &str, scheme: &str, host: Option<&str>, port: Option<u16>) -> bool {
    label == "main" && scheme == "http" && host == Some("127.0.0.1") && port == Some(3010)
}

fn trusted_writing_window(window: &tauri::WebviewWindow) -> Result<(), String> {
    let url = window.url().map_err(|_| "无法确认当前窗口。")?;
    if !trusted_writing_origin(window.label(), url.scheme(), url.host_str(), url.port()) {
        return Err("只能从当前写作工作台保存文件。".into());
    }
    Ok(())
}


#[derive(serde::Serialize)]
#[serde(rename_all = "camelCase")]
struct WritingSaveDiagnostic {
    version: u8,
    stage: &'static str,
    code: &'static str,
    error_type: &'static str,
    error_class: &'static str,
    sanitized_summary: &'static str,
}

fn writing_save_failure(stage: &'static str, code: &'static str, class: &'static str) -> WritingSaveDiagnostic {
    local_save_failure(false, stage, code, class)
}

fn local_save_failure(cg: bool, stage: &'static str, code: &'static str, class: &'static str) -> WritingSaveDiagnostic {
    let diagnostic = WritingSaveDiagnostic { version: 1, stage, code, error_type: "native-string",
        error_class: class, sanitized_summary: "保存未完成；原内容与路径未记录" };
    if let Ok(serialized) = serde_json::to_string(&diagnostic) { eprintln!("{} {serialized}", if cg { "CG_SAVE_DIAGNOSTIC" } else { "WRITING_SAVE_DIAGNOSTIC" }); }
    diagnostic
}

fn writing_save_marker(stage: &'static str) {
    local_save_marker(false, stage);
}

fn local_save_marker(cg: bool, stage: &'static str) {
    let diagnostic = WritingSaveDiagnostic { version: 1, stage, code: "NSV_STAGE", error_type: "none",
        error_class: "STAGE", sanitized_summary: "阶段已到达；未记录路径或内容" };
    if let Ok(serialized) = serde_json::to_string(&diagnostic) { eprintln!("{} {serialized}", if cg { "CG_SAVE_DIAGNOSTIC" } else { "WRITING_SAVE_DIAGNOSTIC" }); }
}

#[tauri::command]
async fn save_writing_local_package(window: tauri::WebviewWindow, root: State<'_, WritingExportRoot>, fence: State<'_, OperationFence>, bytes: Vec<u8>, scope: serde_json::Value, package_ref: String, formal_ref: String) -> Result<WritingSaveOutcome, WritingSaveDiagnostic> {
    writing_save_marker("COMMAND_ENTRY");
    trusted_writing_window(&window).map_err(|_| writing_save_failure("ORIGIN", "NSV_ORIGIN", "ORIGIN_DENIED"))?;
    writing_save_marker("ORIGIN_OK");
    validate_writing_export(&bytes, &scope, &package_ref, &formal_ref)
        .map_err(|_| writing_save_failure("PACKAGE", "NSV_PACKAGE", "PACKAGE_INVALID"))?;
    writing_save_marker("PACKAGE_OK");
    save_verified_local_export(window, root, fence, bytes, false).await
}

#[tauri::command]
async fn save_cg_local_verification(window: tauri::WebviewWindow, root: State<'_, WritingExportRoot>, fence: State<'_, OperationFence>, bytes: Vec<u8>, selection: serde_json::Value) -> Result<WritingSaveOutcome, WritingSaveDiagnostic> {
    local_save_marker(true, "COMMAND_ENTRY");
    trusted_writing_window(&window).map_err(|_| local_save_failure(true, "ORIGIN", "NSV_ORIGIN", "ORIGIN_DENIED"))?;
    local_save_marker(true, "ORIGIN_OK");
    validate_cg_export(&bytes, &selection).map_err(|class| local_save_failure(true, "PACKAGE", "NSV_PACKAGE", class))?;
    local_save_marker(true, "PACKAGE_OK");
    save_verified_local_export(window, root, fence, bytes, true).await
}

async fn save_verified_local_export(window: tauri::WebviewWindow, root: State<'_, WritingExportRoot>, fence: State<'_, OperationFence>, bytes: Vec<u8>, cg: bool) -> Result<WritingSaveOutcome, WritingSaveDiagnostic> {
    let failure = move |stage, code, class| local_save_failure(cg, stage, code, class);
    let stage_marker = move |stage| local_save_marker(cg, stage);
    let _operation = enter_operation(&fence).map_err(|_| failure("LOCK", "NSV_BUSY", "SAVE_BUSY"))?;
    if root.saving.compare_exchange(false, true, std::sync::atomic::Ordering::AcqRel, std::sync::atomic::Ordering::Acquire).is_err() {
        return Err(failure("LOCK", "NSV_BUSY", "SAVE_BUSY"));
    }
    let _save_guard = WritingSaveGuard(&root.saving);
    stage_marker("LOCK_OK");
    let data_root = root.root.clone();
    #[cfg(not(target_os = "macos"))]
    { let _ = data_root; return Err(failure("RESULT", "NSV_UNSUPPORTED", "PLATFORM_UNSUPPORTED")); }
    #[cfg(target_os = "macos")]
    {
        let app = window.app_handle().clone();
        let (sender, receiver) = std::sync::mpsc::channel();
        let panel_root = data_root.clone(); let panel_window = window.clone();
        app.run_on_main_thread(move || {
            use objc2::MainThreadMarker;
            use objc2_app_kit::{NSSavePanel, NSModalResponseOK, NSModalResponseCancel};
            use objc2_foundation::{NSArray, NSString, NSURL};
            stage_marker("MAIN_ENTER");
            let result = (|| -> Result<Option<PathBuf>, WritingSaveDiagnostic> {
                trusted_writing_window(&panel_window).map_err(|_| failure("ORIGIN", "NSV_ORIGIN", "ORIGIN_DENIED"))?;
                let marker = MainThreadMarker::new().ok_or_else(|| failure("MAIN_ENTER", "NSV_MAIN", "MAIN_THREAD_UNAVAILABLE"))?;
                let panel = NSSavePanel::savePanel(marker);
                let root_descriptor = open_writing_root(&panel_root).map_err(|_| failure("DIRECTORY", "NSV_DIRECTORY", "ROOT_UNAVAILABLE"))?;
                let canonical_root = writing_export_root_path(&panel_root, &root_descriptor)
                    .map_err(|class| failure("DIRECTORY", "NSV_DIRECTORY", class))?;
                let _export_descriptor = open_writing_directory(&root_descriptor, std::ffi::OsStr::new("export"), true)
                    .map_err(|_| failure("DIRECTORY", "NSV_DIRECTORY", "EXPORT_DIRECTORY_UNAVAILABLE"))?;
                let initial_directory = canonical_root.join("export");
                panel.setDirectoryURL(Some(&NSURL::fileURLWithPath_isDirectory(&NSString::from_str(&initial_directory.to_string_lossy()), true)));
                panel.setMessage(Some(&NSString::from_str("在当前文件夹命名并保存，不会覆盖已有文件。")));
                panel.setNameFieldStringValue(&NSString::from_str(if cg { "cg-local-verification.json" } else { "writing-local-package.json" }));
                panel.setCanCreateDirectories(true);
                #[allow(deprecated)]
                panel.setAllowedFileTypes(Some(&NSArray::from_retained_slice(&[NSString::from_str("json")])));
                stage_marker("PANEL_CONFIGURED");
                stage_marker("PANEL_PRESENT");
                let response = panel.runModal();
                stage_marker("PANEL_RETURN");
                if response == NSModalResponseCancel { return Ok(None); }
                if response != NSModalResponseOK { return Err(failure("PANEL_RETURN", "NSV_PANEL", "PANEL_ABORTED")); }
                let selected = panel.URL().and_then(|url| url.path())
                    .ok_or_else(|| failure("SELECTION", "NSV_SELECTION", "NO_DESTINATION"))?;
                Ok(Some(PathBuf::from(selected.to_string())))
            })();
            let _ = sender.send(result);
        }).map_err(|_| failure("DISPATCH", "NSV_DISPATCH", "QUEUE_FAILED"))?;
        stage_marker("MAIN_QUEUED");
        let choice = tauri::async_runtime::spawn_blocking(move || receiver.recv()).await
            .map_err(|_| failure("DISPATCH", "NSV_DISPATCH", "RECEIVE_TASK_FAILED"))?
            .map_err(|_| failure("DISPATCH", "NSV_DISPATCH", "CHANNEL_CLOSED"))??;
        let Some(destination) = choice else { return Ok(WritingSaveOutcome { status: "CANCELLED", path: None, bytes: 0, verified: false }); };
        trusted_writing_window(&window).map_err(|_| failure("ORIGIN", "NSV_ORIGIN", "ORIGIN_DENIED"))?;
        stage_marker("WRITE_BEGIN");
        let outcome = tauri::async_runtime::spawn_blocking(move || write_writing_export(&data_root, &destination, &bytes)).await
            .map_err(|_| failure("WRITE", "NSV_WRITE", "WRITE_TASK_FAILED"))?
            .map_err(|class| failure("WRITE", "NSV_WRITE", class))?;
        stage_marker("READBACK_OK");
        trusted_writing_window(&window).map_err(|_| failure("ORIGIN", "NSV_ORIGIN", "ORIGIN_DENIED"))?;
        Ok(outcome)
    }
}

#[tauri::command]
async fn create_curis_backup(window: tauri::WebviewWindow, state: State<'_, RecoveryState>,
    lock: State<'_, InstanceLock>, fence: State<'_, OperationFence>) -> Result<serde_json::Value, String> {
    recovery_origin(&window)?;
    #[cfg(not(target_os = "macos"))]
    { let _ = (&state, &lock, &fence); return Err("此平台暂不支持本机备份。".into()); }
    #[cfg(target_os = "macos")]
    {
        let Some(destination) = recovery_panel(&window, true).await? else { return Ok(serde_json::json!({"status":"CANCELLED"})); };
        recovery_origin(&window)?;
        let _operation = enter_operation(&fence)?;
        let app = window.app_handle();
        let prior = quiesce_business(app, &state.root)?;
        let result = recovery_helper(app, &state.root, &lock, "full-backup", &["--archive", &destination.to_string_lossy()]);
        let resumed = restart_business(app, &state.root, prior);
        resumed?;
        verified_backup_receipt(result?, &destination)
    }
}

#[tauri::command]
async fn preflight_curis_restore(window: tauri::WebviewWindow, state: State<'_, RecoveryState>,
    lock: State<'_, InstanceLock>, fence: State<'_, OperationFence>) -> Result<serde_json::Value, String> {
    recovery_origin(&window)?;
    #[cfg(not(target_os = "macos"))]
    { let _ = (&state, &lock, &fence); return Err("此平台暂不支持本机恢复。".into()); }
    #[cfg(target_os = "macos")]
    {
        let Some(archive) = recovery_panel(&window, false).await? else { return Ok(serde_json::json!({"status":"CANCELLED"})); };
        recovery_origin(&window)?;
        let _operation = enter_operation(&fence)?;
        let value = recovery_helper(window.app_handle(), &state.root, &lock, "full-preflight", &["--archive", &archive.to_string_lossy()])?;
        if value["status"] != "PREFLIGHT_OK" { return Err("恢复预检尚未通过。".into()); }
        let archive_sha = value["archiveSha256"].as_str().ok_or("备份摘要无效。")?.to_string();
        let generation = value["currentGeneration"].as_str().ok_or("当前数据指纹无效。")?.to_string();
        let (root_device, root_inode) = root_identity(&state.root)?;
        let (archive_device, archive_inode, archive_size, archive_mtime_ns) = archive_identity(&archive)?;
        let id = recovery_token()?;
        *state.preview.lock().map_err(|_| "恢复确认状态不可用。")? = Some(RecoveryPreview {
            id: id.clone(), archive, archive_sha, generation, root_device, root_inode,
            archive_device, archive_inode, archive_size, archive_mtime_ns,
            expires: Instant::now() + Duration::from_secs(300),
        });
        let mut display = value;
        display["confirmationId"] = serde_json::json!(id);
        display["expiresInSeconds"] = serde_json::json!(300);
        Ok(display)
    }
}

#[tauri::command]
fn cancel_curis_restore(window: tauri::WebviewWindow, state: State<'_, RecoveryState>) -> Result<serde_json::Value, String> {
    recovery_origin(&window)?;
    *state.preview.lock().map_err(|_| "恢复确认状态不可用。")? = None;
    Ok(serde_json::json!({"status":"CANCELLED"}))
}

#[tauri::command]
fn read_curis_recovery_status(window: tauri::WebviewWindow, state: State<'_, RecoveryState>, lock: State<'_, InstanceLock>) -> Result<serde_json::Value, String> {
    recovery_origin(&window)?;
    recovery_helper(window.app_handle(), &state.root, &lock, "full-status", &[])
}

#[cfg(test)]
mod recovery_boundary_tests {
    use super::*;

    #[test]
    fn operation_fence_excludes_a_concurrent_writing_or_recovery_action() {
        let fence = OperationFence(Arc::new(AtomicBool::new(false)));
        let held = enter_operation(&fence).unwrap();
        assert!(enter_operation(&fence).is_err());
        drop(held);
        assert!(enter_operation(&fence).is_ok());
    }

    #[test]
    fn confirmation_is_unpredictable_and_origin_is_main_loopback_only() {
        let first = recovery_token().unwrap();
        let second = recovery_token().unwrap();
        assert_eq!(first.len(), 64);
        assert_ne!(first, second);
        assert!(trusted_writing_origin("main", "http", Some("127.0.0.1"), Some(3010)));
        for (label, scheme, host, port) in [
            ("other", "http", Some("127.0.0.1"), Some(3010)),
            ("main", "https", Some("127.0.0.1"), Some(3010)),
            ("main", "http", Some("127.0.0.1"), Some(8080)),
            ("main", "http", Some("evil.invalid"), Some(3010)),
        ] {
            assert!(!trusted_writing_origin(label, scheme, host, port));
        }
    }

    #[test]
    fn damaged_or_missing_known_data_enters_frontend_only_recovery_mode() {
        for status in ["UNKNOWN", "RECOVERY_HOLD", "RECOVERY_REQUIRED"] {
            assert!(recovery_requires_safe_mode(&serde_json::json!({"status":status})));
        }
        for status in ["RESTORED", "ROLLED_BACK", "NO_PENDING_RECOVERY"] {
            assert!(!recovery_requires_safe_mode(&serde_json::json!({"status":status})));
        }
    }

    #[test]
    fn failed_readiness_cleans_only_new_owned_children() {
        let preserved = Command::new("/bin/sleep").arg("30").spawn().unwrap();
        let fresh = Command::new("/bin/sleep").arg("30").spawn().unwrap();
        let sidecars = Sidecars {
            workspace: Mutex::new(Some(preserved)), gateway: Mutex::new(Some(fresh)),
            frontend: Mutex::new(None),
        };
        let result = readiness_or_cleanup(&sidecars, false, true, || Err("readiness failed".into()));
        let kept = sidecars.workspace.lock().unwrap().is_some();
        let removed = sidecars.gateway.lock().unwrap().is_none();
        kill_child(&mut sidecars.workspace.lock().unwrap());
        assert_eq!(result.unwrap_err(), "readiness failed");
        assert!(kept, "previously owned child must remain untouched by recovery cleanup");
        assert!(removed, "new gateway child must be stopped and reaped");

        let new_workspace = Command::new("/bin/sleep").arg("30").spawn().unwrap();
        let new_gateway = Command::new("/bin/sleep").arg("30").spawn().unwrap();
        let both_new = Sidecars {
            workspace: Mutex::new(Some(new_workspace)), gateway: Mutex::new(Some(new_gateway)),
            frontend: Mutex::new(None),
        };
        assert!(readiness_or_cleanup(&both_new, true, true, || Err("not ready".into())).is_err());
        assert!(both_new.workspace.lock().unwrap().is_none());
        assert!(both_new.gateway.lock().unwrap().is_none());
    }

    #[test]
    fn selected_backup_destination_is_only_in_verified_user_receipt() {
        let destination = Path::new("/private/tmp/selected-by-user.curis.zip");
        let receipt = verified_backup_receipt(serde_json::json!({"status":"BACKUP_VERIFIED"}), destination).unwrap();
        assert_eq!(receipt["localDestination"], destination.to_string_lossy().as_ref());
        let failure = verified_backup_receipt(serde_json::json!({"status":"FAILED"}), destination).unwrap_err();
        assert!(!failure.contains("selected-by-user"));
    }
}

#[tauri::command]
async fn commit_curis_restore(window: tauri::WebviewWindow, state: State<'_, RecoveryState>,
    lock: State<'_, InstanceLock>, fence: State<'_, OperationFence>, confirmation_id: String) -> Result<serde_json::Value, String> {
    recovery_origin(&window)?;
    let _operation = enter_operation(&fence)?;
    let preview = state.preview.lock().map_err(|_| "恢复确认状态不可用。")?.take().ok_or("请重新选择备份并预检。")?;
    if preview.id != confirmation_id || Instant::now() > preview.expires { return Err("恢复确认已失效，请重新预检。".into()); }
    let (root_device, root_inode) = root_identity(&state.root)?;
    let (archive_device, archive_inode, archive_size, archive_mtime_ns) = archive_identity(&preview.archive)?;
    if (root_device, root_inode) != (preview.root_device, preview.root_inode)
        || (archive_device, archive_inode, archive_size, archive_mtime_ns) !=
           (preview.archive_device, preview.archive_inode, preview.archive_size, preview.archive_mtime_ns) {
        return Err("备份或当前数据目录已变化，请重新预检。".into());
    }
    recovery_origin(&window)?;
    let app = window.app_handle();
    let prior = quiesce_business(app, &state.root)?;
    let archive = preview.archive.to_string_lossy();
    let rerun = recovery_helper(app, &state.root, &lock, "full-preflight", &["--archive", &archive]);
    let result = match rerun {
        Ok(value) if value["archiveSha256"] == preview.archive_sha && value["currentGeneration"] == preview.generation =>
            recovery_helper(app, &state.root, &lock, "full-commit", &["--archive", &archive,
                "--archive-sha256", &preview.archive_sha, "--current-generation", &preview.generation]),
        _ => Err("当前数据或备份已变化，请重新预检。".into()),
    };
    let status = recovery_helper(app, &state.root, &lock, "full-status", &[])?;
    if status["status"] == "UNKNOWN" { return Ok(status); }
    if status["status"] == "RECOVERY_REQUIRED" { return result.map(|_| status); }
    if status["status"] == "RECOVERY_HOLD" {
        return result.map(|value| if value["status"] == "RECOVERY_HOLD" { value } else { status });
    }
    let value = match result {
        Ok(value) => value,
        Err(error) => {
            restart_business(app, &state.root, prior)?;
            return Err(error);
        }
    };
    if value["status"] != "RESTORED" {
        restart_business(app, &state.root, prior)?;
        return Err("恢复未取得完整读回回证。".into());
    }
    restart_business(app, &state.root, BusinessRunState { workspace: true, gateway: true })?;
    Ok(value)
}


#[cfg(test)]
mod writing_export_tests {
    use super::*;
    #[test]
    fn writing_save_acl_origin_and_sanitized_diagnostic() {
        assert!(trusted_writing_origin("main", "http", Some("127.0.0.1"), Some(3010)));
        for (label, scheme, host, port) in [("other", "http", Some("127.0.0.1"), Some(3010)), ("main", "http", Some("localhost"), Some(3010)), ("main", "http", Some("127.0.0.1"), Some(8080)), ("main", "https", Some("127.0.0.1"), Some(3010))] {
            assert!(!trusted_writing_origin(label, scheme, host, port));
        }
        let diagnostic = writing_save_failure("DIRECTORY", "NSV_DIRECTORY", "ROOT_UNAVAILABLE");
        let json = serde_json::to_value(diagnostic).unwrap();
        assert_eq!(json.as_object().unwrap().len(), 6);
        assert_eq!(json["code"], "NSV_DIRECTORY");
        assert!(!json.to_string().contains("/"));
    }

    #[test]
    fn writing_export_rejects_invalid_json_scope_and_paths() {
        let scope = serde_json::json!({"tenant_id":"t","company_id":"c","workspace_id":"w","instance_id":"i","book_ref":"b","chapter_ref":"ch","package_id":"p","package_version":"v","package_digest":"d"});
        let package = serde_json::json!({"schema_version":"writing.local-package/v1","metadata":{"target":"LOCAL_DOWNLOAD"},"external_publication":"NOT_PUBLISHED","scope":scope,"package_ref":"pkg","formal_ref":"formal"});
        let bytes = serde_json::to_vec(&package).unwrap();
        assert!(validate_writing_export(&bytes, &scope, "pkg", "formal").is_ok());
        assert!(validate_writing_export(&bytes, &scope, "other", "formal").is_err());
        assert!(validate_writing_export(b"bad", &scope, "pkg", "formal").is_err());
        assert!(validate_writing_export(&vec![0;2*1024*1024+1], &scope, "pkg", "formal").is_err());
        let root = Path::new("/controlled/root");
        for path in ["/other/out.json","/controlled/root/export/../data/out.json","/controlled/root/export/out.sqlite","/controlled/root/export/.hidden.json"] {
            assert!(writing_export_relative(root, Path::new(path)).is_err(), "{path}");
        }
        assert!(writing_export_relative(root, Path::new("/controlled/root/export/nested/out.json")).is_ok());
    }
    #[test]
    fn writing_export_new_file_readback_and_no_overwrite_or_symlink() {
        use std::os::unix::fs::symlink;
        let base = std::env::var_os("CURIS_EXPORT_TEST_ROOT").expect("exact isolated test root required");
        let root = PathBuf::from(base).join(format!("native-export-{}", std::process::id()));
        create_dir_all(&root).unwrap();
        let path = root.join("export/nested/package.json");
        let result = write_writing_export(&root, &path, b"{\"checked\":true}").unwrap();
        assert_eq!(result.status,"SAVED"); assert!(result.verified);
        assert_eq!(std::fs::read(&path).unwrap(), b"{\"checked\":true}");
        assert!(write_writing_export(&root,&path,b"overwrite").is_err());
        assert_eq!(std::fs::read(&path).unwrap(), b"{\"checked\":true}");
        let target = root.join("owned-symlink-target");create_dir_all(&target).unwrap();
        symlink(&target, root.join("export/link")).unwrap();
        assert!(write_writing_export(&root,&root.join("export/link/no.json"),b"never").is_err());
        assert!(!target.join("no.json").exists());
        symlink(&path, root.join("export/file.json")).unwrap();
        assert!(write_writing_export(&root,&root.join("export/file.json"),b"never").is_err());
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let application = match tauri::Builder::default()
        .manage(Sidecars {
            workspace: Mutex::new(None),
            gateway: Mutex::new(None),
            frontend: Mutex::new(None),
        })
        .manage(OperationFence(Arc::new(AtomicBool::new(false))))
        .invoke_handler(tauri::generate_handler![save_writing_local_package, save_cg_local_verification, create_curis_backup,
            preflight_curis_restore, commit_curis_restore, cancel_curis_restore, read_curis_recovery_status])
        .setup(|app| {
            #[cfg(target_os = "macos")]
            if !app.manage(Arc::new(Mutex::new(reader_vm_broker::FixtureSupervisor::new(app.path().resource_dir()?))))
                || !app.manage(Arc::new(reader_vm_broker::FixtureControl::default())) {
                return Err(std::io::Error::other("Reader fixture owner already registered").into());
            }
            let result = (|| -> Result<(), String> {
                let lock = acquire_instance_lock(app.handle())?;
                app.manage(lock);
                let data_root = application_data(app.handle())?;
                let native_lock: State<InstanceLock> = app.state();
                let recovered = recovery_helper(app.handle(), &data_root, &native_lock, "full-reconcile", &[])?;
                app.manage(RecoveryState { root: data_root.clone(), preview: Mutex::new(None) });
                app.manage(WritingExportRoot { root: data_root.clone(), saving: std::sync::atomic::AtomicBool::new(false) });
                if recovery_requires_safe_mode(&recovered) {
                    // Keep the Settings recovery surface reachable while every business writer stays stopped.
                    let frontend = spawn_frontend(app.handle(), &data_root)?;
                    let state: State<Sidecars> = app.state();
                    *state.frontend.lock().expect("frontend state lock") = Some(frontend);
                    open_recovery_settings(app.handle())?;
                    return Ok(());
                }
                let workspace = spawn_workspace(app.handle(), &data_root)?;
                let gateway = match spawn_gateway(app.handle(), &data_root) {
                    Ok(process) => process,
                    Err(error) => {
                        kill_child(&mut Some(workspace));
                        return Err(error);
                    }
                };
                let frontend = match spawn_frontend(app.handle(), &data_root) {
                    Ok(process) => process,
                    Err(error) => {
                        kill_child(&mut Some(gateway));
                        kill_child(&mut Some(workspace));
                        return Err(error);
                    }
                };
                let state: State<Sidecars> = app.state();
                *state.workspace.lock().expect("workspace state lock") = Some(workspace);
                *state.gateway.lock().expect("gateway state lock") = Some(gateway);
                *state.frontend.lock().expect("frontend state lock") = Some(frontend);
                // T9: 冷启动实测约 50s（三个 sidecar 全部 LISTEN 需要 ~55s），原 45s 门限
                // 会在服务实际就绪前把 app 判死并 exit(1)，导致 E2E 无法启动。放宽到 90s。
                wait_for_ready(90)
            })();
            if let Err(error) = result {
                let duplicate = error.contains("Curis 已经在运行");
                eprintln!("Curis 启动失败: {error}");
                if duplicate {
                    focus_existing_instance();
                } else {
                    kill_sidecars(app.handle());
                }
                app.handle().exit(if duplicate { 0 } else { 1 });
            }
            Ok(())
        })
        .on_window_event(|window, event| {
            if let tauri::WindowEvent::Destroyed = event {
                kill_sidecars(window.app_handle());
            }
        })
        .build(tauri::generate_context!()) {
        Ok(application) => application,
        Err(error) => {
            let message = error.to_string();
            eprintln!("Curis 启动失败: {message}");
            if message.contains("Curis 已经在运行") {
                focus_existing_instance();
            }
            return;
        }
    };
    application.run(|app_handle, event| {
            if let tauri::RunEvent::Exit = event {
                kill_sidecars(app_handle);
            }
        });
}
