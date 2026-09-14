"""
Semana 07 - Visualização e Pipelines
Exemplo de Funções, Classes e ETL (com SQL via sqlite3)
"""

import sqlite3

import matplotlib.pyplot as plt
import pandas as pd


# ---------- Dado de exemplo (mesmo cenário dos slides: filial Centro do Mercado Girassol) ----------

filial_centro = pd.DataFrame({
    "produto": ["Arroz 5kg", "Feijão 1kg", "Feijão 1kg", "Óleo 900ml", "Leite 1L"],
    "preco": [24.9, 8.5, 8.5, None, 4.2],
    "quantidade": [120, 300, 300, 80, 5000],
})


# ---------- Funções ----------

def limpar_dados(df):
    """Remove duplicatas, preenche preço nulo com a mediana e descarta quantidades fora do padrão."""
    df = df.drop_duplicates()
    df["preco"] = df["preco"].fillna(df["preco"].median())
    df = df[df["quantidade"].between(0, 1000)]
    return df

print(limpar_dados(filial_centro.copy()))

# ---------- Classe ----------

class TratamentoDados:
    """Agrupa os métodos de limpeza num só objeto: mesmo princípio da função, organizado em classe."""

    def remover_duplicados(self, df):
        return df.drop_duplicates()

    def preencher_preco(self, df):
        df["preco"] = df["preco"].fillna(df["preco"].median())
        return df

tratamento = TratamentoDados()
df_classe = tratamento.remover_duplicados(filial_centro.copy())
df_classe = tratamento.preencher_preco(df_classe)
print(df_classe)

# ---------- ETL: Extract, Transform, Load ----------

def extrair():
    return filial_centro.copy()


def transformar(df):
    df = df.drop_duplicates()
    df = df[df["quantidade"].between(0, 1000)]
    df["preco"] = df["preco"].fillna(df["preco"].median())
    df["valor_total"] = df["preco"] * df["quantidade"]
    return df


def carregar(df, banco="mercado_girassol.db", tabela="vendas"):
    """Salva o resultado tratado em CSV e grava numa tabela SQL (sqlite3, sem precisar de banco externo)."""
    df.to_csv("vendas_tratadas.csv", index=False)

    conexao = sqlite3.connect(banco)
    df.to_sql(tabela, conexao, if_exists="replace", index=False)

    return pd.read_sql(f"SELECT * FROM {tabela}", conexao)

df = extrair()
df = transformar(df)
df_do_banco = carregar(df)
print(df_do_banco)

plt.bar(df_do_banco["produto"], df_do_banco["valor_total"])
plt.title("Valor total por produto - Filial Centro")
plt.xlabel("Produto")
plt.ylabel("Valor total (R$)")
plt.show()
