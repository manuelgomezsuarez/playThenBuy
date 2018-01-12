import random
import urllib2

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.management import call_command
from django.db.transaction import commit_on_success

from principal.models import Juego, Genero, Usuario, Puntuacion


path = "data"



#call_command('flush', interactive=False)


@commit_on_success
def populateGenero(generos):
    print("Cargando Generos de juegos...")
    while Genero.objects.count():
        ids = Genero.objects.values_list('pk', flat=True)[:100]
        Genero.objects.filter(pk__in = ids).delete()
            
    
    for i in generos:
        print i
        Genero.objects.create(nombre_genero=i)

    
    print("Generos insertados: " + str(Genero.objects.count()))
    print("---------------------------------------------------------")
    

@commit_on_success
def populateJuegos():
    print("Cargando Juegos...")
    while Juego.objects.count():
        ids = Juego.objects.values_list('pk', flat=True)[:100]
        Juego.objects.filter(pk__in = ids).delete()
       
 
    arrayMaestro= obtenDatosDePagina()
    
    populateGenero(arrayMaestro[1])
    
    for data in arrayMaestro[0]:
        try:
            print(data)
            titulo = data[0].decode('unicode-escape')
            desarrolladora = data[1].decode('unicode-escape')
            editor = data[2].decode('unicode-escape')
            fecha_lanzamiento=data[3][-4:].decode('unicode-escape')
            tamano=data[4]
            enlace_Torrent=data[5].decode('unicode-escape')
            enlace_compra=data[6].decode('unicode-escape')
            precio_compra=data[7]
            enlace_gameplay=data[8].decode('unicode-escape')
            info_juego=data[9].decode('unicode-escape')
            generosJuego=data[10]
            version=data[11]
            imagen_gameplay=data[12]
            juegoInstancia=Juego.objects.create(titulo=titulo, desarrolladora=desarrolladora,editor=editor,fecha_lanzamiento=fecha_lanzamiento,tamano=tamano,enlace_Torrent=enlace_Torrent,enlace_compra=enlace_compra,precio_compra=precio_compra,enlace_gameplay=enlace_gameplay,info_juego=info_juego,version=version,imagen_gameplay=imagen_gameplay)   
            
            for a in generosJuego: 
                try:
                    generoJuego = Genero.objects.get(nombre_genero=a)
                    juegoInstancia.generos.add(generoJuego)
                except Genero.DoesNotExist:
                    generoJuego = None   
        except:
            pass
    print("Juegos insertados: " + str(Juego.objects.count()))
    print("---------------------------------------------------------")  
     
  

    
