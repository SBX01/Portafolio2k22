from django.db import connection
from django.shortcuts import redirect, render
from administracion.views import mensajes
from administracion.models import Cliente, Vehiculo
from django.contrib.auth.decorators import login_required
from .forms import RegistroVehiculo
import cx_Oracle

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