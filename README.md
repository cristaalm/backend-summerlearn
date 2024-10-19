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

## Instalación Individual

### [Django](https://www.djangoproject.com/)

Instala Django con:

```sh
pip install django
```

Verifica la instalación:

```sh
django-admin --version
```

### [Rest Framework](https://www.django-rest-framework.org/)

Instala el framework para el manejo de API:

```sh
pip install djangorestframework
pip install markdown
pip install django-filter
```

### [Django-Cors-Headers](https://pypi.org/project/django-cors-headers/)

Instala Django-Cors-Headers:

```sh
python -m pip install django-cors-headers
```

### ⚠️ **Advertencia:**

Si ves el siguiente mensaje:

```
warning: in the working copy of 'README.md', CRLF will be replaced by LF the next time Git touches it
```

Aquí tienes información y posibles soluciones:

## ¿Afecta cuando clones o hagas pull en el futuro?

"No debería causar problemas. Git maneja automáticamente las conversiones de finales de línea según el sistema operativo que estás usando. Si alguien clona o hace pull en un sistema diferente, Git ajustará los finales de línea según la configuración predeterminada o la configuración específica del repositorio." - GPT

## Solución y Recomendaciones:

- Puedes ignorar esta advertencia si no te preocupa la consistencia de los finales de línea entre diferentes sistemas operativos.
- Si deseas evitar esta advertencia en el futuro, puedes configurar Git para manejar los finales de línea de manera automática usando los siguientes comandos:

```sh
git config --global core.autocrlf true  # Convierte LF a CRLF en Windows.
git config --global core.autocrlf input  # Convierte CRLF a LF en Linux/macOS.
```

# Iniciar el Servidor

Para iniciar el servidor, usa el siguiente comando:

```sh
watchfiles "daphne myApp.asgi:application -b 0.0.0.0 -p 8000"
```
