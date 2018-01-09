from django.db import models
from idlelib.idle_test.mock_idle import Editor

# Create your models here.
class Juego(models.Model):
    titulo = models.CharField(max_length=100,null=True)
    desarrolladora=models.CharField(max_length=100,null=True)
    Editor=models.CharField(max_length=100,null=True)
    fecha_lanzamiento=models.CharField(max_length=100,null=True)
    tamano=models.CharField(max_length=50,null=True)
    enlace_Torrent = models.CharField(max_length=100,null=True)
    enlace_compra=models.CharField(max_length=100,null=True)
    enlace_gameplay=models.CharField(max_length=100,null=True)
    info_juego=models.CharField(max_length=500,null=True)
    def __unicode__(self):
        return unicode(self.titulo)
    