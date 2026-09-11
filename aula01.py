import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

cafes = ["gourmet", "melita", "pelé","pilão", "trescoracoes"]
vendas_cafes = [100, 500, 5, 700, 600]

tempo = [30, 40, 20, 20, 50, 20, 30, 25, 30, 45, 60, 30, 25, 30, 45, 60]
nota = [8, 2, 10, 8, 7, 10, 9, 8, 7, 8, 9, 10, 10, 10, 10, 9]

meses = ["jan", "fev", "mar","abr"]
vendas = [100, 250, 440, 1000]

fig, ax = plt.subplots (figsize=(8, 5))
ax.plot(meses, vendas, color="green", lw = 2)
ax.set_title("Vendas por mês")
ax.set_xlabel("Meses")
ax.set_ylabel("Vendas")
ax.legend(["Vendas do site"])
fig.savefig("vendas.png", dpi=300)
plt.show()

fig, axs = plt.subplots(2,2)
axs [0,0].plot(meses,vendas, color="red")
axs [0,1].bar(cafes, vendas_cafes, color="red")
axs [1,0].scatter(nota, tempo, color="red")
axs [1,1].plot(meses,vendas, color="red")
fig.savefig("grafico.png", dpi=300, bbox_inches="tight")
plt.show()