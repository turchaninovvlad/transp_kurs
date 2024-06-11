"""
URL configuration for banka_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bankatest.views import  register_customer,register_worker,authenticate,create_order,get_order,get_orders,create_team_and_vehicle,create_team_and_warehouse,get_user_id,create_order_step,get_order_step,get_vehicles,get_worker_teams
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
   # path('test/', csrf_exempt(test_)),  # Add this decorator
    path('register_customer/', register_customer, name='register_customer'),
    path('register_worker/', register_worker, name='register_worker'),
    path('authenticate/', authenticate, name='authenticate'),
    path('create_order/', create_order, name='create_order'),
    path('get_order/', get_order, name='get_order'),
    path('get_orders/', get_orders, name='get_orders'),
    path('create_team_and_vehicle/', create_team_and_vehicle, name='create_team_and_vehicle'),
    path('create_team_and_warehouse/', create_team_and_warehouse, name='create_team_and_warehouse'),
    path('get_user_id/', get_user_id, name='get_user_id'),
    path('create_order_step/', create_order_step, name='create_order_step'),
    path('get_order_step/', get_order_step, name='get_order_step'),
    path('get_vehicles/', get_vehicles, name='get_vehicles'),
    path('get_worker_teams/', get_worker_teams, name='get_worker_teams'),
]