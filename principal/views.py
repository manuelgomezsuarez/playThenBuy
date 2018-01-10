# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from principal.models import Juego
from principal.forms import TituloForm

def index(request): 
    return render_to_response('index.html')

def listadoJuegos(request):
    juegos=Juego.objects.all()
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def buscarTitulo(request):
    if request.method=='GET':
        form = TituloForm(request.GET, request.FILES)
        if form.is_valid():
            tituloJuego = form.cleaned_data['titulo']
            print tituloJuego
            juegos= Juego.objects.filter(titulo__icontains = tituloJuego)
    
            return render_to_response('titulos.html', {'juegosTitulo':juegos})
    else:
        form=TituloForm()
    return render_to_response('buscarTitulo.html', {'form':form }, context_instance=RequestContext(request))
