"""Step 5：模型网关从「写死单一供应商」扩为「N 个可注册供应商」。

覆盖四层：
1. 常量层：``GATEWAY_TYPE`` 放开为多方言，且只收 OpenAI 兼容协议。
2. Schema 层：``model_gateways.type`` 的 CHECK 清单与 ``GATEWAY_TYPE`` 严格同步；
   既有单类型库经迁移重建后数据不丢、可写新类型。
3. 目录层：``GatewayCatalog.create`` 能登记多个不同类型的供应商。
4. 运行期：``ModelGatewayAdapter.with_model_metadata`` 按 gateway_id 解析出
   **该供应商自己的 base_url + 凭证**，停用网关显式拒绝，未注册网关向后兼容。
"""

from __future__ import annotations

import os
import re
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from app.catalog_constants import GATEWAY_TYPE, is_valid_gateway_type
from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.model_catalog import GatewayCatalog
from app.model_gateway import (
    ModelGatewayAdapter,
    ModelGatewayExecutionError,
    resolve_gateway_api_key,
)

# 旧库形态：单一类型 CHECK（Step 5 之前的线上 schema）。
LEGACY_GATEWAY_DDL = """
create table model_gateways (
  gateway_id      text primary key,
  name            text not null,
  type            text not null default 'newapi'
                    check (type in ('newapi')),
  base_url        text not null,
  status          text not null default 'active'
                    check (status in ('active', 'inactive')),
  credential_ref  text,
  default_model   text,
  created_at      text not null default current_timestamp
);
"""


def _temp_db_path(cleanup) -> str:
    handle = tempfile.NamedTemporaryFile(delete=False)
    path = handle.name
    handle.close()
    cleanup(lambda: os.path.exists(path) and os.unlink(path))
    return path


class Step5GatewayTypeConstantTestCase(unittest.TestCase):
    def test_multiple_types_are_registrable(self):
        self.assertGreater(len(GATEWAY_TYPE), 1, "Step 5 后网关类型不应只剩一个")
        self.assertEqual(GATEWAY_TYPE[0], "newapi", "newapi 必须保持首位以兼容既有种子")
        self.assertEqual(len(GATEWAY_TYPE), len(set(GATEWAY_TYPE)), "类型不得重复")
        for gateway_type in GATEWAY_TYPE:
            self.assertTrue(is_valid_gateway_type(gateway_type))

    def test_non_openai_compatible_dialects_stay_out(self):
        """协议形状不同的厂商未实现前不得进枚举（进了就是撒谎）。"""
        for forbidden in ("anthropic", "gemini", "bedrock", "vertex"):
            self.assertNotIn(forbidden, GATEWAY_TYPE)
            self.assertFalse(is_valid_gateway_type(forbidden))


class Step5GatewaySchemaTestCase(unittest.TestCase):
    def setUp(self):
        self.db_path = _temp_db_path(self.addCleanup)

    @staticmethod
    def _schema_check_types(db_path: str) -> list[str]:
        with sqlite3.connect(db_path) as connection:
            row = connection.execute(
                "select sql from sqlite_master "
                "where type = 'table' and name = 'model_gateways'"
            ).fetchone()
        assert row is not None
        match = re.search(r"check\s*\(\s*type\s+in\s*\(([^)]*)\)", row[0], re.IGNORECASE)
        assert match, f"未找到 type CHECK：{row[0]}"
        return re.findall(r"'([^']+)'", match.group(1))

    def test_schema_check_stays_in_sync_with_constant(self):
        database = Database(self.db_path)
        database.initialize()
        self.assertEqual(self._schema_check_types(self.db_path), list(GATEWAY_TYPE))

    def test_legacy_single_type_db_is_migrated_without_data_loss(self):
        # 1) 造一个 Step 5 之前的旧库：只允许 newapi，并写入一行既有数据。
        with sqlite3.connect(self.db_path) as connection:
            connection.executescript(LEGACY_GATEWAY_DDL)
            connection.execute(
                "insert into model_gateways "
                "(gateway_id, name, type, base_url, status, credential_ref, default_model) "
                "values ('newapi', 'New API Gateway', 'newapi', "
                "'https://api.example.com', 'active', 'env:LEGACY_KEY', 'legacy-model')"
            )
        self.assertEqual(self._schema_check_types(self.db_path), ["newapi"])

        # 2) 初始化触发迁移：CHECK 放开，旧行原样保留。
        Database(self.db_path).initialize()
        self.assertEqual(self._schema_check_types(self.db_path), list(GATEWAY_TYPE))
        legacy = Database(self.db_path).get_model_gateway("newapi")
        self.assertIsNotNone(legacy)
        self.assertEqual(legacy["base_url"], "https://api.example.com")
        self.assertEqual(legacy["credential_ref"], "env:LEGACY_KEY")
        self.assertEqual(legacy["default_model"], "legacy-model")

        # 3) 迁移后可以写入新类型（旧库直接写会被 CHECK 拒绝）。
        database = Database(self.db_path)
        database.save_model_gateway(
            gateway_id="my-deepseek",
            name="DeepSeek",
            gateway_type="deepseek",
            base_url="https://api.deepseek.com",
            credential_ref="env:DEEPSEEK_KEY",
        )
        self.assertEqual(
            database.get_model_gateway("my-deepseek")["type"], "deepseek"
        )

        # 4) 幂等：再次 initialize 不重复重建、不丢数据。
        Database(self.db_path).initialize()
        self.assertIsNotNone(Database(self.db_path).get_model_gateway("my-deepseek"))
        self.assertIsNotNone(Database(self.db_path).get_model_gateway("newapi"))

    def test_unsupported_type_is_still_rejected_by_schema(self):
        database = Database(self.db_path)
        database.initialize()
        with self.assertRaises(sqlite3.IntegrityError):
            database.save_model_gateway(
                gateway_id="bad",
                name="Bad",
                gateway_type="anthropic",
                base_url="https://api.anthropic.com",
            )


