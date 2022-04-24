from django import forms
from administracion.models import Cliente


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmar password',
        'class': 'form-control',
    }))
    class Meta:
        model = Cliente
        fields = ['rut_cli','nombre','apellido','contacto','usermail','rut_empresa','giro','razon_social','password']

    def __init__(self, *args, **kwargs ):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['rut_cli'].widget.attrs['placeholder'] = '123456789-0'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['apellido'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['contacto'].widget.attrs['placeholder'] = 'Ingrese Telefono'
        self.fields['contacto'].required = False
        self.fields['usermail'].widget.attrs['placeholder'] = 'Ingrese email'
        self.fields['rut_empresa'].widget.attrs['placeholder'] = 'Ingrese rut de la empresa'
        self.fields['rut_empresa'].required = False
        self.fields['giro'].widget.attrs['placeholder'] = 'Ingrese giro'
        self.fields['giro'].required = False
        self.fields['razon_social'].widget.attrs['placeholder'] = 'Ingrese razon social'
        self.fields['razon_social'].required = False
        
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Las contrase;as no coinciden"
            )
