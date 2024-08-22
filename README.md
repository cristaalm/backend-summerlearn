# Backend Develop	


# Requirementos

### ⚠️ **Advertencia:**
Revisa que todo tu proyecto contega las siguientes dependencias y versiones

* Python 3.12.4
* Django 5.1
* Django-Cors-Headers 4.4.0
* Django Rest_Framework  3.15.2

### 💡 **Consejo:**
Utiliza `pip list` para ver todas las dependecias con sus versiones

# Instalacion De Dependecias

### Entorno Virtual ( venv )
El entorno virtual cada quien lo tiene que instalar en su maquina este no se sube al git

Instala un entorno virtual

	 python -m venv venv

Activa el entorno virtual

	.\venv\Scripts\activate


## Instalacion rapida (Todo en uno)

	pip install -r requirements.txt

### [Django](https://www.djangoproject.com/)
Has la instalacion de Django con:

	pip install django

Verifica la instalacion

	django-admin --version

### [Rest Framework](https://www.django-rest-framework.org/)
Instala el framework para el manejo de API

	pip install djangorestframework

	pip install markdown

	pip install django-filter 

### [Django-Cors-Headers](https://pypi.org/project/django-cors-headers/)

	python -m pip install django-cors-headers


### ⚠️ **Advertencia:**

    warning: in the working copy of 'README.md', CRLF will be replaced by LF the next time Git touches it

Si ves este mensaje se le pregunto a GPT que es lo que sucedio aqui les dejo la informacion y posibles solucion (Opcional segun GPT)


## ¿Afecta cuando clones o hagas pull en el futuro?

"No debería causar problemas. Git maneja automáticamente las conversiones de finales de línea según el sistema operativo que estás usando. Si alguien clona o hace pull en un sistema diferente, Git ajustará los finales de línea según la configuración predeterminada o la configuración específica del repositorio." - GPT


## Solución y recomendaciones:

* Puedes ignorar esta advertencia si no te preocupa la consistencia de los finales de línea entre diferentes sistemas operativos.

* Si deseas evitar esta advertencia en el futuro, puedes configurar Git para manejar los finales de línea de manera automática usando los siguientes comandos:


		git config --global core.autocrlf true  # Convierte LF a CRLF en Windows.

    	git config --global core.autocrlf input  # Convierte CRLF a LF en Linux/macOS.