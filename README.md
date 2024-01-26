# Django-tenants

I created an application using Django Tenants([docs](https://github.com/django-tenants/django-tenants)) for multi-tenancy with PostgreSQL Schemas, ensuring data isolation. Tenants can be created using a RESTful API implemented with Django Rest Framework.

## Getting started
### Requirements
You need to install [Docker](https://www.docker.com/)
 and [Docker-Compose](https://docs.docker.com/compose/).

### Build

             docker-compose up -d 
### Migrate databases

             docker-compose exec web python manage.py migrate
#### Createsuperuser

             docker-compose exec web python manage.py createsuperuser
#### Create_tenant
             docker-compose exec web python manage.py create_tenant 
<img src="https://github.com/MohamedMeftouh21/django_tenant/blob/main/Capture%20d%E2%80%99e%CC%81cran%202024-01-25%20a%CC%80%2020.35.03.png" width="600" height="450"/>


