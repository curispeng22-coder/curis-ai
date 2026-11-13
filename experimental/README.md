# Experimental

以下能力不属于 Curis 默认启动链：

| 实验项 | 位置 | 默认状态 |
| --- | --- | --- |
| FreeLLMAPI | `deploy/freellmapi/` | 不启动、不发布 |
| selfuse 启动器 | `backend/start-selfuse.sh` | 不调用 |
| D1 单模型链 | `backend/app/d1_*` | `CURIS_D1_FROZEN=1` 且 `CURIS_D1_EXECUTE_ENABLED=0` |

实验项只有在独立 Issue 批准后才能启用或迁移；Sprint 0 不移动现有未提交实验资产。
