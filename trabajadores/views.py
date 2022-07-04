from operator import ge
from sqlite3 import Row
from django.shortcuts import redirect, render
from administracion.models import MedioPago, Reserva,Empleado,Cliente, Producto, OrdenPedidoProducto,Proveedor, OrdenProducto,Documento,TipoDocumento,Servicio
from django.contrib.auth.decorators import login_required
from django.db import connection
from datetime import datetime, timedelta
import cx_Oracle

from django.contrib import messages



# Create your views here.

def workerValid(request):
    if request.user.role == 'worker':
        return True

def workerHome(request):

    if workerValid(request)== True:

        return render(request, 'trabajadores/home.html')

#mover al view de trabajadores
@login_required
def listaReservas(request):
    
    if workerValid(request) ==  True:
        reservas = Reserva.objects.filter(estado=1)

        data = {
            'reserva':reservas,
            'lista': consultasBD.lista_reservas(),
            'esCliente':False
        }
        return render(request,'trabajadores/reservasWork.html',data)

def cotizar_servicio(request):
    
    reserva_id = request.GET.get('id')
    #servicio = Servicio.objects.filter(enuso=1)
    #pago = MedioPago.objects.filter(enuso = 1)

    data ={
        'servicio':consultasBD.lista_servicios(),
        'reserva':Reserva.objects.get(id = reserva_id),
        'productos':consultasBD.lista_productos(),
        'pago': consultasBD.lista_pagos(),
        'documento':consultasBD.lista_documento(),
    }

    return render(request,'trabajadores/cotizacion.html',data)

def add_cotizacion(request):

    rut_cli = request.GET.get('rut')

    if request.method == 'POST':

        comentario = request.POST.get('comentario')
        reserv = request.POST.get('reserva')
        serv = request.POST.get('servicio')
        sku = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))
        doc = request.POST.get('documento')
        pago = request.POST.get('pago')
        mail = request.user.email

        consultasBD.add_cotizacion(comentario,reserv,serv,sku,cantidad,mail,doc,pago)
        data = {
            'lista': consultasBD.lista_reservas(),
            'esCliente':False
        }


        return render(request,'trabajadores/reservasWork.html', data)



def RealizarPedido(request):

    insumos = Producto.objects.filter(enuso=1)
    data = {
        'listaProductos':insumos,
    }
    return render(request,'trabajadores/add_pedido.html',data)


def OrdenPedido(request, sku):
    producto = Producto.objects.get(sku = sku)

    if request.method == 'POST':
        pedido = OrdenPedidoProducto()
        pedido.cantidad = request.POST.get('cantidad')
        fecha = datetime.today()
        pedido.fecha_emision = fecha
        pedido.recibido = 0
        pedido.fecha_recepcion = None
        rut = request.POST.get('rut')
        proveedor = Proveedor.objects.get(rut_proveedor = rut)
        pedido.rut_proveedor = proveedor
        
              
        try:
            pedido.save()
            
            try:
                orden = OrdenProducto()
                orden.sku_fk = Producto.objects.get(sku = sku)
                orden.folio_pedido_fk = OrdenPedidoProducto.objects.get(folio_pedido = pedido.folio_pedido) 
                orden.save()
            except:
                pass

            #PedidoPDF(request)
        except:
            pass

    data ={
        'producto' : producto,
        'prov' : consultasBD.prov_producto(sku),
    }

    return render(request, 'trabajadores/orden_pedido.html', data)


def RecepcionPedido(request):
    

    data = {
        'orden' : consultasBD.pedido_realizado(),
    }

    folio = request.POST.get('folio')

    #buscar el pedido
    if OrdenPedidoProducto.objects.filter(folio_pedido = folio).exists():
        cantidad = request.POST.get('cantidad')
        sku = request.POST.get('sku')
        consultasBD.update_pedido(folio,cantidad,sku)
        data = {
            'orden' : consultasBD.pedido_realizado(),
        }

        return render(request, 'trabajadores/recepcion_pedido.html', data)
    
    
    
    return render(request, 'trabajadores/recepcion_pedido.html', data)

def DetallePedido(request):
    pedido = request.GET.get('pedido')

    data = {
        'pedido' : consultasBD.detalle_pedido(pedido),
        'orden' : OrdenPedidoProducto.objects.get(folio_pedido = pedido)
    }
    return render(request, 'trabajadores/detalle_pedido.html', data)

def PedidoPDF(request):
    #html que contendra los datos para poder generar el pdf con el formato de orden de pedido
    #pasar datos del orden de producto
    #datos del formulario del pedio del producto

    pass

    #return render(request, 'trabajadores/pedido_producto.html')
   

def GenerarPDF():
    #funcion a ejecutar despues del pedidoPDF
    pass

#agregar funcionalidad para recuperar servicio y guardarlo en una tupla para despues ser enviada a la bd

