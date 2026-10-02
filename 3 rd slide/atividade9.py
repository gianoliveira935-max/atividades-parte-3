import tkinter as tk
from datetime import datetime


FUNDO = "#0f172a"
PAINEL = "#1e293b"
TEXTO = "#f8fafc"
CINZA = "#94a3b8"


janela = tk.Tk()
janela.title("Dashboard Gerencial - Métricas & Desempenho Executivo")
janela.geometry("600x420")
janela.resizable(False, False)
janela.configure(bg=FUNDO)

largura = 600
altura = 420
x = (janela.winfo_screenwidth() - largura) // 2
y = (janela.winfo_screenheight() - altura) // 2
janela.geometry(f"{largura}x{altura}+{x}+{y}")

cabecalho = tk.Frame(janela, bg=FUNDO)
cabecalho.pack(fill="x", padx=24, pady=(20, 12))

tk.Label(
	cabecalho,
	text="Dashboard Gerencial",
	font=("Segoe UI", 19, "bold"),
	fg=TEXTO,
	bg=FUNDO,
).pack(anchor="w")

tk.Label(
	cabecalho,
	text="Indicadores executivos",
	font=("Segoe UI", 10),
	fg=CINZA,
	bg=FUNDO,
).pack(anchor="w", pady=(2, 0))

area_kpis = tk.Frame(janela, bg=FUNDO)
area_kpis.pack(fill="both", expand=True, padx=24, pady=8)
area_kpis.grid_columnconfigure(0, weight=1)
area_kpis.grid_columnconfigure(1, weight=1)

indicadores = [
	("Receita Mensal", "R$ 458.900", "#38bdf8"),
	("Custo Operacional", "R$ 182.400", "#f97316"),
	("Margem do Lucro", "60.2%", "#22c55e"),
	("Novos Clientes", "+342", "#a78bfa"),
]

for indice, (titulo, valor, cor) in enumerate(indicadores):
	cartao = tk.Frame(area_kpis, bg=PAINEL, padx=16, pady=12)
	cartao.grid(row=indice // 2, column=indice % 2, sticky="nsew", padx=6, pady=6)
	tk.Label(cartao, text=titulo, font=("Segoe UI", 10), fg=CINZA, bg=PAINEL).pack(anchor="w")
	tk.Label(cartao, text=valor, font=("Segoe UI", 17, "bold"), fg=cor, bg=PAINEL).pack(anchor="w", pady=(8, 0))

rodape = tk.Frame(janela, bg="#111c30")
rodape.pack(fill="x", side="bottom")
horario = datetime.now().strftime("%H:%M:%S")
tk.Label(
	rodape,
	text=f"Sistema v1.0  |  Última atualização: {horario}",
	font=("Segoe UI", 9),
	fg=CINZA,
	bg="#111c30",
	anchor="w",
	padx=24,
	pady=12,
).pack(fill="x")

janela.mainloop()
