"""Backend tests require an explicit repository-external SQLite before imports."""

from .db_safety import require_isolated_test_database


ISOLATED_TEST_DATABASE = require_isolated_test_database()
