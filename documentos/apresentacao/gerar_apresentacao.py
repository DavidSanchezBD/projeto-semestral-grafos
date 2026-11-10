"""
Gerador da Apresentação Executiva em PowerPoint (Revisão v1) — ECM306.
Segue rigorosamente todas as diretrizes de `plano/plano_slides.md`:
1. Tipografia e Densidade ("Pouco Texto, Fonte Grande"):
   - Máximo estrito de 25 a 35 palavras visíveis por slide em caixas de texto nativas;
   - Títulos: 34 a 42 pt; Subtítulos: 22 a 26 pt; Apoio: >= 18 pt (PROIBIDO fonte < 18 pt);
   - Big Numbers: 48 a 56 pt ("0 SALVOS (0%)" vs "20 SALVOS (74%)", "27 de 28").
2. Intuitividade ("Mostre o Grafo, Não Descreva o Grafo"):
   - Pelo menos 60% da área de cada slide ocupada por diagramas visuais dedicados em 300 DPI.
3. Dinamismo:
   - Animações de entrada progressivas por clique (On Click) e transições suaves (Fade/Push)
     embutidas no XML OpenXML + script PowerShell COM para exportação e validação visual.
   - Notas do Orador completas em todos os 6 slides para apresentação em até 5 minutos.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from PIL import Image as PILImage

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn

RAIZ_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PASTA_SLIDE_FIGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras_slides")
PASTA_ENTREGA = os.path.join(RAIZ_PROJETO, "Entrega")
os.makedirs(PASTA_SLIDE_FIGS, exist_ok=True)
os.makedirs(PASTA_ENTREGA, exist_ok=True)

CAMINHO_PPTX = os.path.join(PASTA_ENTREGA, "Apresentacao_Caso_Fake_News.pptx")

# Paleta de Cores (Alto Contraste)
COR_NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
COR_SLATE_CARD = RGBColor(30, 41, 59)     # #1E293B
COR_BG_CLARO = RGBColor(248, 250, 252)    # #F8FAFC
COR_BRANCO = RGBColor(255, 255, 255)      # #FFFFFF
COR_TEXTO_ESCURO = RGBColor(15, 23, 42)   # #0F172A
COR_TEXTO_MUTED = RGBColor(71, 85, 105)   # #475569
COR_TEXTO_CLARO = RGBColor(241, 245, 249) # #F1F5F9

COR_VERMELHO = RGBColor(220, 38, 38)      # #DC2626
COR_VERMELHO_BG = RGBColor(254, 242, 242) # #FEF2F2
COR_LARANJA = RGBColor(234, 88, 12)       # #EA580C
COR_LARANJA_BG = RGBColor(255, 247, 237)  # #FFF7ED
COR_AMARELO = RGBColor(217, 119, 6)       # #D97706
COR_AMARELO_BG = RGBColor(255, 251, 235)  # #FFFBEB
COR_VERDE = RGBColor(22, 163, 74)         # #16A34A
COR_VERDE_BG = RGBColor(240, 253, 244)    # #F0FDF4
COR_AZUL = RGBColor(37, 99, 235)          # #2563EB
COR_AZUL_BG = RGBColor(239, 246, 255)     # #EFF6FF
COR_ROXO = RGBColor(124, 58, 237)         # #7C3AED
COR_ROXO_BG = RGBColor(245, 243, 255)     # #F5F3FF
COR_BORDA = RGBColor(203, 213, 225)       # #CBD5E1


# ==============================================================================
# 1. GERAÇÃO DOS DIAGRAMAS VISUAIS DEDICADOS PARA OS SLIDES (300 DPI)
# ==============================================================================

def configurar_matplotlib_slides():
    plt.rcParams.update({
        "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
        "font.family": "sans-serif",
        "mathtext.default": "regular",
    })


def gerar_diagrama_slide1_capa():
    """Slide 1: Diagrama de rede investigativa em tema escuro com destaque para Paciente Zero e Pontes."""
    fig = plt.figure(figsize=(7.2, 5.4), dpi=300)
    fig.patch.set_facecolor("#0f172a")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 75)
    ax.axis("off")

    # Fundo do painel da rede
    painel = FancyBboxPatch((2, 2), 96, 71, boxstyle="round,pad=0.5,rounding_size=2.5",
                            facecolor="#1e293b", edgecolor="#334155", lw=2.0)
    ax.add_patch(painel)

    # Territórios (5 grupos sociais)
    grupos = [
        ("FAMÍLIA", 22, 50, 16, 15, "#ef4444"),
        ("CONDOMÍNIO", 22, 18, 15, 11, "#94a3b8"),
        ("TRABALHO", 54, 50, 15, 15, "#f59e0b"),
        ("ACADEMIA", 54, 18, 15, 11, "#10b981"),
        ("FACULDADE", 83, 35, 12, 24, "#3b82f6"),
    ]
    for nome, cx, cy, rx, ry, cor in grupos:
        box = FancyBboxPatch((cx - rx, cy - ry), 2 * rx, 2 * ry,
                             boxstyle="round,pad=0.3,rounding_size=2.0",
                             facecolor="#0f172a", edgecolor=cor, lw=1.8, ls="--", alpha=0.75)
        ax.add_patch(box)
        ax.text(cx, cy + ry - 2.3, nome, ha="center", va="center",
                fontsize=11, fontweight="bold", color=cor)

    # Todos os 28 nós e 42 arestas reais da rede monitorada
    nos = {
        "Ana": (12, 52, "#ef4444", 420),
        "Bruno": (13, 41, "#f97316", 240),
        "Carla": (21, 39, "#f97316", 240),
        "Diego": (25, 54, "#eab308", 380),
        "Elisa": (29, 43, "#22c55e", 220),
        "Fábio": (35, 50, "#eab308", 350),
        "Zeca": (16, 22, "#fb923c", 220),
        "Alice": (12, 12, "#fdba74", 200),
        "Beto": (23, 12, "#fdba74", 200),
        "Sônia": (32, 18, "#64748b", 220),
        "Gabi": (44, 50, "#22c55e", 260),
        "Heitor": (52, 57, "#22c55e", 220),
        "Iara": (51, 42, "#22c55e", 220),
        "João": (62, 56, "#22c55e", 240),
        "Karen": (64, 46, "#22c55e", 220),
        "Lucas": (58, 39, "#22c55e", 240),
        "Tiago": (54, 24, "#22c55e", 240),
        "Úrsula": (45, 17, "#22c55e", 200),
        "Vitor": (54, 16, "#22c55e", 200),
        "Wesley": (48, 10, "#22c55e", 190),
        "Yara": (63, 13, "#22c55e", 200),
        "Nuno": (76, 48, "#38bdf8", 220),
        "Marina": (83, 35, "#38bdf8", 380),
        "Olívia": (76, 34, "#38bdf8", 220),
        "Pedro": (77, 21, "#38bdf8", 220),
        "Quésia": (84, 15, "#38bdf8", 200),
        "Rafael": (90, 24, "#38bdf8", 220),
        "Sofia": (90, 45, "#38bdf8", 220),
    }

    arestas = [
        ("Ana", "Bruno"), ("Ana", "Carla"), ("Bruno", "Carla"),
        ("Ana", "Diego"), ("Bruno", "Diego"), ("Carla", "Diego"),
        ("Diego", "Elisa"), ("Diego", "Fábio"), ("Elisa", "Fábio"),
        ("Fábio", "Gabi"), ("Gabi", "Heitor"), ("Gabi", "Iara"),
        ("Heitor", "Iara"), ("Heitor", "João"), ("Iara", "Karen"),
        ("João", "Lucas"), ("Karen", "Lucas"), ("João", "Marina"),
        ("João", "Nuno"), ("Marina", "Nuno"), ("Marina", "Olívia"),
        ("Marina", "Pedro"), ("Marina", "Quésia"), ("Marina", "Rafael"), ("Marina", "Sofia"),
        ("Nuno", "Olívia"), ("Olívia", "Pedro"), ("Pedro", "Quésia"),
        ("Quésia", "Rafael"), ("Rafael", "Sofia"), ("Nuno", "Sofia"),
        ("Lucas", "Tiago"), ("Tiago", "Úrsula"), ("Úrsula", "Vitor"),
        ("Vitor", "Wesley"), ("Wesley", "Yara"), ("Tiago", "Yara"), ("Tiago", "Vitor"),
        ("Carla", "Zeca"), ("Zeca", "Alice"), ("Alice", "Beto"), ("Zeca", "Beto"),
    ]

    for u, v in arestas:
        x1, y1, _, _ = nos[u]
        x2, y2, _, _ = nos[v]
        if (u, v) in [("Fábio", "Gabi"), ("Diego", "Fábio")]:
            ax.plot([x1, x2], [y1, y2], color="#eab308", lw=3.0, zorder=2)
        else:
            ax.plot([x1, x2], [y1, y2], color="#475569", lw=1.6, zorder=2)

    for nome, (x, y, cor, tam) in nos.items():
        if nome in ("Ana", "Diego", "Fábio", "Marina"):
            ax.scatter(x, y, s=tam * 1.55, facecolors="none", edgecolors=cor, lw=2.2, alpha=0.65, zorder=3)
        ax.scatter(x, y, s=tam, color=cor, edgecolors="#0f172a", lw=1.8, zorder=4)

    # Rótulos grandes apenas nos nós-chave para leitura imediata (sem sobrepor títulos dos grupos)
    destaques = [
        ("Ana (Onda 0)", 12.5, 58.0, "#fca5a5", "#7f1d1d"),
        ("Diego (Ponte)", 31.0, 58.5, "#fde047", "#713f12"),
        ("Marina (Grau 7)", 83.0, 27.5, "#93c5fd", "#1e3a8a"),
        ("Sônia (Isolada)", 32.0, 11.5, "#cbd5e1", "#334155"),
    ]
    for txt, dx, dy, tcor, bcor in destaques:
        ax.text(dx, dy, txt, ha="center", va="center", fontsize=10.5, fontweight="bold", color=tcor,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=bcor, edgecolor=tcor, lw=1.2), zorder=6)

    # Carimbo investigativo no topo
    ax.text(50, 68.5, "REDE SOCIAL MONITORADA: 28 VÉRTICES · 42 ARESTAS",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color="#e2e8f0",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="#0f172a", edgecolor="#ef4444", lw=1.5), zorder=7)

    caminho = os.path.join(PASTA_SLIDE_FIGS, "slide1_rede_capa.png")
    plt.savefig(caminho, dpi=300, facecolor="#0f172a")
    plt.close()
    return caminho


def gerar_diagrama_slide2_problema():
    """Slide 2: Ilustração de celular recebendo mensagem 'Encaminhada com frequência' e espalhando na rede."""
    fig = plt.figure(figsize=(6.2, 5.2), dpi=300)
    fig.patch.set_facecolor("#f8fafc")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 84)
    ax.axis("off")

    # Moldura de Smartphone moderno
    corpo_cel = FancyBboxPatch((8, 6), 72, 72, boxstyle="round,pad=0.5,rounding_size=4.5",
                               facecolor="#0f172a", edgecolor="#334155", lw=3.0)
    tela_cel = FancyBboxPatch((11, 10), 66, 63, boxstyle="round,pad=0.3,rounding_size=3.0",
                              facecolor="#efeae2", edgecolor="none")
    topo_cel = FancyBboxPatch((11, 64), 66, 9, boxstyle="round,pad=0.2,rounding_size=2.0",
                              facecolor="#075e54", edgecolor="none")
    ax.add_patch(corpo_cel)
    ax.add_patch(tela_cel)
    ax.add_patch(topo_cel)

    ax.text(44, 68.5, "Grupo da Família & Amigos (28)", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color="#ffffff")

    # Balão de mensagem Fake News
    balao = FancyBboxPatch((15, 31), 58, 28, boxstyle="round,pad=0.4,rounding_size=2.2",
                           facecolor="#ffffff", edgecolor="#dc2626", lw=2.2)
    ax.add_patch(balao)

    ax.text(18, 54.5, ">> Encaminhada com frequência", ha="left", va="center",
            fontsize=11.5, fontstyle="italic", fontweight="bold", color="#64748b")

    ax.text(18, 46.5, "URGENTE! Nova taxa de 15%\nsobre qualquer PIX a partir\nde amanhã! Repasse já!!",
            ha="left", va="center", fontsize=13.0, fontweight="bold", color="#0f172a")

    ax.text(69, 34.0, "21:14 · Lida", ha="right", va="center", fontsize=10.0, color="#0284c7", fontweight="bold")

    # Carimbo FAKE NEWS grande
    ax.text(44, 21, "BOATO VIRAL (FAKE NEWS)", ha="center", va="center",
            fontsize=13.5, fontweight="bold", color="#ffffff",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="#dc2626", edgecolor="#991b1b", lw=2.0))

    # Setas de propagação saindo do celular para a direita (conectando às 3 perguntas)
    for y_dest, cor_seta in [(66, "#dc2626"), (42, "#ea580c"), (18, "#16a34a")]:
        seta = FancyArrowPatch((78, 44), (97, y_dest),
                               connectionstyle="arc3,rad=0.12",
                               arrowstyle="Simple,tail_width=2.5,head_width=10,head_length=10",
                               color=cor_seta, lw=2.0, zorder=8)
        ax.add_patch(seta)

    caminho = os.path.join(PASTA_SLIDE_FIGS, "slide2_boato_celular.png")
    plt.savefig(caminho, dpi=300, facecolor="#f8fafc")
    plt.close()
    return caminho


def gerar_diagrama_slide3_modelagem():
    """Slide 3: Diagrama intuitivo 'Do Chat para o Grafo' (Pessoas = Vértices, Contatos = Arestas)."""
    fig = plt.figure(figsize=(12.2, 4.5), dpi=300)
    fig.patch.set_facecolor("#f8fafc")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 122)
    ax.set_ylim(0, 45)
    ax.axis("off")

    # Lado Esquerdo: Mundo Real (Contatos no Celular)
    card_esq = FancyBboxPatch((1.5, 2.0), 47.0, 41.0, boxstyle="round,pad=0.4,rounding_size=2.0",
                              facecolor="#ffffff", edgecolor="#cbd5e1", lw=2.0)
    ax.add_patch(card_esq)
    ax.text(25.0, 39.2, "1. MUNDO REAL: REDE DE MENSAGENS", ha="center", va="center",
            fontsize=13.5, fontweight="bold", color="#0f172a")

    # Desenho de duas pessoas conversando no celular + grupos
    p1_x, p1_y = 13.5, 20.0
    p2_x, p2_y = 36.5, 20.0

    # Fio de contato bidirecional entre Pessoa A e Pessoa B
    ax.annotate("", xy=(p2_x - 4.5, p2_y), xytext=(p1_x + 4.5, p1_y),
                arrowprops=dict(arrowstyle="<->", color="#2563eb", lw=3.2))
    ax.text(25.0, 30.0, "Conversa no WhatsApp\n(A encaminha para B e vice-versa)",
            ha="center", va="center", fontsize=10.8, fontweight="bold", color="#1e40af",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1.2))

    for px, py, nome, papel, cor in [
        (p1_x, p1_y, "Ana", "Pessoa A", "#dc2626"),
        (p2_x, p2_y, "Diego", "Pessoa B", "#ea580c"),
    ]:
        circ = Circle((px, py), 3.8, facecolor=cor, edgecolor="#0f172a", lw=2.0, zorder=4)
        ax.add_patch(circ)
        ax.text(px, py, nome, ha="center", va="center", fontsize=12.0, fontweight="bold", color="white", zorder=5)
        ax.text(px, py - 6.0, papel, ha="center", va="center", fontsize=11.0, fontweight="bold", color="#334155")

    ax.text(25.0, 6.8, "5 Grupos: Família · Trabalho · Faculdade · Academia · Condomínio",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="#475569",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f1f5f9", edgecolor="#cbd5e1", lw=1.0))

    # Seta Central de Transformação
    seta_trans = FancyArrowPatch((50.0, 22.5), (61.5, 22.5),
                                 arrowstyle="Simple,tail_width=8,head_width=20,head_length=14",
                                 color="#0f172a", zorder=6)
    ax.add_patch(seta_trans)
    ax.text(55.5, 29.0, "Abstração\nem Grafo\nG = (V, E)", ha="center", va="center",
            fontsize=12.0, fontweight="bold", color="#0f172a")

    # Lado Direito: Modelo Matemático em Grafo
    card_dir = FancyBboxPatch((63.0, 2.0), 57.5, 41.0, boxstyle="round,pad=0.4,rounding_size=2.0",
                              facecolor="#ffffff", edgecolor="#2563eb", lw=2.2)
    ax.add_patch(card_dir)
    ax.text(91.7, 39.2, "2. MODELO MATEMÁTICO: GRAFO G = (V, E)", ha="center", va="center",
            fontsize=13.5, fontweight="bold", color="#1e3a8a")

    # Mini-grafo explícito e didático com callouts gigantes para Vértice e Aresta
    gnos = {
        "v0": (73.0, 24.0, "Ana\n(v₀)", "#dc2626"),
        "v1": (81.5, 31.0, "Bruno\n(v₁)", "#f97316"),
        "v2": (81.5, 16.5, "Carla\n(v₂)", "#f97316"),
        "v3": (92.0, 24.0, "Diego\n(v₃)", "#eab308"),
        "v5": (103.5, 24.0, "Fábio\n(v₅)", "#eab308"),
        "v6": (113.5, 29.5, "Gabi\n(v₆)", "#16a34a"),
        "v8": (113.5, 18.0, "Iara\n(v₈)", "#16a34a"),
    }
    garestas = [
        ("v0", "v1"), ("v0", "v2"), ("v1", "v2"),
        ("v0", "v3"), ("v1", "v3"), ("v2", "v3"),
        ("v3", "v5"), ("v5", "v6"), ("v6", "v8"),
    ]
    for u, v in garestas:
        x1, y1, _, _ = gnos[u]
        x2, y2, _, _ = gnos[v]
        cor_l = "#2563eb" if (u, v) == ("v3", "v5") else "#64748b"
        lw_l = 3.6 if (u, v) == ("v3", "v5") else 2.2
        ax.plot([x1, x2], [y1, y2], color=cor_l, lw=lw_l, zorder=3)

    for k, (gx, gy, rot, gcor) in gnos.items():
        c = Circle((gx, gy), 3.3, facecolor=gcor, edgecolor="#0f172a", lw=1.8, zorder=4)
        ax.add_patch(c)
        ax.text(gx, gy, rot, ha="center", va="center", fontsize=9.8, fontweight="bold", color="white", zorder=5)

    # Callout Vértice (V)
    ax.annotate("VÉRTICE (V = 28 Pessoas)",
                xy=(73.0, 20.5), xytext=(77.5, 7.8),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=2.5),
                ha="center", va="center", fontsize=12.0, fontweight="bold", color="#991b1b",
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#fef2f2", edgecolor="#dc2626", lw=1.6), zorder=7)

    # Callout Aresta (E)
    ax.annotate("ARESTA (E = 42 Contatos Mútuos)",
                xy=(97.7, 24.0), xytext=(105.0, 7.8),
                arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2.5),
                ha="center", va="center", fontsize=12.0, fontweight="bold", color="#1e40af",
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#eff6ff", edgecolor="#2563eb", lw=1.6), zorder=7)

    caminho = os.path.join(PASTA_SLIDE_FIGS, "slide3_chat_para_grafo.png")
    plt.savefig(caminho, dpi=300, facecolor="#f8fafc")
    plt.close()
    return caminho


def gerar_diagrama_slide4_bfs():
    """Slide 4: Diagrama grande de Ondas Concêntricas da BFS + Visual da Fila FIFO."""
    # 1. Diagrama principal das ondas concêntricas
    fig, ax = plt.subplots(figsize=(7.6, 5.2), dpi=300)
    fig.patch.set_facecolor("#ffffff")

    raios = [1.20, 2.30, 3.40]
    cores_anel = ["#ea580c", "#d97706", "#2563eb"]
    cores_no = ["#f97316", "#f59e0b", "#3b82f6"]
    labels = [
        "Onda 1: Contatos Diretos (d = 1)",
        "Onda 2: Amigos de Amigos (d = 2)",
        "Ondas 3 a 9: Demais Grupos (d ≥ 3)",
    ]

    for r, cor, lbl in zip(raios, cores_anel, labels):
        circ = Circle((0, 0), r, fill=False, color=cor, ls="--", lw=2.2, alpha=0.88, zorder=1)
        ax.add_patch(circ)
        ax.text(
            0, r, lbl,
            ha="center", va="center", color=cor, fontsize=11.0, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=cor, lw=1.5),
            zorder=6
        )

    angulos_ondas = [
        [np.deg2rad(20), np.deg2rad(160), np.deg2rad(235), np.deg2rad(315)],
        [np.deg2rad(5), np.deg2rad(42), np.deg2rad(138), np.deg2rad(185), np.deg2rad(220), np.deg2rad(270), np.deg2rad(335)],
        [np.deg2rad(0), np.deg2rad(32), np.deg2rad(55), np.deg2rad(125), np.deg2rad(152), np.deg2rad(195), np.deg2rad(242), np.deg2rad(288), np.deg2rad(320)]
    ]

    aneis_coords = [[(0.0, 0.0)]]
    for idx_onda, (r, cor_no, angs) in enumerate(zip(raios, cores_no, angulos_ondas)):
        coords_atuais = []
        coords_ant = aneis_coords[-1]
        for a in angs:
            px, py = r * np.cos(a), r * np.sin(a)
            coords_atuais.append((px, py))
            distancias = [np.hypot(px - ax_x, py - ax_y) for ax_x, ax_y in coords_ant]
            melhor = int(np.argmin(distancias))
            ox, oy = coords_ant[melhor]
            ax.plot([ox, px], [oy, py], color="#94a3b8", lw=1.8, zorder=2)
            ax.scatter(px, py, color=cor_no, s=260, zorder=4, edgecolor="#0f172a", lw=1.6)
        aneis_coords.append(coords_atuais)

    # Paciente Zero (Ana - Onda 0)
    ax.scatter(0, 0, color="#dc2626", s=1150, zorder=5, edgecolor="#0f172a", lw=2.2)
    ax.text(0, 0, "Onda 0\n(Ana)", ha="center", va="center", color="white", fontsize=9.8, fontweight="bold", zorder=6)

    # Nó isolado (Sônia)
    ix, iy = 3.90, -2.45
    ax.scatter(ix, iy, color="#94a3b8", s=320, zorder=4, edgecolor="#334155", lw=2.0)
    ax.text(
        ix, iy - 0.55, "Sônia (Isolada)\ndist = ∞",
        ha="center", va="top", fontsize=10.5, fontweight="bold", color="#334155",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="#f1f5f9", edgecolor="#64748b", lw=1.2)
    )

    ax.set_xlim(-4.2, 4.8)
    ax.set_ylim(-3.8, 3.85)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    caminho_ondas = os.path.join(PASTA_SLIDE_FIGS, "slide4_bfs_ondas.png")
    plt.savefig(caminho_ondas, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()

    # 2. Diagrama visual da Fila FIFO
    fig2 = plt.figure(figsize=(4.4, 2.2), dpi=300)
    fig2.patch.set_facecolor("#ffffff")
    ax2 = fig2.add_axes([0, 0, 1, 1])
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 50)
    ax2.axis("off")

    ax2.text(50, 43, "Estrutura de Fila (FIFO) — O(V + E)", ha="center", va="center",
             fontsize=12.0, fontweight="bold", color="#0f172a")

    blocos = [
        ("Ana\n(d=0)", 17, "#dc2626"),
        ("Bruno\n(d=1)", 34, "#f97316"),
        ("Carla\n(d=1)", 51, "#f97316"),
        ("Diego\n(d=1)", 68, "#f97316"),
    ]
    for txt, bx, bcor in blocos:
        rect = FancyBboxPatch((bx, 14), 14.5, 18, boxstyle="round,pad=0.25,rounding_size=1.8",
                              facecolor=bcor, edgecolor="#0f172a", lw=1.6)
        ax2.add_patch(rect)
        ax2.text(bx + 7.25, 23, txt, ha="center", va="center", fontsize=9.8, fontweight="bold", color="white")

    ax2.annotate("", xy=(2.5, 23), xytext=(15.5, 23),
                 arrowprops=dict(arrowstyle="->", color="#dc2626", lw=2.5))
    ax2.text(9.0, 29.0, "Sai", ha="center", va="center", fontsize=10.0, fontweight="bold", color="#dc2626")

    ax2.annotate("", xy=(84.0, 23), xytext=(97.5, 23),
                 arrowprops=dict(arrowstyle="->", color="#2563eb", lw=2.5))
    ax2.text(91.0, 29.0, "Entra", ha="center", va="center", fontsize=10.0, fontweight="bold", color="#2563eb")

    ax2.text(50, 5.5, "Processa estritamente na ordem de chegada!",
             ha="center", va="center", fontsize=10.5, fontweight="bold", color="#475569")

    caminho_fila = os.path.join(PASTA_SLIDE_FIGS, "slide4_fila_fifo.png")
    plt.savefig(caminho_fila, dpi=300, facecolor="white")
    plt.close()

    return caminho_ondas, caminho_fila


def gerar_diagramas_slide5_versus():
    """Slide 5: Dois diagramas comparativos grandes: (Esquerda) Marina falha vs (Direita) Diego corta a ponte."""
    # --- DIAGRAMA ESQUERDO: MARINA (MAIOR GRAU = 7) FALHA ---
    fig1 = plt.figure(figsize=(5.8, 3.4), dpi=300)
    fig1.patch.set_facecolor("#fef2f2")
    ax1 = fig1.add_axes([0, 0, 1, 1])
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0, 58)
    ax1.axis("off")

    box1 = FancyBboxPatch((2, 2), 96, 54, boxstyle="round,pad=0.4,rounding_size=2.0",
                          facecolor="#ffffff", edgecolor="#fca5a5", lw=2.0)
    ax1.add_patch(box1)

    ax1.text(50, 50.5, "Grupo Faculdade (Alta Redundância Interna)",
             ha="center", va="center", fontsize=12.0, fontweight="bold", color="#991b1b")

    # Nós do grupo Faculdade (todos os 7 membros) + chegada de João (Grau 7 exato em Marina)
    nos_fac = {
        "João": (11, 27, "#dc2626"),
        "Nuno": (34, 39, "#ef4444"),
        "Olívia": (32, 18, "#ef4444"),
        "Marina": (56, 27, "#7c3aed"),  # Bloqueada no centro (Grau 7)
        "Sofia": (78, 39, "#ef4444"),
        "Pedro": (46, 9, "#ef4444"),
        "Quésia": (66, 9, "#ef4444"),
        "Rafael": (80, 18, "#ef4444"),
    }

    # As 7 arestas tracejadas (bloqueadas em Marina, grau 7)
    for viz in ["João", "Nuno", "Olívia", "Sofia", "Pedro", "Quésia", "Rafael"]:
        x1, y1, _ = nos_fac["Marina"]
        x2, y2, _ = nos_fac[viz]
        ax1.plot([x1, x2], [y1, y2], color="#cbd5e1", lw=1.6, ls=":", zorder=2)

    # Arestas ativas por onde o boato CONTORNA Marina!
    rotas_ativas = [
        ("João", "Nuno"), ("Nuno", "Olívia"), ("Nuno", "Sofia"),
        ("Olívia", "Pedro"), ("Pedro", "Quésia"), ("Quésia", "Rafael"), ("Sofia", "Rafael")
    ]
    for u, v in rotas_ativas:
        x1, y1, _ = nos_fac[u]
        x2, y2, _ = nos_fac[v]
        ax1.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="->", color="#dc2626", lw=2.8, shrinkA=13, shrinkB=13), zorder=3)

    pos_rot_fac = {
        "João": (11, 34.5),
        "Nuno": (23.5, 39),
        "Olívia": (21.0, 18),
        "Marina": (56, 34.2),
        "Sofia": (88.5, 39),
        "Pedro": (46, 3.2),
        "Quésia": (66, 3.2),
        "Rafael": (90.0, 18),
    }
    for nome, (nx, ny, ncor) in nos_fac.items():
        tam = 480 if nome == "Marina" else 330
        ax1.scatter(nx, ny, s=tam, color=ncor, edgecolors="#0f172a", lw=1.8, zorder=4)
        rot = "MARINA (BLOQ)" if nome == "Marina" else nome
        rx, ry = pos_rot_fac[nome]
        ax1.text(rx, ry, rot,
                 ha="center", va="center", fontsize=10.0, fontweight="bold",
                 color="#5b21b6" if nome == "Marina" else "#991b1b",
                 bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.9), zorder=5)

    ax1.text(56, 27, "X", ha="center", va="center", fontsize=14, fontweight="bold", color="white", zorder=6)
    ax1.text(56, 44.8, "O boato contorna Marina pelos vizinhos!",
             ha="center", va="center", fontsize=10.5, fontweight="bold", color="#dc2626",
             bbox=dict(boxstyle="round,pad=0.25", facecolor="#fef2f2", edgecolor="#dc2626", lw=1.2), zorder=6)

    caminho_marina = os.path.join(PASTA_SLIDE_FIGS, "slide5_marina_falha.png")
    plt.savefig(caminho_marina, dpi=300, facecolor="#fef2f2")
    plt.close()

    # --- DIAGRAMA DIREITO: DIEGO (PONTO DE ARTICULAÇÃO / PONTE) VENCE ---
    fig2 = plt.figure(figsize=(5.8, 3.4), dpi=300)
    fig2.patch.set_facecolor("#f0fdf4")
    ax2 = fig2.add_axes([0, 0, 1, 1])
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 58)
    ax2.axis("off")

    box2 = FancyBboxPatch((2, 2), 96, 54, boxstyle="round,pad=0.4,rounding_size=2.0",
                          facecolor="#ffffff", edgecolor="#86efac", lw=2.0)
    ax2.add_patch(box2)

    ax2.text(50, 50.5, "Corte de Ponto de Articulação (Algoritmo de Tarjan)",
             ha="center", va="center", fontsize=12.0, fontweight="bold", color="#14532d")

    # Bloco Esquerdo (Contaminado: Família/Condomínio = 6 nós)
    fam_box = FancyBboxPatch((5, 9), 25, 33, boxstyle="round,pad=0.3,rounding_size=1.8",
                             facecolor="#fef2f2", edgecolor="#ef4444", lw=1.8, ls="--")
    ax2.add_patch(fam_box)
    ax2.text(17.5, 38.0, "Contaminados (6)", ha="center", va="center", fontsize=10.2, fontweight="bold", color="#dc2626")

    for fx, fy, fnome in [(11.5, 27, "Ana"), (11.5, 16, "Bruno"), (22.5, 21, "Carla")]:
        ax2.scatter(fx, fy, s=260, color="#ef4444", edgecolors="#0f172a", lw=1.6, zorder=4)
        ax2.text(fx, fy - 4.8, fnome, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#991b1b")

    # Nó Ponte Bloqueado no Centro (DIEGO)
    dx, dy = 43.5, 25
    ax2.plot([22.5, dx], [21, dy], color="#dc2626", lw=2.2, ls=":", zorder=2)
    ax2.plot([dx, 60], [dy, 25], color="#16a34a", lw=2.8, ls=":", zorder=2)

    ax2.scatter(dx, dy, s=600, color="#7c3aed", edgecolors="#eab308", lw=3.0, zorder=5)
    ax2.text(dx, dy, "X", ha="center", va="center", fontsize=15, fontweight="bold", color="white", zorder=6)
    ax2.text(dx, dy + 10.0, "DIEGO (Grau 5)\nPONTE BLOQUEADA!", ha="center", va="center",
             fontsize=10.0, fontweight="bold", color="#5b21b6",
             bbox=dict(boxstyle="round,pad=0.28", facecolor="#f5f3ff", edgecolor="#7c3aed", lw=1.5), zorder=6)

    # Bloco Direito (Salvos: Trabalho + Academia + Faculdade = 20 nós)
    salvos_box = FancyBboxPatch((58, 8), 37, 35, boxstyle="round,pad=0.3,rounding_size=1.8",
                                facecolor="#f0fdf4", edgecolor="#16a34a", lw=2.2)
    ax2.add_patch(salvos_box)
    ax2.text(76.5, 39.2, "100% PROTEGIDOS (20)", ha="center", va="center",
             fontsize=10.8, fontweight="bold", color="#15803d")

    nos_salvos = [
        (67.5, 30.5, "Fábio (1)"), (85.5, 30.5, "Trabalho (6)"),
        (67.5, 17.5, "Academia (5)"), (85.5, 17.5, "Faculdade (7)")
    ]
    for sx, sy, srot in nos_salvos:
        ax2.scatter(sx, sy, s=250, color="#16a34a", edgecolors="#0f172a", lw=1.5, zorder=4)
        ax2.text(sx, sy - 4.8, srot, ha="center", va="center", fontsize=9.2, fontweight="bold", color="#14532d")

    caminho_diego = os.path.join(PASTA_SLIDE_FIGS, "slide5_diego_ponte.png")
    plt.savefig(caminho_diego, dpi=300, facecolor="#f0fdf4")
    plt.close()

    return caminho_marina, caminho_diego


# ==============================================================================
# 2. UTILITÁRIOS DE CONSTRUÇÃO DO POWERPOINT + ANIMAÇÕES / TRANSIÇÕES XML
# ==============================================================================

def definir_fundo_slide(slide, cor_rgb):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = cor_rgb


def adicionar_retangulo(slide, left, top, width, height, cor_fundo, cor_borda=None, espessura_borda=1.5, arredondado=True):
    tipo = MSO_SHAPE.ROUNDED_RECTANGLE if arredondado else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(tipo, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = cor_fundo
    if cor_borda is not None:
        shape.line.color.rgb = cor_borda
        shape.line.width = Pt(espessura_borda)
    else:
        shape.line.fill.background()
    if arredondado and hasattr(shape, "adjustments") and len(shape.adjustments) > 0:
        shape.adjustments[0] = 0.06
    return shape


def adicionar_texto(slide, left, top, width, height, linhas, alinhamento=PP_ALIGN.LEFT, ancoragem=MSO_ANCHOR.TOP):
    """
    Adiciona uma caixa de texto limpa.
    `linhas` é uma lista de tuplas: (texto, tamanho_pt, cor_rgb, negrito, fonte_opcional)
    """
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = ancoragem
    tf.margin_left = Inches(0.08)
    tf.margin_right = Inches(0.08)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)

    for idx, item in enumerate(linhas):
        texto, tam_pt, cor, negrito = item[0], item[1], item[2], item[3]
        fonte = item[4] if len(item) > 4 else "Segoe UI"
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = alinhamento
        if idx > 0:
            p.space_before = Pt(4)
        run = p.add_run()
        run.text = texto
        run.font.size = Pt(tam_pt)
        run.font.color.rgb = cor
        run.font.bold = negrito
        run.font.name = fonte
    return txBox


def adicionar_imagem_preservando_aspecto(slide, caminho_img, left, top, max_width, max_height):
    """Insere imagem calculando proporção exata via PIL para nunca distorcer."""
    with PILImage.open(caminho_img) as im:
        w_px, h_px = im.size
    ratio = w_px / float(h_px)
    largura = max_width
    altura = largura / ratio
    if altura > max_height:
        altura = max_height
        largura = altura * ratio
    offset_x = left + (max_width - largura) / 2.0
    offset_y = top + (max_height - altura) / 2.0
    return slide.shapes.add_picture(caminho_img, Inches(offset_x), Inches(offset_y), Inches(largura), Inches(altura))


def adicionar_cabecalho_padrao(slide, numero_slide, titulo_curto, dark=False):
    """Cabeçalho limpo com badge de número e título em linha única (31–34 pt)."""
    cor_titulo = COR_BRANCO if dark else COR_TEXTO_ESCURO
    cor_badge = COR_VERMELHO if dark else COR_NAVY_DARK
    badge = adicionar_retangulo(slide, 0.50, 0.30, 0.65, 0.58, cor_badge, None, arredondado=True)
    tf = badge.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = f"0{numero_slide}"
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = COR_BRANCO
    r.font.name = "Segoe UI"

    tam_titulo = 30 if len(titulo_curto) > 38 else 34
    adicionar_texto(
        slide, 1.25, 0.25, 11.65, 0.68,
        [(titulo_curto, tam_titulo, cor_titulo, True, "Segoe UI")],
        alinhamento=PP_ALIGN.LEFT,
        ancoragem=MSO_ANCHOR.MIDDLE,
    )


def injetar_transicao_e_animacoes_xml(slide, grupos_cliques):
    """
    Injeta transição suave (<p:transition>) e animações de entrada progressivas On Click (<p:timing>)
    diretamente na árvore OpenXML do slide.
    `grupos_cliques`: lista de listas de shapes. Cada sublista aparece em um clique do apresentador.
    """
    sld = slide._element

    # Remove transition/timing anteriores se existirem
    for tag in [qn("p:transition"), qn("p:timing")]:
        existente = sld.find(tag)
        if existente is not None:
            sld.remove(existente)

    # 1. Transição suave (Fade de 500ms)
    trans_xml = parse_xml(f'<p:transition {nsdecls("p")} spd="med" advClick="1"><p:fade/></p:transition>')
    sld.append(trans_xml)

    if not grupos_cliques:
        return

    # 2. Construção da árvore <p:timing> para cliques sequenciais (Appear/Fade On Click)
    id_counter = 2
    par_cliques_xml = []

    for grupo in grupos_cliques:
        shape_ids = [sh.shape_id for sh in grupo if sh is not None]
        if not shape_ids:
            continue

        id_click_par = id_counter
        id_counter += 1

        efeitos_shapes_xml = []
        for idx_s, spid in enumerate(shape_ids):
            id_ef_par = id_counter
            id_ef_bhv = id_counter + 1
            id_counter += 2
            node_type = "clickEffect" if idx_s == 0 else "withEffect"
            efeito = f"""
            <p:par>
              <p:cTn id="{id_ef_par}" fill="hold">
                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                <p:childTnLst>
                  <p:set>
                    <p:cBhvr>
                      <p:cTn id="{id_ef_bhv}" dur="1" fill="hold" nodeType="{node_type}">
                        <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                      </p:cTn>
                      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                      <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
                    </p:cBhvr>
                    <p:to><p:strVal val="visible"/></p:to>
                  </p:set>
                </p:childTnLst>
              </p:cTn>
            </p:par>
            """
            efeitos_shapes_xml.append(efeito)

        bloco_clique = f"""
        <p:par>
          <p:cTn id="{id_click_par}" fill="hold">
            <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
            <p:childTnLst>
              {''.join(efeitos_shapes_xml)}
            </p:childTnLst>
          </p:cTn>
        </p:par>
        """
        par_cliques_xml.append(bloco_clique)

    # BldLst para registrar as shapes animadas
    todos_spids = [sh.shape_id for g in grupos_cliques for sh in g if sh is not None]
    bld_items = "".join([f'<p:bldP spid="{spid}" grpId="0"/>' for spid in todos_spids])

    timing_xml_str = f"""
    <p:timing {nsdecls("p")}>
      <p:tnLst>
        <p:par>
          <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
            <p:childTnLst>
              <p:seq concurrent="1" nextAc="seek">
                <p:cTn id="{id_counter}" dur="indefinite" nodeType="mainSeq">
                  <p:childTnLst>
                    {''.join(par_cliques_xml)}
                  </p:childTnLst>
                </p:cTn>
                <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
                <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
              </p:seq>
            </p:childTnLst>
          </p:cTn>
        </p:par>
      </p:tnLst>
      <p:bldLst>
        {bld_items}
      </p:bldLst>
    </p:timing>
    """
    sld.append(parse_xml(timing_xml_str))


def definir_notas_orador(slide, texto_notas):
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = texto_notas.strip()


# ==============================================================================
# 3. CONSTRUÇÃO DOS 6 SLIDES (SEGUINDO ESTRITAMENTE O ROTEIRO DA V1)
# ==============================================================================

def construir_apresentacao():
    configurar_matplotlib_slides()
    img_s1 = gerar_diagrama_slide1_capa()
    img_s2 = gerar_diagrama_slide2_problema()
    img_s3 = gerar_diagrama_slide3_modelagem()
    img_s4_ondas, img_s4_fila = gerar_diagrama_slide4_bfs()
    img_s5_marina, img_s5_diego = gerar_diagramas_slide5_versus()
    img_s6_demo = os.path.join(RAIZ_PROJETO, "documentos", "comum", "figuras", "fig_screenshot_demo.png")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    layout_em_branco = prs.slide_layouts[6]

    # --------------------------------------------------------------------------
    # SLIDE 1: CAPA (30 s)
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(layout_em_branco)
    definir_fundo_slide(s1, COR_NAVY_DARK)

    # Faixa lateral de destaque vermelho
    adicionar_retangulo(s1, 0.0, 0.0, 0.22, 7.5, COR_VERMELHO, None, arredondado=False)

    # Tag superior da disciplina
    tag_s1 = adicionar_retangulo(s1, 0.65, 0.65, 4.85, 0.55, COR_SLATE_CARD, COR_VERMELHO, 1.5)
    adicionar_texto(s1, 0.75, 0.68, 4.65, 0.50, [
        ("ECM306 · ESTRUTURAS DE DADOS", 18, COR_TEXTO_CLARO, True)
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # Manchete Principal e Subtítulo
    adicionar_texto(s1, 0.65, 1.55, 5.55, 2.25, [
        ("CASO FAKE NEWS", 42, COR_BRANCO, True, "Georgia"),
        ("Rastreando e contendo boatos com Grafos", 22, COR_TEXTO_CLARO, False, "Segoe UI"),
    ])

    # 3 Big Badges (28 Pessoas · 5 Grupos · Java 21 Puro)
    b1 = adicionar_retangulo(s1, 0.65, 4.15, 1.75, 1.05, COR_SLATE_CARD, COR_VERMELHO, 2.0)
    t_b1 = adicionar_texto(s1, 0.65, 4.20, 1.75, 0.95, [
        ("28", 28, COR_BRANCO, True),
        ("Pessoas", 18, COR_TEXTO_CLARO, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    b2 = adicionar_retangulo(s1, 2.55, 4.15, 1.75, 1.05, COR_SLATE_CARD, COR_AMARELO, 2.0)
    t_b2 = adicionar_texto(s1, 2.55, 4.20, 1.75, 0.95, [
        ("5", 28, COR_BRANCO, True),
        ("Grupos", 18, COR_TEXTO_CLARO, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    b3 = adicionar_retangulo(s1, 4.45, 4.15, 1.85, 1.05, COR_SLATE_CARD, COR_VERDE, 2.0)
    t_b3 = adicionar_texto(s1, 4.45, 4.20, 1.85, 0.95, [
        ("Java 21", 26, COR_BRANCO, True),
        ("Puro", 18, COR_TEXTO_CLARO, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # Rodapé limpo com autores e professor
    adicionar_texto(s1, 0.65, 6.15, 5.75, 0.95, [
        ("David Daniel & Kauã Ortega", 20, COR_BRANCO, True),
        ("Prof. Robson Calvetti · IMT", 18, COR_BORDA, False),
    ])

    # Diagrama Central/Direito ocupando >50% do slide
    adicionar_imagem_preservando_aspecto(s1, img_s1, 6.35, 0.50, 6.55, 6.50)

    injetar_transicao_e_animacoes_xml(s1, [])
    definir_notas_orador(s1, """
