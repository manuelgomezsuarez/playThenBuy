from django import forms
from principal.models import Genero
from django.core.validators import MinValueValidator,MaxValueValidator

class TituloForm(forms.Form):
    titulo = forms.CharField(label='Titulo del juego')

class PuntuacionForm(forms.Form):
    valor = forms.IntegerField(label='valor',required=False,validators=[MinValueValidator(1),MaxValueValidator(5)])

class FiltroForm(forms.Form):
    precioMin= forms.FloatField(label='Precio Minimo',required=False,validators=[MinValueValidator(0)])
    precioMax= forms.FloatField(label='Precio Maximo',required=False,validators=[MinValueValidator(0)])
    generos=Genero.objects.all()
    opciones=[]
    for i in generos:
        opciones.append([i,i])
    Generos = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=opciones,required=False)
    
    
    

    


    
    

    

