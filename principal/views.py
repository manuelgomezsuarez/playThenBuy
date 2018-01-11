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

def orderPrecioDesc(request):
    juegos=Juego.objects.order_by("-precio_compra")
    return render_to_response('listadoJuegos.html', {'juegos':juegos})

def orderPrecioAsc(request):
    juegos=Juego.objects.order_by("precio_compra")
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
            
            
            generosForm = form.cleaned_data.get('Generos')
            
            precioMin = form.cleaned_data.get('precioMin')
            precioMax = form.cleaned_data.get('precioMax')
            
            if precioMin==None:
                precioMin=0.   
            
            if precioMax==None:
                precioMax=999. 
                
            print precioMin
            print precioMax
            if float(precioMax) >= float(precioMin):
                
                
                juegos=[]
                for juego in Juego.objects.all():
                    generosJuegoBucle=[]
                    for i in juego.generos.all():
                        
                        generosJuegoBucle.append(i.nombre_genero) #lista de generos del juego en el bucle
                    
                    if set(generosForm)<set(generosJuegoBucle):
                        
                        juegos.append(juego)
                        
                juegosFiltrados=[]
                for juego in juegos:
                    if juego.precio_compra>=precioMin and juego.precio_compra<=precioMax:
                        juegosFiltrados.append(juego)
                        
                return render_to_response('listadoJuegos.html', {'juegos':juegosFiltrados})
            
    else:      
        form=FiltroForm()
         
    return render_to_response('filtros.html', {'form':form }, context_instance=RequestContext(request))
