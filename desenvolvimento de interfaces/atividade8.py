import tkinter.messagebox as messagebox

import customtkinter as ctk


CORES_PRIORIDADE = {
	"Baixa": "#94a3b8",
	"Média": "#60a5fa",
	"Alta": "#f59e0b",
	"Crítica": "#ef4444",
}
CORES_STATUS = {
	"Em Aberto": "#f59e0b",
	"Em Execução": "#3b82f6",
	"Concluída": "#22c55e",
}


def formatar_moeda(valor):
	return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def converter_valor(texto):
	texto = texto.strip().replace("R$", "").replace(" ", "")
	if "," in texto:
		texto = texto.replace(".", "").replace(",", ".")
	return float(texto)


class ServiceOrdersApp(ctk.CTk):
	def __init__(self):
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("dark-blue")
		super().__init__()
		self.title("Field Service - Gestão e Controle de Ordens de Serviço")
		self.geometry("1000x700")
		self.ordens = []
		self.proximo_id = 1

		self.centralizar_janela()
		self.montar_tela()

	def centralizar_janela(self):
		self.update_idletasks()
		largura, altura = 1000, 700
		x = (self.winfo_screenwidth() - largura) // 2
		y = (self.winfo_screenheight() - altura) // 2
		self.geometry(f"{largura}x{altura}+{x}+{y}")

	def montar_tela(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(3, weight=1)

		ctk.CTkLabel(
			self,
			text="Gestão de Ordens de Serviço",
			font=("Segoe UI", 22, "bold"),
			text_color="#bfdbfe",
		).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 12))

		formulario = ctk.CTkFrame(self)
		formulario.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
		formulario.grid_columnconfigure((0, 1, 2), weight=1)
		self.cliente = ctk.CTkEntry(formulario, placeholder_text="Cliente / Empresa")
		self.servico = ctk.CTkEntry(formulario, placeholder_text="Descrição do serviço")
		self.custo = ctk.CTkEntry(formulario, placeholder_text="Custo estimado (R$)")
		self.cliente.grid(row=0, column=0, sticky="ew", padx=8, pady=10)
		self.servico.grid(row=0, column=1, sticky="ew", padx=8, pady=10)
		self.custo.grid(row=0, column=2, sticky="ew", padx=8, pady=10)

		self.prioridade = ctk.CTkOptionMenu(
			formulario, values=list(CORES_PRIORIDADE), fg_color="#334155", button_color="#475569"
		)
		self.prioridade.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 10))
		ctk.CTkButton(
			formulario,
			text="Abrir Nova O.S.",
			command=self.abrir_os,
			fg_color="#2563eb",
			hover_color="#1d4ed8",
		).grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=(0, 10))

		self.busca = ctk.CTkEntry(self, placeholder_text="Buscar por cliente, ID da O.S. ou descrição")
		self.busca.grid(row=2, column=0, sticky="ew", padx=24, pady=8)
		self.busca.bind("<KeyRelease>", lambda _evento: self.filtrar())

		tabela = ctk.CTkFrame(self)
		tabela.grid(row=3, column=0, sticky="nsew", padx=24, pady=8)
		tabela.grid_columnconfigure(0, weight=1)
		tabela.grid_rowconfigure(1, weight=1)
		colunas = ["ID O.S.", "Cliente", "Serviço", "Prioridade", "Valor R$", "Status"]
		cabecalho = ctk.CTkFrame(tabela, fg_color="#263449")
		cabecalho.grid(row=0, column=0, sticky="ew")
		for indice, titulo in enumerate(colunas):
			cabecalho.grid_columnconfigure(indice, weight=1)
			ctk.CTkLabel(cabecalho, text=titulo, font=("Segoe UI", 12, "bold")).grid(
				row=0, column=indice, sticky="ew", padx=6, pady=10
			)

		self.linhas = ctk.CTkScrollableFrame(tabela)
		self.linhas.grid(row=1, column=0, sticky="nsew")
		for indice in range(len(colunas)):
			self.linhas.grid_columnconfigure(indice, weight=1)

		rodape = ctk.CTkFrame(self, fg_color="transparent")
		rodape.grid(row=4, column=0, sticky="ew", padx=24, pady=(8, 18))
		rodape.grid_columnconfigure(0, weight=1)
		ctk.CTkLabel(rodape, text="Total em aberto:", font=("Segoe UI", 14, "bold")).grid(
			row=0, column=0, sticky="e", padx=8
		)
		self.total = ctk.CTkLabel(rodape, text="R$ 0,00", text_color="#f59e0b", font=("Segoe UI", 18, "bold"))
		self.total.grid(row=0, column=1, sticky="w")

	def abrir_os(self):
		cliente = self.cliente.get().strip()
		servico = self.servico.get().strip()
		try:
			custo = converter_valor(self.custo.get())
		except ValueError:
			messagebox.showerror("Dados inválidos", "Informe um custo estimado válido.", parent=self)
			return
		if not cliente or not servico or custo <= 0:
			messagebox.showerror("Dados inválidos", "Preencha todos os campos com um custo maior que zero.", parent=self)
			return

		self.ordens.insert(0, {
			"id": f"OS-{self.proximo_id:03d}",
			"cliente": cliente,
			"servico": servico,
			"prioridade": self.prioridade.get(),
			"custo": custo,
			"status": "Em Aberto",
		})
		self.proximo_id += 1
		self.cliente.delete(0, "end")
		self.servico.delete(0, "end")
		self.custo.delete(0, "end")
		self.filtrar()

	def filtrar(self):
		termo = self.busca.get().strip().casefold()
		ordens = [
			os for os in self.ordens
			if termo in os["id"].casefold()
			or termo in os["cliente"].casefold()
			or termo in os["servico"].casefold()
		]
		for widget in self.linhas.winfo_children():
			widget.destroy()

		for linha, os in enumerate(ordens):
			valores = [os["id"], os["cliente"], os["servico"], os["prioridade"], formatar_moeda(os["custo"]), os["status"]]
			for coluna, texto in enumerate(valores):
				cor = CORES_PRIORIDADE[os["prioridade"]] if coluna == 3 else CORES_STATUS[os["status"]] if coluna == 5 else "#f1f5f9"
				ctk.CTkLabel(self.linhas, text=texto, text_color=cor).grid(
					row=linha, column=coluna, sticky="ew", padx=6, pady=10
				)

		total_aberto = sum(os["custo"] for os in self.ordens if os["status"] == "Em Aberto")
		self.total.configure(text=formatar_moeda(total_aberto))


if __name__ == "__main__":
	app = ServiceOrdersApp()
	app.mainloop()
