"""
Gera todas as figuras científicas para o Relatório de Pesquisa (PDF) e Apresentação (PPTX).
Segue rigorosamente as diretrizes da Revisão v1 (plano_pesquisa.md):
- Alta resolução (300 DPI);
- Zero colisão de rótulos (uso de bbox com fundo branco e ângulos livres de vértices);
- Proporções calibradas para inserção com preservação exata de aspect ratio.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import numpy as np

PASTA_FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
os.makedirs(PASTA_FIG, exist_ok=True)


def configurar_estilo():
    plt.rcParams.update({
        "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.labelsize": 10.5,
        "axes.titlesize": 11.5,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "figure.titlesize": 12.5,
        "mathtext.default": "regular",
    })


def gerar_figura_kuratowski():
    """Figura 1: Grafos não planares proibidos de Kuratowski (K5 e K3,3)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.2, 3.5), dpi=300)
    fig.patch.set_facecolor("white")

    # (a) Grafo Completo K5
    ang = np.linspace(0, 2 * np.pi, 6)[:-1] + np.pi / 2
    x5, y5 = np.cos(ang), np.sin(ang)
    for i in range(5):
        for j in range(i + 1, 5):
            ax1.plot([x5[i], x5[j]], [y5[i], y5[j]], color="#64748b", lw=1.4, zorder=1)
    ax1.scatter(x5, y5, color="#c0392b", s=300, zorder=3, edgecolor="#1e293b", lw=1.6)
    for i in range(5):
        rx, ry = x5[i] * 1.30, y5[i] * 1.30
        ax1.text(
            rx, ry, f"$v_{i+1}$",
            ha="center", va="center", fontweight="bold", fontsize=10.5, color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.85)
        )
    ax1.set_title("(a) Grafo Completo $K_5$", pad=8, fontweight="bold", color="#0f172a")
    ax1.axis("off")
    ax1.set_xlim(-1.65, 1.65)
    ax1.set_ylim(-1.60, 1.65)
    ax1.set_aspect("equal")

    # (b) Grafo Bipartido Completo K3,3
    x_esq = [-0.95] * 3
    y_esq = [0.85, 0.0, -0.85]
    x_dir = [0.95] * 3
    y_dir = [0.85, 0.0, -0.85]
    for i in range(3):
        for j in range(3):
            ax2.plot([x_esq[i], x_dir[j]], [y_esq[i], y_dir[j]], color="#64748b", lw=1.3, zorder=1)
    ax2.scatter(x_esq, y_esq, color="#2563eb", s=290, zorder=3, edgecolor="#1e293b", lw=1.6, label="Partição X")
    ax2.scatter(x_dir, y_dir, color="#16a34a", s=290, zorder=3, edgecolor="#1e293b", lw=1.6, label="Partição Y")
    for i in range(3):
        ax2.text(
            x_esq[i] - 0.34, y_esq[i], f"$u_{i+1}$",
            ha="center", va="center", fontweight="bold", fontsize=10.5, color="#1e3a8a",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.85)
        )
        ax2.text(
            x_dir[i] + 0.34, y_dir[i], f"$w_{i+1}$",
            ha="center", va="center", fontweight="bold", fontsize=10.5, color="#14532d",
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.85)
        )
    ax2.text(-0.95, 1.25, "Conjunto X", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#2563eb")
    ax2.text(0.95, 1.25, "Conjunto Y", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#16a34a")
    ax2.set_title("(b) Bipartido Completo $K_{3,3}$", pad=8, fontweight="bold", color="#0f172a")
    ax2.axis("off")
    ax2.set_xlim(-1.65, 1.65)
    ax2.set_ylim(-1.40, 1.50)
    ax2.set_aspect("equal")

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.28)
    caminho = os.path.join(PASTA_FIG, "fig_kuratowski.png")
    plt.savefig(caminho, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Gerada:", caminho)


def gerar_figura_bfs_ondas():
    """Figura 2: Propagação em ondas concêntricas da Busca em Largura (BFS) sem colisão de rótulos."""
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=300)
    fig.patch.set_facecolor("white")

    raios = [1.15, 2.20, 3.25]
    cores_anel = ["#ea580c", "#d97706", "#2563eb"]
    cores_no = ["#f97316", "#f59e0b", "#3b82f6"]
    labels = ["Onda 1 (dist = 1)", "Onda 2 (dist = 2)", "Onda 3 (dist = 3)"]

    # Desenha círculos tracejados das ondas e rótulos no topo (90 graus), onde NÃO há vértices
    for r, cor, lbl in zip(raios, cores_anel, labels):
        circ = Circle((0, 0), r, fill=False, color=cor, ls="--", lw=1.6, alpha=0.85, zorder=1)
        ax.add_patch(circ)
        ax.text(
            0, r, lbl,
            ha="center", va="center", color=cor, fontsize=9.2, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor=cor, lw=1.0, alpha=0.98),
            zorder=6
        )

    # Ângulos escolhidos longe de 90° (pi/2 = 1.57 rad) para garantir zero sobreposição com os rótulos
    angulos_ondas = [
        [np.deg2rad(20), np.deg2rad(160), np.deg2rad(230), np.deg2rad(315)],
        [np.deg2rad(5), np.deg2rad(42), np.deg2rad(138), np.deg2rad(185), np.deg2rad(220), np.deg2rad(270), np.deg2rad(335)],
        [np.deg2rad(0), np.deg2rad(32), np.deg2rad(55), np.deg2rad(125), np.deg2rad(152), np.deg2rad(195), np.deg2rad(242), np.deg2rad(288), np.deg2rad(320)]
    ]

    aneis_coords = [[(0.0, 0.0)]]
    for idx_onda, (r, cor_no, angs) in enumerate(zip(raios, cores_no, angulos_ondas)):
        coords_atuais = []
        coords_ant = aneis_coords[-1]
        for k, a in enumerate(angs):
            px, py = r * np.cos(a), r * np.sin(a)
            coords_atuais.append((px, py))
            distancias = [np.hypot(px - ax_x, py - ax_y) for ax_x, ax_y in coords_ant]
            melhor = int(np.argmin(distancias))
            ox, oy = coords_ant[melhor]
            ax.plot([ox, px], [oy, py], color="#94a3b8", lw=1.3, zorder=2)
            ax.scatter(px, py, color=cor_no, s=190, zorder=4, edgecolor="#1e293b", lw=1.3)
        aneis_coords.append(coords_atuais)

    # Origem (Paciente Zero - Onda 0)
    ax.scatter(0, 0, color="#dc2626", s=460, zorder=5, edgecolor="#1e293b", lw=1.8)
    ax.text(0, 0, "Onda 0\n(Ana)", ha="center", va="center", color="white", fontsize=8.2, fontweight="bold", zorder=6)

    # Nó isolado (Sônia) fora do alcance
    ix, iy = 3.85, -2.35
    ax.scatter(ix, iy, color="#94a3b8", s=210, zorder=4, edgecolor="#475569", lw=1.4)
    ax.text(
        ix, iy - 0.48, "Nó Isolado\n(dist = ∞)",
        ha="center", va="top", fontsize=8.5, fontweight="bold", color="#475569",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#f8fafc", edgecolor="#cbd5e1", lw=0.8)
    )

    ax.set_xlim(-4.1, 4.55)
    ax.set_ylim(-3.65, 3.65)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    caminho = os.path.join(PASTA_FIG, "fig_bfs_ondas.png")
    plt.savefig(caminho, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Gerada:", caminho)


def gerar_figura_interface_v1():
    """Figura 3: Visualização limpa da aplicação web (Rede de 28 pessoas em 5 grupos + Comparativo Marina vs. Diego)."""
    fig = plt.figure(figsize=(10.0, 5.2), dpi=300)
    fig.patch.set_facecolor("#f8fafc")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 52)
    ax.axis("off")

    # Barra Superior Unificada
    barra = FancyBboxPatch((1.2, 46.2), 97.6, 4.6, boxstyle="round,pad=0.3,rounding_size=0.8",
                           facecolor="#0f172a", edgecolor="#1e293b", lw=1.2)
    ax.add_patch(barra)
    ax.text(3.0, 48.5, "CASO FAKE NEWS", color="#f8fafc", fontsize=10.5, fontweight="bold", va="center")
    ax.text(22.0, 48.5, "1. Origem: [Ana (Família) v]", color="#cbd5e1", fontsize=8.5, va="center")
    ax.text(44.5, 48.5, "2. BFS: [> Propagar em Ondas]  [>> Passo]", color="#38bdf8", fontsize=8.5, fontweight="bold", va="center")
    ax.text(74.0, 48.5, "3. Contenção: [Comparar Quarentena]", color="#4ade80", fontsize=8.5, fontweight="bold", va="center")

    # Quadro do Grafo (Esquerda: x=1.2..64.5)
    quadro = FancyBboxPatch((1.2, 1.5), 63.0, 43.6, boxstyle="round,pad=0.3,rounding_size=0.8",
                            facecolor="#ffffff", edgecolor="#cbd5e1", lw=1.2)
    ax.add_patch(quadro)

    # 5 Territórios (Grupos)
    territorios = [
        ("FAMÍLIA (6)", 12.5, 31.0, 9.5, 9.5, "#fef2f2", "#ef4444"),
        ("CONDOMÍNIO (4)", 12.5, 11.0, 9.0, 7.2, "#f8fafc", "#64748b"),
        ("TRABALHO (6)", 33.5, 31.0, 9.8, 9.5, "#fffbeb", "#f59e0b"),
        ("ACADEMIA (5)", 33.5, 11.0, 9.5, 7.5, "#f0fdf4", "#10b981"),
        ("FACULDADE (7)", 53.5, 22.5, 9.2, 13.5, "#eff6ff", "#3b82f6"),
    ]
    for titulo, cx, cy, rx, ry, fcor, bcor in territorios:
        box = FancyBboxPatch((cx - rx, cy - ry), 2 * rx, 2 * ry,
                             boxstyle="round,pad=0.2,rounding_size=1.2",
                             facecolor=fcor, edgecolor=bcor, lw=1.1, ls="--", alpha=0.85)
        ax.add_patch(box)
        ax.text(cx, cy + ry - 1.3, titulo, ha="center", va="center", fontsize=7.8, fontweight="bold", color=bcor)

    # Coordenadas dos 28 nós sem sobreposição
    pos = {
        0: (6.5, 34.5, "Ana", "Onda 0"),
        1: (6.8, 27.5, "Bruno", "Onda 1"),
        2: (11.5, 24.0, "Carla", "Onda 1"),
        3: (14.2, 34.5, "Diego", "BLOQ"),
        4: (16.5, 26.5, "Elisa", "Salva"),
        5: (19.8, 32.0, "Fábio", "Salvo"),
        24: (8.5, 13.5, "Zeca", "Onda 2"),
        25: (6.5, 7.2, "Alice", "Onda 3"),
        26: (13.2, 7.2, "Beto", "Onda 3"),
        27: (18.2, 11.5, "Sônia", "Isolada"),
        6: (26.5, 32.0, "Gabi", "Salva"),
        7: (31.0, 36.5, "Heitor", "Salvo"),
        8: (31.0, 26.5, "Iara", "Salva"),
        9: (38.0, 36.0, "João", "Salvo"),
        10: (39.5, 29.8, "Karen", "Salva"),
        11: (36.0, 24.0, "Lucas", "Salvo"),
        19: (33.5, 15.2, "Tiago", "Salvo"),
        20: (27.5, 11.5, "Úrsula", "Salva"),
        21: (33.5, 9.8, "Vitor", "Salvo"),
        22: (29.5, 5.8, "Wesley", "Salvo"),
        23: (38.8, 7.2, "Yara", "Salva"),
        13: (47.5, 31.0, "Nuno", "Salvo"),
        12: (53.8, 23.0, "Marina", "Grau 7"),
        14: (48.0, 23.5, "Olívia", "Salva"),
        15: (48.5, 15.5, "Pedro", "Salvo"),
        16: (54.5, 12.2, "Quésia", "Salva"),
        17: (59.5, 17.5, "Rafael", "Salvo"),
        18: (59.0, 29.0, "Sofia", "Salva"),
    }

    arestas = [
        (0,1),(0,2),(1,2),(0,3),(1,3),(2,3),(3,4),(3,5),(4,5),(5,6),
        (6,7),(6,8),(7,8),(7,9),(8,10),(9,11),(10,11),(9,12),(9,13),
        (12,13),(12,14),(12,15),(12,16),(12,17),(12,18),(13,14),(14,15),(15,16),(16,17),(17,18),(13,18),
        (11,19),(19,20),(20,21),(21,22),(22,23),(19,23),(19,21),
        (2,24),(24,25),(25,26),(24,26)
    ]

    for u, v in arestas:
        x1, y1, _, _ = pos[u]
        x2, y2, _, _ = pos[v]
        if (u, v) == (5, 6) or u == 3 or v == 3:
            ax.plot([x1, x2], [y1, y2], color="#dc2626", lw=1.4, ls=":", zorder=2)
        else:
            ax.plot([x1, x2], [y1, y2], color="#94a3b8", lw=1.1, zorder=2)

    for nid, (x, y, nome, status) in pos.items():
        if status == "Onda 0":
            cor = "#dc2626"
        elif status.startswith("Onda"):
            cor = "#f97316"
        elif status == "BLOQ":
            cor = "#7c3aed"
        elif status == "Grau 7":
            cor = "#f59e0b"
        elif status == "Isolada":
            cor = "#94a3b8"
        else:
            cor = "#16a34a"

        if nid in (3, 5):
            ax.scatter(x, y, s=310, facecolors="none", edgecolors="#eab308", lw=2.2, zorder=3)

        ax.scatter(x, y, s=165, color=cor, edgecolors="#0f172a", lw=1.1, zorder=4)
        ax.text(x, y - 1.65, nome, ha="center", va="top", fontsize=6.8, fontweight="bold", color="#0f172a",
                bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.88), zorder=5)

    # Destaques explicativos no grafo
    ax.annotate(
        "Diego (Grau 5, Ponte)\nBLOQUEADO -> 20 salvos!",
        xy=(14.2, 35.3), xytext=(18.5, 42.2),
        arrowprops=dict(arrowstyle="->", color="#7c3aed", lw=1.5),
        fontsize=7.8, fontweight="bold", color="#5b21b6",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#f5f3ff", edgecolor="#7c3aed", lw=1.1),
        zorder=7
    )
    ax.annotate(
        "Marina (Maior Grau = 7)\nIntragrupo -> 0 salvos",
        xy=(53.8, 24.0), xytext=(46.5, 40.5),
        arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5),
        fontsize=7.8, fontweight="bold", color="#92400e",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#fffbeb", edgecolor="#f59e0b", lw=1.1),
        zorder=7
    )

    # Painel Lateral Direito (2 Abas Limpas: x=65.5..98.8)
    painel = FancyBboxPatch((65.5, 1.5), 33.3, 43.6, boxstyle="round,pad=0.3,rounding_size=0.8",
                            facecolor="#ffffff", edgecolor="#cbd5e1", lw=1.2)
    ax.add_patch(painel)

    # 4 Contadores no topo do painel
    metricas = [
        ("Alcançados", "6 / 28", "#f97316", 66.8),
        ("Protegidos", "20 (74%)", "#16a34a", 74.8),
        ("Quarentena", "Diego (3)", "#7c3aed", 82.8),
        ("Articulações", "8 pontes", "#eab308", 90.8),
    ]
    for lbl, val, mcor, mx in metricas:
        cbox = FancyBboxPatch((mx, 39.2), 7.2, 4.6, boxstyle="round,pad=0.2,rounding_size=0.5",
                              facecolor="#f8fafc", edgecolor=mcor, lw=1.1)
        ax.add_patch(cbox)
        ax.text(mx + 3.6, 42.3, lbl, ha="center", va="center", fontsize=6.5, color="#475569", fontweight="bold")
        ax.text(mx + 3.6, 40.4, val, ha="center", va="center", fontsize=7.6, color=mcor, fontweight="bold")

    # Abas
    aba1 = FancyBboxPatch((66.8, 35.2), 14.8, 2.8, boxstyle="round,pad=0.1,rounding_size=0.4",
                          facecolor="#f1f5f9", edgecolor="#cbd5e1", lw=0.9)
    aba2 = FancyBboxPatch((82.2, 35.2), 15.6, 2.8, boxstyle="round,pad=0.1,rounding_size=0.4",
                          facecolor="#0f172a", edgecolor="#0f172a", lw=0.9)
    ax.add_patch(aba1)
    ax.add_patch(aba2)
    ax.text(74.2, 36.6, "Aba 1: Ondas & Fila BFS", ha="center", va="center", fontsize=7.0, color="#475569", fontweight="bold")
    ax.text(90.0, 36.6, "Aba 2: Quarentena (Ativa)", ha="center", va="center", fontsize=7.0, color="#ffffff", fontweight="bold")

    # Comparativo Lado a Lado na Aba 2
    card_err = FancyBboxPatch((66.8, 24.5), 14.8, 9.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                              facecolor="#fef2f2", edgecolor="#ef4444", lw=1.1)
    card_ok = FancyBboxPatch((82.4, 24.5), 15.4, 9.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                             facecolor="#f0fdf4", edgecolor="#16a34a", lw=1.1)
    ax.add_patch(card_err)
    ax.add_patch(card_ok)

    ax.text(74.2, 32.5, "[X] Heurística Maior Grau", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#b91c1c")
    ax.text(74.2, 30.2, "Marina (Faculdade, Grau 7)", ha="center", va="center", fontsize=6.8, color="#1e293b")
    ax.text(74.2, 27.6, "0 protegidos (0%)", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#dc2626")
    ax.text(74.2, 25.6, "Grupo possui rotas internas", ha="center", va="center", fontsize=6.3, color="#64748b")

    ax.text(90.1, 32.5, "[OK] Ótimo Força Bruta", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#15803d")
    ax.text(90.1, 30.2, "Diego (Família, Grau 5)", ha="center", va="center", fontsize=6.8, color="#1e293b")
    ax.text(90.1, 27.6, "20 protegidos (74%)", ha="center", va="center", fontsize=8.8, fontweight="bold", color="#16a34a")
    ax.text(90.1, 25.6, "Ponto de Articulação (Tarjan)", ha="center", va="center", fontsize=6.3, color="#15803d")

    # Ranking Top 5 Força Bruta
    ax.text(66.8, 22.5, "Ranking Completo de Quarentena — O(V*(V+E)):", fontsize=7.6, fontweight="bold", color="#0f172a")
    ranking = [
        ("#1 Diego (Família, g=5) [Ponte]", 20, "#16a34a"),
        ("#2 Fábio (Família, g=3) [Ponte]", 18, "#16a34a"),
        ("#3 Gabi (Trabalho, g=3) [Ponte]", 17, "#2563eb"),
        ("#4 João (Trabalho, g=4) [Ponte]", 7, "#3b82f6"),
        ("#9 Marina (Faculdade, g=7)", 0, "#ef4444"),
    ]
    y_r = 19.3
    for nome_r, salvos, cor_r in ranking:
        ax.text(66.8, y_r, nome_r, fontsize=6.8, color="#1e293b", va="center", fontweight="bold")
        larg_barra = max(0.6, (salvos / 20.0) * 8.5)
        b_bg = FancyBboxPatch((86.2, y_r - 0.8), 8.5, 1.6, boxstyle="round,pad=0.05", facecolor="#f1f5f9", edgecolor="none")
        b_fg = FancyBboxPatch((86.2, y_r - 0.8), larg_barra, 1.6, boxstyle="round,pad=0.05", facecolor=cor_r, edgecolor="none")
        ax.add_patch(b_bg)
        ax.add_patch(b_fg)
        ax.text(95.3, y_r, f"{salvos}", fontsize=7.0, fontweight="bold", color=cor_r, va="center")
        y_r -= 3.4

    caminho = os.path.join(PASTA_FIG, "fig_screenshot_demo.png")
    plt.savefig(caminho, bbox_inches="tight", facecolor="#f8fafc")
    plt.close()
    print("Gerada:", caminho)


def gerar_figura_benchmark():
    """Figura 4: Gráfico compacto de tempo da força bruta de N=100 a N=2000 sem sobreposição de rótulos."""
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=300)
    fig.patch.set_facecolor("white")

    n = np.array([100, 200, 500, 1000, 2000])
    arestas = np.array([204, 423, 1115, 2207, 4433])
    tempos_ms = np.array([11.1, 8.5, 30.9, 62.5, 275.7])

    ax.plot(n, tempos_ms, marker="o", color="#c0392b", lw=2.3, markersize=7, zorder=4,
            label="Tempo Medido em Java 21 (ms)")

    # Curva assintótica teórica ajustada O(V*(V+E))
    op_teorica = n * (n + arestas)
    fator = tempos_ms[-1] / op_teorica[-1]
    curva_teorica = op_teorica * fator
    ax.plot(n, curva_teorica, ls="--", color="#2563eb", lw=1.8, zorder=3,
            label="Tendência Assintótica $O(V \\cdot (V + E))$")

    # Anotar apenas os marcos principais (N=100, 500, 1000, 2000) com deslocamento calibrado (Regra 2.2)
    anotacoes = [
        (0, (18, 12)),    # N=100
        (2, (0, 13)),     # N=500
        (3, (-8, 14)),    # N=1000
        (4, (-36, -4)),   # N=2000
    ]
    for idx, offset in anotacoes:
        ax.annotate(
            f"N={n[idx]}: {tempos_ms[idx]:.1f} ms",
            (n[idx], tempos_ms[idx]),
            textcoords="offset points",
            xytext=offset,
            ha="center",
            fontsize=8.5,
            fontweight="bold",
            color="#0f172a",
            bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="#cbd5e1", lw=0.8, alpha=0.95),
            zorder=5
        )

    ax.set_xlabel("Ordem do Grafo (Número de Pessoas V)")
    ax.set_ylabel("Tempo de Execução (ms)")
    ax.set_xlim(0, 2180)
    ax.set_ylim(-15, 315)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(frameon=True, loc="upper left", fontsize=9.0)

    plt.tight_layout()
    caminho = os.path.join(PASTA_FIG, "fig_benchmark.png")
    plt.savefig(caminho, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Gerada:", caminho)


if __name__ == "__main__":
    configurar_estilo()
    gerar_figura_kuratowski()
    gerar_figura_bfs_ondas()
    gerar_figura_interface_v1()
    gerar_figura_benchmark()
    print("Todas as figuras da v1 foram geradas com sucesso.")
