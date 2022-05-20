
from django import forms
from administracion.models import Vehiculo


class RegistroVehiculo(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields=['pantente','marca','modelo','anio']

    def __init__(self, *args, **kwargs ):
        super(RegistroVehiculo, self).__init__(*args, **kwargs)
        self.fields['pantente'].widget.attrs['placeholder'] = 'kz-2135'
        self.fields['marca'].widget.attrs['placeholder'] = 'Toyota'
        self.fields['modelo'].widget.attrs['placeholder'] = 'Corolla'
        self.fields['anio'].widget.attrs['placeholder'] = '1997'

        
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        cleaned_data = super(RegistroVehiculo, self).clean()
