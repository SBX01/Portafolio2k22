from django.urls import path
from .import views

urlpatterns = [
    path('', views.adminHome, name='Administracion'),
    path('registro_servicio/', views.registrar_servicio, name='registro_servicio'),
    path('registro_empleado/', views.registrar_usario, name='registro_empleado'),
    path('tipo_empleado/', views.tipo_empleado, name='tipo_empleado'),
    path('registro_proveedor/', views.registrarProveedor, name='registro_Proveedor'),
    path('eliminarempleado/<str:rut_empleado>/', views.eliminarEmp, name='eliminarempleado'),
    path('eliminar_servicio/<int:idServ>/', views.eliminarServicio, name='eliminar_servicio'),
]