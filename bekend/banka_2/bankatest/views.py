from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, UserInfo, Worker, Role, Customer, Order, LogisticPoint, ProductList, Product, OrderStep, Vehicle, Warehouse, WarehouseType, VehicleType, Team
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import models
from decimal import Decimal
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, ProductList, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Customer, Product, ProductList, LogisticPoint
from django.shortcuts import get_object_or_404
import uuid

@csrf_exempt
def register_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            mail = data.get('mail')

            if not all([username, password, mail]):  # Check if all required fields are present
                return HttpResponse("Invalid request body")

            if Customer.objects.filter(user_id__username=username).exists():
                return HttpResponse("Username already exists")

            user_info = UserInfo(firstname=data.get('firstname', ''),
                                 lastname=data.get('lastname', ''),
                                 patronymic=data.get('patronymic', ''),
                                 passport=data.get('passport', ''),
                                 mail=mail)
            user_info.save()

            user = User(password=password, info_id=user_info,username=username)
            user.save()

            customer = Customer(user_id=user, bank_card=data.get('bank_card', ''))
            customer.save()

            return HttpResponse("Customer created successfully!")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format")
    return HttpResponse("Invalid request method")

@csrf_exempt
def register_worker(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            mail = data.get('mail')
            role = data.get('role')

            if not all([username, password, mail, role]):  # Check if all required fields are present
                return HttpResponse("Invalid request body")

            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists")

            user_info = UserInfo(firstname=data.get('firstname', ''),
                                 lastname=data.get('lastname', ''),
                                 patronymic=data.get('patronymic', ''),
                                 mail=mail,
                                 passport=data.get('passport', ''))
            user_info.save()

            user = User(password=password, username=username, info_id=user_info)
            user.save()

            try:
                rolee = Role.objects.get(role_name=role)
                worker = Worker(user_id=user, 
                               salary=data.get('salary', 0), 
                               role_id=rolee,
                               work_class=data.get('work_class', ''), 
                               work_experience=data.get('work_experience', 0), 
                               garage=data.get('garage', ''))
                worker.save()
            except Role.DoesNotExist:
                return HttpResponse("Role does not exist")

            return HttpResponse("Worker created successfully!")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON format")
    return HttpResponse("Invalid request method")

@csrf_exempt
def authenticate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            try:
                # Retrieve the user instance from the database
                user = User.objects.get(username=username)
                if user.password == password:
                    #print(password)
                    #print(username)
                    if Customer.objects.filter(user_id=user.user_id).exists():
                            return HttpResponse("Client authenticated successfully!")
                    else:
                        Worker.objects.filter(user_id=user.user_id).exists()
                        return HttpResponse("Worker authenticated successfully!")
                else:
                    return HttpResponse("Invalid username or password")
            except (User.DoesNotExist):
                return HttpResponse("User not found")
        except (json.JSONDecodeError, KeyError):
            return HttpResponse("Invalid request body")
    else:
        return HttpResponse("Invalid request method")
    

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            product_list = data.get('product_list')
            description = data.get('description')
            start_location = data.get('start_location')
            end_location = data.get('end_location')
            num_steps = data.get('num_steps')

            if not all([username, product_list, description, start_location, end_location, num_steps]):
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            try:
                customer = User.objects.get_or_create(username=username)[0]
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=404)

            product_list_data = json.loads(json.dumps(product_list))
            product_list_ids = []
            product_list_num = 0

            product_list = []
            for product_data in product_list_data:
                print(product_data)
                product_name = product_data.get('product_name')
                mass = int(product_data.get('mass'))  # Convert mass to int
                width = int(product_data.get('width'))  # Convert width to int
                length = int(product_data.get('length'))  # Convert length to int
                height = int(product_data.get('height'))  # Convert height to int
                cost = float(product_data.get('cost'))  # Convert cost to float
                description = product_data.get('description')

                if not all([product_name, mass, width, length, height, cost, description]):
                    return JsonResponse({'error': [product_name, mass, width, length, height, cost, description]}, status=400)

                try:
                    product = Product.objects.get_or_create(product_name=product_name, mass=mass, width=width, length=length, height=height, cost=cost, description=description)[0]
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)

                product_list.append(product)
                product_list_num = None
                for product in product_list:
                    print("55", product.product_id)
                    if product_list_num is None:
                        product_list_obj = ProductList.objects.create(product_id=product)
                        product_list_num = product_list_obj.product_list_id
                    else:
                        product_list_obj = ProductList.objects.create(product_id=product ,product_list_num=product_list_num)
                    print("@", product_list_obj.product_list_num)
                    product_list_obj = ProductList.objects.get(product_list_id=product_list_num)
                    ProductList.objects.filter(product_list_id=product_list_num-1).delete()
                    product_list_obj.product_list_num = product_list_obj.product_list_id
                    product_list_obj.save()

            order = Order.objects.create(
                customer_id=customer,
                product_list_num=product_list_num,
                description=description,
                start_location=LogisticPoint.objects.get_or_create(address=start_location)[0],
                end_location=LogisticPoint.objects.get_or_create(address=end_location)[0],
                num_steps=int(num_steps)
            )

            order.save()
            return JsonResponse({'message': 'Order created successfully!'}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('ord_id')

            if not order_id:
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            try:
                order = Order.objects.get(order_id=order_id)
                product_list_num = order.product_list_num
                product_list_entries = ProductList.objects.filter(product_list_num=product_list_num)
                product_info_list = []
                for entry in product_list_entries:
                    product_id = entry.product_id_id
                    product = Product.objects.get(product_id=product_id)
                    product_info = {
                        "product_name": product.product_name,
                        "mass": product.mass,
                        "width": product.width,
                        "length": product.length,
                        "height": product.height,
                        "cost": product.cost,
                        "description": product.description
                    }
                    product_info_list.append(product_info)

                order_data = {
                    "username": order.customer_id.username,
                    "product_list": product_info_list,
                    "description": order.description,
                    "start_location": order.start_location.address,
                    "end_location": order.end_location.address,
                    "num_steps": order.num_steps
                }
                return JsonResponse(order_data, status=200)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': 'Invalid request body'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def get_orders(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            orders = Order.objects.filter(customer_id__user_id=user_id).values('order_id')

            order_ids = [order['order_id'] for order in orders]

            return JsonResponse({'order_ids': order_ids}, status=200)

        except Customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def create_team_and_vehicle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_ids = data.get('user_id').split(",") if data.get('user_id') else []
            vehicle_type_name = data.get('vehicle_type_name')

            if not all([user_ids, vehicle_type_name]):
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            team_num = str(uuid.uuid4())

            # Check if the generated team_num already exists
            while Team.objects.filter(team_num=team_num).exists():
                team_num = str(uuid.uuid4())  # Generate a new team_num

            # Add workers to the team
            for user_id in user_ids:
                try:
                    worker = Worker.objects.get(user_id=user_id)
                    team = Team.objects.create(team_num=team_num, worker_id=worker)
                    team.save()
                except Worker.DoesNotExist:
                    return JsonResponse({'error': f'Worker with id {user_id} not found'}, status=404)
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)

            # Create a record in the vehicle table
            try:
                vehicle_type = VehicleType.objects.get(vehicle_type_name=vehicle_type_name)
                vehicle = Vehicle.objects.create(
                    vehicle_type_id=vehicle_type,
                    team_num=team_num,
                    brand=data.get('brand'),
                    manufacturer=data.get('manufacturer'),
                    state_number=data.get('state_number'),
                    payload_capacity=data.get('payload_capacity'),
                    fuel_consumption=data.get('fuel_consumption'),
                    trailer_length=data.get('trailer_length'),
                    transportation_cost_per_km=data.get('transportation_cost_per_km')
                )
                vehicle.save()
                return JsonResponse({'vehicle_id': vehicle.vehicle_id}, status=201)
            except VehicleType.DoesNotExist:
                return JsonResponse({'error': f'Veicle type {vehicle_type_name} not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def create_team_and_warehouse(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_ids = data.get('user_id').split(",") if data.get('user_id') else []
            warehouse_type_name = data.get('warehouse_type_name')
            print(warehouse_type_name)
            if not all([user_ids, warehouse_type_name]):
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            # Generate a unique team_num
            team_num = str(uuid.uuid4())
            while Team.objects.filter(team_num=team_num).exists():
                team_num = str(uuid.uuid4())  # Generate a new team_num if it already exists

            # Add workers to the team
            for user_id in user_ids:
                try:
                    worker = Worker.objects.get(user_id=user_id)
                    team = Team.objects.create(team_num=team_num, worker_id=worker)
                    team.save()
                except Worker.DoesNotExist:
                    return JsonResponse({'error': f'Worker with id {user_id} not found'}, status=404)
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)

            # Create a record in the Warehouse table
            try:
                warehouse_type = WarehouseType.objects.get(type=warehouse_type_name)
                warehouse = Warehouse.objects.create(warehouse_type_id=warehouse_type, team_num=team_num)
                warehouse.save()
                return JsonResponse({'warehouse_id': warehouse.warehouse_id}, status=201)
            except WarehouseType.DoesNotExist:
                return JsonResponse({'error': f'Warehouse type {warehouse_type_name} not found'}, status=404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt
def get_user_id(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')  # Получение имени пользователя из параметров запроса

        if username:    
            try:
                user = User.objects.get(username=username)  # Поиск пользователя по имени
                return JsonResponse({'user_id': user.user_id})  # Возврат id пользователя в формате JSON
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'Username parameter is required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_order_step(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            step = data.get('step')
            description = data.get('description')
            order_id = data.get('order_id')
            location = data.get('location')
            location_type = data.get('location_type')
            distanse = data.get('distanse')

            if not all([step, description, order_id, location, location_type, distanse]):
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            # Get the order with the specified id
            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order with id {} not found'.format(order_id)}, status=404)

            # Create a new OrderStep record
            order_step = OrderStep.objects.create(step=step, description=description, order_id=order, location=location, location_type=location_type, distanse=distanse)
            order_step.save()

            return JsonResponse({'order_step_id': order_step.order_step_id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_order_step(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            step = data.get('step')

            if not all([order_id, step]):
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            # Get the order with the specified id
            try:
                order = Order.objects.get(order_id=order_id)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Order with id {} not found'.format(order_id)}, status=404)

            # Get the order step with the specified step
            try:
                order_step = OrderStep.objects.get(order_id=order_id, step=step)
            except OrderStep.DoesNotExist:
                return JsonResponse({'error': 'Order step with id {} and step {} not found'.format(order_id, step)}, status=404)

            # Get the location and location type
            if order_step.location_type == 'vh':
                vehicle = Vehicle.objects.get(vehicle_id=order_step.location)
                location = vehicle.vehicle_id
                vehicle_type = VehicleType.objects.get(vehicle_type_id=vehicle.vehicle_type_id.vehicle_type_id)
                location_type = vehicle_type.vehicle_type_name
                team_num = vehicle.team_num
            elif order_step.location_type == 'wh':
                warehouse = Warehouse.objects.get(warehouse_id=order_step.location)
                location = warehouse.warehouse_id
                location_type = WarehouseType.objects.get(warehouse_type_id=warehouse.warehouse_type_id.warehouse_type_id)
                location_type = location_type.type
                team_num = warehouse.team_num
            else:
                return JsonResponse({'error': 'Invalid location type'}, status=400)

            # Return the response
            return JsonResponse({
                'step': order_step.step,
                'description': order_step.description,
                'order_id': order_id,
                'location': location,
                'location_type': location_type,
                #'vehicle': vehicle.vehicle_type_name if vehicle else '',
                'team': team_num,#','.join([str(team.worker_id) for team in Team.objects.filter(vehicle=vehicle)])
                "distanse":order_step.distanse
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt
def get_vehicles(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            worker_id = data.get('worker_id')

            if not worker_id:
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            teams = Team.objects.filter(worker_id=worker_id)
            vehicles = []
            for team in teams:
                vehicles.extend(Vehicle.objects.filter(team_num=team.team_num))

            vehicle_ids = [vehicle.vehicle_id for vehicle in vehicles]

            return JsonResponse({'vehicle_ids': vehicle_ids}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def get_worker_teams(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            worker_id = data.get('worker_id')

            if not worker_id:
                return JsonResponse({'error': 'Invalid request body'}, status=400)

            teams = Team.objects.filter(worker_id=worker_id)
            team_info = []

            for team in teams:
                team_workers = Worker.objects.filter(team=team)
                team_info.append({
                    'team_id': team.team_id,
                    #'team_name': team.garage,
                    'worker_ids': [worker.worker_id for worker in team_workers]
                })

            return JsonResponse({'team_info': team_info}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)