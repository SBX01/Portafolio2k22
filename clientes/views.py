from django.db import connection
from django.shortcuts import redirect, render
from administracion.views import mensajes
from administracion.models import Cliente, Reserva, Vehiculo
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
    if clientValid(request) == True:
        form = RegistroVehiculo()
        if request.method == 'POST':
            form = RegistroVehiculo(request.POST)
            if form.is_valid():
                patente = form.cleaned_data['pantente']
                marca = form.cleaned_data['marca']
                modelo = form.cleaned_data['modelo']
                anio = int(form.cleaned_data['anio'])
                cli = Cliente.objects.filter(usermail=request.user.email)
                rut_cli = str(cli[0])
                
                if Vehiculo.objects.filter(pantente = patente).exists():
                    mensajes(request,0)
                    return redirect ('registro_vehiculo')
                else:
                    salida = add_vehiculo(patente,marca,modelo,anio,rut_cli)
                    mensajes(request,salida)
                   
                    return redirect ('registro_vehiculo')
    data = {'form': form}               
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
            diaReserva = form.cleaned_data['fecha'].strftime('%Y-%m-%d')
            comentarios = form.cleaned_data['comentario']
            horaReserva = request.POST.get('hora','')
            print('esta es la fecha: ' + diaReserva)
            print('esta es la hora: ' + horaReserva)
            fechaReservada = diaReserva +' ' + horaReserva+'+00:00'
            print('esta es la fecha de reserva: ' + fechaReservada)
            prueba = Reserva.objects.filter(fecha = fechaReservada)
            #formato db: 25/05/22 10:00:00,000000000
            #            25/05/22 11:00:00,000000000
            #cambiar scritps de cracion de tablas (reserva: timespan? comentario)
            if Reserva.objects.filter(fecha = fechaReservada).exists():
                mensajes(request,0,'Hora reservada, por favor elija otra.')
            else:
                diaReserva = form.cleaned_data['fecha'].strftime('%d-%m-%y')
                mensajes(request,1,'Su hora ha sido registrada exitosamente.')
                fechaSave = diaReserva.replace('-','/') + ' ' + horaReserva + ',000000000'
                print(fechaSave)

    data = {
        'form':form
    }
    return render(request,'clientes/registro_reserva.html',data)