#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ice_creamology.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se ha podido importar Django. ¿Estás seguro de que está instalado "
            "ay disponible en tu variable de entorno PYTHONPATH? ¿Te olvidaste de "
            "activar un entrono virtual?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
