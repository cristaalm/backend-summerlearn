# Backend Develop

# Requisitos

### ⚠️ **Advertencia:**

Asegúrate de que tu proyecto contenga las siguientes dependencias y versiones:

- Python 3.12.4
- Django 5.1
- Django-Cors-Headers 4.4.0
- Django Rest Framework 3.15.2

### 💡 **Consejo:**

Utiliza `pip list` para ver todas las dependencias con sus versiones.

# Instalación de Dependencias

## Entorno Virtual (venv)

El entorno virtual debe ser instalado localmente y no se debe subir a Git.

### Instalación del Entorno Virtual

```sh
python -m venv venv
```

### Activación del Entorno Virtual

#### En Windows

```sh
.\venv\Scripts\activate
```

#### En Linux/MacOS

```sh
source venv/bin/activate
```

## Instalación Rápida (Todo en uno)

```sh
pip install -r requirements.txt
```

# Iniciar el Servidor

Para iniciar el servidor, usa el siguiente comando:

```sh
watchfiles "daphne myApp.asgi:application -b 0.0.0.0 -p 8000"
```
