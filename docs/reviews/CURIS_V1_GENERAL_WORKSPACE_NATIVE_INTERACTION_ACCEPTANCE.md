# CURIS V1 — General Workspace Native Interaction Acceptance

Status: Review
Authority Class: EVIDENCE / ACCEPTANCE REVIEW
Issue: `V1-P1-010`
Owner: Main Development Session
Date: 2026-08-30

## Verdict

`V1-P1-010: BLOCKED BY NATIVE AUTOMATION TOOLING`

`GENERAL WORKSPACE P1 = IMPLEMENTED / PARTIAL`

The remaining gate is the native interaction evidence toolchain. This run did not identify a Curis product or packaged-WebView defect, and it does not substitute Browser, HTTP, API, SQLite or screenshots for a successful native user action.

## Packaged App Identity

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Executable: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app/Contents/MacOS/curis-desktop`
- Executable SHA-256: `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`
- Isolated HOME root: `/tmp/curis-general-p1-desktop.wcPpRU/home`
- Isolated app-data DB: `/tmp/curis-general-p1-desktop.wcPpRU/home/Library/Application Support/com.curis.desktop/data/curis.sqlite`
- Native interaction tool: `@oai/sky` Computer Use over macOS Accessibility/native bridge

## Native Attempt Timeline

All timestamps are Asia/Shanghai on 2026-08-30.

1. `00:03:56` — launched the exact packaged executable with the isolated HOME; packaged frontend and sidecars became ready on `127.0.0.1:3010`, `127.0.0.1:8002` and `127.0.0.1:8080`.
2. `00:04` — Computer Use read the real `Curis — CEO Office` window and its packaged Tauri WebView Accessibility tree. The tree exposed `回到业务现场 →` with the canonical route `workspace_id=workspace-v1-general`.
3. `00:04` — element-index click on that real link failed immediately with `Sky Computer Use native pipe closed before response`. A fresh state read proved the page remained on `/ceo-office`.
4. `00:05` — coordinate click against the same visible packaged link failed with the same native-pipe error and produced no navigation.
5. `00:05` — a display-name diagnostic revealed that the automation bridge could start a second Curis copy from `/Users/yy/.codex/worktrees/d126/...` because several installed builds share `com.curis.desktop`. That automation-created duplicate was terminated. The accepted packaged instance and its sidecars remained the only Curis processes.
6. `00:05` — after duplicate removal and a fresh bridge reset, a full-path element click against the exact accepted app again failed with the same native-pipe error. The WebView remained on `/ceo-office`.
7. `00:06` — the exact packaged app was closed and reopened with the same isolated HOME. Computer Use again read `/ceo-office`, `通用业务公司`, and the same `workspace-v1-general` link from the real native window.

## Fault Attribution

### Independently proven

- The accepted packaged executable launches and renders its real Tauri WebView.
- The native Accessibility tree is readable and contains the expected CEO Desk and canonical General Workspace link.
- The packaged sidecars start without port conflict.
- The same isolated state is readable after app restart.
- The isolated DB retains `company-v1-general`, `business-v1-general` and `workspace-v1-general` with `RESOLVED` canonical business relation.
- Supporting persisted Work/Result truth remains present, including `work-b99c62c719f7bc7bc89bcd229e748468`, `work-dee6304689df3d39bd4470504efd8e53` and their real FAILED/COMPLETED task and Artifact records.

### Not proven

- Native navigation from CEO Desk into General Workspace.
- Any native Result/Evidence, Work, Conversation or return interaction.
- Native close/reopen followed by interactive re-entry to the same Workspace.

### Attribution decision

The failure is classified as native automation tooling, not a Curis implementation failure:

- window rendering and Accessibility reads succeed;
- both element and coordinate actions fail at the bridge boundary before a response;
- the action does not navigate the WebView;
- removing the only observed duplicate/process conflict does not change the failure;
- no repository-provided Tauri/WebDriver/native harness was found that could legitimately replace Computer Use for this gate.

The existence of multiple registered builds with the same bundle identifier is relevant to display-name targeting, but it does not explain the final failure because the final attempt used the exact app path with only that instance running.

## Evidence

- Before native action: `/tmp/curis-v1-p1-010-native-before.png`
- After failed full-path action: `/tmp/curis-v1-p1-010-native-after-failed-click.png`
- Same isolated state after packaged restart: `/tmp/curis-v1-p1-010-native-reopen.png`
- Exact native error: `Sky Computer Use native pipe closed before response`
- Supporting isolated DB final integrity: `ok`

The screenshots and SQLite facts are supporting evidence only. They do not close the native interaction gate.

## Active DB Safety

Both repository-active SQLite files were byte-identical before and after this acceptance run:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

Only the repository-external isolated app-data DB was opened by the packaged app.

## Recovery Entry

Retry only `V1-P1-010` when a native automation tool can successfully act on the exact packaged Tauri WebView. Start the accepted package by full path with the same or a newly approved isolated state, avoid display-name targeting while duplicate bundle registrations exist, and require one successful native CEO Desk → General Workspace action before continuing the remaining interaction/restart path.

No General Workspace feature, Runtime schema, Product Authority or UI semantics should be changed to address this tooling failure.

