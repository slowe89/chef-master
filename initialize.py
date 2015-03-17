#! usr/bin/env python3

#############################################################
# 
# Author: John Turner
# Version: 1.0
# Last Updated: 2/18/2015
# 
# This file contains the database initialization script for
# the Recruiter Connect Database. This file will drop, recreate
# and migrate the db, and then insert the data necessary to 
# start working, including:
#	- Creating a SuperUser
#	- Adding the Groups
#	- Adding Users to the Groups
# 
#############################################################

import random
import os
import datetime
import sys

# Initialize the django environment, import the models
os.environ['DJANGO_SETTINGS_MODULE'] = 'chef.settings'
import base_app.models as mod
import django
django.setup()

# grab models that I'll need 
from django.contrib.auth.models import Group, Permission, ContentType
from django.db import connection
import subprocess

# Drop database, recreate it, migrate it
cursor = connection.cursor()
cursor.execute('DROP SCHEMA PUBLIC CASCADE')
cursor.execute('CREATE SCHEMA PUBLIC')
subprocess.call([sys.executable, 'manage.py', 'migrate'])

#############################################################################
############################## GROUPS/USERS #################################
#############################################################################

Group.objects.all().delete()

############################# ADMINISTRATORS ################################

# Administrators - have full rights to all system
# 	- add superuser to this group
group = Group()
group.name = "Administrator"
group.save()

# Add all permissions to Admin group
permissions = Permission.objects.all()

for permission in permissions:
    group.permissions.add(permission)

mod.User.objects.all().delete()

# Create superuser with the following credentials:
# 	- username = admin
# 	- password: password
# 	- email = john.duane.turner@gmail.com
user = mod.User.objects.create_superuser( username='admin', email='test@fake.com', password='password' )
user.first_name = 'Spencer'
user.last_name = 'Lowe'
user.address1 = '129 S 1011 W'
user.city = 'Provo'
user.state = 'Utah'
user.ZIP = '84601'
user.phone = '707-330-3952'
user.security_question = 'What?'
user.security_answer = 'Yaya!'
user.save()

group.user_set.add(user)

################################# MANAGERS ###################################

# Managers - can add/edit/delete the following:
#	- Events
#	- Areas
# 	- Inventory
#	- Transactions
group = Group()
group.name = 'Manager'
group.save()

# Add permissions for the Managers
# Get content types first
content_types = ContentType.objects.exclude(app_label='auth').exclude(app_label='admin')
content_types.exclude(app_label='base_app', model='User').exclude(app_label='contenttypes').exclude(app_label='sessions')

for content_type in content_types:
    permissions = Permission.objects.filter(content_type=content_type)

    for permission in permissions:
        group.permissions.add(permission)

################################## GUESTS ####################################

# Guests have no permissions, they are used in creating new users
group = Group()
group.name = 'Guest'
group.save()

venue = mod.Venue()
venue.name = 'The Park'
venue.address = '123 Lollipop Ln.'
venue.save()

publicEvent = mod.PublicEvent()
publicEvent.name = 'Pool Party'
publicEvent.description = 'Cool people party hardy, gettin all wet and wild.'
publicEvent.save()

event = mod.Event()
event.venue = venue
event.name = 'Party Time'
event.start_date = '2015-01-25'
event.end_date = '2015-03-22'
event.save()

area = mod.Area()
area.name = 'The Spot'
area.description = 'Here goes the description'
area.place_number = 1
area.event = event
area.save()

expectedSaleItem = mod.ExpectedSaleItem()
expectedSaleItem.area = area
expectedSaleItem.high_price = 15
expectedSaleItem.low_price = 10
expectedSaleItem.name = 'Breeches'
expectedSaleItem.description = 'Here goes the description'
expectedSaleItem.save()

category = mod.Category()
category.description = 'Here goes a category'
category.save()

productSpecification = mod.ProductSpecification()
productSpecification.description = 'Description'
productSpecification.category = category
productSpecification.average_cost = 19
productSpecification.manufacturer = 'Manufacturer'
productSpecification.price = 13.99
productSpecification.produced_by = user
productSpecification.production_time = '3 hrs'
productSpecification.save()

