# Runtime Foundation Implementation Input Snapshot

Snapshot time: 2026-08-09  
Base HEAD: `dd77c672428999b5d96868c0380313eab53f31f9`  
Working tree: dirty; existing changes are pre-existing input and must not be reset or overwritten.  
Tracked modified paths at snapshot: 41  
Untracked paths at snapshot: 52

本快照不是 Git commit；它用 SHA-256 固定本次 Runtime Foundation 评审读取的文件内容，并要求实现会话在修改前保留完整的 pre-existing diff。清单外路径不得因为实现便利而变更。

## Product / Runtime / Review inputs

| Path | SHA-256 |
| --- | --- |
| `docs/01_Product/Curis_Product_Blueprint.html` | `e944576bd5be3c64d3fe75cdf88d26c6d1f8edef4dd6f45479e8d01d41a7a16e` |
| `docs/01_Product/Curis_Business_Runtime_Definition_v0.1.md` | `ef60cdf7d348b591d9e8974366408ce7711697f8688a322b22bf0ff16dac6b99` |
| `docs/00_Context/CURRENT_STATE.md` | `04b07a7f1a1ad390b695b35b62cccd5500fe94e612e83ce028f28edb737e26c6` |
| `docs/reviews/runtime-foundation-review-2026-08-09/README.md` | `397614a670a0e225fc99b8821a9bec1ab8655d5390f45532a56d2a51f31e8fb3` |
| `docs/reviews/three-business-runtime-simulation-plan-2026-08-09/README.md` | `7fa25ae18e27307e652ebd84290d5a761d9995d21440418282d9362f274b46f7` |
| `docs/reviews/next-stage-product-plan-evoflow-2026-08-09/README.md` | `e9b9d2fc0c2a84f47c84f2f32c4f6edfed6d9580eafac146a5cee27b28202c12` |
| `issues/20260809_runtime_foundation_001.md` | `3b57eab0ebd2e41e3a94a57d132785df8eebee3ca82cd2116d11ec7640ec45b3` |

## Allowed Runtime code inputs

| Path | SHA-256 |
| --- | --- |
| `backend/app/database.py` | `93247b08cd2c55943a33baf3355cdf87bc48e4046502aee4a42d20b17146ff13` |
| `backend/app/runtime/__init__.py` | `ea20c51ff3ce4e92b76fcb23e560000665c97833b6d56703daf130117a600b5c` |
| `backend/app/runtime/models.py` | `c796c3242e6be8d5c2e1fa5ecee0d0a26ee25e9d0ccb8506229021720f953f10` |
| `backend/app/runtime/states.py` | `c817c7a2dfce2a93c2938957a86f630ec6d6d6d4d8e393c188ae312b08877b86` |
| `backend/app/runtime/state_machine.py` | `5589fe03573668a401beaa8c8d4ad90ae761ae1dbf26ac07f1a958a41335c854` |
| `backend/app/runtime/registry.py` | `e7db9d1a65bfb8a2966f0a7ac2c904c5cd64010f68e013249dcb1669336bf487` |
| `backend/app/runtime/store.py` | `803b1825a26727be200286883136d4b5be0c730648f9a784cc28765b8206b09f` |

## Snapshot rules

1. 不使用 `git reset`、`git checkout --` 或删除命令清理工作树。
2. 实现前保存 `git diff` 和 untracked manifest；只修改 `RUNTIME-FOUNDATION-001` 封闭清单。
3. 如果需要修改 `backend/app/main.py`、旧运行模块、前端、桌面壳或数据库文件，先停止并提交 Issue Amendment。
4. 新建临时 SQLite 路径完成 fresh / upgrade / restart / isolation 验证；不写入 `data/curis.sqlite` 或 `backend/data/curis.sqlite`。
5. 交付反馈必须重新输出本清单涉及文件的 SHA-256、测试结果、数据库路径和差异范围。
