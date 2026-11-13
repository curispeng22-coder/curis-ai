# Git Worktree Audit

Status: Review  
Authority Class: REVIEW / IMPLEMENTATION STATE

Source: live `git worktree list --porcelain`, per-existing-worktree `git status --porcelain --untracked-files=no`, grouped untracked listing, `git rev-list --left-right --count <main>...<HEAD>`, `merge-base --is-ancestor`, and targeted `du -sk` for existing non-root worktrees. No worktree was mutated. Current `main` HEAD is `78cacbd0857cc36c9f3fe0e4b11346489993b728`; main working tree is broadly dirty, including code, docs, tests and product files.

| Path | Branch | HEAD | Dirty tracked | Untracked | Ahead/behind / relation | Size | Unique commit? | Disposition |
|---|---|---|---:|---:|---|---:|---|---|
| `/private/tmp/curis-assistant-live-validation` | codex/global-assistant-live-validation | 1f295c06eec32e8e8d410e6f04c015d220978782 | 0 | 0 | prunable metadata; worktree path missing | 0 B present | Unknown branch retention | REVIEW_REQUIRED |
| `/private/tmp/curis-live-runtime-snapshot` | detached | a57098c6dce4ac25d185863b7012c2daf12ade8d | 0 | 0 | prunable metadata; worktree path missing | 0 B present | Unknown branch retention | REVIEW_REQUIRED |
| `/private/tmp/curis-s10-clean.n8CNPY` | detached | UNKNOWN (missing path; SHA not captured) | 0 | 0 | prunable metadata; worktree path missing | 0 B present | Unknown branch retention | REVIEW_REQUIRED |
| `/private/tmp/curis-s11-clean` | detached | 6fad07439b18e0dce12aef6b9fe7baeaf06174e8 | 0 | 0 | prunable metadata; worktree path missing | 0 B present | Unknown branch retention | REVIEW_REQUIRED |
| `/private/tmp/curis-s12-clean` | detached | 486bbc0a2ec2c3600ceb24838046169294ae0a18 | 0 | 0 | prunable metadata; worktree path missing | 0 B present | Unknown branch retention | REVIEW_REQUIRED |
| `/Users/yy/.codex/worktrees/95a9/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 2 | 5 | unique commit vs main; see state summary | 666,288,128 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/.codex/worktrees/98d0/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 4 | 5 | unique commit vs main; see state summary | 585,306,112 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/.codex/worktrees/aeb0/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 1 | 14 | unique commit vs main; see state summary | 3,301,838,848 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/.codex/worktrees/curis-shared-runtime-snapshot-20260813/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 0 | 0 | unique commit vs main; see state summary | 47,906,816 B | YES | BLOCKED_UNPUSHED |
| `/Users/yy/.codex/worktrees/d126/Curis AI Workspace` | detached | `dd77c672428999b5d96868c0380313eab53f31f9` | 59 | 143 | HEAD ancestor of main; see state summary | 5,254,688,768 B | NO, but dirty/untracked | BLOCKED_DIRTY |
| `/Users/yy/.codex/worktrees/rd-current-root-20260813/Curis AI Workspace` | detached | `dd77c672428999b5d96868c0380313eab53f31f9` | 0 | 2 | HEAD ancestor of main; see state summary | 44,810,240 B | NO, but dirty/untracked | BLOCKED_DIRTY |
| `/Users/yy/.codex/worktrees/rd-migration-dd77` | detached | `dd77c672428999b5d96868c0380313eab53f31f9` | 0 | 0 | HEAD ancestor of main; see state summary | 44,802,048 B | NO, but dirty/untracked | BLOCKED_DIRTY |
| `/Users/yy/.codex/worktrees/rd-shared-runtime-20260813/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 0 | 2 | unique commit vs main; see state summary | 1,201,381,376 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/.codex/worktrees/ttk-current-root-20260813/Curis AI Workspace` | detached | `dd77c672428999b5d96868c0380313eab53f31f9` | 0 | 2 | HEAD ancestor of main; see state summary | 44,810,240 B | NO, but dirty/untracked | BLOCKED_DIRTY |
| `/Users/yy/.codex/worktrees/ttk-shared-runtime-20260813/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 0 | 5 | unique commit vs main; see state summary | 3,286,183,936 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/.codex/worktrees/xhs-current-root-20260813/Curis AI Workspace` | detached | `dd77c672428999b5d96868c0380313eab53f31f9` | 0 | 2 | HEAD ancestor of main; see state summary | 44,810,240 B | NO, but dirty/untracked | BLOCKED_DIRTY |
| `/Users/yy/.codex/worktrees/xhs-dd77` | detached | `dd77c672428999b5d96868c0380313eab53f31f9` | 0 | 3 | HEAD ancestor of main; see state summary | 530,534,400 B | NO, but dirty/untracked | BLOCKED_DIRTY |
| `/Users/yy/.codex/worktrees/xhs-shared-runtime-20260813/Curis AI Workspace` | detached | `96cc3406645de69757f63190886ebe99933188a8` | 3 | 2 | unique commit vs main; see state summary | 585,244,672 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/ai-secretary-planning` | codex/ai-secretary-planning | `8191f8d71ee41970571a64453f6a72f0229e3752` | 0 | 4 | unique commit vs main; branch ahead by 269/323/5/7 commits respectively | 1,623,159,188 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/company-runtime-office-view` | codex/company-runtime-office-view | `67f01151ad0caa5d41146ffbceaf9bc172fcf65d` | 1 | 2 | unique commit vs main; branch ahead by 269/323/5/7 commits respectively | 714,955,640 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/phase1c-ceo-office-first-slice` | codex/phase1c-ceo-office-first-slice | `ceb3ce6f79594bf87578701f68153aaa95cb412a` | 0 | 1 | unique commit vs main; branch ahead by 269/323/5/7 commits respectively | 486,371,948 B | YES | BLOCKED_DIRTY + BLOCKED_UNPUSHED |
| `/Users/yy/Documents/Curis AI Workspace/.worktrees/phase1c-company-project-bootstrap-ui` | codex/phase1c-company-project-bootstrap-ui | `d44457683c453bbdcb33f40e63fc417ca63ed3c7` | 0 | 0 | unique commit vs main; branch ahead by 269/323/5/7 commits respectively | 478,702,325 B | YES | BLOCKED_UNPUSHED |

