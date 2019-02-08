CameraStore Python/Django sample application for Tradenity ecommerce API
============================================

This is a sample application for [Tradenity](https://www.tradenity.com) ecommerce API using the [Python SDK](https://github.com/tradenity/python-sdk) with django to build ecommerce web application

To run it on your local machine:

## Prerequisites

-  Python 2.7

## Get the application

Choose one of the following:

- Download the source code.
- Clone `git clone git@github.com:tradenity/camerastore-python-django-sample.git`
- Fork this repository

## Create store and load sample data

- If you are not yet registered, create a new [Tradenity account](https://www.tradenity.com).
- After you login to your account, go to [Getting started](https://admin.tradenity.com/admin/getting_started) page, click "Create sample store", this will create a new store and populate it with sample data
- From the administration side menu, choose "Developers" > "API Keys", you can use the default key or generate a new one.

## Edit Credentials

From the previous step, copy the `SecretKey` and use it as your API Key.

Open `tradenity_python_django_sample.settings`, modify this line: 

`Configuration.API_KEY = 'sk_xxxxxxxxxxxxxxxxx'` 

to reflect your store's API key.

If you configured your store to use stripe for payment processing, then edit this line:

`STRIPE_PUBLIC_KEY = 'pk_xxxxxxxxxxxxxxxxxxxxxxxxxx'` to reflect your public key.


## Install requirements

`pip install -r requirements.txt`


## Run

python manage.py runserver