import tkinter as tk
from tkinter import messagebox, ttk


FUNDO = "#0f172a"
PAINEL = "#172033"
CAMPO = "#1e293b"
BRANCO = "#f8fafc"
CINZA = "#94a3b8"
VERDE = "#22c55e"
VERMELHO = "#ef4444"


def centralizar(janela, largura, altura):
	x = (janela.winfo_screenwidth() - largura) // 2
	y = (janela.winfo_screenheight() - altura) // 2
	janela.geometry(f"{largura}x{altura}+{x}+{y}")


def cadastrar():
	campos = {
		"Matrícula": matricula.get().strip(),
		"Nome completo": nome.get().strip(),
		"Cargo/Função": cargo.get().strip(),
		"Departamento": departamento.get().strip(),
	}
	vazios = [campo for campo, valor in campos.items() if not valor]

	if vazios:
		auditoria.config(text="Atenção: preencha todos os campos obrigatórios.", fg=VERMELHO)
		messagebox.showwarning("Cadastro incompleto", "Preencha todos os campos institucionais.")
		return

	auditoria.config(
		text=f"Registro salvo: {campos['Nome completo']} | Matrícula {campos['Matrícula']}",
		fg=VERDE,
	)
	messagebox.showinfo("Cadastro realizado", "Colaborador cadastrado com sucesso.")


def limpar():
	if messagebox.askyesno("Confirmar limpeza", "Deseja limpar todos os campos do formulário?"):
		matricula.delete(0, tk.END)
		nome.delete(0, tk.END)
		cargo.delete(0, tk.END)
		departamento.set("")
		auditoria.config(text="Formulário limpo. Aguardando novo cadastro.", fg=CINZA)


janela = tk.Tk()
janela.title("Módulo de Recursos Humanos - HRMS")
janela.configure(bg=FUNDO)
janela.resizable(False, False)
centralizar(janela, 500, 430)

estilo = ttk.Style(janela)
estilo.theme_use("clam")
estilo.configure("Campo.TEntry", fieldbackground=CAMPO, foreground=BRANCO)
estilo.configure("Campo.TCombobox", fieldbackground=CAMPO, foreground=BRANCO)

conteudo = tk.Frame(janela, bg=FUNDO)
conteudo.pack(fill="both", expand=True, padx=32, pady=24)

tk.Label(conteudo, text="CADASTRO DE COLABORADORES", bg=FUNDO, fg=BRANCO,
		 font=("Segoe UI", 16, "bold")).pack(anchor="w")
tk.Label(conteudo, text="Módulo de Recursos Humanos • Atribuição de perfis operacionais",
		 bg=FUNDO, fg=CINZA, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 20))

formulario = tk.Frame(conteudo, bg=PAINEL, padx=20, pady=18)
formulario.pack(fill="x")

tk.Label(formulario, text="DADOS INSTITUCIONAIS", bg=PAINEL, fg=CINZA,
		 font=("Segoe UI", 8, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

tk.Label(formulario, text="Matrícula *", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=6)
matricula = ttk.Entry(formulario, style="Campo.TEntry", width=34)
matricula.grid(row=1, column=1, pady=6, padx=(18, 0))

tk.Label(formulario, text="Nome Completo *", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=6)
nome = ttk.Entry(formulario, style="Campo.TEntry", width=34)
nome.grid(row=2, column=1, pady=6, padx=(18, 0))

tk.Label(formulario, text="Cargo/Função *", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w", pady=6)
cargo = ttk.Entry(formulario, style="Campo.TEntry", width=34)
cargo.grid(row=3, column=1, pady=6, padx=(18, 0))

tk.Label(formulario, text="Departamento *", bg=PAINEL, fg=BRANCO,
		 font=("Segoe UI", 9)).grid(row=4, column=0, sticky="w", pady=6)
departamento = ttk.Combobox(
	formulario,
	values=("Operações", "Manutenção", "Tecnologia", "Recursos Humanos", "Financeiro"),
	style="Campo.TCombobox",
	width=32,
	state="readonly",
)
departamento.grid(row=4, column=1, pady=6, padx=(18, 0))

botoes = tk.Frame(conteudo, bg=FUNDO)
botoes.pack(fill="x", pady=(18, 14))
tk.Button(botoes, text="CONFIRMAR CADASTRO", command=cadastrar, bg=VERDE, fg="#052e16",
		  activebackground="#16a34a", relief="flat", cursor="hand2",
		  font=("Segoe UI", 9, "bold"), padx=12, pady=9).pack(side="left")
tk.Button(botoes, text="RESETAR", command=limpar, bg=CAMPO, fg=BRANCO,
		  activebackground="#334155", relief="flat", cursor="hand2",
		  font=("Segoe UI", 9, "bold"), padx=18, pady=9).pack(side="right")

auditoria = tk.Label(conteudo, text="Aguardando preenchimento do formulário.", bg=FUNDO,
					 fg=CINZA, font=("Segoe UI", 8), anchor="w")
auditoria.pack(fill="x")

janela.mainloop()
