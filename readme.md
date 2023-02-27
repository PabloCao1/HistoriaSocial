# Historia Social Única

### ACERCA DEL PROYECTO:

App web que permite visualizar y gestionar información de personas en situación de vulnerabilidad, sus dimensiones (social, económica, habitacional, sanitaria, etc.) y realizar un seguimiento de los objetivos e intervenciones realizadas desde los organismos que trabajan acompañandolas.  


---
### TECNOLOGÍAS UTILIZADAS

![HTML5](https://img.shields.io/badge/-HTML5-%23F11423?style=flat-square&logo=html5&logoColor=ffffff)
![CSS3](https://img.shields.io/badge/-CSS3-%231572B6?style=flat-square&logo=css3)
![JavaScript](https://img.shields.io/badge/-JavaScript-%23F7DF1C?style=flat-square&logo=javascript&logoColor=000000&labelColor=%23F7DF1C&color=%23FFCE5A)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-BE85C6?style=flat-square&logo=Bootstrap)
![Python](http://img.shields.io/badge/-Python-DAD031?style=flat-square&logo=python)
![Django](http://img.shields.io/badge/-Django-025922?style=flat-square&logo=django&logoColor=025922&labelColor=DAD031)
![MySQL](https://img.shields.io/badge/-MySQL-ffffff?style=flat-square&logo=mysql)
![Github](https://img.shields.io/badge/Github-000?style=flat-square&logo=Github)



---

### INSTALACION

#### PRE REQUISITOS:
> python 3.7 o superior

> Mysql 5.0 o superior (Solo para el uso en Ambiente de Producción)

> Graphviz (Solo para la generación de diagramas de la BD, puede consultar [Aquí](https://django-extensions.readthedocs.io/en/latest/graph_models.html))


#### PASOS:
<sub>* Ejemplos de código para SO Windows</sub>

1. Clonar repositorio

```
    git clone https://github.com/mariana-git/HSU.git
```

2. Crear Entorno Virtual y activarlo
```
    virtualenv <nombre-del-entorno>
    <nombre-del-entorno>09\Scripts\activate 
```
3. Instalar paquetes, dependecias y librerías
```
    pip install -r requirements.txt 
```

4. Realizar migraciones
```
    python manage.py makemigrations 
    python manage.py migrate
```
5. Crear un super usuario
```
    python manage.py createsuperuser
```
6. Correr el servidor 
```
    python manage.py runserver
```


---
<center><sub>Desarrolladores:  Mariana Sayago - Pablo Cao</sub></center>


