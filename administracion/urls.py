from django.urls import path
from .import views

urlpatterns = [
    path('', views.adminHome, name='Administracion'),
    path('registro_empleado/', views.registrar_usario, name='registro_empleado'),
    path('tipo_empleado/', views.tipo_empleado, name='tipo_empleado'),
    path('registro_proveedor/', views.registrarProveedor, name='registro_Proveedor'),
    path('eliminarempleado/<str:rut_empleado>/', views.eliminarEmp, name='eliminarempleado'),
    path('registro_servicio/', views.registrar_servicio, name='registro_servicio'),
    path('eliminar_servicio/<int:idServ>/', views.eliminarServicio, name='eliminar_servicio'),
    path('editar_servicio/<int:idServ>/', views.editarServicio, name='editar_servicio'),
    path('editar_empleado/<str:rut>/', views.editarEmpleado, name='editar_empleado'),
    path('eliminar_producto/<str:idprod>/', views.eliminarProducto, name='eliminar_producto'),
    path('modificar_producto/<str:idpro>/', views.modificarProducto, name='modificar_producto'),
    path('registrar_producto/', views.addProducto, name='agregar_producto'),
    path('categoria/', views.categoria_subCategoria, name='sub_categoria'),
]