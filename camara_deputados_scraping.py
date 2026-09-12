"""
Web scraping de deputados federais (camara.leg.br)
------------------------------------------------------
O site da Câmara dos Deputados é um órgão público e o HTML da busca de
deputados vem pronto do servidor, sem proteção anti-bot, então dá pra
usar só requests + BeautifulSoup.

Busca deputados por nome (deixe em branco pra listar todos, de todas as
legislaturas) e extrai, de cada um:
  - nome e partido/estado
  - situação (em exercício ou ex-deputado)
  - link do perfil

No final, os dados coletados são exportados pra uma planilha Excel.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
    )
}

nome_busca = input('Buscar por qual nome? (Enter pra listar todos) ')

url = 'https://www.camara.leg.br/deputados/quem-sao/resultado?search=' + nome_busca

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
site = BeautifulSoup(response.text, 'html.parser')

# Cada deputado é um <li class="lista-resultados__item">
deputados = site.find_all('li', attrs={'class': 'lista-resultados__item'})

if not deputados:
    print('Nenhum deputado encontrado. O site da Câmara pode ter mudado o nome')
    print('das classes HTML, nesse caso é preciso inspecionar a página de novo')
    print('(botão direito > Inspecionar) e atualizar os nomes usados no código.')

dados = []

for deputado in deputados:
    nome_tag = deputado.find('a', attrs={'class': 'nome-deputado'})
    situacao_tag = deputado.find('span', attrs={'class': 'lista-resultados__info-exercicio'})

    if not nome_tag:
        continue

    # O texto vem no formato "Nome Completo (PARTIDO-UF)"
    texto_completo = nome_tag.text.strip()
    link = nome_tag['href']
    situacao = situacao_tag.text.strip() if situacao_tag else None

    abre_parenteses = texto_completo.rfind('(')
    if abre_parenteses != -1 and texto_completo.endswith(')'):
        nome = texto_completo[:abre_parenteses].strip()
        partido, uf = texto_completo[abre_parenteses + 1:-1].rsplit('-', 1)
    else:
        nome, partido, uf = texto_completo, None, None

    print('Deputado:', texto_completo)
    print('Link:', link)

    if situacao:
        print('Situação:', situacao)

    print('\n')

    dados.append({
        'Nome': nome,
        'Partido': partido,
        'UF': uf,
        'Situação': situacao,
        'Link': link,
    })

df = pd.DataFrame(dados)
df.to_excel('deputados.xlsx', index=False)
print(f'{len(df)} deputados exportados para deputados.xlsx')
