# CURIS Workspace Storage Breakdown

Status: Review  
Authority Class: REVIEW / STORAGE EVIDENCE  
Measured: 2026-09-24  
Method: metadata-only `lstat` file sizes; no file contents or database records read. Decimal GB/MB (1 GB = 1,000,000,000 B).

## Scope and reconciliation

- Live metadata scan: **269,451 files / 50,521 directories / 13,940,609,106 B (13.941 GB apparent file size)**. Compared with the supplied Wave 3 snapshot (269,430 files / 50,521 directories / 13,940,578,383 B), the scan is +21 files and +30,723 B. Category totals reconcile to this live scan; the small delta is filesystem state drift since the supplied snapshot.
- The byte total sums apparent file lengths (`st_size`), not allocated filesystem blocks. Allocated bytes reported separately: 14,701,899,776 B. Symlink directories were counted as directory entries and not followed; directory metadata is excluded. Hard-linked content may be counted once per path, so allocated physical usage can differ.
- Main tables below cover only this Workspace. External Codex worktrees are secondary and are not added to the Workspace total. The four in-workspace `.worktrees/` directories are counted once under Git Worktrees.
- The storage scan reads names/stat metadata only; it does not read file or database contents. Worktree size rows were refreshed from path metadata, while branch/dirty/untracked details use the existing Worktree Audit. No cleanup was performed.

## Main storage categories

| Category | Files | Directories | Bytes | GB | % Workspace | Reclaimability |
|---|---:|---:|---:|---:|---:|---|
| Git Worktrees | 166,764 | 36,604 | 3,303,189,101 | 3.303 | 23.69% | HOLD |
| Git Repository Data | 6,403 | 359 | 3,421,311,272 | 3.421 | 24.54% | HOLD |
| Dependencies | 37,202 | 5,817 | 1,042,668,338 | 1.043 | 7.48% | CONDITIONAL |
| Regenerable bytecode/test cache | 3,470 | 191 | 46,880,927 | 0.047 | 0.34% | REGENERABLE |
| Build / Cache / Generated | 18,157 | 3,376 | 4,061,511,539 | 4.062 | 29.13% | CONDITIONAL |
| Runtime Distribution / Staging | 210 | 52 | 327,384,030 | 0.327 | 2.35% | HOLD |
| Product / Project Documentation | 3,011 | 294 | 349,149,265 | 0.349 | 2.50% | KEEP |
| Active HTML / UI References | 32 | 2 | 6,899,736 | 0.007 | 0.05% | KEEP |
| Historical Exploration / UI | 907 | 156 | 93,581,087 | 0.094 | 0.67% | HOLD |
| Design / Figma Assets | 7 | 0 | 69,488 | 0.000 | 0.00% | HOLD |
| Images / Screenshots | 423 | 67 | 290,737,003 | 0.291 | 2.09% | HOLD |
| Business Assets | 5 | 0 | 96,463 | 0.000 | 0.00% | KEEP |
| Database / Persistent Data | 13 | 7 | 6,971,392 | 0.007 | 0.05% | HOLD |
| Logs | 67 | 29 | 7,821,240 | 0.008 | 0.06% | CONDITIONAL |
| Archives / Backups | 23,637 | 2,652 | 745,110,769 | 0.745 | 5.34% | HOLD |
| Production Source Code | 7,548 | 778 | 79,886,741 | 0.080 | 0.57% | KEEP |
| Other / Unknown | 1,595 | 137 | 157,340,715 | 0.157 | 1.13% | UNKNOWN |

**Check:** category sums = 13,940,609,106 B; filesystem scan = 13,940,609,106 B; difference = 0 B. Files: 269,451; directories: 50,521.

Build / Cache / Generated includes current desktop build output and remaining cache/output roots; its row-level `CONDITIONAL` status is not deletion approval. Clearly disposable cache candidates are isolated as `Regenerable bytecode/test cache`. Worktree subcategories are shown separately and are HOLD regardless of child type.

## Raw top 30 directories (parent and child rows can overlap)

| Rank | Path | Subtree bytes | % Workspace | Dominant category |
|---:|---|---:|---:|---|
| 1 | `desktop` | 6,104,498,057 | 43.79% | Build / Cache / Generated |
| 2 | `desktop/target` | 4,720,773,313 | 33.86% | Build / Cache / Generated |
| 3 | `desktop/target/release` | 3,629,771,759 | 26.04% | Build / Cache / Generated |
| 4 | `.git` | 3,421,311,272 | 24.54% | Git Repository Data |
| 5 | `.git/objects` | 3,416,899,967 | 24.51% | Git Repository Data |
| 6 | `.worktrees` | 3,303,189,101 | 23.69% | Git Worktrees |
| 7 | `.git/objects/pack` | 3,039,248,430 | 21.80% | Git Repository Data |
| 8 | `.worktrees/ai-secretary-planning` | 1,623,159,188 | 11.64% | Git Worktrees |
| 9 | `desktop/target/release/bundle` | 1,440,178,695 | 10.33% | Build / Cache / Generated |
| 10 | `desktop/.runtime` | 1,353,136,631 | 9.71% | Archives / Backups |
| 11 | `.worktrees/ai-secretary-planning/.curis` | 1,137,858,825 | 8.16% | Git Worktrees |
| 12 | `.worktrees/ai-secretary-planning/.curis/content-runtime` | 1,136,834,825 | 8.15% | Git Worktrees |
| 13 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources` | 1,108,589,047 | 7.95% | Git Worktrees |
| 14 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn` | 1,098,959,264 | 7.88% | Git Worktrees |
| 15 | `desktop/target/debug` | 1,090,991,221 | 7.83% | Build / Cache / Generated |
| 16 | `desktop/target/release/deps` | 1,037,264,853 | 7.44% | Build / Cache / Generated |
| 17 | `desktop/target/release/bundle/macos` | 990,900,234 | 7.11% | Build / Cache / Generated |
| 18 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project` | 969,780,526 | 6.96% | Git Worktrees |
| 19 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-backend` | 871,670,348 | 6.25% | Git Worktrees |
| 20 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-backend/node_modules` | 842,227,293 | 6.04% | Git Worktrees |
| 21 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-backend/node_modules/.pnpm` | 841,994,853 | 6.04% | Git Worktrees |
| 22 | `desktop/target/release/runtime` | 818,914,896 | 5.87% | Build / Cache / Generated |
| 23 | `desktop/.runtime/.trash` | 745,110,769 | 5.34% | Archives / Backups |
| 24 | `.worktrees/company-runtime-office-view` | 714,955,640 | 5.13% | Git Worktrees |
| 25 | `.worktrees/company-runtime-office-view/frontend` | 676,874,542 | 4.86% | Git Worktrees |
| 26 | `desktop/.runtime/.trash/runtime` | 604,511,701 | 4.34% | Archives / Backups |
| 27 | `desktop/target/release/bundle/macos/CurisCopy.app` | 533,406,149 | 3.83% | Build / Cache / Generated |
| 28 | `desktop/target/release/bundle/macos/CurisCopy.app/Contents` | 533,406,149 | 3.83% | Build / Cache / Generated |
| 29 | `desktop/target/debug/deps` | 528,623,418 | 3.79% | Build / Cache / Generated |
| 30 | `desktop/target/release/bundle/macos/CurisCopy.app/Contents/Resources` | 525,360,728 | 3.77% | Build / Cache / Generated |

