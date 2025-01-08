# Asset Management System

In this project I aim to build an asset management system for companies to effectively manage their assets like Laptops, etc. which they will assign to their employees

## Architecture and Technologies

This project uses a microservices architecture in which two microservices are present:
- Authentication Microservice: Used for authentication services like signup, login etc.
- Assets Microservice: Used to manage assets like add, delete, assign etc.

This project uses latest technologies like:
- Flask
- SQLAlchemy
- JWT
- Redis Cache

## Project Overview

### Types of Users:
- Admin: Has All types of permissions
- Assets Manager: Can add, update or delete assets
- HR: Can Assign Assets to different employees
- Employee: Can request for assets or to release them

### Databases:
- User Database
- Assets Database

### Working

- The users can register themselves according to their roles and then using those credentials they can Login.
- The Assets Manager will manage the assets so he can add, update or delete any assets. They can also create New Category of Assets.
- The Employees can make a request for any assets they need or they can release any assets they possess.
- The Requests will go to the HR who will then either acccept the request to grant the resources to employees or reject it.
