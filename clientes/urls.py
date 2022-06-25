from django.urls import path
from .import views

urlpatterns = [
    path('', views.clienteHome, name='clientes'),
    path('registro_vehiculo/', views.registroVehiculo, name='registro_vehiculo'),
    path('reserva/', views.registroReserva, name='registro_reserva'),
    path('lista_servicio/', views.listaServicio, name='lista_servicio'),
    path('documento_servicio/<int:detalle>', views.documento_servicio, name='documento_servicio'),

]