# -*- coding: utf-8 -*-
# Create your views here.
import random

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext

from principal.forms import TituloForm, FiltroForm, PuntuacionForm
from principal.models import Juego, Usuario, Puntuacion
import recommendations
from pattern.web import Twitter

from pattern.vector import KNN, count
from populate import busquedaTitulos


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
            palabraDescripcion = form.cleaned_data.get('palabraDescripcion')
            
            
            if precioMin==None:
                precioMin=0.   
            
            if precioMax==None:
                precioMax=999. 
                
            if float(precioMax) >= float(precioMin):
                
                
                juegos=[]
                for juego in Juego.objects.all():
                    generosJuegoBucle=[]
                    for i in juego.generos.all():
                        
                        generosJuegoBucle.append(i.nombre_genero) #lista de generos del juego en el bucle
                    
                    if set(generosForm)<set(generosJuegoBucle):
                        
                        juegos.append(juego)
                 
                juegosFiltrados=[]
                
                if palabraDescripcion=="":

                
                    for juego in juegos:
                        if juego.precio_compra>=precioMin and juego.precio_compra<=precioMax:
                            juegosFiltrados.append(juego)
                else:  
                        
                    for juego in juegos:
                        if juego.precio_compra>=precioMin and juego.precio_compra<=precioMax and (juego.titulo in busquedaTitulos(palabraDescripcion)):
                            juegosFiltrados.append(juego)
                
                
                        
                        
                        
                return render_to_response('listadoJuegos.html', {'juegos':juegosFiltrados})
            
    else:      
        form=FiltroForm()
         
    return render_to_response('filtros.html', {'form':form }, context_instance=RequestContext(request))

def juego(request):
    idJuego=request.GET.get("id")
    juego=Juego.objects.get(id=idJuego)
    juegoRecomendado=0
    
    generos=[]
    for i in juego.generos.all():
        generos.append(i.nombre_genero)
        
        
    try:
        juegoRecomendado=recommendations.juegoSimilar(juego.version)[0]
    except:
        pass
    
    
    

    try:
        resultado=recommendations.juegosRecomendados(request.user.first_name)
        juegosRecomendadosUsuario=[]
        for r in resultado:
            
            j=Juego.objects.filter(version=r[1])
            
            juegosRecomendadosUsuario.append(j[0])
        juegosQueRecomendo=Puntuacion.objects.filter(usuario_id=request.user.id)
        
        juegoUsuario=juegosQueRecomendo[random.randrange(0,len(juegosQueRecomendo)+1)].juego

    except:
        
        juegosRecomendadosUsuario=0
        return render_to_response('juego.html',{"juego":juego , "generos":generos, 
                                            "juegoRecomendado":juegoRecomendado,"login":request.user,
                                            "juegosRecomendadosUsuario":juegosRecomendadosUsuario})

    

    
    
    
        
    
    
    return render_to_response('juego.html',{"juego":juego , "generos":generos, 
                                            "juegoRecomendado":juegoRecomendado,"login":request.user,
                                            "juegosRecomendadosUsuario":juegosRecomendadosUsuario,
                                            "juegoUsuario":juegoUsuario})

def puntua(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PuntuacionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            valorPuntuacion = request.POST.get("valor")
            juego=  Juego.objects.get(id=request.GET.get("id"))
            usuario=Usuario.objects.get(id=request.user.id)
            yaPuntuado=Puntuacion.objects.filter(juego=juego,usuario=usuario)
            if len(yaPuntuado)>0:
                error="Ya has votado este juego, no puedes votar dos veces."
                return render(request, 'puntua.html', {'form': form,"error":error})
            Puntuacion.objects.create(usuario=usuario,juego=juego,valor=valorPuntuacion)
            return HttpResponseRedirect('/juego/?id='+request.GET.get("id"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PuntuacionForm()
        
    return render(request, 'puntua.html', {'form': form})


def obtenerTweets(request):
    twitterEn = Twitter(language='en')
    twitterEs = Twitter(language='es')
    idJuego = request.GET.get("id")
    juego = Juego.objects.get(id=idJuego)
    tweets = []
    for tweet in twitterEs.search(juego.titulo, cached=False):
        tweets.append(tweet.text)
    for tweet in twitterEn.search(juego.titulo, cached=False):
        tweets.append(tweet.text)
    return render(request, 'obtenerTweets.html', {'tweets': tweets})
    




