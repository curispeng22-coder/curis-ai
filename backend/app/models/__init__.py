"""D1-related data models (scope B).

This subpackage intentionally only hosts append-only, desensitized record stores
used by the D1 controlled-gate (e.g. ``d1_execution_log``). It must not import
or mutate any shared core schema; table registration lives in
``app.database.Database.initialize()``.
"""