## Top 30 non-overlapping storage roots

Each row is a disjoint root; no selected row is nested under another selected row. A parent such as `desktop` can contain several subcategories; its largest children are shown in the raw directory table. The Content Growth root is mixed: its four explicitly active files are KEEP_ACTIVE, while older files under the same root dominate its historical roll-up.

| Rank | Path | Size | % Workspace | Category | Git / Worktree? | Current Role | Potentially Regenerable? | Safety Status |
|---:|---|---:|---:|---|---|---|---|---|
| 1 | `desktop` | 6,104,498,057 | 43.79% | Build / Cache / Generated | no | Generated / installed data | Conditional | Requires a separate process/rebuild/safety gate |
| 2 | `.git` | 3,421,311,272 | 24.54% | Git Repository Data | no | Protected or status unresolved | No — HOLD | Do not touch under current decisions |
| 3 | `.worktrees` | 3,303,189,101 | 23.69% | Git Worktrees | yes | Protected or status unresolved | No — HOLD | Do not touch under current decisions |
| 4 | `docs` | 364,328,547 | 2.61% | Product / Project Documentation | no | Current / retained | No — KEEP | Retain as current input |
| 5 | `RD_MULTI_AGENT_RESEARCH_LAB` | 255,382,651 | 1.83% | Other / Unknown | no | Protected or status unresolved | Unknown | Retain pending evidence |
| 6 | `artifacts` | 209,359,336 | 1.50% | Images / Screenshots | no | Protected or status unresolved | No — HOLD | Do not touch under current decisions |
| 7 | `backend` | 78,409,201 | 0.56% | Dependencies | no | Generated / installed data | Conditional | Requires a separate process/rebuild/safety gate |
| 8 | `deploy` | 46,568,464 | 0.33% | Build / Cache / Generated | no | Generated / installed data | Conditional | Requires a separate process/rebuild/safety gate |
| 9 | `.venv` | 42,625,793 | 0.31% | Dependencies | no | Generated / installed data | Conditional | Requires a separate process/rebuild/safety gate |
| 10 | `curis-ui-prototype` | 27,458,526 | 0.20% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 11 | `.design` | 12,768,941 | 0.09% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 12 | `frontend` | 7,848,970 | 0.06% | Production Source Code | no | Current / retained | No — KEEP | Retain as current input |
| 13 | `MUSIC_BUSINESS_CODEX_HTML_EXPLORATION` | 6,422,483 | 0.05% | Active HTML / UI References | no | Current / retained | No — KEEP | Retain as current input |
| 14 | `CURIS_PROJECT_WORKSPACE_VISUAL_EXPLORATION` | 6,179,068 | 0.04% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 15 | `RD_WORKSPACE_HTML_EXPLORATION` | 5,277,004 | 0.04% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 16 | `data` | 4,903,878 | 0.04% | Database / Persistent Data | no | Protected or status unresolved | No — HOLD | Do not touch under current decisions |
| 17 | `MUSIC_WORKSPACE_HTML_EXPLORATION` | 4,038,350 | 0.03% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 18 | `CURIS_OPERATIONAL_VISUAL_EXPLORATION` | 3,033,661 | 0.02% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 19 | `issues` | 2,056,210 | 0.01% | Product / Project Documentation | no | Current / retained | No — KEEP | Retain as current input |
| 20 | `CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION` | 2,049,373 | 0.01% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 21 | `curis-ui-prototype.bak` | 2,028,544 | 0.01% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 22 | `.workbuddy` | 1,511,576 | 0.01% | Product / Project Documentation | no | Current / retained | No — KEEP | Retain as current input |
| 23 | `WRITING_BUSINESS_HTML_EXPLORATION` | 1,485,323 | 0.01% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 24 | `reviews` | 1,462,594 | 0.01% | Product / Project Documentation | no | Current / retained | No — KEEP | Retain as current input |
| 25 | `CONTENT_GROWTH_CODEX_HTML_EXPLORATION` | 824,675 | 0.01% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 26 | `CONTENT_GROWTH_FIGMA_STRUCTURAL_REFERENCES` | 787,584 | 0.01% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |
| 27 | `delivery` | 632,460 | 0.00% | Product / Project Documentation | no | Current / retained | No — KEEP | Retain as current input |
| 28 | `ai-tech-workspace` | 378,045 | 0.00% | Production Source Code | no | Current / retained | No — KEEP | Retain as current input |
| 29 | `browser-capability-research` | 329,560 | 0.00% | Product / Project Documentation | no | Current / retained | No — KEEP | Retain as current input |
| 30 | `CONTENT_GROWTH_WORKSPACE_HTML_EXPLORATION` | 327,422 | 0.00% | Historical Exploration / UI | no | Historical / evidence | No — HOLD | Do not touch under current decisions |

## Top 50 largest files

| Rank | Path | Size (B) | Extension | Category | Main Git tracked? | Likely role | State |
|---:|---|---:|---|---|---|---|---|
| 1 | `.git/objects/pack/pack-78231c0c24e021d74743c705754e52f105f72576.pack` | 1,786,248,192 | `.pack` | Git Repository Data | No | Git object pack | Unknown |
| 2 | `.git/objects/pack/pack-c8783798df2992e2e32f94356409eace53456c24.pack` | 486,543,232 | `.pack` | Git Repository Data | No | Git object pack | Unknown |
| 3 | `.git/objects/pack/pack-3764bc01eb2ed535d5cc0f0f0f646812eef527f2.pack` | 389,497,651 | `.pack` | Git Repository Data | No | Git object pack | Unknown |
| 4 | `desktop/.runtime/runtime/node` | 243,486,096 | `[no extension]` | Runtime Distribution / Staging | No | Current runtime bundle/staging | Current |
| 5 | `desktop/target/release/bundle/macos/Curis.app/Contents/Resources/runtime/node` | 243,486,096 | `[no extension]` | Build / Cache / Generated | No | Desktop build/package output | Generated |
| 6 | `desktop/target/release/bundle/macos/CurisCopy.app/Contents/Resources/runtime/node` | 243,486,096 | `[no extension]` | Build / Cache / Generated | No | Desktop build/package output | Generated |
| 7 | `desktop/target/release/runtime/node` | 243,486,096 | `[no extension]` | Build / Cache / Generated | No | Desktop build/package output | Generated |
| 8 | `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_WORKSPACE_FILE_MANIFEST.csv` | 238,120,362 | `.csv` | Product / Project Documentation | No | Audit manifest/report evidence | Generated |
| 9 | `desktop/target/release/bundle/dmg/Curis_0.1.0-beta_arm64.dmg` | 228,147,450 | `.dmg` | Build / Cache / Generated | No | Desktop installer package | Generated |
| 10 | `desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg` | 221,034,025 | `.dmg` | Build / Cache / Generated | No | Desktop installer package | Generated |
| 11 | `.git/objects/pack/pack-722fdd62f9e4c81a9768b64ce1cbc764726eecb3.pack` | 188,824,900 | `.pack` | Git Repository Data | No | Git object pack | Unknown |
| 12 | `desktop/target/release/libcuris_desktop_lib.a` | 154,491,696 | `.a` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 13 | `desktop/target/release/deps/libcuris_desktop_lib.a` | 154,350,720 | `.a` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 14 | `.worktrees/phase1c-ceo-office-first-slice/frontend/node_modules/.pnpm/@next+swc-darwin-arm64@16.2.10/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node` | 121,773,448 | `.node` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 15 | `.worktrees/company-runtime-office-view/frontend/node_modules/.pnpm/@next+swc-darwin-arm64@16.2.10/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node` | 121,773,448 | `.node` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 16 | `.worktrees/phase1c-company-project-bootstrap-ui/frontend/node_modules/.pnpm/@next+swc-darwin-arm64@16.2.10/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node` | 121,773,448 | `.node` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 17 | `.worktrees/ai-secretary-planning/frontend/node_modules/.pnpm/@next+swc-darwin-arm64@16.2.10/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node` | 121,773,448 | `.node` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 18 | `desktop/.runtime/.trash/runtime/frontend/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node` | 121,773,448 | `.node` | Archives / Backups | No | Installed dependency/runtime package | Historical |
| 19 | `desktop/target/release/runtime/frontend/node_modules/@next/swc-darwin-arm64/next-swc.darwin-arm64.node` | 121,773,448 | `.node` | Dependencies | No | Installed dependency/runtime package | Generated |
| 20 | `desktop/.runtime/.trash/runtime/node` | 112,989,184 | `[no extension]` | Archives / Backups | No | Retained backup/trash set | Historical |
| 21 | `desktop/target/debug/runtime/node` | 112,989,184 | `[no extension]` | Build / Cache / Generated | No | Desktop build/package output | Generated |
| 22 | `.git/objects/pack/pack-2e2a2b2ec960658e79ddd1ed0e8ebbe62a41aceb.pack` | 101,018,185 | `.pack` | Git Repository Data | No | Git object pack | Unknown |
| 23 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/.git/objects/pack/pack-c67186fb16c1818903173ab13b2ff1cc8e5e181a.pack` | 98,863,071 | `.pack` | Git Worktrees | Worktree checkout | Worktree checkout file (source/dependency/build by path) | Unknown |
| 24 | `RD_MULTI_AGENT_RESEARCH_LAB/repos/agent-orchestrator/.git/objects/pack/pack-61c0d88c33820f20cd019834c533541483a21b34.pack` | 74,187,481 | `.pack` | Other / Unknown | No | Project file; semantic role unresolved from metadata | Unknown |
| 25 | `.git/objects/pack/pack-0632aff588e98d6500ed9f7024f18670b6b00852.pack` | 71,804,170 | `.pack` | Git Repository Data | No | Git object pack | Unknown |
| 26 | `desktop/target/release/libcuris_desktop_lib.rlib` | 69,352,456 | `.rlib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 27 | `desktop/target/release/deps/libcuris_desktop_lib.rlib` | 69,218,864 | `.rlib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 28 | `.worktrees/company-runtime-office-view/frontend/.next/dev/cache/turbopack/v16.2.10/00000761.sst` | 40,059,562 | `.sst` | Git Worktrees | Worktree checkout | Worktree checkout file (source/dependency/build by path) | Unknown |
| 29 | `.worktrees/company-runtime-office-view/frontend/.next/cache/webpack/client-production/0.pack` | 37,929,940 | `.pack` | Git Worktrees | Worktree checkout | Worktree checkout file (source/dependency/build by path) | Unknown |
| 30 | `.worktrees/company-runtime-office-view/frontend/.next/cache/webpack/server-production/0.pack` | 36,918,377 | `.pack` | Git Worktrees | Worktree checkout | Worktree checkout file (source/dependency/build by path) | Unknown |
| 31 | `desktop/target/debug/deps/libtauri_utils-e87872785009ae16.rlib` | 33,546,624 | `.rlib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 32 | `desktop/target/release/deps/libtauri_utils-f0276b2aedc3b1ec.rlib` | 33,133,928 | `.rlib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 33 | `.worktrees/company-runtime-office-view/frontend/.next/dev/cache/turbopack/v16.2.10/00000762.sst` | 32,072,566 | `.sst` | Git Worktrees | Worktree checkout | Worktree checkout file (source/dependency/build by path) | Unknown |
| 34 | `desktop/target/debug/deps/libtauri_macros-77300b898e144037.dylib` | 22,861,864 | `.dylib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 35 | `desktop/target/release/deps/libtauri_utils-1e30b2602d5cf442.rlib` | 22,039,920 | `.rlib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 36 | `RD_MULTI_AGENT_RESEARCH_LAB/repos/parallel-code/.git/objects/pack/pack-2a21f13c784de196161ca52ff5979e66c719075c.pack` | 20,678,109 | `.pack` | Other / Unknown | No | Project file; semantic role unresolved from metadata | Unknown |
| 37 | `desktop/target/debug/build/curis-desktop-83ca5de622c30dad/build_script_build-83ca5de622c30dad` | 20,026,160 | `[no extension]` | Build / Cache / Generated | No | Desktop build/package output | Generated |
| 38 | `desktop/target/debug/build/curis-desktop-83ca5de622c30dad/build-script-build` | 20,026,160 | `[no extension]` | Build / Cache / Generated | No | Desktop build/package output | Generated |
| 39 | `.worktrees/company-runtime-office-view/frontend/.next/dev/cache/webpack/client-development/1.pack.gz` | 20,000,819 | `.gz` | Git Worktrees | Worktree checkout | Worktree checkout file (source/dependency/build by path) | Unknown |
| 40 | `desktop/target/release/deps/libobjc2_app_kit-45934adc274ec943.rlib` | 19,701,376 | `.rlib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 41 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-backend/node_modules/.pnpm/@rolldown+binding-darwin-arm64@1.0.0-rc.17/node_modules/@rolldown/binding-darwin-arm64/rolldown-binding.darwin-arm64.node` | 19,671,008 | `.node` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 42 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-backend/node_modules/.pnpm/@nx+nx-darwin-arm64@22.7.1/node_modules/@nx/nx-darwin-arm64/nx.darwin-arm64.node` | 19,082,384 | `.node` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 43 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-web/public/assets/welcome/interaction.mp4` | 18,389,723 | `.mp4` | Git Worktrees | Worktree checkout | Media asset | Unknown |
| 44 | `desktop/target/release/runtime/workspace/_internal/libpython3.12.dylib` | 17,986,864 | `.dylib` | Build / Cache / Generated | No | Compiled library/binary | Generated |
| 45 | `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_WORKSPACE_DIRECTORY_MANIFEST.md` | 17,399,936 | `.md` | Product / Project Documentation | No | Audit manifest/report evidence | Generated |
| 46 | `.worktrees/phase1c-ceo-office-first-slice/frontend/node_modules/.pnpm/@img+sharp-libvips-darwin-arm64@1.2.4/node_modules/@img/sharp-libvips-darwin-arm64/lib/libvips-cpp.8.17.3.dylib` | 16,076,984 | `.dylib` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 47 | `.worktrees/company-runtime-office-view/frontend/node_modules/.pnpm/@img+sharp-libvips-darwin-arm64@1.2.4/node_modules/@img/sharp-libvips-darwin-arm64/lib/libvips-cpp.8.17.3.dylib` | 16,076,984 | `.dylib` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 48 | `.worktrees/phase1c-company-project-bootstrap-ui/frontend/node_modules/.pnpm/@img+sharp-libvips-darwin-arm64@1.2.4/node_modules/@img/sharp-libvips-darwin-arm64/lib/libvips-cpp.8.17.3.dylib` | 16,076,984 | `.dylib` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 49 | `.worktrees/ai-secretary-planning/.curis/content-runtime/sources/AiToEarn/project/aitoearn-backend/node_modules/.pnpm/@img+sharp-libvips-darwin-arm64@1.2.4/node_modules/@img/sharp-libvips-darwin-arm64/lib/libvips-cpp.8.17.3.dylib` | 16,076,984 | `.dylib` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |
| 50 | `.worktrees/ai-secretary-planning/frontend/node_modules/.pnpm/@img+sharp-libvips-darwin-arm64@1.2.4/node_modules/@img/sharp-libvips-darwin-arm64/lib/libvips-cpp.8.17.3.dylib` | 16,076,984 | `.dylib` | Git Worktrees | Worktree checkout | Installed dependency/runtime package | Unknown |

## Git Worktree space

Existing Worktree Audit registered 17 present paths plus 5 missing. Current path-only check finds **13 present paths and 9 absent paths** among those 22 registrations; four previously reported present external paths are now absent. No worktree action was taken. Current apparent bytes for paths that still exist: **8,725,973,585 B (8.726 GB)**; of that, 3,303,189,101 B is inside this Workspace and already included in the main table, while 5,422,784,484 B is in external Codex worktrees and excluded from the Workspace total.

| ID | Path | Branch (prior audit) | Current size | Source | Dependencies | Build / Cache | Other | Dirty? | Untracked? | Block reason / status |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| WT-01 | `/private/tmp/curis-assistant-live-validation` | codex/global-assistant-live-validation | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Already missing/prunable in the existing Worktree Audit; no action taken. |
| WT-02 | `/private/tmp/curis-live-runtime-snapshot` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Already missing/prunable in the existing Worktree Audit; no action taken. |
| WT-03 | `/private/tmp/curis-s10-clean.n8CNPY` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Already missing/prunable in the existing Worktree Audit; no action taken. |
| WT-04 | `/private/tmp/curis-s11-clean` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Already missing/prunable in the existing Worktree Audit; no action taken. |
| WT-05 | `/private/tmp/curis-s12-clean` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Already missing/prunable in the existing Worktree Audit; no action taken. |
| WT-06 | `/Users/yy/.codex/worktrees/95a9/Curis AI Workspace` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Previously listed as present; path absent in current metadata check; no action taken. |
| WT-07 | `/Users/yy/.codex/worktrees/98d0/Curis AI Workspace` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Previously listed as present; path absent in current metadata check; no action taken. |
| WT-08 | `/Users/yy/.codex/worktrees/aeb0/Curis AI Workspace` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Previously listed as present; path absent in current metadata check; no action taken. |
| WT-09 | `/Users/yy/.codex/worktrees/curis-shared-runtime-snapshot-20260813/Curis AI Workspace` | detached | 42,940,075 | 12,787,382 | 0 | 0 | 30,152,693 | No / prior audit | No / prior audit | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-10 | `/Users/yy/.codex/worktrees/d126/Curis AI Workspace` | detached | 0 | 0 | 0 | 0 | 0 | Unknown (path absent) | Unknown (path absent) | ABSENT now; no action; Previously listed as present; path absent in current metadata check; no action taken. |
| WT-11 | `/Users/yy/.codex/worktrees/rd-current-root-20260813/Curis AI Workspace` | detached | 40,430,411 | 10,799,659 | 0 | 0 | 29,630,752 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-12 | `/Users/yy/.codex/worktrees/rd-migration-dd77` | detached | 40,425,274 | 10,799,659 | 0 | 0 | 29,625,615 | No / prior audit | No / prior audit | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-13 | `/Users/yy/.codex/worktrees/rd-shared-runtime-20260813/Curis AI Workspace` | detached | 1,099,429,160 | 32,236,813 | 540,030,148 | 47,624,063 | 479,538,136 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-14 | `/Users/yy/.codex/worktrees/ttk-current-root-20260813/Curis AI Workspace` | detached | 40,431,199 | 10,799,659 | 0 | 0 | 29,631,540 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-15 | `/Users/yy/.codex/worktrees/ttk-shared-runtime-20260813/Curis AI Workspace` | detached | 3,152,379,960 | 32,540,267 | 783,188,539 | 1,865,504,319 | 471,146,835 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-16 | `/Users/yy/.codex/worktrees/xhs-current-root-20260813/Curis AI Workspace` | detached | 40,429,809 | 10,799,659 | 0 | 0 | 29,630,150 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-17 | `/Users/yy/.codex/worktrees/xhs-dd77` | detached | 459,870,927 | 10,812,204 | 394,312,217 | 21,782,078 | 32,964,428 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-18 | `/Users/yy/.codex/worktrees/xhs-shared-runtime-20260813/Curis AI Workspace` | detached | 506,447,669 | 12,791,155 | 425,909,973 | 36,012,511 | 31,734,030 | Yes | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-19 | `/Users/yy/Documents/Curis AI Workspace/.worktrees/ai-secretary-planning` | codex/ai-secretary-planning | 1,623,159,188 | 27,161,675 | 1,236,685,134 | 101,519,200 | 257,793,179 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-20 | `/Users/yy/Documents/Curis AI Workspace/.worktrees/company-runtime-office-view` | codex/company-runtime-office-view | 714,955,640 | 3,064,277 | 423,502,340 | 274,167,098 | 14,221,925 | Yes | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-21 | `/Users/yy/Documents/Curis AI Workspace/.worktrees/phase1c-ceo-office-first-slice` | codex/phase1c-ceo-office-first-slice | 486,371,948 | 1,978,163 | 394,431,891 | 84,973,974 | 4,987,920 | No / prior audit | Yes | PRESENT; Deletion loses user work/unique commits; main also dirty |
| WT-22 | `/Users/yy/Documents/Curis AI Workspace/.worktrees/phase1c-company-project-bootstrap-ui` | codex/phase1c-company-project-bootstrap-ui | 478,702,325 | 1,998,872 | 394,436,055 | 77,791,832 | 4,475,566 | No / prior audit | No / prior audit | PRESENT; Deletion loses user work/unique commits; main also dirty |

**Current Worktree subtotal:** 8.726 GB over 13 present registered paths; dependencies 4.592 GB; build/cache 2.509 GB. All existing and absent registrations remain **HOLD**. These subtotals are nested within the Worktree total and must not be added to the main category table again.

### Dependencies

- Canonical checkout dependency roots outside `.worktrees/`: **1,042,668,338 B (1042.67 MB)**. Dependencies inside Worktrees are included under Worktree in the main table; their current all-worktree subtotals are 4.592 GB.

| Path | Project / scope | Size | Manager / lock metadata | State | Retention reason |
|---|---|---:|---|---|---|
| `desktop/target/release/runtime/frontend/node_modules` | desktop | 348,202,025 | not identified at this project root | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/.runtime/runtime/frontend/node_modules` | desktop | 114,120,770 | not identified at this project root | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/target/debug/runtime/frontend/node_modules` | desktop | 114,120,770 | not identified at this project root | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/target/release/bundle/macos/Curis.app/Contents/Resources/runtime/frontend/node_modules` | desktop | 114,120,770 | not identified at this project root | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/target/release/bundle/macos/CurisCopy.app/Contents/Resources/runtime/frontend/node_modules` | desktop | 114,120,770 | not identified at this project root | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `.venv` | .venv | 42,625,793 | not identified at this project root | Current checkout | Installed dependencies; conditional only after process, lockfile and rebuild checks. |
| `backend/.venv` | backend | 42,605,918 | requirements.txt | Current checkout | Installed dependencies; conditional only after process, lockfile and rebuild checks. |
| `desktop/target/debug/runtime/workspace/_internal/backend/.venv` | desktop | 40,963,556 | requirements.txt | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/target/release/bundle/macos/CurisCopy.app/Contents/Resources/runtime/workspace/_internal/backend/.venv` | desktop | 40,963,556 | requirements.txt | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/target/release/runtime/workspace/_internal/backend/.venv` | desktop | 40,963,556 | requirements.txt | Packaged runtime output | Embedded package dependencies; counted by path marker, parent runtime/build output remains conditional or HOLD. |
| `desktop/node_modules` | desktop | 29,860,854 | pnpm-lock.yaml, package-lock.json | Current checkout | Installed dependencies; conditional only after process, lockfile and rebuild checks. |

**desktop/node_modules:** 29,860,854 B; Gate 3 records npm and pnpm lockfiles together and leaves this root skipped. No package manager was selected here.

## Build / Cache / Generated

Workspace build/cache/generated category (excluding the Worktree category): **4,108,392,466 B (4.108 GB)**. Current Worktree build/cache child data adds 2.509 GB inside the blocked Worktree subtotal; not a Workspace-category add-on.

| Largest path root | Bytes | State | Notes |
|---|---:|---|---|
| `desktop/target` | 4,720,773,313 | CONDITIONAL | Rust/Tauri target output; source/lockfiles retained; process/rebuild gate still required. |
| `desktop/.runtime` | 1,353,136,631 | MIXED / HOLD | Mixed build/dist, current runtime staging and .trash; split below; no deletion approved. |
| `desktop/node_modules` | 29,860,854 | CONDITIONAL | Skipped Gate 3; npm/pnpm lock ambiguity. |
| `backend/.venv` | 42,605,918 | CONDITIONAL | Python environment; conditional after process/rebuild checks. |
| `.venv` | 42,625,793 | CONDITIONAL | Python environment; conditional after process/rebuild checks. |

`desktop/.runtime` immediate metadata rollup: `target` 0 B; `runtime` 452,134,109 B; `.trash` 745,110,769 B; `workspace-build` 37,152,455 B; `workspace-dist` 41,609,225 B; `gateway-build` 11,937,892 B; `gateway-dist` 8,464,784 B; `guardian-build` 11,765,977 B; `guardian-dist` 8,380,688 B; `recovery-build` 12,522,405 B; `recovery-dist` 9,114,016 B. Packaged runtime and `.trash` remain HOLD; build outputs remain conditional.

Across the main checkout only, clearly named bytecode/test-cache entries (`.ruff_cache`, `.pytest_cache`, `.mypy_cache`, `__pycache__`) total **46,880,927 B** and are classed REGENERABLE by type. This does not authorize deletion of any specific path.

## `.git` repository data

`.git` total: **3,421,311,272 B (3.421 GB)**.

| `.git` component | Bytes |
|---|---:|
| `objects` | 3,416,899,967 |
| `worktrees` | 4,048,738 |
| `logs` | 31,808 |
| `refs` | 482 |
| `hooks` | 25,827 |
| `info` | 3,552 |
| Other direct metadata and index | 300,898 |

No `git gc`, prune, repack or worktree operation was run. `.git` is HOLD.

## Product and project documentation

All project-documentation category files: **3,011 files / 349,149,265 B (349.15 MB, 0.349 GB)**. This includes the Full Workspace Audit family but excludes dependency README files and code/package JSON.

- Markdown / MDX: 2,272 files / 47,118,808 B (47.12 MB).
- CSV project documents: 17 files / 247,980,986 B (247.98 MB).
- JSON/JSONL in `docs/` classified as project records: 55 files / 1,143,246 B (1.14 MB; estimate based on path and extension).
- `docs/` tree total: 364,328,547 B (364.33 MB).
- `docs/research/`: 37,654,812 B; `docs/reviews/`: 12,579,363 B; `docs/audit/`: 268,262,864 B.

Non-overlapping document subfamilies (priority-based path/name assignment):

| Document group | Files | Bytes |
|---|---:|---:|
| Audit | 74 | 268,262,864 |
| Research | 569 | 37,576,788 |
| Other Project Documentation | 1,687 | 31,633,832 |
| Review | 558 | 9,360,674 |
| Authority / Current Governance | 66 | 1,680,212 |
| Closure | 49 | 359,435 |
| Governance / Context | 5 | 227,681 |
| Backlog | 3 | 47,779 |

**Answer:** Curis project documentation is about **349.15 MB**, not 13.94 GB.

## UI / exploration and images

| UI set | Files | Bytes |
|---|---:|---:|
| Active HTML / UI References | 32 | 6,899,736 |
| Historical Exploration / UI | 907 | 93,581,087 |
| Design / Figma Assets | 7 | 69,488 |

Active Exploration Registry rows marked KEEP_ACTIVE that still exist: 32 files. Historical / held exploration currently found: 907 files. Standalone Design / Figma category files occupy 69,488 B; `.design` exports nested inside historical exploration are counted in that historical set. Active + historical HTML/UI/design sets together occupy 100.55 MB; screenshots inside those sets are included once in those main categories.
Secondary cross-category image count (PNG/JPG/JPEG/WEBP/GIF/BMP/TIF/AVIF, regardless of primary category): **1,767 files / 480,705,652 B (480.71 MB)**.

No dedicated long-term Business Asset root was positively identified from existing paths/registries in this metadata pass. The main category reports any path-explicit Business Assets; opaque or ambiguous data remains Database or Other/Unknown. This is not a content-level claim that no business asset exists.

## Full Workspace Audit footprint

`docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/` before this output file: **73 files / 268,254,668 B (268.25 MB)**. The report itself is included in the audit-family post-output accounting below; the pre-report scan is kept as the storage-table denominator.

Final governance / execution evidence to retain includes the CEO decision table, remaining exploration resolution, Gate 4 approved execution manifest, Wave 3 exact delete manifest, Root resolution and `docs/99_Archive/CURIS_CLEANUP_LEDGER.md`. Large intermediate measurement records should remain available until Final Workspace Consolidation decides their retention: Workspace File Manifest, Directory Manifest, consolidation decision matrix, file disposition matrix, and Gate 2/3/5 manifests. No audit files were removed.

| Largest files in this audit family | Bytes |
|---|---:|
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_WORKSPACE_FILE_MANIFEST.csv` | 238,120,362 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_WORKSPACE_DIRECTORY_MANIFEST.md` | 17,399,936 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_FILE_DISPOSITION_MATRIX.csv` | 5,274,809 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_WORKSPACE_CONSOLIDATION_DECISION_MATRIX.csv` | 2,351,775 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_BACKLOG_REGISTRY.md` | 1,252,212 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_EXPLORATION_FILE_DISPOSITION.csv` | 1,020,029 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_GATE_2_SAFE_GENERATED_CLEANUP.csv` | 555,853 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_DECISION_HISTORY_REGISTRY.md` | 438,266 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_GATE_4_APPROVED_EXECUTION_MANIFEST.csv` | 411,960 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_PRODUCT_FACT_SOURCE_REGISTRY.md` | 392,640 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_EXPLORATION_REGISTRY.md` | 254,904 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_MULTI_AGENT_DIRECTORY_DRIFT_AUDIT.md` | 163,166 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_STORAGE_RECLAMATION_MATRIX.csv` | 70,474 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_MINIMAL_EVIDENCE_COMPRESSION.csv` | 56,389 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_RUNTIME_REALITY.md` | 38,658 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_WAVE_3_DELETE_CANDIDATES.csv` | 37,354 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/build_audit.py` | 34,802 |
| `docs/audit/CURIS_FULL_WORKSPACE_TRUTH_AUDIT_2026-09-24/CURIS_EXPLORATION_FAMILY_REGISTRY.md` | 24,868 |