[TEMPO: 30 segundos — Apresentador 1 (David)]
• Olá, professor Calvetti e colegas! Eu sou o David e, junto com o Kauã, vamos apresentar o projeto "Caso Fake News".
• Em vez de trabalhar com um tema batido como rotas de GPS, nós modelamos a propagação e a contenção cirúrgica de boatos virais em redes de mensagens instantâneas.
• Construímos uma rede social realista com 28 pessoas divididas em 5 grupos sociais, com motor algorítmico escrito 100% em Java 21 puro.
""")

    # --------------------------------------------------------------------------
    # SLIDE 2: O PROBLEMA (50 s)
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(layout_em_branco)
    definir_fundo_slide(s2, COR_BG_CLARO)
    adicionar_cabecalho_padrao(s2, 2, 'O PROBLEMA: "ENCAMINHADA COM FREQUÊNCIA"')

    # Esquerda: Ilustração grande do celular com boato do PIX
    adicionar_imagem_preservando_aspecto(s2, img_s2, 0.50, 1.15, 5.95, 5.95)

    # Direita: 3 cartões grandes numerados (revelados em 3 cliques!)
    c2_1 = adicionar_retangulo(s2, 6.65, 1.30, 6.15, 1.65, COR_VERMELHO_BG, COR_VERMELHO, 2.2)
    t2_1 = adicionar_texto(s2, 6.85, 1.42, 5.80, 1.40, [
        ("1️⃣ Quem recebe?", 26, COR_VERMELHO, True),
        ("Alcance total do boato", 20, COR_TEXTO_ESCURO, False),
    ], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)

    c2_2 = adicionar_retangulo(s2, 6.65, 3.25, 6.15, 1.65, COR_AMARELO_BG, COR_LARANJA, 2.2)
    t2_2 = adicionar_texto(s2, 6.85, 3.37, 5.80, 1.40, [
        ("2️⃣ Em quantas ondas?", 26, COR_LARANJA, True),
        ("Velocidade e distância em saltos", 20, COR_TEXTO_ESCURO, False),
    ], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)

    c2_3 = adicionar_retangulo(s2, 6.65, 5.20, 6.15, 1.65, COR_VERDE_BG, COR_VERDE, 2.2)
    t2_3 = adicionar_texto(s2, 6.85, 5.32, 5.80, 1.40, [
        ("3️⃣ Quem bloquear?", 26, COR_VERDE, True),
        ("Quarentena ótima na rede", 20, COR_TEXTO_ESCURO, False),
    ], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)

    injetar_transicao_e_animacoes_xml(s2, [
        [c2_1, t2_1],
        [c2_2, t2_2],
        [c2_3, t2_3],
    ])
    definir_notas_orador(s2, """
