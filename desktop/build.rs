fn main() {
    tauri_build::try_build(tauri_build::Attributes::new().app_manifest(
        tauri_build::AppManifest::new().commands(&[
            "save_writing_local_package", "save_cg_local_verification", "create_curis_backup", "preflight_curis_restore",
            "commit_curis_restore", "cancel_curis_restore", "read_curis_recovery_status",
        ]),
    )).expect("Tauri build failed");
}
