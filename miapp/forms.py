from django import forms
from datetime import time

from .models import Paciente
from .models import Expediente


class PacienteForm(forms.ModelForm):

    class Meta:

        model = Paciente

        fields = [

            'nombre',

            'cedula',

            'telefono',

            'correo'

        ]


class ExpedienteForm(forms.ModelForm):

    class Meta:

        model = Expediente

        fields = [

            'fecha',

            'hora',

            'tratamiento',

            'notas',

            'codigo_cie',

            'diagnostico',

            'nota_adicional'

        ]

        widgets = {

            'fecha': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'hora': forms.TimeInput(

            attrs={

                'type': 'time',

                'min': '07:00',

                'max': '17:00',

                'step': '3600'

            }

        ),

            'tratamiento': forms.Textarea(
                attrs={
                    'rows': 3
                }
            ),

            'notas': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),

            'nota_adicional': forms.Textarea(
                attrs={
                    'rows': 3
                }
            )

        }

    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        if hora is None:
            return hora
        if hora < time(7, 0) or hora > time(17, 0):
            raise forms.ValidationError('La hora debe estar entre 07:00 y 17:00')
        return hora