from xml.dom import ValidationErr

from django import forms

from .models import Empleado, Producto, Proveedor, Servicio, TipoEmpleado

import datetime

#dic
UnidadMedida=(
    ('unidad','c/u'),
    ('centimetro cubico','cc'),
    ('pulgada','in'),
    ('litro','L'),
    ('centimetro','cm')
)



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

class DateInput(forms.DateTimeInput):
    input_type = 'date' #'datetime-local' para fecha y hora

class AddProducto(forms.ModelForm):
    date = forms.DateField(widget=DateInput, required=False)

    medida = forms.ChoiceField(choices=UnidadMedida)

    class Meta:
        model = Producto
        fields = ['nombre_corto','descripcion','precio_compra','precio_venta','stock','stock_critico']

    def __init__(self, *args, **kwargs ):
        super(AddProducto, self).__init__(*args, **kwargs)
        self.fields['nombre_corto'].widget.attrs['placeholder'] = 'Nehumático diagonal 16'
        self.fields['descripcion'].widget.attrs['placeholder'] = 'Nehumático diagonal aro 16'
        self.fields['precio_compra'].widget.attrs['placeholder'] = '125000'
        self.fields['precio_venta'].widget.attrs['placeholder'] = '131990'
        self.fields['stock'].widget.attrs['placeholder'] = '1000'
        self.fields['stock_critico'].widget.attrs['placeholder'] = '75'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(AddProducto, self).clean()

class UpdateEmp(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre','apellidos','telefono']
    def __init__(self, *args, **kwargs ):
        super(UpdateEmp, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['apellidos'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['telefono'].widget.attrs['placeholder'] = '999 999 999'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(UpdateEmp, self).clean()

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
        fields = ['rut_emp','nombre','apellidos','telefono','usermail','password','activo']

    def __init__(self, *args, **kwargs ):
        super(RegistroEmp, self).__init__(*args, **kwargs)
        self.fields['rut_emp'].widget.attrs['placeholder'] = '123456789-0'
        self.fields['nombre'].widget.attrs['placeholder'] = 'Ingrese nombre'
        self.fields['apellidos'].widget.attrs['placeholder'] = 'Ingrese apellidos'
        self.fields['telefono'].widget.attrs['placeholder'] = '999 999 999'
        self.fields['usermail'].widget.attrs['placeholder'] = 'Example@example.com'
        self.fields['activo']
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

class EditarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['precio_compra','precio_venta','stock','stock_critico']

    def __init__(self, *args, **kwargs ):
        super(EditarProducto, self).__init__(*args, **kwargs)
        self.fields['precio_compra'].widget.attrs['placeholder'] = '$10000'
        self.fields['precio_venta'].widget.attrs['placeholder'] = '$12000'
        self.fields['stock'].widget.attrs['placeholder'] = '100'
        self.fields['stock_critico'].widget.attrs['placeholder'] = '25'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(EditarProducto, self).clean()
