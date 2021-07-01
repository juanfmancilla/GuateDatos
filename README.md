# GuateDatos
PortalGuateDatos

Manual para correr GuateDatos

- conectarse a traves de ssh haciendo forward del puerto 8000 a cualquiera local (en el ejemplo 9000):
ssh -v -L 9000:localhost:8000 jfmancilla@192.168.10.125

- crear un folder llamado django (opcional)
mkdir django
cd django

- crear un virtual environment llamado django
python3 -m venv django

- activar el virtual environment de django
cd django
source django/bin/activate

- crear un folder llamado GuateDatos (opcional)
mkdir GuateDatos
cd GuateDatos

- clonar el repositorio en el servidor deseado
git clone https://github.com/juanfmancilla/GuateDatos.git

- instalar en servidor django, crispy-forms, plotly, pandas, summernote
pip install Django
pip install django-crispy-forms
pip install plotly==4.14.3
pip install django-summernote
pip install pandas

- activar el virtual environment de django, si no esta activado
cd django
source django/bin/activate

- correr el servidor de GuateDatos
cd GuateDatos
python3 manage.py runserver

- acceder al portal a traves del localhost y el puerto seleccionado
localhost:9000
