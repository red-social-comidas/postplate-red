* --------------------------------------------- PASO A PASOS ---------------------------------- 
# c21-16-m-python-react


1: Activar el entorno virtual

# En Windows
env\Scripts\activate.bat

# En macOS/Linux
source env/bin/activate
_______________________________________________________________________________
=======
1. Crear el entorno virtual:

```bash
python -m venv venv
```

2. Abrir el entorno virtual desde vs code con la extension de python:

3. instalar dependencias:
```bash
pip install -r requirements.txt
```
_______________________________________________________________________________
3. Crear migraciones
python manage.py makemigrations

ACLARACIÓN: en el caso de correr el comando del paso 3 y que de como resultado lo siguiente
No changes detected

tenemos que escribir el comando mas el nombre de la app ej = "python manage.py makemigrations users "  "python manage.py makemigrations publication" 
_______________________________________________________________________________

4. Iniciar el servidor:

```bash
python manage.py runserver
```

## Nota:

Si el mensaje de despues de iniciar el servidor, es que hay migraciones sin aplicar, apagar el servidor y usar el siguiente comando:

```bash
python manage.py migrate
_______________________________________________________________________________

5:Crear Superuser 
python manage.py createsuperuser
_______________________________________________________________________________

6:Ejecutar el servidor
python manage.py runserver