class Step5GatewayCatalogTestCase(unittest.TestCase):
    def setUp(self):
        self.db_path = _temp_db_path(self.addCleanup)
        self.database = Database(self.db_path)
        self.database.initialize()
        self.catalog = GatewayCatalog(self.database, EvolutionEventLog(self.database))

    def test_can_register_several_suppliers_side_by_side(self):
        specs = [
            ("gw-openai", "OpenAI", "openai", "https://api.openai.com"),
            ("gw-deepseek", "DeepSeek", "deepseek", "https://api.deepseek.com"),
            ("gw-ollama", "本地 Ollama", "ollama", "http://127.0.0.1:11434"),
        ]
        for gateway_id, name, gateway_type, base_url in specs:
            row = self.catalog.create(
                gateway_id=gateway_id,
                name=name,
                gateway_type=gateway_type,
                base_url=base_url,
                credential_ref="env:SOME_KEY",
            )
            self.assertEqual(row["type"], gateway_type)
        registered = {row["gateway_id"] for row in self.database.list_model_gateways()}
        self.assertTrue({s[0] for s in specs} <= registered)

    def test_unknown_type_rejected_before_hitting_db(self):
        with self.assertRaises(ValueError):
            self.catalog.create(
                gateway_id="gw-claude",
                name="Claude",
                gateway_type="anthropic",
                base_url="https://api.anthropic.com",
            )


