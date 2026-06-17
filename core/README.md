# Cafe Management System

## Description

Cafe Management System is a Django-based web application for managing a cafe. It allows staff to manage menu items, orders, tables, shifts, and promo codes.

## Features

* Menu management
* Order management
* Table management
* Shift management
* Revenue calculation
* Promo code support
* Django Admin panel
* Automated tests

## Technologies

* Python 3
* Django 5
* SQLite3
* Bootstrap 5

## Models

* Shift
* Table
* MenuItem
* Order
* OrderItem
* PromoCode

## Installation

```bash
git clone <repository-url>
cd cafe_management
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Running Tests

```bash
python manage.py test
```

## Author

Joloev Erjan

