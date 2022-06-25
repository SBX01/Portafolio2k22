from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from administracion.views import mensajes
from administracion.models import Cliente, DetalleServicio, Producto, Reserva, Vehiculo
from django.contrib.auth.decorators import login_required
from .forms import RegistroReserva, RegistroVehiculo
import cx_Oracle
import datetime
from clientes.forms import RegistroVehiculo

from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.
def clientValid(request):
    if request.user.role == 'client':
        return True


def clienteHome(request):
    if clientValid(request) == True:
        
        return render(request,'clientes/clienteHome.html')


@login_required
def registroVehiculo(request):
    form = RegistroVehiculo()
    cli = Cliente.objects.filter(usermail=request.user.email)
    rut_cliente = str(cli[0])
    print(rut_cliente)
    listaAutos = Vehiculo.objects.filter(cliente_rut_cli = rut_cliente,activo=1 )
    if request.method == 'POST':
        form = RegistroVehiculo(request.POST)
        if form.is_valid():
            patente = form.cleaned_data['pantente']
            marca = form.cleaned_data['marca']
            modelo = form.cleaned_data['modelo']
            anio = int(form.cleaned_data['anio'])

            if Vehiculo.objects.filter(pantente = patente).exists():
                mensajes(request,0)
                return redirect ('registro_vehiculo')
            else:
                salida = add_vehiculo(patente,marca,modelo,anio,rut_cliente)
                mensajes(request,salida)
                
                return redirect ('registro_vehiculo')

    data = {
        'form': form,
        'listaVehiculos': listaAutos
        }               
    return render(request,'clientes/registro_vehiculo.html',data)

def add_vehiculo(patente,marca,modelo,anno,rutClient):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_REGISTRO_VEHICULO',[patente,marca,modelo,anno,rutClient,salida])
    return salida.getvalue()

@login_required
def registroReserva(request):
    form = RegistroReserva
    if request.method == 'POST':
        form = RegistroReserva(request.POST)
        if form.is_valid():
            #cli = Cliente.objects.filter(usermail=request.user.email)
            #rut_cli = str(cli[0])
            #print('Rut cliente:' + rut_cli)
            mail = request.user.email
            diaReserva = form.cleaned_data['fecha'].strftime('%Y-%m-%d')
            comentario = form.cleaned_data['comentario']
            horaReserva = request.POST.get('hora','')
            #print('esta es la fecha: ' + diaReserva)
            #print('esta es la hora: ' + horaReserva)
            fechaReservada = diaReserva +' ' + horaReserva+'+00:00'
            #print('esta es la fecha de reserva: ' + fechaReservada)
            #formato db: 25/05/22 10:00:00,000000000
            #            25/05/22 11:00:00,000000000
            #cambiar scritps de cracion de tablas (reserva: timespan? comentario)
            if Reserva.objects.filter(fecha = diaReserva).exists():
                mensajes(request,0,'Hora reservada, por favor escoja otra.')
            else:
                diaReserva = form.cleaned_data['fecha'].strftime('%d-%m-%y')
                fechaSave = diaReserva.replace('-','/') + ' ' + horaReserva
                #print(fechaSave)
                #print(rut_cli)
                salida = add_reserva(fechaSave,mail,comentario)
                mensajes(request,salida,'Su hora ha sido registrada exitosamente.')
                return redirect('registro_reserva')

    data = {
        'form':form
    }
    return render(request,'clientes/registro_reserva.html',data)

def add_reserva(fecha,mail,comentarios):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_REGISTRAR_RESERVA',[fecha,mail,comentarios,salida])
    return salida.getvalue()
    
def listaServicio(request):

    data = {
        'servicio': lista_servicios_realizados(request.user.email)
    }
    
    return render(request, 'clientes/lista_servicio.html', data)

def documento_servicio(request,detalle):
    user = request.user
    mail = request.user.email
    try:
        template = get_template('clientes/documento.html')
        context = {
            'factura':documento(detalle)
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response)

        return response
    except:
        pass
    return redirect('documento_servicio')

def lista_servicios_realizados(mail):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTA_SERVICIOS_REALIZADOS',[out_cur,mail])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def documento(id_detalle):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTA_DOCUMENTO',[out_cur, id_detalle])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista
