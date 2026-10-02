import tkinter.messagebox as messagebox

import customtkinter as ctk


class SalesControl(ctk.CTk):
	def __init__(self):
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("green")
		super().__init__()
		self.title("Sales Control - Registro de Vendas e Checkout")
		self.geometry("900x650")
		self.vendas = []
		self.proximo_id = 1

		self.centralizar_janela()
		self.montar_tela()

	def centralizar_janela(self):
		self.update_idletasks()
		largura, altura = 900, 650
		x = (self.winfo_screenwidth() - largura) // 2
		y = (self.winfo_screenheight() - altura) // 2
		self.geometry(f"{largura}x{altura}+{x}+{y}")

	def montar_tela(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(3, weight=1)

		ctk.CTkLabel(
			self, text="Registro de Vendas e Checkout",
			font=("Segoe UI", 22, "bold"), text_color="#4ade80",
		).grid(row=0, column=0, sticky="w", padx=24, pady=(20, 12))

		formulario = ctk.CTkFrame(self)
		formulario.grid(row=1, column=0, sticky="ew", padx=24, pady=8)
		formulario.grid_columnconfigure((0, 1, 2), weight=1)

		self.produto = ctk.CTkEntry(formulario, placeholder_text="Produto")
		self.quantidade = ctk.CTkEntry(formulario, placeholder_text="Quantidade")
		self.valor = ctk.CTkEntry(formulario, placeholder_text="Valor unitário (R$)")
		self.produto.grid(row=0, column=0, sticky="ew", padx=8, pady=10)
		self.quantidade.grid(row=0, column=1, sticky="ew", padx=8, pady=10)
		self.valor.grid(row=0, column=2, sticky="ew", padx=8, pady=10)

		self.pagamento = ctk.CTkOptionMenu(
			formulario, values=["Pix", "Cartão", "Débito", "Dinheiro"],
			fg_color="#15803d", button_color="#15803d",
		)
		self.pagamento.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 10))
		ctk.CTkButton(
			formulario, text="Registrar Venda", command=self.registrar_venda,
			fg_color="#22c55e", hover_color="#15803d", text_color="#052e16",
		).grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=(0, 10))

		self.busca = ctk.CTkEntry(self, placeholder_text="Buscar por produto ou ID da venda")
		self.busca.grid(row=2, column=0, sticky="ew", padx=24, pady=8)
		self.busca.bind("<KeyRelease>", lambda _evento: self.filtrar())

		tabela = ctk.CTkFrame(self)
		tabela.grid(row=3, column=0, sticky="nsew", padx=24, pady=8)
		tabela.grid_columnconfigure(0, weight=1)
		tabela.grid_rowconfigure(1, weight=1)

		colunas = ["ID Venda", "Produto", "Qtd", "Total R$", "Pagamento"]
		cabecalho = ctk.CTkFrame(tabela, fg_color="#223128")
		cabecalho.grid(row=0, column=0, sticky="ew")
		for indice, nome in enumerate(colunas):
			cabecalho.grid_columnconfigure(indice, weight=1)
			ctk.CTkLabel(cabecalho, text=nome, font=("Segoe UI", 12, "bold")).grid(
				row=0, column=indice, sticky="ew", padx=8, pady=10
			)

		self.linhas = ctk.CTkScrollableFrame(tabela)
		self.linhas.grid(row=1, column=0, sticky="nsew")
		for indice in range(len(colunas)):
			self.linhas.grid_columnconfigure(indice, weight=1)

		rodape = ctk.CTkFrame(self, fg_color="transparent")
		rodape.grid(row=4, column=0, sticky="ew", padx=24, pady=(8, 18))
		rodape.grid_columnconfigure(0, weight=1)
		ctk.CTkLabel(rodape, text="Total acumulado:", font=("Segoe UI", 14, "bold")).grid(
			row=0, column=0, sticky="e", padx=8
		)
		self.total = ctk.CTkLabel(rodape, text="R$ 0,00", text_color="#4ade80", font=("Segoe UI", 18, "bold"))
		self.total.grid(row=0, column=1, sticky="w")

	def registrar_venda(self):
		produto = self.produto.get().strip()
		try:
			quantidade = int(self.quantidade.get())
			valor = float(self.valor.get().replace(".", "").replace(",", "."))
		except ValueError:
			messagebox.showerror("Dados inválidos", "Informe quantidade e valor válidos.", parent=self)
			return
		if not produto or quantidade <= 0 or valor <= 0:
			messagebox.showerror("Dados inválidos", "Preencha os campos com valores maiores que zero.", parent=self)
			return

		self.vendas.insert(0, {
			"id": f"V-{self.proximo_id:03d}", "produto": produto,
			"quantidade": quantidade, "total": quantidade * valor,
			"pagamento": self.pagamento.get(),
		})
		self.proximo_id += 1
		self.produto.delete(0, "end")
		self.quantidade.delete(0, "end")
		self.valor.delete(0, "end")
		self.filtrar()

	def filtrar(self):
		termo = self.busca.get().strip().casefold()
		vendas = [v for v in self.vendas if termo in v["id"].casefold() or termo in v["produto"].casefold()]
		for widget in self.linhas.winfo_children():
			widget.destroy()

		cores = {"Pix": "#4ade80", "Cartão": "#60a5fa", "Débito": "#fbbf24", "Dinheiro": "#a3e635"}
		for linha, venda in enumerate(vendas):
			valores = [venda["id"], venda["produto"], str(venda["quantidade"]), f'R$ {venda["total"]:.2f}'.replace(".", ","), venda["pagamento"]]
			for coluna, texto in enumerate(valores):
				ctk.CTkLabel(
					self.linhas, text=texto,
					text_color=cores[venda["pagamento"]] if coluna == 4 else "#4ade80" if coluna == 3 else "#f1f5f9",
				).grid(row=linha, column=coluna, sticky="ew", padx=8, pady=10)

		total = sum(v["total"] for v in self.vendas)
		self.total.configure(text=f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))


if __name__ == "__main__":
	app = SalesControl()
	app.mainloop()
