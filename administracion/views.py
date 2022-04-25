import imp
from sqlite3 import Cursor
import django
from django.shortcuts import redirect, render
from accounts.models import Roles, Account
from .forms import RegistroServicio, TipoEmp, RegistroEmp
from django.db import connection
from django.contrib.auth.hashers import make_password
import cx_Oracle
from django.contrib import messages

# Create your views here.

def is_admin(request):
    #validacion verga xd
    if request.user.role == 'admin':
        return True
    
def adminHome(request):

    if is_admin(request) == True:
        #la vista
        
        return render(request,'administracion/adminHome.html')

    return redirect('home')


def registrar_servicio(request):
    
    if is_admin(request) == True:
        form = RegistroServicio()
        try:
            if request.method == 'POST':
                form = RegistroServicio(request.POST)
                if form.is_valid():
                    
                    nombre = form.cleaned_data['nombre']
                    precio = form.cleaned_data['precio']
                    

                    salida = add_servicio(nombre,precio)
                    mensajes(request,salida)
        except:
             messages.error(request, 'Houston tenemos problemas.')

        data ={
            'formulario': form,       
        }

        return render(request,'administracion/registro_servicio.html', data)
    return redirect('home')

def tipo_empleado(request):
    if is_admin(request) == True:
        form = TipoEmp()
        if request.method == 'POST':
            form = TipoEmp(request.POST)

            if form.is_valid():
                seccion = form.cleaned_data['seccion']

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
            'form_emp' : form_emp
        }
        return render(request, 'administracion/registro_empleado.html', context)
    
    return redirect('home')
    
def mensajes(request,salida):
    if salida == 1:
        messages.success(request, 'Se agregó correctamente.')
    else:
        messages.error(request, 'Houston tenemos problemas.')


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