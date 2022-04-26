# Proyecto portafolio DUOC UC 2022

## Inicializar

Para poder comenzar a ejecutar el proyecto Necesita tener instalado python y el framework Django y una base de datos Oracle XE.

Ejecutar los scripts SQL y DDL de creación de usuario y tablas.

Ejecutar el script PROCEDIMIENTOS.SQL incluida en este proyecto.

Mediante la terminal vaya a la carpeta del proyecto y escriba el siguiente comando:

> python manage.py migrate

Esto hará que Django se conecte a Oracle y cree las tablas para ejecutar el proyecto.

Una vez terminado todos estos procesos ejecute:

> python manage.py runserver

y django correrá el servicio. :D
