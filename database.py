from datetime import datetime
from uuid import uuid4
from mongoengine import (
    connect, StringField, DateTimeField, ReferenceField, EmailField,
    BooleanField, Document, FloatField, ListField
)

connect(
    db="assessment2",  # Replace with your database name
    host="localhost",
    port=27017
)

class Roles(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))  # UUID as primary key
    role_name = StringField(required=True)
    status = BooleanField(required=True, default=True)
    meta = {'collection': 'Roles'}

class User(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))  # UUID as primary key
    role_id = ReferenceField(Roles, required=True)
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    time_stamp = DateTimeField(default=datetime.utcnow)
    status = BooleanField(required=True, default=True)
    meta = {'collection': 'User'}


class AuthDetails(Document):
    id = ReferenceField(User, primary_key=True)  # Linked with User's UUID
    password = StringField(required=True)
    verified = BooleanField(default=False)
    status = BooleanField(required=True, default=True)
    meta = {'collection': 'AuthDetails'}


class Products(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))  # UUID as primary key
    product_name = StringField(required=True)
    price = FloatField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    image = StringField(required=True)
    status = BooleanField(required=True, default=True)
    meta = {'collection': 'Products'}


class Orders(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid4()))  # UUID as primary key
    user_id = ReferenceField(User, required=True)
    order_status = StringField(required=True)
    total_price = FloatField()
    products = ListField()
    time_stamp = DateTimeField(default=datetime.utcnow)
    status = BooleanField(required=True, default=True)
    meta = {'collection': 'Orders'}

'''
# #Example of inserting and querying with UUIDs

# role = Roles(role_name="Admin")
# role1 = Roles(role_name="User")
# role2 = Roles(role_name="Guest")
# role.save()
# role1.save()
# role2.save()
# print(f"Inserted Role ID: {role.id}")

# # Querying a role
# role = Roles.objects.get(id="3a066061-3f59-41e5-b834-7271a7c7e50c")
# if role:
#     print(f"Role found: {role.role_name}")
# else:
#     print("Role not found.")

'''

'''
products_list = [
    Products(
    product_name = "Solar Panel 300W Mono",
    price =  249000,
    description = "High-efficiency solar panel suitable for home use and off-grid applications. Perfect for powering small appliances or charging batteries.",
    category = "solar panels",
    image = "https://media.istockphoto.com/id/1290204324/photo/colse-up-solar-panels-on-sunset-3d-illustration.jpg?s=612x612&w=0&k=20&c=mTbT9WcKQs2xPSMwm4JAUQ6sJyD4SuGlt-IelNg1tMs="
    ),
    Products(
    product_name = "Wind Turbine 5kW",
    price = 129999,
    description = "Compact and durable wind turbine for residential and small commercial use. Generates up to 5kW of power in optimal wind conditions.",
    category = "wind turbines",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdZmRlVwuQMRyvF8MVfuSOCv37738FgOSyzA&s"
    ),
    Products(
    product_name = "Solar Panel Kit 100W ",
    price = 139899,
    description = "Complete solar kit that includes a 100W solar panel, charge controller, and all necessary wiring. Perfect for camping and off-grid living.",
    category = "solar panels",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQf9qqxwjiXcO4l5JHsu5nhS5tKe7jQO23jmw&s"
    ),
    Products(
    product_name = "Wind Turbine 10kW",
    price = 2799999,
    description = "Large-scale wind turbine designed for commercial use, generating up to 10kW of power in ideal conditions.",
    category = "wind turbines",
    image = "https://www.ryse.energy/wp-content/uploads/2020/07/IMG_0483-3-scaled.jpg"
    ),
    Products(
    product_name = "Solar Panel 500W High ",
    price = 599999,
    description = "500W high-efficiency solar panel with superior durability and performance in various weather conditions. Ideal for large-scale installations.",
    category = "solar panels",
    image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIb--QcykxbwIOF-qkCCwagUfPFbj95iJxZw&s"
    ),
    Products(
    product_name = "Wind Turbine 3kW",
    price = 899999,
    description = "Reliable wind turbine generating up to 3kW of power, suitable for residential applications or small businesses.",
    category = "wind turbines",
    image = "https://5.imimg.com/data5/BB/XR/OB/GLADMIN-5852969/img-20141118-wa0002-500x500.jpg"
    )
    ]

Products.objects.insert(products_list)
'''