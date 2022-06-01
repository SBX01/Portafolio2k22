
from tkinter import Widget
from django import forms
from administracion.models import Reserva, Vehiculo
import datetime


HORAS_ATENCION = (
    ('10:00:00','10:00 AM'),
    ('11:00:00','11:00 AM'),
    ('12:00:00','12:00 PM'),
    ('13:00:00','1:00 PM'),
    ('14:00:00','2:00 PM'),
    ('15:00:00','3:00 PM'),
    ('16:00:00','4:00 PM'),
    ('17:00:00','5:00 PM'),
    ('18:00:00','6:00 PM'),
    ('19:00:00','7:00 PM'),

)

class DateTimeInput(forms.DateTimeInput):
    input_type = 'date' #'datetime-local' para fecha y hora

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

class RegistroReserva(forms.ModelForm):

    date_now = datetime.date.today() + datetime.timedelta(days=1)
    years_to_add = date_now.year + 1


    fechaDeHoy = date_now.strftime('%Y-%m-%d')
    date_max = date_now.replace(year=years_to_add).strftime('%Y-%m-%d')
    fecha = forms.DateField(widget=DateTimeInput(attrs={'min':fechaDeHoy,'max':date_max,'onclick':'weekends()'}), required=True )

    hora = forms.ChoiceField(choices = HORAS_ATENCION)
 
    class Meta:
        model = Reserva
        fields =['comentario']

    def __init__(self, *args, **kwargs ):
        super(RegistroReserva, self).__init__(*args, **kwargs)
        self.fields['comentario'].widget.attrs['placeholder'] = 'auto no enciende'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


    def clean(self):
        cleaned_data = super(RegistroReserva, self).clean()