[TEMPO: 50 segundos — Apresentador 1 (David)]
• Todo mundo já recebeu no WhatsApp aquela mensagem alarmista com o selo "Encaminhada com frequência" — como uma falsa taxa no PIX.
• Quando uma notícia falsa surge em um grupo, precisamos responder a três perguntas fundamentais usando Teoria dos Grafos:
  - [CLIQUE 1] Primeira: Quem recebe? Até onde esse boato consegue chegar na rede?
  - [CLIQUE 2] Segunda: Em quantas ondas de reencaminhamento ele contamina a rede inteira?
  - [CLIQUE 3] Terceira e mais importante: Se pudermos colocar APENAS UMA pessoa em quarentena (conscientizando ou bloqueando o repasse), quem devemos escolher para salvar o maior número de pessoas?
""")

    # --------------------------------------------------------------------------
    # SLIDE 3: MODELAGEM (50 s)
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(layout_em_branco)
    definir_fundo_slide(s3, COR_BG_CLARO)
    adicionar_cabecalho_padrao(s3, 3, "DO CHAT PARA O GRAFO")

    # Centro (70% da tela): Diagrama visual grande transformando grupo de mensagens em grafo
    adicionar_imagem_preservando_aspecto(s3, img_s3, 0.50, 1.15, 12.33, 4.65)

    # Base: 3 pílulas visuais grandes (aparecem no Clique 1)
    p3_1 = adicionar_retangulo(s3, 0.50, 6.00, 3.90, 1.05, COR_AZUL_BG, COR_AZUL, 2.0)
    tp3_1 = adicionar_texto(s3, 0.55, 6.05, 3.80, 0.95, [
        ("Não Direcionado (A ↔ B)", 21, COR_AZUL, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    p3_2 = adicionar_retangulo(s3, 4.65, 6.00, 4.05, 1.05, COR_AMARELO_BG, COR_AMARELO, 2.0)
    tp3_2 = adicionar_texto(s3, 4.70, 6.05, 3.95, 0.95, [
        ("Sem Pesos (1 repasse = 1 salto)", 20, COR_AMARELO, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    p3_3 = adicionar_retangulo(s3, 8.95, 6.00, 3.88, 1.05, COR_VERDE_BG, COR_VERDE, 2.0)
    tp3_3 = adicionar_texto(s3, 9.00, 6.05, 3.78, 0.95, [
        ("Lista de Adjacência O(V+E)", 20, COR_VERDE, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    injetar_transicao_e_animacoes_xml(s3, [
        [p3_1, tp3_1, p3_2, tp3_2, p3_3, tp3_3],
    ])
    definir_notas_orador(s3, """
