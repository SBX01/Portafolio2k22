from django.urls import path
from .import views

urlpatterns = [
    path('', views.clienteHome, name='clientes'),
    path('registro_vehiculo/', views.registroVehiculo, name='registro_vehiculo'),
    path('reserva/', views.registroReserva, name='registro_reserva'),
    path('reservas/', views.listaReservas, name='lista_reserva'),
    path('pedidos/', views.RealizarPedido, name='pedidos'),
    path('eliminar_reserva/<int:idReserva>/', views.cancelarReserva, name='eliminar_reserva'),
    path('modificar_reserva/<int:idReserva>/', views.modificarReserva, name='modificar_reserva'),
]