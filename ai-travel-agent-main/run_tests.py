"""Tiny test runner for the project so tests can be executed without pytest.

This will run the test modules under `tests/` by importing them and
reporting failures. It is intentionally minimal and intended for local use.
"""
import importlib
import sys
from pathlib import Path

TEST_DIR = Path(__file__).parent / 'tests'

modules = [f.stem for f in TEST_DIR.glob('test_*.py')]

failed = 0
for m in modules:
    try:
        importlib.import_module(f'tests.{m}')
        print(f'OK: {m}')
    except Exception as e:
        failed += 1
        print(f'FAIL: {m} -> {e}')

if failed:
    print(f"{failed} test module(s) failed")
    sys.exit(1)
else:
    print('All test modules imported successfully')
    sys.exit(0)