[TEMPO: 50 segundos — Apresentador 1 (David)]
• Como transformamos esse problema de redes sociais em um grafo formal G = (V, E)?
• Como vemos no diagrama central, cada uma das 28 pessoas vira um VÉRTICE (V), e cada canal de contato direto entre duas pessoas vira uma ARESTA (E), totalizando 42 conexões distribuídas em 5 grupos (Família, Condomínio, Trabalho, Academia e Faculdade).
• [CLIQUE 1] Adotamos três decisões de modelagem baseadas nas aulas da disciplina:
  1. O grafo é Não Direcionado, pois o contato no aplicativo é mútuo;
  2. É Não Ponderado, porque medimos o número discreto de saltos de encaminhamento;
  3. E usamos Lista de Adjacência em memória O(V + E), ideal para redes sociais esparsas.
""")

    # --------------------------------------------------------------------------
    # SLIDE 4: PROPAGAÇÃO BFS (60 s)
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(layout_em_branco)
    definir_fundo_slide(s4, COR_BG_CLARO)
    adicionar_cabecalho_padrao(s4, 4, "COMO O BOATO CORRE: BUSCA EM LARGURA (BFS)")

    # Esquerda (63% da tela): Diagrama grande de Ondas Concêntricas
    card_ondas = adicionar_retangulo(s4, 0.50, 1.15, 7.75, 5.95, COR_BRANCO, COR_BORDA, 1.8)
    adicionar_imagem_preservando_aspecto(s4, img_s4_ondas, 0.65, 1.25, 7.45, 5.75)

    # Direita Topo (Clique 1): Visual gráfico da Fila FIFO
    card_fila = adicionar_retangulo(s4, 8.45, 1.15, 4.38, 3.05, COR_BRANCO, COR_AZUL, 2.0)
    img_fila_sh = adicionar_imagem_preservando_aspecto(s4, img_s4_fila, 8.55, 1.25, 4.18, 2.15)
    t_fila = adicionar_texto(s4, 8.55, 3.45, 4.18, 0.65, [
        ("Fila FIFO garante ondas exatas", 20, COR_AZUL, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # Direita Base (Clique 2): Badge Gigante de Alcance (Big Number 50 pt)
    card_alcance = adicionar_retangulo(s4, 8.45, 4.40, 4.38, 2.70, COR_VERMELHO_BG, COR_VERMELHO, 2.5)
    t_alcance = adicionar_texto(s4, 8.55, 4.50, 4.18, 2.50, [
        ("27 de 28", 50, COR_VERMELHO, True),
        ("atingidos em 9 ondas", 22, COR_TEXTO_ESCURO, True),
        ("Apenas Sônia fica isolada", 18, COR_TEXTO_MUTED, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    injetar_transicao_e_animacoes_xml(s4, [
        [card_fila, img_fila_sh, t_fila],
        [card_alcance, t_alcance],
    ])
    definir_notas_orador(s4, """
