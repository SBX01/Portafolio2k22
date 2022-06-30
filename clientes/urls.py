from django.urls import path
from .import views

urlpatterns = [
    path('', views.clienteHome, name='clientes'),
    path('registro_vehiculo/', views.registroVehiculo, name='registro_vehiculo'),
    path('reserva/', views.registroReserva, name='registro_reserva'),
    path('reservas/', views.listaReservas, name='lista_reservas'),
    path('pedidos/', views.RealizarPedido, name='pedidos'),
    path('eliminar_reserva/<int:idReserva>/', views.cancelarReserva, name='eliminar_reserva'),
    path('modificar_reserva/<int:idReserva>/', views.modificarReserva, name='modificar_reserva'),
    path('eliminar_vehiculo/<str:patente>/', views.eliminarVehiculo, name='eliminar_vehiculo'),
    path('modificar_vehiculo/<str:patente>/', views.modificarVehiculo, name='modificar_vehiculo'),
    path('lista_servicio/', views.listaServicio, name='lista_servicio'),
    path('documento_servicio/<int:detalle>', views.documento_servicio, name='documento_servicio'),
]