from django import forms
from principal.models import Genero
from django.core.validators import MinValueValidator,MaxValueValidator

class TituloForm(forms.Form):
    titulo = forms.CharField(label='Titulo juego')
    
class FiltroForm(forms.Form):
    precioMin= forms.FloatField(label='Precio maximo',required=False,validators=[MinValueValidator(0)])
    precioMax= forms.FloatField(label='Precio mimimo',required=False,validators=[MinValueValidator(0)])
    
   
    
    generos=Genero.objects.all()
    
    opciones=[]
    for i in generos:
        opciones.append([i,i])

    Generos = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=opciones,required=False)
    
    
    

    