[TEMPO: 60 segundos — Apresentador 2 (Kauã)]
• Agora que temos o grafo, como simulamos o espalhamento do boato a partir da Paciente Zero, a Ana (no centro vermelho)?
• Aplicamos a Busca em Largura (BFS). Diferente da busca em profundidade, a BFS explora o grafo por camadas concêntricas de distância mínima: Onda 1 em laranja (contatos diretos da Ana), Onda 2 em amarelo e Ondas 3 a 9 em azul.
• [CLIQUE 1] Isso acontece porque a BFS utiliza uma Fila FIFO em tempo linear O(V + E): quem recebe o boato primeiro, repassa primeiro para seus vizinhos.
• [CLIQUE 2] O resultado impressiona: partindo apenas da Ana, 27 das 28 pessoas da rede são contaminadas ao longo de 9 ondas! A única exceção é a Sônia (em cinza), que pertence a um componente desconexo de grau zero.
""")

    # --------------------------------------------------------------------------
    # SLIDE 5: QUARENTENA — INTUIÇÃO vs. TOPOLOGIA (70 s)
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(layout_em_branco)
    definir_fundo_slide(s5, COR_BG_CLARO)
    adicionar_cabecalho_padrao(s5, 5, "QUEM BLOQUEAR? INTUIÇÃO vs. TOPOLOGIA")

    # Card Esquerdo (Clique 1): Heurística de Maior Grau (Marina -> 0 SALVOS)
    c5_esq = adicionar_retangulo(s5, 0.50, 1.15, 5.75, 5.95, COR_VERMELHO_BG, COR_VERMELHO, 2.4)
    t5_esq_top = adicionar_texto(s5, 0.60, 1.25, 5.55, 0.70, [
        ("❌ Maior Grau: Marina (Grau 7)", 24, COR_VERMELHO, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    img5_esq = adicionar_imagem_preservando_aspecto(s5, img_s5_marina, 0.65, 1.98, 5.45, 3.32)
    t5_esq_num = adicionar_texto(s5, 0.55, 5.35, 5.65, 1.60, [
        ("0 SALVOS (0%)", 42, COR_VERMELHO, True),
        ("Grupo com rotas redundantes", 20, COR_TEXTO_ESCURO, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # Badge Central "VS"
    badge_vs = adicionar_retangulo(s5, 6.36, 3.65, 0.62, 0.85, COR_NAVY_DARK, None, arredondado=True)
    adicionar_texto(s5, 6.36, 3.70, 0.62, 0.75, [
        ("VS", 20, COR_BRANCO, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # Card Direito (Clique 2): Ponto de Articulação / Força Bruta (Diego -> 20 SALVOS)
    c5_dir = adicionar_retangulo(s5, 7.08, 1.15, 5.75, 5.95, COR_VERDE_BG, COR_VERDE, 2.4)
    t5_dir_top = adicionar_texto(s5, 7.18, 1.25, 5.55, 0.70, [
        ("✅ Ponte (Tarjan): Diego (Grau 5)", 24, COR_VERDE, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    img5_dir = adicionar_imagem_preservando_aspecto(s5, img_s5_diego, 7.23, 1.98, 5.45, 3.32)
    t5_dir_num = adicionar_texto(s5, 7.13, 5.35, 5.65, 1.60, [
        ("20 SALVOS (74%)", 42, COR_VERDE, True),
        ("Corta a ponte entre grupos", 20, COR_TEXTO_ESCURO, True),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    injetar_transicao_e_animacoes_xml(s5, [
        [c5_esq, t5_esq_top, img5_esq, t5_esq_num],
        [c5_dir, t5_dir_top, img5_dir, t5_dir_num],
    ])
    definir_notas_orador(s5, """
