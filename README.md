# Proyecto portafolio DUOC UC 2022

## Inicializar

Para poder comenzar a ejecutar el proyecto Necesita tener instalado python y el framework Django y una base de datos Oracle XE.

Ejecutar los scripts de creación de usuario con el usuario administrador de la base de datos (DBA).

Ejecutar el script serviexpress.SQL incluida en este proyecto.

Mediante la terminal vaya a la carpeta del proyecto y escriba los isguientes comandos:

> pip install -r requirements.txt

una vez terminado el proceso continue con el siguiente:

> python manage.py makemigrations

> python manage.py migrate

Esto hará que Django se conecte a Oracle y cree las tablas para ejecutar el proyecto.

Una vez terminado todos estos procesos ejecute:

> python manage.py runserver

y django correrá el servicio. :D
