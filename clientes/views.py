from django.db import connection
from django.shortcuts import redirect, render
from administracion.views import mensajes
from administracion.models import Cliente, Producto, Reserva, Vehiculo
from django.contrib.auth.decorators import login_required
from .forms import RegistroReserva, RegistroVehiculo
import cx_Oracle
import datetime
from clientes.forms import RegistroVehiculo

# Create your views here.
def clientValid(request):
    if request.user.role == 'client':
        return True

def workerValid(request):
    if request.user.role == 'worker':
        return True
    

def clienteHome(request):
    if clientValid(request) == True:
        
        return render(request,'clientes/clienteHome.html')
    else:
        return render(request,'clientes/workerhome.html')

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
            cli = Cliente.objects.filter(usermail=request.user.email)
            rut_cli = str(cli[0])
            diaReserva = form.cleaned_data['fecha'].strftime('%Y-%m-%d')
            comentario = form.cleaned_data['comentario']
            horaReserva = request.POST.get('hora','')
            print('esta es la fecha: ' + diaReserva)
            print('esta es la hora: ' + horaReserva)
            fechaReservada = diaReserva +' ' + horaReserva+'+00:00'
            print('esta es la fecha de reserva: ' + fechaReservada)
            #formato db: 25/05/22 10:00:00,000000000
            #            25/05/22 11:00:00,000000000
            #cambiar scritps de cracion de tablas (reserva: timespan? comentario)
            if Reserva.objects.filter(fecha = fechaReservada).exists():
                mensajes(request,0,'Hora reservada, por favor escoja otra.')
            else:
                diaReserva = form.cleaned_data['fecha'].strftime('%d-%m-%y')
                fechaSave = diaReserva.replace('-','/') + ' ' + horaReserva
                print(fechaSave)
                print(rut_cli)
                salida = add_reserva(fechaSave,rut_cli,comentario)
                mensajes(request,salida,'Su hora ha sido registrada exitosamente.')
                return redirect('registro_reserva')

    data = {
        'form':form
    }
    return render(request,'clientes/registro_reserva.html',data)

def add_reserva(fecha,rut,comentarios):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_REGISTRAR_RESERVA',[fecha,rut,comentarios,salida])
    return salida.getvalue()

@login_required
def listaReservas(request):
    if clientValid(request) == True:
        cli = Cliente.objects.filter(usermail=request.user.email)
        rut_cli = str(cli[0])
        reservas = Reserva.objects.filter(cliente_rut_cli=rut_cli,estado=1)
        data = {
            'reserva':reservas,
            'esCliente':True
        }
        return render(request,'clientes/reservas.html',data)
    else:
        reservas = Reserva.objects.filter(estado=1)
        data = {
            'reserva':reservas,
            'esCliente':False
        }
        return render(request,'clientes/reservasWork.html',data)

def RealizarPedido(request):

    insumos = Producto.objects.filter(enuso=1)
    data = {
        'listaProductos':insumos,
    }
    return render(request,'clientes/add_pedido.html',data)