## Count and safety result

- Active root checkout: 1, KEEP_ACTIVE; main is dirty and cannot be replaced or cleaned.
- Registered worktrees besides main: **22**. Existing directories measured: **17**; missing/prunable paths: **5**.
- Existing worktrees safe to remove: **0**. Removal candidates: **0**.
- Existing worktrees blocked: **17**; 5 registered `/private/tmp` entries have no directory and are metadata-only review items.
- Four in-repo worktrees occupy 3,303,189,101 apparent bytes in the supplied manifest; external Codex worktrees are outside that manifest and targeted disk-usage readings total 15,638,605,824 allocated bytes, but this is not a safe reclamation amount.
- Aeb0's worktree contains about 1.14 GB in `.curis/content-runtime/sources/AiToEarn`; that is unique business/user source, not generated cleanup.

Every dirty, untracked, branch-unique or unknown item remains blocked. Even the one fully clean worktree based on a unique commit remains `BLOCKED_UNPUSHED`. Detached `dd77` worktrees with HEAD already in main still contain untracked files in five cases; the one clean `rd-migration-dd77` also is not auto-removed because it is a detached checkout requiring owner confirmation. There are no unpushed facts inferred solely from branch name: unique commits were measured relative to main.

No `git worktree remove`, prune, clean, branch deletion, reset, commit or push was performed. Part 4 must first resolve source ownership, preserve/merge unique commits, inspect untracked files by owner, then remeasure exact size; no worktree is presently eligible for a destructive command.