## Root-level directory storage

| Root directory | Files | Subdirectories | Size | % Workspace | Dominant category |
|---|---:|---:|---:|---:|---|
| `desktop` | 77,576 | 10 | 6,104,498,057 | 43.79% | Build / Cache / Generated |
| `.git` | 6,403 | 6 | 3,421,311,272 | 24.54% | Git Repository Data |
| `.worktrees` | 166,764 | 4 | 3,303,189,101 | 23.69% | Git Worktrees |
| `docs` | 2,079 | 38 | 364,328,547 | 2.61% | Product / Project Documentation |
| `RD_MULTI_AGENT_RESEARCH_LAB` | 6,849 | 2 | 255,382,651 | 1.83% | Other / Unknown |
| `artifacts` | 158 | 4 | 209,359,336 | 1.50% | Images / Screenshots |
| `backend` | 2,904 | 7 | 78,409,201 | 0.56% | Dependencies |
| `deploy` | 2,280 | 5 | 46,568,464 | 0.33% | Build / Cache / Generated |
| `.venv` | 2,443 | 3 | 42,625,793 | 0.31% | Dependencies |
| `curis-ui-prototype` | 261 | 9 | 27,458,526 | 0.20% | Historical Exploration / UI |
| `.design` | 144 | 9 | 12,768,941 | 0.09% | Historical Exploration / UI |
| `frontend` | 390 | 9 | 7,848,970 | 0.06% | Production Source Code |
| `MUSIC_BUSINESS_CODEX_HTML_EXPLORATION` | 31 | 3 | 6,422,483 | 0.05% | Active HTML / UI References |
| `CURIS_PROJECT_WORKSPACE_VISUAL_EXPLORATION` | 10 | 3 | 6,179,068 | 0.04% | Historical Exploration / UI |
| `RD_WORKSPACE_HTML_EXPLORATION` | 23 | 1 | 5,277,004 | 0.04% | Historical Exploration / UI |
| `data` | 7 | 1 | 4,903,878 | 0.04% | Database / Persistent Data |
| `MUSIC_WORKSPACE_HTML_EXPLORATION` | 27 | 1 | 4,038,350 | 0.03% | Historical Exploration / UI |
| `CURIS_OPERATIONAL_VISUAL_EXPLORATION` | 14 | 4 | 3,033,661 | 0.02% | Historical Exploration / UI |
| `issues` | 391 | 1 | 2,056,210 | 0.01% | Product / Project Documentation |
| `CURIS_V1_EMPLOYEE_INTERACTION_EXPLORATION` | 13 | 1 | 2,049,373 | 0.01% | Historical Exploration / UI |
| `curis-ui-prototype.bak` | 26 | 3 | 2,028,544 | 0.01% | Historical Exploration / UI |
| `.workbuddy` | 55 | 4 | 1,511,576 | 0.01% | Product / Project Documentation |
| `WRITING_BUSINESS_HTML_EXPLORATION` | 58 | 18 | 1,485,323 | 0.01% | Historical Exploration / UI |
| `reviews` | 280 | 0 | 1,462,594 | 0.01% | Product / Project Documentation |
| `CONTENT_GROWTH_CODEX_HTML_EXPLORATION` | 13 | 1 | 824,675 | 0.01% | Historical Exploration / UI |
| `CONTENT_GROWTH_FIGMA_STRUCTURAL_REFERENCES` | 8 | 0 | 787,584 | 0.01% | Historical Exploration / UI |
| `delivery` | 9 | 0 | 632,460 | 0.00% | Product / Project Documentation |
| `ai-tech-workspace` | 20 | 3 | 378,045 | 0.00% | Production Source Code |
| `browser-capability-research` | 25 | 1 | 329,560 | 0.00% | Product / Project Documentation |
| `CONTENT_GROWTH_WORKSPACE_HTML_EXPLORATION` | 41 | 13 | 327,422 | 0.00% | Historical Exploration / UI |
| `.agents` | 15 | 2 | 314,805 | 0.00% | Product / Project Documentation |
| `knowledge` | 13 | 1 | 242,755 | 0.00% | Product / Project Documentation |
| `diagrams` | 10 | 0 | 217,877 | 0.00% | Production Source Code |
| `deliverables` | 7 | 1 | 215,721 | 0.00% | Historical Exploration / UI |
| `shared` | 9 | 4 | 110,418 | 0.00% | Product / Project Documentation |
| `tools` | 11 | 2 | 54,296 | 0.00% | Production Source Code |
| `Curis 产品与愿景资料库` | 9 | 3 | 34,406 | 0.00% | Product / Project Documentation |
| `previews` | 1 | 0 | 31,937 | 0.00% | Historical Exploration / UI |
| `CONTENT_GROWTH_FULL_VISUAL_EXPLORATION` | 5 | 2 | 12,373 | 0.00% | Historical Exploration / UI |
| `CONTENT_GROWTH_FULL_VISUAL_REEXPRESSION` | 1 | 3 | 7,514 | 0.00% | Historical Exploration / UI |
| `workspace` | 2 | 3 | 7,418 | 0.00% | Other / Unknown |
| `CURIS_COLOR_DIRECTION_EXPLORATION` | 2 | 0 | 6,307 | 0.00% | Historical Exploration / UI |
| `.obsidian` | 5 | 0 | 5,980 | 0.00% | Production Source Code |
| `plugins` | 2 | 1 | 4,347 | 0.00% | Product / Project Documentation |
| `CONTENT_GROWTH_VISUAL_REEXPRESSION_TEST` | 2 | 4 | 3,930 | 0.00% | Historical Exploration / UI |
| `admin-platform` | 1 | 0 | 1,244 | 0.00% | Product / Project Documentation |
| `curis_workspace_blueprint` | 2 | 1 | 1,220 | 0.00% | Product / Project Documentation |
| `.githooks` | 2 | 0 | 783 | 0.00% | Product / Project Documentation |
| `.github` | 1 | 1 | 768 | 0.00% | Production Source Code |
| `experimental` | 1 | 0 | 457 | 0.00% | Product / Project Documentation |
| `screenshots` | 0 | 0 | 0 | 0.00% | Historical Exploration / UI |
| `.trae-work` | 0 | 0 | 0 | 0.00% | Other / Unknown |
| `AI` | 0 | 0 | 0 | 0.00% | Other / Unknown |
| `~` | 0 | 1 | 0 | 0.00% | Other / Unknown |
| `[root files]` | 48 | 0 | 21,857,881 | 0.16% | Product / Project Documentation / mixed |

