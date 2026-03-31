from django.urls import path , include
from .views import Registracion, App


urlpatterns = [
    path("",                         Registracion.Cadastrar,             name="Cadastro"),
    path("login/",                   Registracion.Logar,                 name="Login"),
    path("home/",                    App.Inicio,                         name="Home"),
    path("jogo/<int:id>/",           App.Informacoes_Jogo,               name="Info_Jogo"),
    path("config_<str:username>/",   App.User_Page,                     name="ConfiguracaoConta")
]