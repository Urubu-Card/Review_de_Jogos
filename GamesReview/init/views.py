from django.shortcuts import render,redirect , get_object_or_404
from .forms import Cadastro , Login 
from django.contrib.auth import authenticate , login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Game,Review

class Registracion:

    def Cadastrar(request):

        if request.method =="POST":
            form = Cadastro(request.POST)

            if form.is_valid():
                form.save()
                print("Redirecionando...")
                return redirect("Login")    
        
        else:
            form = Cadastro()

        return render(request,"registration/cadastro.html",{"form":form})


    def Logar(request):

        if request.method =="POST":
            form = Login(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")

                user = authenticate(request,username=username,password=password )
            

                if user is None :
                    messages.error(request,"Usuario não encontrado")
                    return redirect("Login")

                else:
                    login(request,user)
                    return redirect("Home")
        else:
            form = Login()


        return render(request,"registration/login.html",{"form":form})

class App:

    @login_required
    def Inicio(request):

        jogos  = Game.objects.all()

        return render(request,"home/index.html",{"jogos":jogos})
    
    
    @login_required
    def Informacoes_Jogo(request,id):
        
        jogo = get_object_or_404(Game,id=id)
        reviews = Review.objects.filter(jogo=jogo)
        
        if request.method =="POST":
            del_game    = request.POST.get("deletar-jogo")
            nova_review = request.POST.get("nova-review")
            
            if del_game:
                Game.objects.get(id=id).delete()
                return redirect("Home")
            
            if nova_review:
                Review.objects.create(
                    jogo = jogo,
                    user = request.user,
                    nota = request.POST.get("rating"),
                    desc = request.POST.get("comentario")
                )
                return redirect("Info_Jogo",id = id)
            

        
        return render(request,"home/info_jogos.html",{"jogo":jogo,"reviews":reviews})
        
        