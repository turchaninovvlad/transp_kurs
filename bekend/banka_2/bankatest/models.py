from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,default="")
    password = models.CharField(max_length=255)
    info_id = models.ForeignKey('UserInfo', on_delete=models.CASCADE)

class UserInfo(models.Model):
    user_info_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50,default="-")
    mail = models.CharField(max_length=255, null=True)
    #username = models.CharField(max_length=50)
    passport = models.CharField(max_length=20)

class Worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    role_id = models.ForeignKey('Role', on_delete=models.CASCADE)
    work_class = models.CharField(max_length=50, default="")  # Классность
    work_experience = models.IntegerField(default=0)  # Стаж работы
    garage = models.CharField(max_length=50, default="")  # Автобаза

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50)


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_card = models.CharField(max_length=255)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product_list_num = models.TextField()
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    start_location = models.ForeignKey('LogisticPoint', related_name='start_location', on_delete=models.CASCADE)
    end_location = models.ForeignKey('LogisticPoint', related_name='end_location', on_delete=models.CASCADE)
    num_steps = models.IntegerField()

class LogisticPoint(models.Model):
    logistic_point_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)
    input = models.BooleanField(default=False)
    output = models.BooleanField(default=False)

class ProductList(models.Model):
    product_list_id = models.AutoField(primary_key=True)
    product_list_num = models.TextField(default="")
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=155, decimal_places=2,default="1")

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField(default="")
    mass = models.DecimalField(max_digits=100, decimal_places=2,default="0")
    width = models.DecimalField(max_digits=100, decimal_places=2,default="0")
    length = models.DecimalField(max_digits=100, decimal_places=2,default="0")
    height = models.DecimalField(max_digits=100, decimal_places=2,default="0")
    cost = models.DecimalField(max_digits=100, decimal_places=2,default="0")
    description = models.TextField()
class OrderStep(models.Model):
    order_step_id = models.AutoField(primary_key=True)
    step = models.CharField(max_length=255)
    description = models.TextField()
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    location = models.TextField(default='0.0')
    location_type = models.TextField(default='0.0')
    distanse = models.IntegerField(default=0)
    
class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_type_id = models.ForeignKey('VehicleType', on_delete=models.CASCADE)
    team_num = models.TextField(default="0")
    brand = models.CharField(default="0",max_length=50)
    manufacturer = models.CharField(max_length=50,default="0")
    state_number = models.TextField(default="0")
    payload_capacity = models.IntegerField(default="0")
    fuel_consumption = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    trailer_length = models.IntegerField(default="0")
    transportation_cost_per_km = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)


class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    team_num = models.TextField(default="NULL")
    warehouse_type_id = models.ForeignKey('WarehouseType', on_delete=models.CASCADE)

class WarehouseType(models.Model):
    warehouse_type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)

class VehicleType(models.Model):
    vehicle_type_id = models.AutoField(primary_key=True)
    vehicle_type_name = models.CharField(max_length=255)

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_num = models.TextField(default="NULL")
    worker_id = models.ForeignKey('Worker', on_delete=models.CASCADE)


