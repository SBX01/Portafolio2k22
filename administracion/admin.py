from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Empleado,Cliente,Proveedor,Servicio,Producto,TipoProducto,GrupoProducto,MedioPago,TipoDocumento,TipoEmpleado


admin.site.site_header = "Administración TMSE"

class TipoEmpleadoAdmin(admin.ModelAdmin):
    fields = ['seccion']
    list_display = ('seccion','id_tipo_emp')

class TipoDocumentoAdmin(admin.ModelAdmin):
    fields = ['nombre']
    list_display = ('nombre','id_tipo_doc')

class MedioPagoAdmin(admin.ModelAdmin):
    fields = ['nombre','enuso']
    list_display = ('nombre','id_pago','enuso')

class TipoProductoAdmin(admin.ModelAdmin):
    fields = ['nombre']
    list_display = ('nombre','id')

class GrupoProductoAdmin(admin.ModelAdmin):
    fields = ['nombre','tipo_producto']
    list_display = ('nombre','tipo_producto')


# Register your models here.
admin.site.register(TipoProducto, TipoProductoAdmin)
admin.site.register(GrupoProducto, GrupoProductoAdmin)
admin.site.register(MedioPago, MedioPagoAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(TipoEmpleado, TipoEmpleadoAdmin)
admin.site.unregister(Group)


