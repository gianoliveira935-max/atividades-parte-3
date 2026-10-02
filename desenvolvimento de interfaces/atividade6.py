from datetime import datetime
import customtkinter as ctk

EMPRESAS = [
    {"cnpj": "12.345.678/0001-90", "razao": "TechSolutions Ltda", "segmento": "Tecnologia", "data": "10/01/2026", "status": "Ativa"},
    {"cnpj": "98.765.432/0001-10", "razao": "Logística Brasil S/A", "segmento": "Transportes", "data": "15/02/2026", "status": "Ativa"},
    {"cnpj": "45.123.890/0001-55", "razao": "Global Serviços Financeiros", "segmento": "Consultoria", "data": "01/03/2026", "status": "Em Análise"},
    {"cnpj": "33.987.111/0001-22", "razao": "Comércio de Alimentos Silva", "segmento": "Varejo", "data": "12/03/2026", "status": "Inativa"}
]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Corporate ERP - Sistema de Cadastro de Empresas")
        self.geometry("900x650")
        
        # Centralizar janela
        self.update_idletasks()
        self.geometry(f"+{(self.winfo_screenwidth()-900)//2}+{(self.winfo_screenheight()-650)//2}")

        # Título
        ctk.CTkLabel(self, text="SISTEMA DE CADASTRO E DIRETÓRIO DE EMPRESAS", font=("Arial", 16, "bold")).pack(pady=15)

        # Cadastro
        f_cad = ctk.CTkFrame(self)
        f_cad.pack(fill="x", padx=20, pady=5)
        self.e_raz = ctk.CTkEntry(f_cad, placeholder_text="Razão Social", width=250)
        self.e_raz.pack(side="left", padx=5, pady=10, expand=True)
        self.e_cnpj = ctk.CTkEntry(f_cad, placeholder_text="CNPJ (00.000.000/0000-00)", width=200)
        self.e_cnpj.pack(side="left", padx=5, pady=10, expand=True)
        self.e_seg = ctk.CTkEntry(f_cad, placeholder_text="Segmento / Atuação", width=180)
        self.e_seg.pack(side="left", padx=5, pady=10, expand=True)
        ctk.CTkButton(f_cad, text="Cadastrar Empresa", command=self.cadastrar).pack(side="left", padx=5, pady=10)

        # Filtro
        f_busca = ctk.CTkFrame(self)
        f_busca.pack(fill="x", padx=20, pady=5)
        self.e_busca = ctk.CTkEntry(f_busca, placeholder_text="Buscar por Razão Social ou CNPJ...")
        self.e_busca.pack(side="left", fill="x", expand=True, padx=10, pady=10)
        ctk.CTkButton(f_busca, text="Filtrar", command=self.filtrar).pack(side="right", padx=10, pady=10)

        # Tabela
        f_tab = ctk.CTkFrame(self)
        f_tab.pack(fill="both", expand=True, padx=20, pady=10)
        f_cab = ctk.CTkFrame(f_tab, fg_color="#1f2937", height=30)
        f_cab.pack(fill="x")
        for col in ["CNPJ", "Razão Social", "Segmento", "Data Cadastro", "Status"]:
            ctk.CTkLabel(f_cab, text=col, font=("Arial", 11, "bold")).pack(side="left", expand=True, fill="x")

        self.scroll = ctk.CTkScrollableFrame(f_tab)
        self.scroll.pack(fill="both", expand=True)

        # Rodapé
        self.lbl_rod = ctk.CTkLabel(self, text="", font=("Arial", 12, "bold"), text_color="#38bdf8")
        self.lbl_rod.pack(pady=10)

        self.atualizar(EMPRESAS)

    def atualizar(self, lista):
        for w in self.scroll.winfo_children():
            w.destroy()
        cores = {"Ativa": "#22c55e", "Em Análise": "#f59e0b", "Inativa": "#ef4444"}
        for e in lista:
            row = ctk.CTkFrame(self.scroll, height=35)
            row.pack(fill="x", pady=2)
            vals = [e["cnpj"], e["razao"], e["segmento"], e["data"], e["status"]]
            for i, v in enumerate(vals):
                ctk.CTkLabel(row, text=v, text_color=cores.get(v, "#f1f5f9") if i == 4 else "#f1f5f9").pack(side="left", expand=True, fill="x")
        self.lbl_rod.configure(text=f"Total de Empresas Listadas: {len(lista)} registro(s)")

    def cadastrar(self):
        r, c, s = self.e_raz.get(), self.e_cnpj.get(), self.e_seg.get()
        if r and c and s:
            EMPRESAS.append({"cnpj": c, "razao": r, "segmento": s, "data": datetime.now().strftime("%d/%m/%Y"), "status": "Ativa"})
            self.e_raz.delete(0, 'end'); self.e_cnpj.delete(0, 'end'); self.e_seg.delete(0, 'end')
            self.atualizar(EMPRESAS)

    def filtrar(self):
        t = self.e_busca.get().lower()
        self.atualizar([e for e in EMPRESAS if t in e["razao"].lower() or t in e["cnpj"].lower()] if t else EMPRESAS)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    App().mainloop()