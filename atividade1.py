import tkinter as tk
from tkinter import ttk


BACKGROUND = "#0f172a"
PANEL = "#172033"
PANEL_LIGHT = "#1e293b"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
GREEN = "#22c55e"
AMBER = "#f59e0b"
RED = "#ef4444"


def centralizar_janela(janela: tk.Tk, largura: int, altura: int) -> None:
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    posicao_x = (largura_tela - largura) // 2
    posicao_y = (altura_tela - altura) // 2
    janela.geometry(f"{largura}x{altura}+{posicao_x}+{posicao_y}")


def criar_kpi(parent: tk.Frame, coluna: int, titulo: str, valor: str, cor: str) -> None:
    card = tk.Frame(parent, bg=PANEL_LIGHT, width=104, height=88,
                    highlightthickness=1, highlightbackground="#293548")
    card.grid(row=0, column=coluna, sticky="nsew", padx=4)
    card.pack_propagate(False)
    tk.Frame(card, bg=cor, height=3).pack(fill="x")
    tk.Label(card, text=valor, bg=PANEL_LIGHT, fg=TEXT, font=("Segoe UI", 19, "bold")).pack(pady=(10, 1))
    tk.Label(card, text=titulo, bg=PANEL_LIGHT, fg=MUTED, font=("Segoe UI", 8), wraplength=90, justify="center").pack(pady=(0, 10))


def criar_dashboard() -> tk.Tk:
    janela = tk.Tk()
    janela.title("Painel de Controle - Gestão de Ativos Corporativos (EAM)")
    janela.resizable(False, False)
    janela.configure(bg=BACKGROUND)
    centralizar_janela(janela, 500, 350)

    estilo = ttk.Style(janela)
    estilo.theme_use("clam")
    estilo.configure("TProgressbar", troughcolor="#263449", background=GREEN, bordercolor="#263449")

    conteudo = tk.Frame(janela, bg=BACKGROUND)
    conteudo.pack(fill="both", expand=True, padx=24, pady=20)

    cabecalho = tk.Frame(conteudo, bg=BACKGROUND)
    cabecalho.pack(fill="x")
    tk.Label(cabecalho, text="MONITORAMENTO DE ATIVOS", bg=BACKGROUND,
             fg=TEXT, font=("Segoe UI", 15, "bold")).pack(side="left")
    status = tk.Frame(cabecalho, bg="#123524", padx=8, pady=3)
    status.pack(side="right")
    tk.Label(status, text="●  ONLINE", bg="#123524", fg=GREEN,
             font=("Segoe UI", 8, "bold")).pack()
    tk.Label(conteudo, text="Visão geral da infraestrutura industrial",
             bg=BACKGROUND, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 15))

    metricas = tk.Frame(conteudo, bg=BACKGROUND)
    metricas.pack(fill="x")
    for coluna in range(4):
        metricas.columnconfigure(coluna, weight=1)

    criar_kpi(metricas, 0, "Equipamentos\ncadastrados", "248", "#38bdf8")
    criar_kpi(metricas, 1, "Ativos em\noperação", "217", GREEN)
    criar_kpi(metricas, 2, "Manutenção\npreventiva", "24", AMBER)
    criar_kpi(metricas, 3, "Equipamentos\ncríticos", "07", RED)

    painel_saude = tk.Frame(conteudo, bg=PANEL, height=106,
                            highlightthickness=1, highlightbackground="#293548")
    painel_saude.pack(fill="x", pady=(18, 0))
    painel_saude.pack_propagate(False)
    tk.Label(painel_saude, text="SAÚDE OPERACIONAL DA INFRAESTRUTURA",
             bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(pady=(11, 1))
    tk.Label(painel_saude, text="●  EXCELENTE", bg=PANEL, fg=GREEN,
             font=("Segoe UI", 19, "bold")).pack()
    barra = ttk.Progressbar(painel_saude, length=320, mode="determinate", value=92)
    barra.pack(pady=(5, 2))
    tk.Label(painel_saude, text="92% de disponibilidade operacional", bg=PANEL, fg=MUTED, font=("Segoe UI", 8)).pack(pady=(0, 12))
    tk.Label(conteudo, text="Última atualização: agora  •  Dados sincronizados", bg=BACKGROUND, fg="#64748b", font=("Segoe UI", 8)).pack(anchor="w", pady=(12, 0))

    return janela


if __name__ == "__main__":
    app = criar_dashboard()
    app.mainloop()

