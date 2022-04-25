from xml.dom import ValidationErr
from django import forms
from .models import Empleado, Proveedor, Servicio, TipoEmpleado

class TipoEmp(forms.ModelForm):
    class Meta:
        model = TipoEmpleado
        fields = ['seccion']

    def __init__(self, *args, **kwargs ):
        super(TipoEmp, self).__init__(*args, **kwargs)
        self.fields['seccion'].widget.attrs['placeholder'] = 'Bodega'


        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(TipoEmp, self).clean()

class RegistroEmp(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar password',
        'class': 'form-control',
    }))
    class Meta:
        model = Empleado
        fields = ['rut_emp','nombre','apellidos','telefono','usermail','password']

    def __init__(self, *args, **kwargs ):
        super(RegistroEmp, self).__init__(*args, **kwargs)
        self.fields['rut_emp'].widget.attrs['placeholder'] = '123456789-0'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['apellidos'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['telefono'].widget.attrs['placeholder'] = '999 999 999'
        self.fields['usermail'].widget.attrs['placeholder'] = 'Example@example.com'
        self.fields['rut_emp'].widget.attrs['onInput'] = 'checkRut(this)'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistroEmp, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Las contrase;as no coinciden"
            )

class RegistroServicio(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre','precio']

    def __init__(self, *args, **kwargs ):
        super(RegistroServicio, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Revisión'
        self.fields['precio'].widget.attrs['placeholder'] = '$50.000'
        


        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistroServicio, self).clean()

class RegistroProveedor(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rut_proveedor','nombre','correo']

    def __init__(self, *args, **kwargs ):
        super(RegistroProveedor, self).__init__(*args, **kwargs)
        self.fields['rut_proveedor'].widget.attrs['placeholder'] = '11111111-1'
        self.fields['nombre'].widget.attrs['placeholder'] = 'José'
        self.fields['correo'].widget.attrs['placeholder'] = 'Jose@pernos.cl'
        self.fields['rut_proveedor'].widget.attrs['onInput'] = 'checkRut(this)'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistroProveedor, self).clean()