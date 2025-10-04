#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    # Set the default settings module for the 'DivUnion' project.  This allows
    # Django commands (e.g. runserver, migrate) to locate the correct
    # configuration without requiring the user to export DJANGO_SETTINGS_MODULE.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DivUnion.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # The import may fail if Django isn't installed in the current
        # environment.  Provide a helpful message so users know what to do.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
