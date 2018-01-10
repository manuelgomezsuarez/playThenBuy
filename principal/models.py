from django.db import models
from idlelib.idle_test.mock_idle import Editor
from django.contrib.auth.models import User
# Create your models here.

    
class Genero(models.Model):
    nombre_genero = models.CharField(max_length=20) 
    def __unicode__(self):
        return unicode(self.nombre_genero)
                       
class Juego(models.Model):
    titulo = models.CharField(max_length=100,null=True)
    desarrolladora=models.CharField(max_length=100,null=True)
    editor=models.CharField(max_length=100,null=True)
    fecha_lanzamiento=models.IntegerField(null=True)
    tamano=models.FloatField(null=True)
    enlace_Torrent = models.CharField(max_length=100,null=True)
    enlace_compra=models.CharField(max_length=100,null=True)
    precio_compra=models.FloatField(null=True)
    enlace_gameplay=models.CharField(max_length=100,null=True)
    info_juego=models.CharField(max_length=500,null=True)
    generos = models.ManyToManyField(Genero)
    def __unicode__(self):
        return unicode(self.titulo)
    
class Usuario(models.Model):
    useraccount=models.OneToOneField(User)
    lista_deseados=models.ManyToManyField(Juego)
    def __unicode__(self):
        return unicode(self.useraccount.username)
    
    