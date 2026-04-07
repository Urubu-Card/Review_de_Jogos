from django.core.management.base import BaseCommand
import requests as re
import os
from ...models import Game
import json
from django.db import IntegrityError


class Command(BaseCommand):

    help = "Esse comando insere dados da API RAWG dentro do banco de dados"

    def handle(self, *args, **options):

        script_dir = os.path.dirname(os.path.abspath(__file__))

        local_Data = os.path.join(script_dir, "data", "data_Games.json")
        
        with open(local_Data,"r",encoding="utf-8") as f:
            data = json.load(f)
            for jogo in data:
                nome_jogo       = jogo.get("titulo")
                desc            = jogo.get("descricao")
                img_capa        = jogo.get("imagem")
                plaforma        = jogo.get("plataformas")
                ano_lancamento  = jogo.get("ano_lancamento")
                genero          = jogo.get("genero")

                try:
                    Game.objects.create(
                        titulo=nome_jogo,
                        desc=desc,
                        img_capa=img_capa,
                        genero=genero,
                        plataforma=plaforma,
                        ano_lancamento=ano_lancamento
                    )
                    print(f"Jogo: {nome_jogo} foi salvo com sucesso! ")
                except IntegrityError as e:
                    print(f"Jogo ja esta no banco de dados: {e}")
            
                
            
        
        