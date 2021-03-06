from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
#dicc tipo de usuario
Roles = (
    ('admin', 'ADMINISTRADOR'),
    ('client', 'CLIENTE'),
    ('worker', 'TRABAJADOR'),
    ('suplier', 'PROVEEDOR'),
)

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name,role , username, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un email')

        if not username:
            raise ValueError('El usuario debe tener username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            role = role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    #prueba
    def create_employee(self, first_name, last_name, username,phone_number, email, role, password=None ):
        if not email:
            raise ValueError('El usuario debe tener un email')

        if not username:
            raise ValueError('El usuario debe tener username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            is_active = True,
            role = role,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user   


    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            role = 'admin'
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique= True)
    email = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=Roles, default='client')
    
 
    #campos django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    #login con el mail
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    #admin
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
