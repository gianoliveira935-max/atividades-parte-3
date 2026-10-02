import customtkinter as ctk


MOVIMENTACOES = [
	{"sku": "SKU-10482", "produto": "Teclado mecânico K2", "categoria": "Periféricos", "quantidade": 48, "tipo": "Entrada"},
	{"sku": "SKU-20831", "produto": "Monitor IPS 27\"", "categoria": "Monitores", "quantidade": 7, "tipo": "Saída"},
	{"sku": "SKU-31007", "produto": "Mouse sem fio M510", "categoria": "Periféricos", "quantidade": 23, "tipo": "Entrada"},
	{"sku": "SKU-41596", "produto": "Headset corporativo H3", "categoria": "Áudio", "quantidade": 4, "tipo": "Ajuste"},
	{"sku": "SKU-50214", "produto": "Dock USB-C universal", "categoria": "Acessórios", "quantidade": 16, "tipo": "Saída"},
	{"sku": "SKU-61840", "produto": "Webcam Full HD C920", "categoria": "Periféricos", "quantidade": 9, "tipo": "Entrada"},
	{"sku": "SKU-72033", "produto": "SSD externo 1 TB", "categoria": "Armazenamento", "quantidade": 31, "tipo": "Ajuste"},
	{"sku": "SKU-83419", "produto": "Cabo HDMI 2 m", "categoria": "Acessórios", "quantidade": 3, "tipo": "Saída"},
	{"sku": "SKU-94602", "produto": "Notebook Pro 14\"", "categoria": "Computadores", "quantidade": 12, "tipo": "Entrada"},
]


class ControleEstoqueApp(ctk.CTk):
	def __init__(self):
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("dark-blue")
		super().__init__()
		self.title("Inventory & Warehouse - Controle de Estoque e Audit Trail")
		self.geometry("1220x780")
		self.minsize(920, 640)
		self.configure(fg_color="#101820")

		self.centralizar_janela()
		self._construir_interface()
		self._renderizar_linhas(MOVIMENTACOES)

	def centralizar_janela(self):
		self.update_idletasks()
		largura = 1220
		altura = 780
		posicao_x = (self.winfo_screenwidth() - largura) // 2
		posicao_y = (self.winfo_screenheight() - altura) // 2
		self.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")

	def _construir_interface(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(2, weight=1)

		cabecalho = ctk.CTkFrame(self, fg_color="#17232d", corner_radius=0, height=112)
		cabecalho.grid(row=0, column=0, sticky="ew")
		cabecalho.grid_columnconfigure(0, weight=1)
		ctk.CTkLabel(
			cabecalho,
			text="INVENTORY  /  WAREHOUSE",
			font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
			text_color="#38bdf8",
		).grid(row=0, column=0, sticky="w", padx=30, pady=(20, 4))
		ctk.CTkLabel(
			cabecalho,
			text="Controle de Estoque e Audit Trail",
			font=ctk.CTkFont(family="Segoe UI", size=25, weight="bold"),
			text_color="#f1f5f9",
		).grid(row=1, column=0, sticky="w", padx=30, pady=(0, 18))
		ctk.CTkLabel(
			cabecalho,
			text="OPERAÇÃO  •  INVENTÁRIO",
			font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
			text_color="#94a3b8",
		).grid(row=0, column=1, rowspan=2, padx=30)

		barra_busca = ctk.CTkFrame(self, fg_color="transparent")
		barra_busca.grid(row=1, column=0, sticky="ew", padx=30, pady=(24, 18))
		barra_busca.grid_columnconfigure(0, weight=1)
		self.campo_busca = ctk.CTkEntry(
			barra_busca,
			height=42,
			placeholder_text="Buscar por SKU ou descrição do produto...",
			font=ctk.CTkFont(family="Segoe UI", size=14),
			fg_color="#17232d",
			border_color="#334452",
			text_color="#e2e8f0",
			placeholder_text_color="#8293a1",
		)
		self.campo_busca.grid(row=0, column=0, sticky="ew", padx=(0, 12))
		self.campo_busca.bind("<Return>", lambda _evento: self.filtrar_estoque())
		ctk.CTkButton(
			barra_busca,
			text="Filtrar Estoque",
			command=self.filtrar_estoque,
			height=42,
			width=165,
			fg_color="#0e7490",
			hover_color="#155e75",
			font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
		).grid(row=0, column=1)
		self.contagem_label = ctk.CTkLabel(
			barra_busca,
			text="9 registros exibidos",
			font=ctk.CTkFont(family="Segoe UI", size=11),
			text_color="#94a3b8",
		)
		self.contagem_label.grid(row=1, column=0, columnspan=2, sticky="e", pady=(8, 0))

		area_tabela = ctk.CTkFrame(self, fg_color="#17232d", corner_radius=8, border_width=1, border_color="#293945")
		area_tabela.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
		area_tabela.grid_columnconfigure(0, weight=1)
		area_tabela.grid_rowconfigure(1, weight=1)

		colunas = [
			("SKU", 150),
			("PRODUTO", 250),
			("CATEGORIA", 175),
			("QUANTIDADE", 125),
			("TIPO", 115),
			("STATUS", 145),
		]
		cabecalho_tabela = ctk.CTkFrame(area_tabela, fg_color="#202f3a", corner_radius=0, height=44)
		cabecalho_tabela.grid(row=0, column=0, sticky="ew")
		cabecalho_tabela.grid_propagate(False)
		for indice, (titulo, largura) in enumerate(colunas):
			cabecalho_tabela.grid_columnconfigure(indice, minsize=largura, weight=1 if indice == 1 else 0)
			ctk.CTkLabel(
				cabecalho_tabela,
				text=titulo,
				anchor="w",
				font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
				text_color="#9fb0bc",
			).grid(row=0, column=indice, sticky="ew", padx=(16, 8), pady=12)

		self.lista_linhas = ctk.CTkScrollableFrame(
			area_tabela,
			fg_color="#17232d",
			corner_radius=0,
			scrollbar_button_color="#405563",
			scrollbar_button_hover_color="#5b7281",
		)
		self.lista_linhas.grid(row=1, column=0, sticky="nsew")
		for indice, (_, largura) in enumerate(colunas):
			self.lista_linhas.grid_columnconfigure(indice, minsize=largura, weight=1 if indice == 1 else 0)

		rodape = ctk.CTkFrame(self, fg_color="#17232d", corner_radius=0, height=76)
		rodape.grid(row=3, column=0, sticky="ew")
		rodape.grid_columnconfigure(0, weight=1)
		ctk.CTkLabel(
			rodape,
			text="QUANTIDADE CONSOLIDADA EM ESTOQUE",
			font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
			text_color="#94a3b8",
		).grid(row=0, column=0, sticky="e", padx=(20, 12), pady=20)
		self.total_label = ctk.CTkLabel(
			rodape,
			text="",
			font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
			text_color="#22c55e",
		)
		self.total_label.grid(row=0, column=1, sticky="w", padx=(0, 30), pady=16)

	def filtrar_estoque(self):
		termo = self.campo_busca.get().strip().casefold()
		resultados = [
			item for item in MOVIMENTACOES
			if termo in item["sku"].casefold() or termo in item["produto"].casefold()
		]
		self._renderizar_linhas(resultados)

	def _renderizar_linhas(self, itens):
		for widget in self.lista_linhas.winfo_children():
			widget.destroy()

		cores_tipo = {"Entrada": "#22c55e", "Saída": "#ef4444", "Ajuste": "#38bdf8"}
		for indice, item in enumerate(itens):
			quantidade = item["quantidade"]
			status = "Crítico" if quantidade <= 5 else "Estoque baixo" if quantidade <= 12 else "OK"
			cor_status = "#ef4444" if status == "Crítico" else "#f59e0b" if status == "Estoque baixo" else "#22c55e"
			fundo = "#192832" if indice % 2 == 0 else "#17232d"
			linha = ctk.CTkFrame(self.lista_linhas, fg_color=fundo, corner_radius=0, height=52)
			linha.grid(row=indice, column=0, columnspan=6, sticky="ew")
			linha.grid_propagate(False)
			for coluna, largura in enumerate((150, 250, 175, 125, 115, 145)):
				linha.grid_columnconfigure(coluna, minsize=largura, weight=1 if coluna == 1 else 0)

			valores = (
				(item["sku"], "#cbd5e1", True),
				(item["produto"], "#f1f5f9", True),
				(item["categoria"], "#a8b6c1", False),
				(f'{quantidade:,} un.'.replace(",", "."), cor_status, True),
				(item["tipo"], cores_tipo[item["tipo"]], True),
				(status, cor_status, True),
			)
			for coluna, (texto, cor, destaque) in enumerate(valores):
				ctk.CTkLabel(
					linha,
					text=texto,
					anchor="w",
					font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold" if destaque else "normal"),
					text_color=cor,
				).grid(row=0, column=coluna, sticky="ew", padx=(16, 8), pady=15)

		total = sum(item["quantidade"] for item in MOVIMENTACOES)
		self.total_label.configure(text=f"{total:,} un.".replace(",", "."))
		self.contagem_label.configure(text=f"{len(itens)} registro(s) exibido(s)")


if __name__ == "__main__":
	app = ControleEstoqueApp()
	app.mainloop()