def obtenDatosDePagina():
    generos=[]
    arrayMaestro=[]
    cont=0
    for n in range(1,2):
        enlace="https://www.skidrowreloaded.com/pc/?lcp_page1="+str(n)
        datosPagina = urllib2.urlopen(enlace).read()
        soup = BeautifulSoup(datosPagina, 'html.parser')
        listaJuegos=soup.find_all("ul",attrs={"class":"lcp_catlist"})
        for juego in listaJuegos[0].find_all("a"):
            try:
                arrayEsclavo=[0,0,0,0,0,0,0,0,0,0,0,0,0]
                
                enlaceJuego=(juego.get("href"))
                tituloJuego=(juego.get("title")).encode("utf-8")
                datosJuego=urllib2.urlopen(enlaceJuego).read()
                soup2 = BeautifulSoup(datosJuego, 'html.parser')
                infoJuego=soup2.find("div",attrs={"class":"wordpress-post-tabs"})
                infoJuego2=infoJuego.find_all("p")
                informacionJuego=infoJuego2[0].text.encode("utf-8")
                print informacionJuego
                datosJuego=infoJuego2[1].text.split("\n")
                titulo=tituloJuego.replace("'","")
                genero="No Encontrado"
                desarrolladora="No Encontrado"
                editor="No Encontrado"
                fecha_salida=None
                for p in datosJuego:
                    ind=p.split(":")
                    if(ind[0]=="Title"):
                        titulo=ind[1][1:].replace("'","").encode("utf-8")
                    elif(ind[0]=="Genre"):
                        genero=ind[1][1:].strip(" ")
                    elif(ind[0]=="Developer"):
                        desarrolladora=ind[1][1:]
                    elif(ind[0]=="Publisher"):
                        editor=ind[1][1:]
                    elif(ind[0]=="Release Date"):
                        fecha_salida=ind[1][1:]
                desarrolladora=desarrolladora.encode("utf-8")
                print(titulo)
                print(genero)
                print(desarrolladora)
                print(editor)
                print(fecha_salida)
                sepGeneros=genero.replace(" ", "").split(",")
                for s in sepGeneros:
                    generos.append(s.replace(" ",""))
                peso =infoJuego2[3].text.split("\n")[1].split(" ")
                if "MB" in peso[2]:
                    pesoConvertido=round(float(peso[1])/1024,2)
                else:
                    pesoConvertido=float(peso[1])
                    
                print pesoConvertido
                
                enlaceAPrecio="https://isthereanydeal.com/search/?q="+titulo.replace(" ","+").encode("utf-8")
                print enlaceAPrecio
                datosPagina2 = urllib2.urlopen(enlaceAPrecio).read()
                soup3 = BeautifulSoup(datosPagina2, 'html.parser')
                precio =soup3.find("div",attrs={"class":"result"})
                precio1= precio.find_all("a")[len(precio.find_all("a"))-1]
                
                precioEnlaceJuego=precio1.get("href")
                precioJuego=float(precio1.span.text.replace(",",".")[:-1])
                
                print precioEnlaceJuego
                print precioJuego
                
                EnlacesDescarga=soup2.findAll("a")
                enlaceTorrent="Subiendo Torrent, intentelo en otro momento"
                for e in EnlacesDescarga:
                    if("zippy" in e.get("href")):
                        enlaceTorrent=e.get("href")
                print(enlaceTorrent)
                
                
                textToSearch = titulo
                query = urllib2.quote(textToSearch)
                url = "https://www.youtube.com/results?search_query=" + query
                
                response = urllib2.urlopen(url)
                html = response.read()
                soup4 = BeautifulSoup(html,'html.parser')
                videos=soup4.findAll(attrs={'class':'yt-uix-tile-link'})
                
                
                enlaceGameplay= 'https://www.youtube.com' + videos[0]["href"]
                enlaceGameplay=enlaceGameplay.replace("watch?v=","embed/")
                
                imagenGameplay= 'http://img.youtube.com' + videos[0]["href"]+'/default.jpg'
                
                imagenGameplay=imagenGameplay.replace("watch?v=","vi/")
                
                
                arrayEsclavo[0]=titulo
                arrayEsclavo[1]=desarrolladora
                arrayEsclavo[2]=editor
                arrayEsclavo[3]=fecha_salida
                arrayEsclavo[4]=pesoConvertido
                arrayEsclavo[5]=enlaceTorrent
                arrayEsclavo[6]=precioEnlaceJuego
                arrayEsclavo[7]=precioJuego
                arrayEsclavo[8]=enlaceGameplay
                arrayEsclavo[9]=informacionJuego
                arrayEsclavo[10]=sepGeneros
                arrayEsclavo[11]=tituloJuego
                arrayEsclavo[12]=imagenGameplay
                arrayMaestro.append(arrayEsclavo)
                cont=cont+1
            except Exception as e:
                print e
                pass
           
            
            print("*************")
            if cont==10:
                print "Se extrajeron "+str(cont)+" juegos"
                return arrayMaestro,set(generos)
            
            
    print "datos extraidos correctamente de la pagina"
    return arrayMaestro,set(generos)
      
def populateUserAccounts():
    print("Cargando Cuentas de Usuario ...")
    while User.objects.count():
        ids = User.objects.values_list('pk', flat=True)[:100]
        User.objects.filter(pk__in = ids).delete()
    
    u1=User.objects.create(username="user1",first_name="Usuario 1",last_name="Usuario 1 apellido",email="user1@gmail.com",password="user1")
    u1.set_password(u1.password)
    u1.save()
    u2=User.objects.create(username="user2",first_name="Usuario 2",last_name="Usuario 2 apellido",email="user2@gmail.com",password="user2")
    u2.set_password(u2.password)
    u2.save()
    u3=User.objects.create(username="user3",first_name="Usuario 3",last_name="Usuario 3 apellido",email="user3@gmail.com",password="user3")
    u3.set_password(u3.password)
    u3.save()
    u4=User.objects.create(username="user4",first_name="Usuario 4",last_name="Usuario 4 apellido",email="user4@gmail.com",password="user4")
    u4.set_password(u4.password)
    u4.save()
    print("Cuentas insertados: " + str(User.objects.count()))
    print("---------------------------------------------------------")

          
def populateUsuarios():
    print("Cargando Usuarios ...")
    
    while Usuario.objects.count():
        ids = Usuario.objects.values_list('pk', flat=True)[:100]
        Usuario.objects.filter(pk__in = ids).delete()
    for n in User.objects.all():
        Usuario.objects.create(useraccount=n)
        
    print("Usuarios insertados: " + str(Usuario.objects.count()))
    print("---------------------------------------------------------")
    

def populatePuntuaciones():
    usuarios=[]
    for n in range(1,5):
        usuarios.append(Usuario.objects.get(id=n))
    for u in usuarios:
        for n in range(1,8):
            puntuacionRandom=random.randrange(1,5)
            juegoRandom=random.randrange(1,10)
            juego=Juego.objects.get(id=juegoRandom)
            Puntuacion.objects.create(usuario=u,juego=juego,valor=puntuacionRandom)
    print("Puntuaciones insertadas: " + str(Puntuacion.objects.count()))
    print("---------------------------------------------------------")
    
    

def populateDatabase():
    populateJuegos()
    populateUserAccounts()
    populateUsuarios()
    populatePuntuaciones()



    print("Terminada database population")





if __name__ == '__main__':
    populateDatabase()