inventory = mod.Inventory()
inventory.name = 'Shirt'
inventory.condition = 'Ancient'
inventory.note = 'Last washed four years ago'
inventory.price = 84.99
inventory.order_file = 'order file here'
inventory.quantity_on_hand = 25
inventory.shelf_location = 'in ya face'
inventory.specs = productSpecification
inventory.save()

inventory = mod.Inventory()
inventory.name = 'Stick'
inventory.condition = 'Used'
inventory.note = 'A traveling companion'
inventory.price = 29.99
inventory.order_file = 'order file here'
inventory.quantity_on_hand = 29
inventory.shelf_location = 'in ya face'
inventory.specs = productSpecification
inventory.save()

inventory = mod.Inventory()
inventory.name = 'Bomb'
inventory.condition = 'Shifty'
inventory.note = 'Here is a note'
inventory.price = 0.99
inventory.order_file = 'order file here'
inventory.quantity_on_hand = 100
inventory.shelf_location = 'in ya face'
inventory.specs = productSpecification
inventory.save()

inventory = mod.Inventory()
inventory.name = 'Wheel'
inventory.condition = 'Good'
inventory.note = 'Here is a note'
inventory.price = 16.99
inventory.order_file = 'order file here'
inventory.quantity_on_hand = 58
inventory.shelf_location = 'in ya face'
inventory.specs = productSpecification
inventory.save()

inventory = mod.Inventory()
inventory.name = 'Bread'
inventory.condition = 'Fresh'
inventory.note = 'Here is a note'
inventory.price = 4.99
inventory.order_file = 'order file here'
inventory.quantity_on_hand = 12
inventory.shelf_location = 'in ya face'
inventory.specs = productSpecification
inventory.save()

item = mod.Item()
item.standard_rental_price = 130.28
item.owner = user
item.condition = 'great'
item.times_rented = 23
item.price_per_day = 18
item.replacement_price = 56.99
item.name = 'Goves Breeches'
item.save()

wardrobeItem = mod.WardrobeItem()
wardrobeItem.size = 5
wardrobeItem.size_modifier = 'Baggy'
wardrobeItem.gender = 'F'
wardrobeItem.color = 'green'
wardrobeItem.pattern = 'cross-stiched'
wardrobeItem.start_year = '2000-01-02'
wardrobeItem.end_year = '2040-11-25'
wardrobeItem.save()

serializedProduct = mod.SerializedProduct()
serializedProduct.name = 'Poop'
serializedProduct.serial_number = '3938239'
serializedProduct.date_acquired = '2000-01-01'
serializedProduct.cost = 29.29
serializedProduct.status = 'G2G'
serializedProduct.save()

lineItem = mod.LineItem()
lineItem.amount = 5

rentalItem = mod.RentalItem()
rentalItem.date_out = '2010-01-01'
rentalItem.date_in = '2010-01-01'
rentalItem.due_date = '2010-01-01'
rentalItem.discount_percent = 0.10
rentalItem.item = item

# Add a couple of guests
for data in [
    {'first_name':'Joseph', 'last_name':'Townson', 'email':'fake@fake.com', 'phone':'7134088245', 'security_question':'What is your name?', 'security_answer':'Joseph', 'username':'jobro1', },
    {'first_name':'Sarah', 'last_name':'Townson', 'email':'fake@fake.com', 'phone':'7134088245', 'security_question':'What is your name?', 'security_answer':'Joseph', 'username':'sarahbro1', }
]:

    user = mod.User()

    for key in data:

        setattr(user, key, data[key])

    user.set_password('password')

    user.save()

#############################################################################
############################## TRANSACTIONS #################################
#############################################################################

for data in [

    {'customer': user}

]:

    transaction = mod.Transaction()

    for key in data:

        setattr(transaction, key, data[key])

    transaction.save()

################################# RENTAL #####################################

for data in [

    {'date_out':'2000-01-01 00:00:00', 'due_date': '2001-01-01', 'date_in':'2002-01-01 00:00:00', 'item':item, 'transaction':transaction, 'amount':20.00},
    {'date_out':'2014-12-01 00:00:00', 'due_date': '2015-12-01', 'item':item, 'transaction':transaction, 'amount':20.00},
    {'date_out':'2014-01-01 00:00:00', 'due_date': '2015-01-01', 'item':item, 'transaction':transaction, 'amount':20.00}

]:

    rental = mod.RentalItem()

    for key in data:

        setattr(rental, key, data[key])

    rental.save()









