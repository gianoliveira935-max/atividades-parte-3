import tkinter as tk
from tkinter import messagebox


FUNDO = "#0f172a"
PAINEL = "#172033"
CAMPO = "#253149"
BRANCO = "#f8fafc"
CINZA = "#94a3b8"
VERDE = "#22c55e"
VERMELHO = "#ef4444"
AZUL = "#38bdf8"


def centralizar(janela, largura, altura):
	x = (janela.winfo_screenwidth() - largura) // 2
	y = (janela.winfo_screenheight() - altura) // 2
	janela.geometry(f"{largura}x{altura}+{x}+{y}")


def limpar_filtros():
	volume.delete(0, tk.END)
	ambiente.set("homologacao")
	tipo.set("financeiro")
	progresso.set(0)
	status.config(text="Aguardando configuração do lote.", fg=CINZA)


def encerrar_sessao():
	if messagebox.askyesno("Encerramento", "Deseja encerrar a sessão?"):
		janela.destroy()


def sobre():
	messagebox.showinfo("Sobre o sistema", "Central de Batch Jobs\nKernel de Processamento v1.0")


def executar():
	try:
		tamanho = int(volume.get())
		if tamanho <= 0:
			raise ValueError
	except ValueError:
		messagebox.showerror("Lote inválido", "Informe um volume numérico maior que zero.")
		return

	if ambiente.get() == "producao":
		autorizado = messagebox.askyesno(
			"Validação de segurança",
			"O lote será executado em PRODUÇÃO.\n\nDeseja confirmar a execução?",
		)
		if not autorizado:
			status.config(text="Execução bloqueada: validação não confirmada.", fg=VERMELHO)
			return

	progresso.set(0)
	status.config(text="Processando lote...", fg=AZUL)
	botao_executar.config(state="disabled")
	processar(0, tamanho)


def processar(valor, tamanho):
	if valor >= 100:
		status.config(text="Trabalho concluído com sucesso.", fg=VERDE)
		botao_executar.config(state="normal")
		return
	progresso.set(valor + 5)
	janela.after(max(30, 3000 // tamanho), processar, valor + 5, tamanho)


def abortar():
	janela.after_cancel if False else None
	progresso.set(0)
	status.config(text="Trabalho interrompido pelo operador.", fg=VERMELHO)
	botao_executar.config(state="normal")


janela = tk.Tk()
janela.title("Central de Processamento de Lotes - Batch Jobs")
janela.configure(bg=FUNDO)
janela.resizable(False, False)
centralizar(janela, 560, 430)

menu = tk.Menu(janela)
operacoes = tk.Menu(menu, tearoff=False)
operacoes.add_command(label="Limpar Filtros", command=limpar_filtros)
operacoes.add_separator()
operacoes.add_command(label="Encerramento de Sessão", command=encerrar_sessao)
menu.add_cascade(label="Operações", menu=operacoes)
ajuda = tk.Menu(menu, tearoff=False)
ajuda.add_command(label="Sobre o Sistema", command=sobre)
ajuda.add_command(label="Versão do Kernel", command=sobre)
menu.add_cascade(label="Ajuda", menu=ajuda)
janela.config(menu=menu)

conteudo = tk.Frame(janela, bg=FUNDO)
conteudo.pack(fill="both", expand=True, padx=35, pady=24)

tk.Label(conteudo, text="CENTRAL DE BATCH JOBS", bg=FUNDO, fg=BRANCO,
		 font=("Segoe UI", 16, "bold")).pack(anchor="w")
tk.Label(conteudo, text="Processamento de transações financeiras e notificações",
		 bg=FUNDO, fg=CINZA, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 18))

formulario = tk.Frame(conteudo, bg=PAINEL, padx=20, pady=16)
formulario.pack(fill="x")

tk.Label(formulario, text="Volume/Tamanho do Lote", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=5)
volume = tk.Entry(formulario, width=30, bg=CAMPO, fg=BRANCO,
				  insertbackground=BRANCO, relief="flat")
volume.grid(row=0, column=1, padx=(20, 0), pady=5)

tk.Label(formulario, text="Ambiente de destino", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=5)
ambiente = tk.StringVar(value="homologacao")
tk.Radiobutton(formulario, text="Homologação", variable=ambiente, value="homologacao",
			   bg=PAINEL, fg=CINZA, selectcolor=CAMPO, activebackground=PAINEL).grid(row=1, column=1, sticky="w", padx=(16, 0))
tk.Radiobutton(formulario, text="Produção", variable=ambiente, value="producao",
			   bg=PAINEL, fg=CINZA, selectcolor=CAMPO, activebackground=PAINEL).grid(row=1, column=1, sticky="e")

tk.Label(formulario, text="Tipo de processamento", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=5)
tipo = tk.StringVar(value="financeiro")
tk.Radiobutton(formulario, text="Lote Financeiro", variable=tipo, value="financeiro",
			   bg=PAINEL, fg=CINZA, selectcolor=CAMPO, activebackground=PAINEL).grid(row=2, column=1, sticky="w", padx=(16, 0))
tk.Radiobutton(formulario, text="Notificações", variable=tipo, value="notificacoes",
			   bg=PAINEL, fg=CINZA, selectcolor=CAMPO, activebackground=PAINEL).grid(row=2, column=1, sticky="e")

status = tk.Label(conteudo, text="Aguardando configuração do lote.", bg=FUNDO,
				  fg=CINZA, font=("Segoe UI", 10), anchor="w")
status.pack(fill="x", pady=(20, 8))
progresso = tk.DoubleVar(value=0)
tk.Scale(conteudo, variable=progresso, from_=0, to=100, orient="horizontal",
		 state="disabled", showvalue=False, length=480, bg=FUNDO,
		 troughcolor=PAINEL, highlightthickness=0, activebackground=VERDE).pack()

botoes = tk.Frame(conteudo, bg=FUNDO)
botoes.pack(fill="x", pady=18)
botao_executar = tk.Button(botoes, text="EXECUTAR LOTE", command=executar,
						   bg=VERDE, fg="#052e16", relief="flat",
						   font=("Segoe UI", 9, "bold"), padx=16, pady=9)
botao_executar.pack(side="left")
tk.Button(botoes, text="ABORTAR", command=abortar, bg=VERMELHO, fg=BRANCO,
		  relief="flat", font=("Segoe UI", 9, "bold"), padx=18, pady=9).pack(side="right")

janela.mainloop()
