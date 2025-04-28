import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dir_files = [filename.lower() for filename in os.listdir(BASE_DIR)]

files_list = ['program.py', 'readme.md']


def test_program():
    for filename in files_list:
        assert filename in dir_files, f"No se ha encontrado el archivo `{filename}` en la raíz del repositorio"

    try:
        import program
    except Exception as e:
        assert False, (
            'Fallo al ejecutar `program.py`. '
            'Corrige los errores:\\n'
            f'{e}'
        )
