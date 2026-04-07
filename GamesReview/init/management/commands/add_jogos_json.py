import requests as re
from deep_translator import GoogleTranslator
import json
import os
from django.core.management.base import BaseCommand



API_KEY = "" #!Tirar daqui se for hospedar apenas em modo testes
tradutor = GoogleTranslator(source='en',target='pt')


def traduzir_texto_longo(texto, limite=4500):
    if not texto:
        return ""
    # Se o texto for menor que o limite, traduz direto
    if len(texto) <= limite:
        return tradutor.translate(texto)
    
    # Se for maior, divide em partes (por parágrafos ou pontos)
    partes = [texto[i:i+limite] for i in range(0, len(texto), limite)]
    traducoes = [tradutor.translate(p) for p in partes]
    return "".join(traducoes)

class Command(BaseCommand):
    def handle(self, *args, **options):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_Data = os.path.join(script_dir, "data", "data_Games.json")

        # 1. Carrega o que já existe
        if os.path.exists(local_Data) and os.path.getsize(local_Data) > 0:
            with open(local_Data, "r", encoding="utf-8") as arq:
                lista_total_jogos = json.load(arq)
        else:
            lista_total_jogos = []


        titulos_existentes = {jogo['titulo'] for jogo in lista_total_jogos}

        qntd = int(input("Quantas paginas de jogos você quer adicionar? (Cada pag tem 20 Jogos): "))


        for i in range(1, qntd + 1): 
            print(f"\n--- Processando página {i} ---")
            url = f"https://api.rawg.io/api/games?page={i}&key={API_KEY}"
            resposta = re.get(url)
            dados = resposta.json()
            
            for dado in dados.get('results', []):
                nome_temp = dado.get("name") 


                if nome_temp in titulos_existentes:
                    print(f"PULANDO: {nome_temp} já está no arquivo.")
                    continue
                
                id_jogo = dado.get("id")
                url_detalhe = f"https://api.rawg.io/api/games/{id_jogo}?key={API_KEY}"
                resposta_detalhe = re.get(url_detalhe)
                dados_games = resposta_detalhe.json()
                
                nome_jogo = dados_games.get('name')
                desc_temp = dados_games.get("description_raw")
                
                
                desc = traduzir_texto_longo(desc_temp)

                jogo_atual = {
                    "titulo": nome_jogo,
                    "descricao": desc,
                    "genero": ", ".join([g['name'] for g in dados_games.get('genres', [])]),
                    "imagem": dados_games.get('background_image'),
                    "plataformas": ", ".join([plata['platform']['name'] for plata in dados_games.get('platforms', [])]),
                    "ano_lancamento": dados_games.get('released'),
                }
            
                lista_total_jogos.append(jogo_atual)
                titulos_existentes.add(nome_jogo) 
                print(f"Jogo {nome_jogo} adicionado com sucesso.")


        with open(local_Data, "w", encoding="utf-8") as arq:
            json.dump(lista_total_jogos, arq, indent=4, ensure_ascii=False, sort_keys=True)

        print(f"\nFinalizado! Total de jogos no arquivo: {len(lista_total_jogos)}")

            