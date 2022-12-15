# ACRM

<img src="https://github.com/lestec-al/url-shortener-django/blob/main/pic_crm.png" width="640" height="360"/>

Simple Django CRM website. A good starting point for creating a custom CRM with specific functions.

Basicaly, site have two interfaces: one for managers (white), one for staff users (blue). Blue interface it's modified django standard admin interface. Language there should be you language.
On white interface you can:
- login/logout
- create/edit sales
On blue interface you can:
- login/logout
- create/edit/delete users
- create/edit/delete sales
- create/edit/delete products
- handle settings (sales table and timezonas for users).


# To run on a local server you need:
- install Python (v3.10 or higher)
- download or clone this project
- through the command line, go to the project folder and type (press enter after each command): 'pip install -r requirements.txt', 'python manage.py makemigrations', 'python manage.py migrate', 'python manage.py runserver', 'python manage.py createsuperuser' (and follow instructions).