from django.urls import path
from .import views

urlpatterns = [
    path('', views.workerHome, name='trabajadores'),
    path('reservas/', views.listaReservas, name='lista_reserva'),
    path('pedidos/', views.RealizarPedido, name='pedidos'),
    path('orden-pedido/<str:sku>', views.OrdenPedido, name='orden-pedido'),
    path('recepcion/', views.RecepcionPedido, name='recepcion'),
    path('detalle_pedido/', views.DetallePedido, name='detalle_pedido'),
    path('cotizar_servicio/', views.cotizar_servicio, name='cotizar_servicio'),
    path('add_cotizacion/', views.add_cotizacion, name='add_cotizacion'),
    path('ventas/<int:tipodoc>', views.crearVenta, name='documento_venta'),
    
]