from django import forms
from django.utils.safestring import SafeString
from principal.models import Genero


class TituloForm(forms.Form):
    titulo = forms.CharField(label='Titulo juego')
    
class FiltroForm(forms.Form):
#     precioMin= forms.FloatField(null=True())(label='precioMin')
#     precioMax= forms.FloatField(null=True())(label='precioMax')
    
    generos=Genero.objects.all()
    
    opciones=[]
    for i in generos:
        opciones.append([i,i])

    countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=opciones)

