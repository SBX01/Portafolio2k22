from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account, Roles
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.db import connection
import cx_Oracle

# Create your views here.

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            run = form.cleaned_data['rut_cli']
            first_name = form.cleaned_data['nombre']
            last_name = form.cleaned_data['apellido']
            phone_number = form.cleaned_data['contacto']
            email = form.cleaned_data['usermail']
            rut_emp = form.cleaned_data['rut_empresa']
            giro = form.cleaned_data['giro']
            razon = form.cleaned_data['razon_social']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,role='client', username=username, password=password)
            user.phone_number = phone_number
            user.save()

            pasw = make_password(password)
            #llamar al procedimiento almacenado
            agregar_cliente(run,first_name,last_name,phone_number,1,email,pasw,rut_emp,giro,razon)
        
            #manda link de activacion de cuenta al correo
            current_site = get_current_site(request)
            mail_subject = 'por favor activa tu cuenta de SERVIEXPRESS'
            body = render_to_string('accounts/account_verification_email.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode( force_bytes (user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()
           
            return redirect('/accounts/login/?command=verification&email='+email)

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html',context)

#funcion del procedimiento
def agregar_cliente(run,nombre,apellido,contacto,activo,email,password,rut_empresa,giro,razon):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)

    cursor.callproc('sp_agregar_cliente',[run,nombre,apellido,contacto,activo,email,password,rut_empresa,giro,razon, salida])

    return salida.getvalue()


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
            
                auth.login(request, user)
                messages.success(request, 'has iniciado sesion exitosamente')
                
                if user.role == 'admin':
                    
                    return render(request,'administracion/adminHome.html')
                    
                elif user.role == 'client':
                    
                    return redirect('home')
                
                elif user.role == 'worker':

                    return render(request, 'trabajadores/home.html')
                 

            
        else:
            messages.error(request, 'las credenciales son incorrectas')
            return redirect('login')

            
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):

    auth.logout(request)
    messages.success(request,'has salido de la sesion')

    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta esta activa')
        return redirect('login')
    else:
        messages.error(request,'La activacion es invalida')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')

def mensajes(request,salida):
    if salida == 1:
        messages.success(request, 'Se agregó correctamente.')
    else:
        messages.error(request, 'Houston tenemos problemas.')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = 'Resetear Password'
            body = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),

            })
            to_email = email
            send_email = EmailMessage(mail_subject, body, to=[to_email])
            send_email.send()

            messages.success(request,' Revisa tu correo para resetear tu contrasena')
            return redirect('login')
        else:
            messages.error(request,'Tu cuenta de Usuario no existe en nuestros registros')
            return redirect(request,'register')

    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,' por favor resetea tu contrasena')
        return redirect('resetPassword')
    else:
        messages.error(request, 'El link ha expirado')
        return render('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, ' la contrasena se restablecio correctamente ')
            return redirect('login')
        else:
            messages.error(request, 'Las contrasenas no coinciden')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')
