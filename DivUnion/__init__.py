"""Project package initialisation helpers."""

from __future__ import annotations

import importlib
import os


def _install_pymysql() -> None:
    """Install PyMySQL as the MySQLdb replacement when available."""

    if os.environ.get("DJANGO_USE_PYMYSQL", "1") != "1":
        return

    if importlib.util.find_spec("pymysql") is None:
        return

    pymysql = importlib.import_module("pymysql")
    pymysql.install_as_MySQLdb()


_install_pymysql()
