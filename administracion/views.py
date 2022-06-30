from ast import Pass
from cmath import e
from genericpath import exists
import imp
from pickle import TRUE
from sqlite3 import Cursor
from time import strftime
import django
from django.shortcuts import redirect, render
from .models import Empleado, GrupoProducto, Producto, Proveedor, Servicio, TipoEmpleado, TipoProducto
from accounts.models import Roles, Account
from .forms import AddProducto, EditarProducto, RegistroServicio, TipoEmp, RegistroEmp ,RegistroProveedor, UpdateEmp
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

def editarEmpleado(request,rut):
    emp = Empleado.objects.get(rut_emp=rut)
    if request.method == 'POST':
        form = UpdateEmp(request.POST,instance=emp)
        if form.is_valid():
            print('formulario valido') 
            if Empleado.objects.filter(rut_emp=emp.rut_emp).exists():
                emp.nombre = form.cleaned_data['nombre']
                emp.apellido = form.cleaned_data['apellidos']
                emp.telefono = form.cleaned_data['telefono']            
                rol = request.POST.get('rol','')
                emp.tipo_emp = request.POST.get('tipo_empleado','')
                emp.save()
                mensajes(request,1)
                print('si pasa')
                return redirect('registro_empleado')
            else:                
                print('no pasa')       
                mensajes(request,0)
                return redirect('editar_empleado')
        else:
            print('formulario  no valido')    
    else:
        print('no pasa a post') 
        form = RegistroEmp(instance=emp)
    context = {
        'form' : form,
        'emp':emp,
        'rol' : Roles,
        'tip_emp' : listar('sp_lista_tipo_empleado'),
        }
    return render(request,'administracion/editar_empleado.html',context)

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
                if rol == 'worker':
                   
                    user = Account.objects.create_employee(first_name=nombre, last_name=apellido,phone_number =telefono, email=email, username=username, password=password, role=rol)
                    user.save()
                    salida = add_empleado(run,nombre,apellido,telefono,activo,tipo_emp,email,pasw)
                    mensajes(request,salida)
                    return redirect('registro_empleado')
                else:
                    mensajes(request,0)
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
                if Proveedor.objects.filter(rut_proveedor=rut).exists():
                    mensajes(request,0)
                else:
                    mensajes(request,1)
                    form.save()
                    return redirect('registro_Proveedor')
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

def addProducto(request):
    if is_admin(request) == True:
        form = AddProducto()
        if request.method == 'POST':
            form = AddProducto(request.POST)
            if form.is_valid():

                nombre = form.cleaned_data['nombre_corto']
                descripcion = form.cleaned_data['descripcion']
                precio_compra = form.cleaned_data['precio_compra']
                precio_venta = form.cleaned_data['precio_venta']
                stock = form.cleaned_data['stock']
                stock_critico = form.cleaned_data['stock_critico']
                fecha = form.cleaned_data['date']
                um = form.cleaned_data['medida']
                enuso = True
                id_grupo = request.POST.get('categorias','')
                rut_prov = request.POST.get('proveedores','')
                tipo = request.POST.get('tipos','')
                id_producto = rut_prov[:3]
                if id_grupo == '':
                    pass
                else: 
                    id_cat = int(id_grupo)
                    if id_cat <= 9:
                        id_grupo = '00' + id_grupo
                        print(id_grupo[:3])
                    elif id_cat >= 10 and  id_cat <= 99:
                        id_grupo = '0'+ id_grupo
                id_producto = id_producto + id_grupo[:3]
                #print('esta es la fecha: '+ fecha.strftime("%m/%d/%Y"))
                if fecha is None:
                    fecha = '00000000'
                else:
                    fecha = fecha.strftime("%m/%d/%Y")
                    fecha = fecha.replace('/','')
                id_producto = id_producto + fecha
                id_producto = id_producto + tipo[:3]
                # 999 tipo de producto
                #se vuelven a cargar las variables
                nombre = form.cleaned_data['nombre_corto']
                descripcion = form.cleaned_data['descripcion']
                precio_compra = form.cleaned_data['precio_compra']
                precio_venta = form.cleaned_data['precio_venta']
                stock = form.cleaned_data['stock']
                stock_critico = form.cleaned_data['stock_critico']
                um = form.cleaned_data['medida']
                enuso = True
                id_grupo = request.POST.get('tipos','')
                rut_prov = request.POST.get('proveedores','')
                tipo = request.POST.get('tipos','')
                rut_prov = rut_prov.replace(' ','')
                fecha = form.cleaned_data['date']
                if fecha is None:
                    fecha = '00000000'
                if Producto.objects.filter(nombre_corto=nombre.lower()).exists():
                    mensajes(request,0)
                else: 
                    resultado = registroProducto(id_producto,nombre,descripcion,precio_compra,precio_venta,stock,stock_critico,id_grupo,um,rut_prov,fecha)
                    mensajes(request,resultado)
                    return redirect('agregar_producto')

        data ={
            'form': form,   
            'categorias': GrupoProducto.objects.all(),
            'supliers': Proveedor.objects.all(),
            'tipos': TipoProducto.objects.all(),
            'productos': Producto.objects.filter(enuso = 1)
        }       
        return render(request,'administracion/agregar_producto.html', data)
    return redirect('home')


def categoria_subCategoria(request):
    cat = request.GET.get('categorias')

    context = {
        'sub_categoria' : GrupoProducto.objects.filter(tipo_producto = cat)
    }

    return render(request,'administracion/sub_categoria.html', context)


def registroProducto(sku,nombre,descripcion,precioC,precioV,stock,stock_cr,categoria,medida,rut_pr,fecha):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    print(sku,nombre,descripcion,precioC,precioV,stock,stock_cr,categoria,fecha,medida,rut_pr)
    cursor.callproc('SP_AGREGAR_PRODUCTO',[sku,nombre,descripcion,precioC,precioV,stock,stock_cr,categoria,fecha,medida,rut_pr, salida])

    return salida.getvalue()

def eliminarProducto(request,idprod):
    pr = Producto.objects.get(sku = idprod)
    pr.enuso = 0
    pr.save()
    return redirect('agregar_producto')

def modificarProducto(request,idpro):
    pr = Producto.objects.get(sku=idpro)
    print(pr)
    if request.method == 'POST':
        form = EditarProducto(request.POST,instance=pr)
        if form.is_valid():

                pr.precio_compra = form.cleaned_data['precio_compra']
                pr.precio_venta = form.cleaned_data['precio_venta']
                pr.stock = form.cleaned_data['stock']
                pr.stock_critico = form.cleaned_data['stock_critico']
                pr.save()
                mensajes(request,1)
                return redirect('agregar_producto')
        else:                       
            mensajes(request,0)

    else:
        form = EditarProducto(instance=pr)
    context = {'form' : form,'producto':pr}
    return render(request,'administracion/editar_producto.html',context)