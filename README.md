CameraStore Python/Django sample application
============================================

This is a demonstration of using Tradenity SDK with Flask to build ecommerce web application

To run it on your local machine:

## Prerequisites

-  Python 2.7

## Get the application

Choose one of the following:

- Download the source code.
- Clone `git clone git@github.com:tradenity/camerastore-python-django-sample.git`
- Fork this repository

## Edit Credentials

Open `tradenity_python_django_sample.settings`, modify this line: 

`Tradenity.API_KEY = 'sk_xxxxxxxxxxxxxxxxx'` 

to reflect your store's API key.

If you configured your store to use stripe for payment processing, then edit this line:

`STRIPE_PUBLIC_KEY = 'pk_xxxxxxxxxxxxxxxxxxxxxxxxxx'` to reflect your public key.


## Install requirements

`pip install -r requirements.txt`


## Run

python manage.py runserver