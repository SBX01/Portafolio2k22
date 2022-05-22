from django.urls import path
from .import views

urlpatterns = [
    path('', views.clienteHome, name='clientes'),
    path('registro_vehiculo/', views.registroVehiculo, name='registro_vehiculo'),
    path('reserva/', views.registroReserva, name='registro_reserva'),
]