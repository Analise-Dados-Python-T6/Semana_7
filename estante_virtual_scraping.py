"""
Web scraping da Estante Virtual (estantevirtual.com.br)
---------------------------------------------------------
Estante Virtual é o maior marketplace brasileiro de livros usados e
novos. A página de busca é renderizada no servidor (sem SPA vazio nem
proteção anti-bot como a do Mercado Livre), então dá pra usar só
requests + BeautifulSoup.

Busca um livro e extrai, de cada resultado:
  - título
  - autor
  - ano
  - preço a partir de
  - link

No final, os dados coletados são exportados pra uma planilha Excel.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

url_base = 'https://www.estantevirtual.com.br/busca?q='

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
    )
}

livro_nome = input('Qual livro você deseja? ')

response = requests.get(url_base + livro_nome, headers=headers)
response.encoding = 'utf-8'

site = BeautifulSoup(response.text, 'html.parser')

# Cada resultado é um <div class="product-item product-list__item">
livros = site.find_all('div', attrs={'class': 'product-item product-list__item'})

dados = []

for livro in livros:
    titulo_tag = livro.find('h2', attrs={'class': 'product-item__title product-item__title--mt product-item__name'})
    autor_tag = livro.find('p', attrs={'class': 'product-item__text product-item__text--mt product-item__author'})
    ano_tag = livro.find('p', attrs={'class': 'product-item__text product-item__text--mt product-item__text-light product-item__year'})
    preco_tag = livro.find('span', attrs={'class': 'product-item__sale-price product-item__text--darken'})
    link_tag = livro.find('a', attrs={'class': 'product-item__link smarthint-tracking-card'})

    titulo = titulo_tag.text.strip()
    autor = autor_tag.text.strip() if autor_tag else None
    ano = ano_tag.text.strip() if ano_tag else None
    preco = preco_tag.text.strip()
    link = 'https://www.estantevirtual.com.br' + link_tag['href'] if link_tag else None

    print('Título do livro:', titulo)

    if autor:
        print('Autor:', autor)

    if ano:
        print('Ano:', ano)

    print('Preço a partir de:', preco)

    if link:
        print('Link:', link)

    print('\n')

    dados.append({
        'Título': titulo,
        'Autor': autor,
        'Ano': ano,
        'Preço a partir de': preco,
        'Link': link,
    })

df = pd.DataFrame(dados)
print(df)
df.to_excel('livros_estante_virtual.xlsx', index=False)
print(f'{len(df)} livros exportados para livros_estante_virtual.xlsx')
