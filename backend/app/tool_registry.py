from __future__ import annotations

from typing import Any

from .database import Database


class ToolRegistry:
    def __init__(self, database: Database):
        self.database = database

    def register(self, tool: dict[str, str]) -> dict[str, Any]:
        name = tool["name"].strip()
        if not name:
            raise ValueError("tool name is required")
        with self.database.connect() as connection:
            connection.execute(
                """
                insert into tools (name, type, description, entry, created_from_template_id)
                values (?, ?, ?, ?, ?)
                on conflict(name) do update set
                  type = excluded.type,
                  description = excluded.description,
                  entry = excluded.entry,
                  created_from_template_id = excluded.created_from_template_id
                """,
                (
                    name,
                    tool.get("type", ""),
                    tool.get("description", ""),
                    tool.get("entry", ""),
                    tool.get("created_from_template_id") or None,
                ),
            )
        return self.get(name)

    def get(self, name: str) -> dict[str, Any]:
        with self.database.connect() as connection:
            row = connection.execute("select * from tools where name = ?", (name,)).fetchone()
            if row is None:
                raise KeyError("tool not found")
            return dict(row)

    def list(self) -> list[dict[str, Any]]:
        with self.database.connect() as connection:
            rows = connection.execute("select * from tools order by name").fetchall()
            return [dict(row) for row in rows]

    def register_real_rd_tool(self) -> str:
        """注册 real_rd_executor_tool，返回工具名。"""
        tool_name = "real_rd_executor_tool"
        self.register({
            "name": tool_name,
            "type": "executor",
            "description": "RealRD 代码修改执行器：读代码→改代码→跑测试→交付 git diff",
            "entry": "real_rd_executor",
        })
        return tool_name

    @staticmethod
    def get_real_rd_tool_name() -> str:
        return "real_rd_executor_tool"
