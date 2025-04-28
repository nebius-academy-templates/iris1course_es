import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'wordicum'
MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
# Asegúrate de que la raíz del repositorio contenga el directorio del proyecto
if (
        PROJECT_DIR_NAME not in root_dir_content
        or not os.path.isdir(MANAGE_PATH)
):
    assert False, (
        f'No se encuentra la carpeta del proyecto `{PROJECT_DIR_NAME}` en `{BASE_DIR}`. '
        f'Asegúrate de mantener una estructura de árbol de proyecto adecuada.'
    )

project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'
# Asegúrate de que la estructura es correcta y de que manage.py está en su sitio
if FILENAME not in project_dir_content:
    assert False, (
        f'El archivo `{FILENAME}` no se encuentra en el directorio `{MANAGE_PATH}`. '
        f'Asegúrate de mantener una estructura de árbol de proyecto adecuada.'
    )

from django.utils.version import get_version

assert get_version() < '3.0.0', 'Por favor, utiliza una versión de Django < 3.0.0'

from wordicum.settings import INSTALLED_APPS

assert any(app in INSTALLED_APPS for app in ['posts.apps.PostsConfig', 'posts']), (
    'Por favor, registra la aplicación en `settings.INSTALLED_APPS`'
)

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]
