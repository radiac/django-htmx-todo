"""
Add support for django-configurations to django-stubs

Based on https://github.com/typeddjango/django-stubs/pull/180#issuecomment-820062352
"""
from os import environ

from configurations.importer import install
from mypy_django_plugin import main


def plugin(version):
    environ.setdefault("DJANGO_SETTINGS_MODULE", "todo.config")
    environ.setdefault("DJANGO_CONFIGURATION", "Test")
    install()
    return main.plugin(version)