class Step5AdapterResolutionTestCase(unittest.TestCase):
    """运行期：切模型时必须连端点带凭证一起换。"""

    GATEWAYS = {
        "gw-a": {
            "gateway_id": "gw-a",
            "name": "A 供应商",
            "type": "openai_compatible",
            "base_url": "https://a.example.com/",
            "status": "active",
            "credential_ref": "env:STEP5_A_KEY",
        },
        "gw-b": {
            "gateway_id": "gw-b",
            "name": "B 供应商",
            "type": "deepseek",
            "base_url": "https://b.example.com",
            "status": "active",
            "credential_ref": "env:STEP5_B_KEY",
        },
        "gw-off": {
            "gateway_id": "gw-off",
            "name": "已停用",
            "type": "openai",
            "base_url": "https://off.example.com",
            "status": "inactive",
            "credential_ref": "env:STEP5_A_KEY",
        },
        "gw-novault": {
            "gateway_id": "gw-novault",
            "name": "尚未接入 vault",
            "type": "openai",
            "base_url": "https://vault.example.com",
            "status": "active",
            "credential_ref": "vault:not-wired-yet",
        },
    }

    def setUp(self):
        self.env = patch.dict(
            os.environ,
            {
                "STEP5_A_KEY": "key-a",
                "STEP5_B_KEY": "key-b",
                "CURIS_MODEL_GATEWAY_BASE_URL": "https://default.example.com",
                "CURIS_MODEL_GATEWAY_API_KEY": "key-default",
                "CURIS_MODEL_GATEWAY_ID": "newapi",
                "CURIS_MODEL_GATEWAY_MODEL": "default-model",
                "CURIS_MODEL_GATEWAY_PROFILE": "",
            },
        )
        self.env.start()
        self.addCleanup(self.env.stop)
        self.calls = []

        def http_post(url, payload, headers, timeout):
            self.calls.append((url, headers.get("Authorization"), payload.get("model")))
            return {"choices": [{"message": {"content": "ok"}}]}

        self.adapter = ModelGatewayAdapter(
            gateway_resolver=self.GATEWAYS.get,
            http_post=http_post,
        )

    def test_credential_ref_only_resolves_env_scheme(self):
        self.assertEqual(resolve_gateway_api_key("env:STEP5_A_KEY"), "key-a")
        self.assertEqual(resolve_gateway_api_key("env:MISSING_VAR"), "")
        self.assertEqual(resolve_gateway_api_key("vault:whatever"), "")
        self.assertEqual(resolve_gateway_api_key("kms:whatever"), "")
        self.assertEqual(resolve_gateway_api_key(""), "")
        self.assertEqual(resolve_gateway_api_key(None), "")

    def test_switching_gateway_switches_endpoint_and_key(self):
        a = self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model")
        b = self.adapter.with_model_metadata(gateway_id="gw-b", model_name="b-model")
        self.assertEqual(a.base_url, "https://a.example.com")  # 末尾斜杠被归一
        self.assertEqual(a.api_key, "key-a")
        self.assertEqual(b.base_url, "https://b.example.com")
        self.assertEqual(b.api_key, "key-b")

        a.execute("hello")
        b.execute("hello")
        self.assertEqual(
            self.calls,
            [
                ("https://a.example.com/v1/chat/completions", "Bearer key-a", "a-model"),
                ("https://b.example.com/v1/chat/completions", "Bearer key-b", "b-model"),
            ],
        )

    def test_never_sends_default_key_to_another_supplier(self):
        """红线：换了端点却沿用旧密钥 = 把 A 家的 key 发给 B 家。"""
        novault = self.adapter.with_model_metadata(
            gateway_id="gw-novault", model_name="x"
        )
        self.assertEqual(novault.base_url, "https://vault.example.com")
        self.assertEqual(novault.api_key, "", "vault: 未接入时必须留空，不得回落默认 key")
        with self.assertRaises(RuntimeError):
            novault.execute("hello")
        self.assertEqual(self.calls, [], "配置不完整不得发出任何出站请求")

    def test_disabled_gateway_is_rejected_not_silently_rerouted(self):
        off = self.adapter.with_model_metadata(gateway_id="gw-off", model_name="x")
        self.assertTrue(off.disabled_reason)
        with self.assertRaises(ModelGatewayExecutionError) as ctx:
            off.execute("hello")
        self.assertEqual(ctx.exception.status, "configuration_rejected")
        self.assertEqual(self.calls, [])

    def test_unregistered_different_gateway_is_rejected(self):
        with self.assertRaises(ModelGatewayExecutionError) as error:
            self.adapter.with_model_metadata(gateway_id="not-registered", model_name="m")
        self.assertFalse(error.exception.outbound_attempted)
        self.assertEqual(self.calls, [])

    def test_same_single_gateway_keeps_its_configuration(self):
        for resolver in (None, lambda _: None):
            plain = ModelGatewayAdapter(gateway_resolver=resolver, http_post=lambda *args: {})
            switched = plain.with_model_metadata(gateway_id=plain.gateway_id, model_name="m")
            self.assertEqual(switched.base_url, plain.base_url)
            self.assertEqual(switched.api_key, plain.api_key)
        with self.assertRaises(ModelGatewayExecutionError):
            plain.with_model_metadata(gateway_id="another", model_name="m")

    def test_resolver_exception_and_foreign_row_reject_before_transport(self):
        def broken(_):
            raise RuntimeError("must not expose resolver details")
        for resolver in (broken, lambda _: self.GATEWAYS["gw-b"], lambda _: []):
            self.adapter.gateway_resolver = resolver
            with self.assertRaises(ModelGatewayExecutionError) as error:
                self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model")
            self.assertEqual(error.exception.status, "configuration_rejected")
            self.assertFalse(error.exception.outbound_attempted)
        self.assertEqual(self.calls, [])

    def test_incomplete_registered_route_never_borrows_default(self):
        for field in ("base_url", "credential_ref"):
            row = {**self.GATEWAYS["gw-a"], field: ""}
            self.adapter.gateway_resolver = lambda _, row=row: row
            selected = self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model")
            with self.assertRaises(RuntimeError):
                selected.execute("hello")
        self.assertEqual(self.calls, [])

    def test_registered_openai_route_does_not_inherit_native_protocol(self):
        self.adapter.protocol = "anthropic_messages"
        self.adapter.chat_path = "/v1/messages"
        selected = self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model")
        selected.execute("hello")
        self.assertEqual(selected.protocol, "openai_chat")
        self.assertEqual(self.calls, [("https://a.example.com/v1/chat/completions", "Bearer key-a", "a-model")])

    def test_cross_route_does_not_inherit_environment_price(self):
        self.adapter.price_version = "default-model-only"
        self.adapter.estimated_rate = "10"
        self.adapter.http_post = lambda *args: {"choices": [{"message": {"content": "ok"}}], "usage": {"total_tokens": 10}}
        result = self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model").execute("hello")
        self.assertEqual(result["price_version"], "")
        self.assertIsNone(result["estimated_cost"])
        self.assertEqual(result["ledger_cost_source"], "unknown")

    def test_unknown_cost_is_not_a_zero_estimate(self):
        with patch.dict(os.environ, {"CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS": "0"}):
            selected = self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model")
            result = selected.execute("hello")
        self.assertIsNone(result["estimated_cost"])
        self.assertEqual(result["ledger_cost_source"], "unknown")
        self.assertIsNone(result["total_tokens"])

    def test_provider_reported_zero_is_distinct_from_unknown(self):
        self.adapter.http_post = lambda *args: {"choices": [{"message": {"content": "ok"}}], "usage": {"cost": 0}}
        result = self.adapter.with_model_metadata(gateway_id="gw-a", model_name="a-model").execute("hello")
        self.assertEqual(result["estimated_cost"], 0)
        self.assertEqual(result["ledger_cost_source"], "provider_reported")


if __name__ == "__main__":
    unittest.main()
