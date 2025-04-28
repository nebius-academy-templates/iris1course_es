import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir_content = os.listdir(BASE_DIR)
PROJECT_DIR_NAME = 'wordicum'
MANAGE_PATH = os.path.join(BASE_DIR, PROJECT_DIR_NAME)
# Comprueba que la raíz del repositorio contenga el directorio del proyecto
if (
        PROJECT_DIR_NAME not in root_dir_content
        or not os.path.isdir(MANAGE_PATH)
):
    assert False, (
        f'La carpeta del proyecto `{BASE_DIR}` no se encuentra en `{PROJECT_DIR_NAME}`. '
        f'Asegúrate de tener la correcta estructura de árbol del proyecto.'
    )

project_dir_content = os.listdir(MANAGE_PATH)
FILENAME = 'manage.py'
# Comprueba que la estructura sea correcta y que manage.py está en su lugar
if FILENAME not in project_dir_content:
    assert False, (
        f'El archivo `{MANAGE_PATH}` no se encuentra en el directorio `{FILENAME}`. '
        f'Asegúrate de tener la estructura de árbol del proyecto correcta.'
    )

from django.utils.version import get_version

assert get_version() < '3.0.0', 'Por favor, utiliza la versión < 3.0.0'

from wordicum.settings import INSTALLED_APPS

assert any(app in INSTALLED_APPS for app in ['posts.apps.PostsConfig', 'posts']), (
    'Por favor registra la aplicación en `settings.INSTALLED_APPS`'
)

pytest_plugins = [
    'tests.fixtures.fixture_user',
    'tests.fixtures.fixture_data',
]
