# Iris para amistades

## Cómo trabajar con el repositorio
### Clona el proyecto Iris para amistades en la carpeta *Dev/*.

Deberías obtener esta estructura:

```
Dev/
 └── iris1course/
     ├── iris_for_fiends/
     ├── html_templates/
     ├── .gitignore
     ├── LICENSE
     ├── requirements.txt
     └── README.md
```

### Creación de un entorno virtual

1. Abre Visual Studio Code, ve a *"Archivo" / "Abrir carpeta"*, y abre *Dev/iris1course/*.
2. Inicia la terminal en VS Code y asegúrate de trabajar desde el directorio *iris1course/*. Si usas Windows, asegúrate de que se ejecute Git Bash en la terminal, y no a través de PowerShell o algún otro. Ejecuta este comando:
- Linux/macOS
    
    ```bash
    python3 -m venv venv
    ```
    
- Windows
    
    ```python
    python -m venv venv
    ```

El entorno virtual se desplegará en el directorio *iris1course/*. La carpeta `venv` también aparecerá allí, y almacenará todas las dependencias del proyecto. La estructura del archivo se vera así:

```

Dev/
└── iris1course/
    ├── iris_for_friends/
    ├── html_templates/
    ├── venv/   
    ├── .gitignore
    ├── LICENSE
    ├── requirements.txt
    └── README.md
```

### Activar el entorno virtual
En la terminal, accede al directorio raíz del proyecto *Dev/iris1course/* y ejecuta este comando:
- Linux/macOS
    
    ```bash
    source venv/bin/activate
    ```
    
- Windows
    
    ```bash
    source venv/Scripts/activate
    ```

Todos los comandos de la terminal irán ahora precedidos por el string (`venv`).

💡 Todos los siguientes comandos de la consola se deben ejecutar con el entorno virtual de trabajo.

Actualiza pip:

```bash
python -m pip install --upgrade pip
```

### Instalar las dependencias del archivo *requirements.txt*
Ejecuta el siguiente comando mientras estás en la carpeta *Dev/iris1course/*:

```bash
pip install -r requirements.txt
```

### Uso de migraciones

    
En el directorio con el archivo manage.py, ejecuta el siguiente comando:

```bash
python manage.py migrate
```

### Ejecutar el proyecto en modo dev

    
En el directorio con el archivo manage.py, ejecuta el siguiente comando:

```bash
python manage.py runserver
```

En respuesta a este comando, Django indicará que el servidor está funcionando y que el proyecto está disponible en [http://127.0.0.1:8000/](http://127.0.0.1:8000/). 
