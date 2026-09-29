import tkinter as tk
from tkinter import messagebox


FUNDO = "#0f172a"
PAINEL = "#172033"
BRANCO = "#f8fafc"
CINZA = "#94a3b8"
VERDE = "#22c55e"
VERMELHO = "#ef4444"


def centralizar(janela, largura, altura):
	x = (janela.winfo_screenwidth() - largura) // 2
	y = (janela.winfo_screenheight() - altura) // 2
	janela.geometry(f"{largura}x{altura}+{x}+{y}")


def calcular():
	nome_executivo = nome.get().strip()

	try:
		salario = float(salario_base.get().replace(",", "."))
		metas = float(atingimento.get().replace(",", "."))
	except ValueError:
		messagebox.showerror("Dados inválidos", "Digite valores numéricos válidos.")
		return

	if not nome_executivo:
		messagebox.showwarning("Campo obrigatório", "Informe o nome do executivo ou gestor.")
		return

	if salario <= 0 or metas <= 0:
		messagebox.showerror("Validação financeira", "Salário e metas devem ser maiores que zero.")
		return

	if metas > 200:
		messagebox.showerror("Percentual inválido", "O atingimento de metas deve estar entre 0% e 200%.")
		return

	if metas < 80:
		percentual_bonus = 0
		categoria = "Sem direito à bonificação"
	elif metas < 100:
		percentual_bonus = 0.5
		categoria = "Performance regular"
	elif metas <= 120:
		percentual_bonus = 1
		categoria = "Meta atingida"
	elif metas <= 150:
		percentual_bonus = 1.5
		categoria = "Superação de metas"
	else:
		percentual_bonus = 2
		categoria = "Performance executiva máxima"

	bonificacao = salario * percentual_bonus
	resultado.config(
		text=f"Executivo: {nome_executivo}\n"
			 f"Categoria: {categoria}\n"
			 f"Bonificação: R$ {bonificacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
		fg=VERDE if bonificacao > 0 else VERMELHO,
	)


def limpar():
	nome.delete(0, tk.END)
	salario_base.delete(0, tk.END)
	atingimento.delete(0, tk.END)
	resultado.config(text="Preencha os dados para calcular a bonificação.", fg=CINZA)


janela = tk.Tk()
janela.title("Módulo de Bonificação Semestral e Metas")
janela.configure(bg=FUNDO)
janela.resizable(False, False)
centralizar(janela, 500, 430)

conteudo = tk.Frame(janela, bg=FUNDO)
conteudo.pack(fill="both", expand=True, padx=35, pady=25)

tk.Label(conteudo, text="CÁLCULO DE BONIFICAÇÃO EXECUTIVA", bg=FUNDO,
		 fg=BRANCO, font=("Segoe UI", 15, "bold")).pack(anchor="w")
tk.Label(conteudo, text="Participação nos Lucros (PLR) • Apuração semestral",
		 bg=FUNDO, fg=CINZA, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 18))

formulario = tk.Frame(conteudo, bg=PAINEL, padx=20, pady=18)
formulario.pack(fill="x")

tk.Label(formulario, text="Nome do Executivo/Gestor", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=6)
nome = tk.Entry(formulario, width=32, bg="#253149", fg=BRANCO,
				insertbackground=BRANCO, relief="flat")
nome.grid(row=0, column=1, padx=(16, 0), pady=6)

tk.Label(formulario, text="Salário Base (R$)", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=6)
salario_base = tk.Entry(formulario, width=32, bg="#253149", fg=BRANCO,
						insertbackground=BRANCO, relief="flat")
salario_base.grid(row=1, column=1, padx=(16, 0), pady=6)

tk.Label(formulario, text="Atingimento de Metas (%)", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=6)
atingimento = tk.Entry(formulario, width=32, bg="#253149", fg=BRANCO,
					   insertbackground=BRANCO, relief="flat")
atingimento.grid(row=2, column=1, padx=(16, 0), pady=6)

botoes = tk.Frame(conteudo, bg=FUNDO)
botoes.pack(fill="x", pady=(18, 15))
tk.Button(botoes, text="CALCULAR BONIFICAÇÃO", command=calcular, bg=VERDE,
		  fg="#052e16", relief="flat", font=("Segoe UI", 9, "bold"),
		  padx=12, pady=9).pack(side="left")
tk.Button(botoes, text="LIMPAR", command=limpar, bg=PAINEL, fg=BRANCO,
		  relief="flat", font=("Segoe UI", 9, "bold"), padx=22, pady=9).pack(side="right")

resultado = tk.Label(conteudo, text="Preencha os dados para calcular a bonificação.",
					 bg=FUNDO, fg=CINZA, font=("Segoe UI", 10), justify="left",
					 anchor="w")
resultado.pack(fill="x")

janela.mainloop()
