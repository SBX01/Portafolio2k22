from django.contrib import admin

from .models import Empleado,Cliente,Proveedor,Servicio,Producto,TipoProducto,GrupoProducto,MedioPago,TipoDocumento,TipoEmpleado

# Register your models here.
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Servicio)
admin.site.register(Producto)
admin.site.register(TipoProducto)
admin.site.register(GrupoProducto)
admin.site.register(MedioPago)
admin.site.register(TipoDocumento)
admin.site.register(TipoEmpleado)