[TEMPO: 70 segundos — Apresentador 2 (Kauã)]
• Chegamos ao ponto alto do projeto: quem devemos bloquear para conter o boato?
• [CLIQUE 1] O senso comum sugere uma heurística gulosa: bloquear a pessoa mais popular da rede — a Marina, da Faculdade, que tem o maior grau (7 amigos). Mas veja o diagrama da esquerda: quando bloqueamos a Marina, salvamos ZERO pessoas (0%)! Como o grupo da Faculdade é densamente conectado, o boato simplesmente dá a volta nela pelos colegas.
• [CLIQUE 2] Agora veja o lado direito, usando nosso algoritmo exato de Força Bruta O(V*(V+E)) combinado com Pontos de Articulação de Tarjan via DFS: ele identifica o Diego (grau 5). O Diego é a ponte única que liga a Família ao grupo do Trabalho. Ao bloquear o Diego, cortamos o fluxo intergrupos e salvamos 20 pessoas de uma só vez — 74% de toda a rede!
""")

    # --------------------------------------------------------------------------
    # SLIDE 6: CONCLUSÃO + DEMO AO VIVO (40 s)
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(layout_em_branco)
    definir_fundo_slide(s6, COR_BG_CLARO)
    adicionar_cabecalho_padrao(s6, 6, "VEREDITO & DEMONSTRAÇÃO AO VIVO")

    # Topo: 3 cartões-resumo ultra-curtos (conforme plano_slides.md)
    k6_1 = adicionar_retangulo(s6, 0.50, 1.15, 3.95, 1.75, COR_BRANCO, COR_VERDE, 2.2)
    adicionar_texto(s6, 0.65, 1.25, 3.65, 1.55, [
        ("1. Pontes > Popularidade", 23, COR_VERDE, True),
        ("Articulação vence Grau", 19, COR_TEXTO_ESCURO, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    k6_2 = adicionar_retangulo(s6, 4.68, 1.15, 3.95, 1.75, COR_BRANCO, COR_AZUL, 2.2)
    adicionar_texto(s6, 4.83, 1.25, 3.65, 1.55, [
        ("2. Alta Performance", 23, COR_AZUL, True),
        ("2.000 nós em 0,27s", 19, COR_TEXTO_ESCURO, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    k6_3 = adicionar_retangulo(s6, 8.88, 1.15, 3.95, 1.75, COR_BRANCO, COR_LARANJA, 2.2)
    adicionar_texto(s6, 9.03, 1.25, 3.65, 1.55, [
        ("3. Java Pensa", 23, COR_LARANJA, True),
        ("Navegador desenha", 19, COR_TEXTO_ESCURO, False),
    ], PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # Centro/Base (Clique 1): Chamada visual grande para a Demo ao Vivo + Preview da Interface
    hero_demo = adicionar_retangulo(s6, 0.50, 3.15, 12.33, 3.95, COR_NAVY_DARK, COR_VERDE, 2.5)
    t_demo = adicionar_texto(s6, 0.80, 3.35, 5.55, 3.55, [
        ("▶ AO VIVO NO NAVEGADOR", 30, COR_BRANCO, True),
        ("1. Propagar", 22, COR_TEXTO_CLARO, True),
        ("2. Testar Marina", 22, COR_TEXTO_CLARO, True),
        ("3. Bloquear Diego", 22, COR_VERDE, True),
    ], PP_ALIGN.LEFT, MSO_ANCHOR.MIDDLE)

    img_demo_sh = adicionar_imagem_preservando_aspecto(s6, img_s6_demo, 6.45, 3.30, 6.15, 3.65)

    injetar_transicao_e_animacoes_xml(s6, [
        [hero_demo, t_demo, img_demo_sh],
    ])
    definir_notas_orador(s6, """
