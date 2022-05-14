from ast import Pass
from cmath import e
from genericpath import exists
import imp
from pickle import TRUE
from sqlite3 import Cursor
import django
from django.shortcuts import redirect, render
from .models import Empleado, Servicio, TipoEmpleado
from accounts.models import Roles, Account
from .forms import RegistroServicio, TipoEmp, RegistroEmp ,RegistroProveedor
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle
from django.contrib import messages

# Create your views here.

def is_admin(request):
    #validacion verga xd
    if request.user.role == 'admin':
        return True
def hardAdmin(request):
    if is_admin(request) == True:
        return render (request,'admin')
    return redirect('home')

def adminHome(request):

    if is_admin(request) == True:
        #la vista
        
        return render(request,'administracion/adminHome.html')

    return redirect('home')


def registrar_servicio(request):
    
    if is_admin(request) == True:
        

        form = RegistroServicio()
        if request.method == 'POST':
            form = RegistroServicio(request.POST)
            
            if form.is_valid():
                
                nombre = form.cleaned_data['nombre']
                precio = form.cleaned_data['precio']
                if Servicio.objects.filter(nombre=nombre.lower()).exists():
                    mensajes(request,0)
                else:                       
                    salida = add_servicio(nombre.lower(),precio)
                    mensajes(request,salida)
                    return redirect('registro_servicio')
        data ={
            'formulario': form,   
            'listServicios': Servicio.objects.all().filter(enuso=1)    
        }

        return render(request,'administracion/registro_servicio.html', data)
    return redirect('home')

def eliminarServicio(request,idServ):
    serv = Servicio.objects.get(id_sevicio=idServ)
    serv.enuso = 0
    serv.save()
    return redirect('registro_servicio')

def editarServicio(request,idServ):
    serv = Servicio.objects.get(id_sevicio=idServ)
    if request.method == 'POST':
        form = RegistroServicio(request.POST,instance=serv)
        if form.is_valid():
            if Servicio.objects.filter(nombre=serv.nombre.lower()).exists():
                serv.precio = form.cleaned_data['precio']
                serv.save()
                mensajes(request,1)
            else:                       
                mensajes(request,0)
                return redirect('registro_servicio')
           
            return redirect('registro_servicio')
    else:
        form = RegistroServicio(instance=serv)
    context = {'form' : form,'serv':serv}
    return render(request,'administracion/editar_servicio.html',context)


def tipo_empleado(request):
    if is_admin(request) == True:
        form = TipoEmp()
        if request.method == 'POST':
            form = TipoEmp(request.POST)

            if form.is_valid():
                seccion = form.cleaned_data['seccion']
                if TipoEmpleado.objects.filter(seccion=seccion).exists():
                    mensajes(request,0)
                else:
                    salida = add_tipo_empleado(seccion)
                    mensajes(request,salida)
                    return redirect('registro_empleado')
    
        return render(request, 'administracion/registro_empleado.html')
    return redirect('home')

def registrar_usario(request):
    
    if is_admin(request) == True:

        form = TipoEmp()
        form_emp = RegistroEmp()
        if request.POST:
            form_emp = RegistroEmp(request.POST)
            
            if form_emp.is_valid():
                run = form_emp.cleaned_data['rut_emp']
                nombre = form_emp.cleaned_data['nombre']
                apellido = form_emp.cleaned_data['apellidos']
                telefono = form_emp.cleaned_data['telefono']
                
                email = form_emp.cleaned_data['usermail']
                password = form_emp.cleaned_data['password']
                username = email.split("@")[0]
                rol = request.POST.get('rol','')
                tipo_emp = request.POST.get('tipo_empleado','')
                #rol = 'worker'
                #tipo_emp = '4'
                activo = '1'
                

                pasw = make_password(password)
                
                user = Account.objects.create_employee(first_name=nombre, last_name=apellido,phone_number =telefono, email=email, username=username, password=password, role=rol)
                user.save()
                salida = add_empleado(run,nombre,apellido,telefono,activo,tipo_emp,email,pasw)
                mensajes(request,salida)
                return redirect('registro_empleado')

        context = {
            'rol' : Roles,
            'form' : form,
            'tip_emp' : listar('sp_lista_tipo_empleado'),
            'form_emp' : form_emp,
            'listEmp': Empleado.objects.all().filter(activo=1)
        }
        return render(request, 'administracion/registro_empleado.html', context)
    
    return redirect('home')
    
def mensajes(request,salida):
    if salida == 1:
        messages.success(request, 'Se agregó correctamente.')
    else:
        messages.error(request, 'Houston tenemos problemas.' )

def add_tipo_empleado(seccion):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('SP_TIPO_EMPLEADO',[seccion, salida])

    return salida.getvalue()

def add_servicio(nombre,valor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('SP_AGREGAR_SERVICIO',[nombre,valor,salida])
    return salida.getvalue()

def add_empleado(run,nombre,apellido,telefono,activo,tipo_emp,usermail,pasw):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('SP_AGREGAR_TRABAJADOR',[run,nombre,apellido,telefono,activo,tipo_emp,usermail,pasw, salida])

    return salida.getvalue()

def listar(procedimiento):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc(procedimiento,[out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def registrarProveedor(request):
    if is_admin(request) == True:
        form = RegistroProveedor()
        if request.method == 'POST':
            form = RegistroProveedor(request.POST)

            if form.is_valid():
                rut = form.cleaned_data['rut_proveedor']
                name_prov = form.cleaned_data['nombre']
                correo = form.cleaned_data['correo']

                form.save()
                return redirect('registrarProveedor')
        context = {
            'form' : form,
        }
         
        return render(request, 'administracion/registro_proveedor.html',context)
    return redirect('home')


def eliminarEmp(request,rut_empleado):
    emp = Empleado.objects.get(rut_emp = rut_empleado)
    emp.activo = 0
    emp.save()
    return redirect('registro_empleado')