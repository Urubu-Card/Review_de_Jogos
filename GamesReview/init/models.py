from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(AbstractUser):
    """Model definition for Users."""

    foto_perfil = models.URLField(max_length=255,blank=True,null=True)
    bio = models.CharField(blank=True)


class Game(models.Model):
    """Model definitionn for Games."""

    titulo          = models.CharField(max_length=250,unique=True)
    desc            = models.CharField(max_length=250)
    img_capa        = models.URLField()
    genero          = models.CharField(max_length=250)
    plataforma      = models.CharField(max_length=250)
    ano_lancamento  = models.DateField()
    criado_em       = models.DateTimeField(auto_now_add=True)
    

    
    def __str__(self):
        return self.titulo
    


class Review(models.Model):

    jogo       = models.ForeignKey(Game,on_delete=models.CASCADE)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    nota       = models.IntegerField(validators=[MinValueValidator(1,"Nota minima permitida é 1"),MaxValueValidator(10,"Nota maxima permitida é 10")])
    desc       = models.CharField(max_length=250,null=True)
    criado_em  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review de {self.jogo} feita por :{self.user}"