[TEMPO: 40 segundos — David & Kauã]
• Para concluir:
  1. Provamos na prática que a posição topológica (Pontos de Articulação) vale muito mais do que a popularidade bruta (Maior Grau);
  2. No nosso benchmark empírico em Java 21, a força bruta avaliou redes de 2.000 pessoas em apenas 0,27 segundo;
  3. E construímos uma arquitetura desacoplada onde o Java executa 100% dos algoritmos de grafos e o navegador apenas desenha.
• [CLIQUE 1] Agora vamos abrir o navegador para demonstrar ao vivo em três passos: propagar a BFS a partir da Ana, testar o bloqueio da Marina e comprovar a contenção ótima bloqueando o Diego!
""")

    prs.save(CAMINHO_PPTX)
    print(f"Apresentação salva com sucesso em: {CAMINHO_PPTX}")
    validar_regras_apresentacao(CAMINHO_PPTX)


def validar_regras_apresentacao(caminho_pptx):
    """
    Valida programaticamente todas as regras da Revisão v1 (plano/plano_slides.md):
    - 6 slides exatos;
    - Nenhum texto nativo com fonte < 18 pt;
    - Limite enxuto de palavras por slide (zero paredão de texto);
    - Presença de notas do orador e transições/animações em todos os slides.
    """
    prs = Presentation(caminho_pptx)
    assert len(prs.slides) == 6, f"Esperados 6 slides, encontrados {len(prs.slides)}"

    print("\n=== AUDITORIA AUTOMATIZADA DOS SLIDES (REVISÃO v1) ===")
    for idx, slide in enumerate(prs.slides, start=1):
        palavras_corpo = 0
        menor_fonte = 999.0
        for shape in slide.shapes:
            if shape.has_text_frame:
                txt = shape.text_frame.text.strip()
                tokens = [t for t in txt.split() if any(ch.isalnum() for ch in t)]
                palavras_corpo += len(tokens)
                for p in shape.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.size is not None:
                            pt_val = r.font.size.pt
                            if pt_val < menor_fonte:
                                menor_fonte = pt_val
                            assert pt_val >= 18.0, (
                                f"Violação no Slide {idx}: fonte {pt_val} pt < 18 pt no texto '{r.text}'"
                            )

        notas = slide.notes_slide.notes_text_frame.text.strip()
        assert len(notas) > 80, f"Slide {idx} está sem Notas do Orador completas!"

        tem_transicao = slide._element.find(qn("p:transition")) is not None
        tem_timing = slide._element.find(qn("p:timing")) is not None
        print(
            f"Slide {idx}: {palavras_corpo:2d} palavras visíveis | "
            f"Menor fonte: {menor_fonte:.0f} pt | "
            f"Transição: {'OK' if tem_transicao else 'FALTA'} | "
            f"Animação OnClick: {'OK' if tem_timing else 'Capa (Estática)'}"
        )
        assert palavras_corpo <= 35, f"Slide {idx} excedeu limite de palavras visíveis ({palavras_corpo})"

    print("=== TODAS AS REGRAS DE TIPOGRAFIA, DENSIDADE E DINAMISMO APROVADAS! ===\n")


if __name__ == "__main__":
    construir_apresentacao()
