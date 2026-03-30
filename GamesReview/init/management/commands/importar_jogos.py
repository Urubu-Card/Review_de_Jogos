from django.core.management.base import BaseCommand
import requests as re
from ...models import Game
from deep_translator import GoogleTranslator
from django.db import IntegrityError

API_KEY = "" #!Tirar daqui se for hospedar apenas em modo testes
tradutor = GoogleTranslator(source='en',target='pt')
class Command(BaseCommand):

    help = "Esse comando insere dados da API RAWG dentro do banco de dados"

    def handle(self, *args, **options):

        qntd = int(input("Quantidade de jogo que quer adicionar:(MAX:40)"))
        

        url = f"https://api.rawg.io/api/games?page_size={qntd}&key="

        resposta = re.get(f"{url}{API_KEY}")

        dados = resposta.json()

        url_games = "https://api.rawg.io/api/games/"

        for dado in  dados['results']:
            
            id = dado.get("id")
            
            resposta = re.get(f"{url_games}{id}?key={API_KEY}")
            
            dados_games = resposta.json()
            
            nome_jogo = dados_games.get('name')
            if Game.objects.filter(titulo=nome_jogo).exists():
                print(f"{nome_jogo} já está no banco de dados")
                continue
            else:
                desc_temp   = dados_games.get("description_raw")
                img_capa = dados_games.get('background_image')
                genero = ", ".join([g['name'] for g in dados_games['genres']])
                plaforma = ", ".join([plata['platform']['name'] for plata in dados_games['platforms']])
                ano_lancamento = dados_games.get('released')
                desc = tradutor.translate(desc_temp)

            
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
                
                
            
        
        