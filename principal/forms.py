
from django import forms

class TituloForm(forms.Form):
    titulo = forms.CharField(label='Titulo juego')