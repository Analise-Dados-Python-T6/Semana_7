"""
Web scraping de vagas de emprego (vagas.com.br)
--------------------------------------------------
O Vagas.com.br é um site brasileiro de vagas de emprego com HTML
renderizado no servidor (sem SPA, sem proteção anti-bot), então dá
pra usar só requests + BeautifulSoup.

Busca vagas por cargo e extrai, de cada resultado:
  - cargo (título da vaga)
  - empresa
  - nível (júnior, pleno, sênior etc., quando informado)
  - local de trabalho
  - data de publicação
  - link

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

cargo_nome = input('Qual cargo você deseja buscar? ')

# O site usa o padrão de URL "vagas-de-<cargo com espaços trocados por hífen>"
url = 'https://www.vagas.com.br/vagas-de-' + cargo_nome.replace(' ', '-')

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'
site = BeautifulSoup(response.text, 'html.parser')

# Cada vaga é um <li class="vaga ...">
vagas = site.find_all('li', attrs={'class': 'vaga'})

if not vagas:
    print('Nenhuma vaga encontrada. O Vagas.com.br pode ter mudado o nome')
    print('das classes HTML, nesse caso é preciso inspecionar a página de novo')
    print('(botão direito > Inspecionar) e atualizar os nomes usados no código.')

dados = []

for vaga in vagas:
    link_tag = vaga.find('a', attrs={'class': 'link-detalhes-vaga'})
    empresa_tag = vaga.find('span', attrs={'class': 'emprVaga'})
    nivel_tag = vaga.find('span', attrs={'class': 'nivelVaga'})
    local_tag = vaga.find('span', attrs={'class': 'vaga-local'})
    data_tag = vaga.find('span', attrs={'class': 'data-publicacao'})

    if not link_tag:
        continue

    # O título vem no atributo "title" pra evitar pegar a tag <mark> usada
    # pra destacar o termo buscado dentro do texto
    cargo = link_tag['title']
    link = 'https://www.vagas.com.br' + link_tag['href']
    empresa = empresa_tag.text.strip() if empresa_tag else None
    nivel = nivel_tag.text.strip() if nivel_tag else None
    local = local_tag.text.strip() if local_tag else None
    data_publicacao = data_tag.text.strip() if data_tag else None

    print('Cargo:', cargo)
    print('Link:', link)

    if empresa:
        print('Empresa:', empresa)

    if nivel:
        print('Nível:', nivel)

    if local:
        print('Local:', local)

    if data_publicacao:
        print('Publicada em:', data_publicacao)

    print('\n')

    dados.append({
        'Cargo': cargo,
        'Empresa': empresa,
        'Nível': nivel,
        'Local': local,
        'Publicada em': data_publicacao,
        'Link': link,
    })

df = pd.DataFrame(dados)
df.to_excel('vagas_emprego.xlsx', index=False)
print(f'{len(df)} vagas exportadas para vagas_emprego.xlsx')
