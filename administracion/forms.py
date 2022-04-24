from django import forms
from .models import Empleado, TipoEmpleado

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