def crearVenta(request,tipodoc):

    if request.POST:
        tipo =request.POST.get('doc')
        print(tipo)
        total = request.POST.get('total')
        servicioElegido = request.POST.getlist('servicio')
        mailEmp = request.user.email
        clienteSeleccionado = request.POST.get('Rut_cliente')
        descuentos = 0#(request.POST.get('descuento'))
        pago = int(request.POST.get('medioPago'))
        print(pago)
        if not total=='0':
            crear_documento_venta(tipo,mailEmp,clienteSeleccionado,total,pago,descuentos)
            mensajes(request,1)
        else:
            mensajes(request,0,"Calcule el total antes de enviar.")
        for col in servicioElegido: 
            crear_detalle_venta(col)
  

        

    data = {
        'servicios' : Servicio.objects.all().filter(enuso = 1),
        'Clientes' : Cliente.objects.all().filter(activo =1),
        'pago': MedioPago.objects.all().filter(enuso = 1)
    }
    return render(request, 'trabajadores/DocumentoVenta.html', data)

def crear_documento_venta(tipo_doc, mail_emp,rut_cli,total,tipoPago,descuento):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_CREAR_DOCUMENTO',[total,tipo_doc,mail_emp,rut_cli,tipoPago,descuento,salida])

def crear_detalle_venta(servicioSelect):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    cursor.callproc('sp_detalle_documento',[servicioSelect])

def mensajes(request,salida,mensajeEnvio=None):
    if salida == 1:
        if mensajeEnvio is None:

            messages.success(request, 'El proceso se finalizó correctamente.')
        else:
             
            messages.success(request, mensajeEnvio)
    else:
        if mensajeEnvio is None:
            messages.error(request, 'Houston tenemos problemas.' )
        else:
            messages.error(request, mensajeEnvio)
class consultasBD():
    def prov_producto(sku):
        
        with connection.cursor() as cursor:
            cursor.execute('''Select p.rut_proveedor,p.nombre,p.correo
                            from proveedor p join "PROV-PRODUCTO" pp on (p.rut_proveedor = pp.rut_proveedor)
                            where pp.sku = %s''', [sku])
            row = cursor.fetchone()

        return row

    def pedido_realizado():
        with connection.cursor() as cursor:
            cursor.execute('''select op.folio_pedido,op.rut_proveedor,op.cantidad,p.nombre_corto,p.descripcion
                            from orden_pedido_producto op join "ORDEN-PRODUCTO" o on(op.folio_pedido = o.folio_pedido_fk)
                            join producto p on (o.sku_fk = p.sku)
                            where op.recibido = 0''')
            
            row = cursor.fetchall()

        return row

    def detalle_pedido(pedido):
        with connection.cursor() as cursor:
            cursor.execute('''select op.folio_pedido,o.sku_fk,op.rut_proveedor,pv.nombre,op.cantidad,
                            p.nombre_corto||' '||p.descripcion AS nombre_producto,p.precio_compra
                            from orden_pedido_producto op join "ORDEN-PRODUCTO" o on(op.folio_pedido = o.folio_pedido_fk)
                            join producto p on (o.sku_fk = p.sku)
                            join proveedor pv on (op.rut_proveedor = pv.rut_proveedor)
                            where op.folio_pedido = %s;''', [pedido])
            row = cursor.fetchone()
        return row
    
    def update_pedido(folio,cantidad, sku):
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()

        cursor.callproc('sp_actualizar_pedido_producto',[folio,cantidad,sku])

    def lista_reservas():
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()

        cursor.callproc('SP_LISTA_RESERVAS',[out_cur])

        lista = []
        for fila in out_cur:
            lista.append(fila)
        return lista
    
    def lista_servicios():
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()

        cursor.callproc('SP_LISTA_SERVICIOS',[out_cur])

        lista = []
        for fila in out_cur:
            lista.append(fila)
        return lista
    
    def lista_productos():
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()

        cursor.callproc('SP_LISTA_PRODUCTOS',[out_cur])

        lista = []
        for fila in out_cur:
            lista.append(fila)
        return lista
    
    def lista_pagos():
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()

        cursor.callproc('SP_LISTA_PAGOS',[out_cur])

        lista = []
        for fila in out_cur:
            lista.append(fila)
        return lista
        
    
    def lista_documento():
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()

        cursor.callproc('SP_LISTA_DOCUMENTO_TIPO',[out_cur])

        lista = []
        for fila in out_cur:
            lista.append(fila)
        return lista
    
    
    def add_cotizacion(comentario,reserva,servicio,sku,cantidad,mail,tipo_doc,pago):
        
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()

        cursor.callproc('sp_add_cotizacion',[comentario,reserva,servicio,sku,cantidad,mail,tipo_doc,pago])