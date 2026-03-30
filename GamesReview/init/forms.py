from django import forms 
from .models import Usuario,Game,Review
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.password_validation import validate_password

class Cadastro(UserCreationForm):
    """Cadastro definition."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget     = forms.PasswordInput(attrs={"placeholder":"Digite sua senha"}) #! Adiciona o placeholder e o formato de senha
        self.fields['password1'].validators = [validate_password]  #!Adiciona o Validador de Senhas(Senhas Fracas,Senhas Comuns,etc)
        self.fields.pop('password2')    #! Remove a segunda senha 


    foto_perfil     = forms.URLField(
                                max_length=255,
                                required=False,
                                widget=forms.URLInput(attrs={"placeholder":"Coloque a URL da sua foto de perfil"}))
    
    bio             = forms.CharField(
                                max_length=355,
                                required=False,
                                widget=forms.TextInput(attrs={"placeholder":"Coloque a sua BIO"}))
    
    


    class Meta:
        
        model = Usuario

        fields = ["username",
                  'email'
                  ]
        
        widgets = {
            "username"   : forms.TextInput          (attrs={"placeholder":"Digite seu usuario"}),
            "email"      : forms.EmailInput         (attrs={"placeholder":"Digite seu e-mail"}),
            }


class Login(forms.Form):
    """Login definition."""

    username = forms.CharField(max_length=150,
                               required=True,
                               widget=forms.TextInput({"placeholder":"Digite seu usuario:"})
                               )


    password = forms.CharField(max_length=250,
                               required=True,
                               widget=forms.PasswordInput(attrs={"placeholder":"Digite sua senha:"}))

