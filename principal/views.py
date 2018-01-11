# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from principal.models import Juego
from principal.forms import TituloForm,FiltroForm

def index(request): 
    return render_to_response('index.html')

def listadoJuegos(request):
    juegos=Juego.objects.all()
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderLanzamientoDesc(request):
    juegos=Juego.objects.order_by("-fecha_lanzamiento")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderLanzamientoAsc(request):
    juegos=Juego.objects.order_by("fecha_lanzamiento")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderTituloAsc(request):
    juegos=Juego.objects.order_by("titulo")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderTituloDesc(request):
    juegos=Juego.objects.order_by("-titulo")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderPesoAsc(request):
    juegos=Juego.objects.order_by("tamano")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderPesoDesc(request):
    juegos=Juego.objects.order_by("-tamano")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderDesarrolladoraAsc(request):
    juegos=Juego.objects.order_by("desarrolladora")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderDesarrolladoraDesc(request):
    juegos=Juego.objects.order_by("-desarrolladora")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def buscarTitulo(request):
    if request.method=='GET':
        form = TituloForm(request.GET, request.FILES)
        
        if form.is_valid():
            tituloJuego = form.cleaned_data['titulo']
            print tituloJuego
            juegos= Juego.objects.filter(titulo__icontains = tituloJuego)
    
            return render_to_response('listadoJuegos.html', {'juegos':juegos})
    else:
        form=TituloForm()
    return render_to_response('buscarTitulo.html', {'form':form }, context_instance=RequestContext(request))



def filtros(request):
    if request.method=='POST':
        form = FiltroForm(request.POST)
        if form.is_valid():
            countries = form.cleaned_data.get('countries')
            print countries
            
            juegos=[]
            for juego in Juego.objects.all():
                generosJuegoBucle=[]
                for i in juego.generos.all():
                    
                    generosJuegoBucle.append(i.nombre_genero) #lista de generos del juego en el bucle
                
                if set(countries)<set(generosJuegoBucle):
                    print generosJuegoBucle
                    juegos.append(juego)
                    
            return render_to_response('listadoJuegos.html', {'juegos':juegos})
    else:      
        form=FiltroForm()
         
    return render_to_response('filtros.html', {'form':form }, context_instance=RequestContext(request))