## Reclaimability view (no cleanup performed)

| Reclaimability | Bytes | GB | % Workspace | Meaning in this snapshot |
|---|---:|---:|---:|---|
| KEEP | 436,032,205 | 0.436 | 3.13% | Current source, authorities, active references, identified business assets. |
| REGENERABLE | 46,880,927 | 0.047 | 0.34% | Only named bytecode/test caches by type; path-level deletion still needs approval. |
| CONDITIONAL | 5,112,001,117 | 5.112 | 36.67% | Generated output/dependencies/logs; process, dependency, rebuild and exact-set gates apply. |
| HOLD | 8,188,354,142 | 8.188 | 58.74% | Worktrees, Git data, history, databases, runtime staging, archives and design evidence. |
| UNKNOWN | 157,340,715 | 0.157 | 1.13% | Unclassified path/provenance; keep pending scoped review. |

**Theoretical space worth a separate cleanup gate:** 5.159 GB in REGENERABLE + CONDITIONAL categories, of which 5.112 GB is conditional and not currently approved. This excludes every Worktree, `.git`, runtime staging, database, archive and unknown path. Previously approved Wave 1–3 sets are already reflected in this scan; do not add them again.

## Other / Unknown breakdown

Other / Unknown = 157,340,715 B (0.157 GB; 1.13% of Workspace).
低于 5% 阈值，无需扩展拆分。主要剩余项：
- `RD_MULTI_AGENT_RESEARCH_LAB` — 111,547,166 B
- `backend` — 22,654,980 B
- `data` — 1,687,552 B
- `<app.database.Database object at 0x10e6274d0>` — 1,306,624 B
- `<app.database.Database object at 0x10e627700>` — 1,306,624 B
- `<app.database.Database object at 0x10f54fd90>` — 1,159,168 B
- `<app.database.Database object at 0x10173d220>` — 1,159,168 B
- `<app.database.Database object at 0x10ec85e00>` — 1,159,168 B
- `<app.database.Database object at 0x10a4196d0>` — 1,159,168 B
- `<app.database.Database object at 0x10b57da90>` — 1,159,168 B

