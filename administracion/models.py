# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsAccount(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(unique=True, max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateTimeField()
    last_joined = models.DateTimeField()
    is_admin = models.BooleanField()
    is_staff = models.BooleanField(blank=True, null=True)
    is_active = models.BooleanField()
    is_superadmin = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'accounts_account'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Cliente(models.Model):
    rut_cli = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    contacto = models.IntegerField(blank=True, null=True)
    activo = models.FloatField()
    usermail = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    rut_empresa = models.CharField(max_length=10, blank=True, null=True)
    giro = models.CharField(max_length=50, blank=True, null=True)
    razon_social = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'

    def __str__(self):
        return str(self.rut_cli)


class Cotizacion(models.Model):
    numero_folio = models.IntegerField(primary_key=True)
    comentario = models.CharField(max_length=300)
    reserva = models.ForeignKey('Reserva', models.DO_NOTHING)
    id_sevicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='id_sevicio')
    valor = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cotizacion'


class DetalleDocumento(models.Model):
    servicio_id_sevicio = models.OneToOneField('Servicio', models.DO_NOTHING, db_column='servicio_id_sevicio', primary_key=True)
    documento_id_documento = models.ForeignKey('Documento', models.DO_NOTHING, db_column='documento_id_documento')

    class Meta:
        managed = False
        db_table = 'detalle_documento'
        unique_together = (('servicio_id_sevicio', 'documento_id_documento'),)


class DetalleServicio(models.Model):
    id_detalle_servicio = models.IntegerField()
    cantidad = models.IntegerField()
    servicio_id_sevicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='servicio_id_sevicio')
    producto_sku = models.OneToOneField('Producto', models.DO_NOTHING, db_column='producto_sku', primary_key=True)

    class Meta:
        managed = False
        db_table = 'detalle_servicio'
        unique_together = (('producto_sku', 'servicio_id_sevicio', 'id_detalle_servicio'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsAccount, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Documento(models.Model):
    id_documento = models.IntegerField(primary_key=True)
    folio = models.IntegerField()
    fecha_emision = models.DateField()
    total = models.IntegerField()
    nulo = models.FloatField()
    id_tipo_doc = models.ForeignKey('TipoDocumento', models.DO_NOTHING, db_column='id_tipo_doc')
    rut_emp = models.ForeignKey('Empleado', models.DO_NOTHING, db_column='rut_emp')
    rut_cli = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cli')
    id_pago = models.ForeignKey('MedioPago', models.DO_NOTHING, db_column='id_pago')
    descuento = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documento'


class Empleado(models.Model):
    rut_emp = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=50)
    telefono = models.IntegerField()
    activo = models.BooleanField()
    id_tipo_emp = models.ForeignKey('TipoEmpleado',on_delete=models.RESTRICT, db_column='id_tipo_emp')
    usermail = models.CharField(max_length=100)
    password = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'empleado'
    
    def __str__(self):
        return str(self.nombre)


class GrupoProducto(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=25)
    tipo_producto = models.ForeignKey('TipoProducto', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'grupo_producto'

    def __str__(self):
        return self.nombre


class MedioPago(models.Model):
    id_pago = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    enuso = models.FloatField()

    class Meta:
        managed = False
        db_table = 'medio_pago'


class OrdenProducto(models.Model):
    sku_fk = models.OneToOneField('Producto', models.DO_NOTHING, db_column='sku_fk', primary_key=True)
    folio_pedido_fk = models.ForeignKey('OrdenPedidoProducto', models.DO_NOTHING, db_column='folio_pedido_fk')

    class Meta:
        managed = False
        db_table = 'orden-producto'
        unique_together = (('sku_fk', 'folio_pedido_fk'),)


class OrdenPedidoProducto(models.Model):
    folio_pedido = models.IntegerField(primary_key=True)
    cantidad = models.IntegerField()
    fecha_emision = models.DateField()
    recibido = models.FloatField()
    fecha_recepcion = models.DateField(blank=True, null=True)
    rut_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='rut_proveedor')

    class Meta:
        managed = False
        db_table = 'orden_pedido_producto'


class Producto(models.Model):
    sku = models.IntegerField(primary_key=True)
    nombre_corto = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=200)
    precio_compra = models.IntegerField()
    precio_venta = models.IntegerField()
    stock = models.IntegerField()
    stock_critico = models.IntegerField()
    enuso = models.FloatField()
    id_categoria = models.ForeignKey(GrupoProducto, models.DO_NOTHING, db_column='id_categoria')
    fecha_vencimiento = models.DateField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'producto'


class ProvProducto(models.Model):
    rut_proveedor = models.OneToOneField('Proveedor', models.DO_NOTHING, db_column='rut_proveedor', primary_key=True)
    sku = models.ForeignKey(Producto, models.DO_NOTHING, db_column='sku')

    class Meta:
        managed = False
        db_table = 'prov-producto'
        unique_together = (('rut_proveedor', 'sku'),)


class Proveedor(models.Model):
    rut_proveedor = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=100)
    correo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Reserva(models.Model):
    id = models.IntegerField(primary_key=True)
    fecha = models.DateField()
    estado = models.FloatField()
    cliente_rut_cli = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_rut_cli')

    class Meta:
        managed = False
        db_table = 'reserva'


class Servicio(models.Model):
    id_sevicio = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=35)
    precio = models.IntegerField()
    enuso = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'servicio'


class TipoDocumento(models.Model):
    id_tipo_doc = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'tipo_documento'


class TipoEmpleado(models.Model):
    id_tipo_emp = models.IntegerField(primary_key=True)
    seccion = models.CharField(max_length=35)

    class Meta:
        managed = False
        db_table = 'tipo_empleado'

    def __str__(self):
        return str(self.seccion)


class TipoProducto(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_producto'

    def __str__(self):
        return str(self.nombre)


class Vehiculo(models.Model):
    pantente = models.CharField(primary_key=True, max_length=6)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    anio = models.IntegerField()
    activo = models.BooleanField()
    cliente_rut_cli = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='rut_cli')

    class Meta:
        managed = False
        db_table = 'vehiculo'