## CEO questions answered

1. Workspace 内最大的五个不重叠来源：`desktop` 6.104 GB（其中 `desktop/target` 4.721 GB，`desktop/.runtime` 1.353 GB）；`.git` 3.421 GB；`.worktrees` 3.303 GB；`docs` 0.364 GB；`RD_MULTI_AGENT_RESEARCH_LAB` 0.255 GB。
2. 当前存在 Worktree：13 条路径 / 8.726 GB；先前 17 条预期存在路径中有 4 条现已缺失。
3. Dependencies：Workspace 主类别 1.043 GB；包含 Worktree 子分析后，当前所有存在 Worktree 的 dependency 部分为 4.592 GB（与 Worktree 总额重叠，不可重复加总）。
4. Build / Cache：Workspace 主类别 4.108 GB；Worktree 子分析另有 2.509 GB（HOLD）。
5. `.git`：3.421 GB。
6. Production Source Code：0.080 GB。
7. Curis 项目文档：349.15 MB。
8. HTML / UI Exploration（Active + Historical + Design）：100.55 MB。
9. Screenshot / Image：480.71 MB（跨主类别 secondary stat）。
10. 本次 Full Workspace Audit 家族：268.25 MB（生成本报告前）；本报告加入后约 268.30 MB。大型 Intermediate Manifest 仍全部保留。
11. Other / Unknown：0.157 GB (1.13%).
12. 适合单独开清理 Gate 的理论上限：5.159 GB；当前全部需重新核验与审批。
13. 现在不可碰：17 条 Worktree Audit 原记录对应的现存 Worktrees（当前还存在的全部 13 条）、`.git`、数据库/persistent stores、Runtime staging、`.runtime/.trash`、未确认依赖、Authority、Active HTML/UI、Business Assets 和所有 Unknown / HOLD 内容。

## Scope and cautions

This is a size aggregation from the supplied baseline and current filesystem metadata. It does not update Product Truth, classify document authority, resolve Worktree ownership, identify safe delete sets, or authorize cleanup. Worktree status/branch/dirty details are copied from the existing Worktree Audit; current presence and byte totals were refreshed from path/stat metadata only. Current external path absence does not imply permission to prune Git metadata.
Post-output accounting: report file=48,142 B; scan baseline=13,940,609,106 B; post-output workspace=13,940,657,248 B; audit family post-output=268,302,810 B; files=269,452; directories=50,521.
