"""
Gera todas as figuras científicas necessárias para o Relatório ABNT e Apresentação PPTX.
Salva as figuras em alta resolução (300 DPI) na pasta documentos/comum/figuras/.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PASTA_FIG = os.path.join(os.path.dirname(__file__), "figuras")
os.makedirs(PASTA_FIG, exist_ok=True)

def estilo_base():
    plt.rcParams.update({
        'font.sans-serif': 'DejaVu Sans',
        'font.family': 'sans-serif',
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'figure.titlesize': 13
    })

def gerar_figura_kuratowski():
    """Gera ilustração de K5 e K3,3 (não planares - Kuratowski, Aula T24)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.5, 3.4), dpi=300)
    
    # K5
    ang = np.linspace(0, 2*np.pi, 6)[:-1] + np.pi/2
    x5, y5 = np.cos(ang), np.sin(ang)
    for i in range(5):
        for j in range(i+1, 5):
            ax1.plot([x5[i], x5[j]], [y5[i], y5[j]], color='#7f8c8d', lw=1.2, zorder=1)
    ax1.scatter(x5, y5, color='#c0392b', s=260, zorder=2, edgecolor='#1b1b1b', lw=1.5)
    for i in range(5):
        ax1.text(x5[i]*1.25, y5[i]*1.25, f'$v_{i+1}$', ha='center', va='center', fontweight='bold', fontsize=11)
    ax1.set_title('(a) Grafo Completo $K_5$ (10 arestas)', pad=12)
    ax1.axis('off')
    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)

    # K3,3
    x_esq = [-0.8]*3
    y_esq = [0.8, 0, -0.8]
    x_dir = [0.8]*3
    y_dir = [0.8, 0, -0.8]
    for i in range(3):
        for j in range(3):
            ax2.plot([x_esq[i], x_dir[j]], [y_esq[i], y_dir[j]], color='#7f8c8d', lw=1.2, zorder=1)
    ax2.scatter(x_esq, y_esq, color='#2980b9', s=240, zorder=2, edgecolor='#1b1b1b', lw=1.5)
    ax2.scatter(x_dir, y_dir, color='#27ae60', s=240, zorder=2, edgecolor='#1b1b1b', lw=1.5)
    for i in range(3):
        ax2.text(x_esq[i]-0.3, y_esq[i], f'$u_{i+1}$', ha='center', va='center', fontweight='bold', fontsize=11)
        ax2.text(x_dir[i]+0.3, y_dir[i], f'$w_{i+1}$', ha='center', va='center', fontweight='bold', fontsize=11)
    ax2.set_title('(b) Grafo Bipartido Completo $K_{3,3}$ (9 arestas)', pad=12)
    ax2.axis('off')
    ax2.set_xlim(-1.5, 1.5)
    ax2.set_ylim(-1.3, 1.3)

    plt.tight_layout()
    caminho = os.path.join(PASTA_FIG, "fig_kuratowski.png")
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print("Gerada:", caminho)

def gerar_figura_hall():
    """Gera visualização de emparelhamento bipartido e condição de Hall (Aula T20)."""
    fig, ax = plt.subplots(figsize=(6.5, 3.5), dpi=300)
    
    # 4 técnicos e 4 chamados
    t_y = [1.2, 0.4, -0.4, -1.2]
    c_y = [1.2, 0.4, -0.4, -1.2]
    t_x = [-1.2]*4
    c_x = [1.2]*4
    
    # Todas as arestas possíveis
    arestas = [(0,0), (0,1), (1,1), (1,2), (2,2), (2,3), (3,0), (3,3)]
    emparelhadas = {(0,0), (1,1), (2,2), (3,3)}
    
    for u, v in arestas:
        if (u, v) in emparelhadas:
            ax.plot([t_x[u], c_x[v]], [t_y[u], c_y[v]], color='#c0392b', lw=3, zorder=2, label='Emparelhamento $M$' if (u,v)==(0,0) else '')
        else:
            ax.plot([t_x[u], c_x[v]], [t_y[u], c_y[v]], color='#bdc3c7', lw=1.2, ls='--', zorder=1)
            
    ax.scatter(t_x, t_y, color='#34495e', s=280, zorder=3, edgecolor='#111')
    ax.scatter(c_x, c_y, color='#16a085', s=280, zorder=3, edgecolor='#111')
    
    labels_t = ['T1: {C1,C2}', 'T2: {C2,C3}', 'T3: {C3,C4}', 'T4: {C1,C4}']
    labels_c = ['C1', 'C2', 'C3', 'C4']
    for i in range(4):
        ax.text(t_x[i]-0.15, t_y[i], labels_t[i], ha='right', va='center', fontsize=9, fontweight='bold')
        ax.text(c_x[i]+0.15, c_y[i], labels_c[i], ha='left', va='center', fontsize=10, fontweight='bold')
        
    ax.text(-1.2, 1.7, 'Grupo $X$ (Técnicos)', ha='center', fontsize=11, fontweight='bold', color='#2c3e50')
    ax.text(1.2, 1.7, 'Grupo $Y$ (Chamados)', ha='center', fontsize=11, fontweight='bold', color='#16a085')
    
    ax.set_xlim(-2.8, 2.0)
    ax.set_ylim(-1.6, 2.0)
    ax.axis('off')
    ax.legend(loc='lower center', frameon=True, fontsize=9)
    plt.tight_layout()
    caminho = os.path.join(PASTA_FIG, "fig_hall_emparelhamento.png")
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print("Gerada:", caminho)

def gerar_figura_benchmark():
    """Gera gráfico do benchmark de desempenho da Quarentena O(V*(V+E))."""
    fig, ax = plt.subplots(figsize=(6.5, 3.6), dpi=300)
    
    n = np.array([100, 200, 500, 1000, 2000])
    arestas = np.array([204, 423, 1115, 2207, 4433])
    # Tempos medidos no JVM benchmark real
    tempos_ms = np.array([11.14, 8.46, 30.86, 62.51, 275.67])
    
    ax.plot(n, tempos_ms, marker='o', color='#c0392b', lw=2.2, markersize=7, label='Tempo Real (Java JDK 21)')
    
    # Curva teórica ajustada c * V * (V + E)
    complexidade_teorica = n * (n + arestas)
    fator = tempos_ms[-1] / complexidade_teorica[-1]
    curva_teorica = complexidade_teorica * fator
    ax.plot(n, curva_teorica, ls='--', color='#2980b9', lw=1.8, label='Curva Assintótica Teórica $O(V(V+E))$')
    
    for i, txt in enumerate(tempos_ms):
        ax.annotate(f'{txt:.1f} ms', (n[i], tempos_ms[i]), textcoords="offset points", xytext=(0,9), ha='center', fontsize=8.5, fontweight='bold')
        
    ax.set_title('Desempenho da Análise de Quarentena por Força Bruta', pad=12, fontweight='bold')
    ax.set_xlabel('Quantidade de Vértices ($V$ na rede)')
    ax.set_ylabel('Tempo de Execução (milissegundos)')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(frameon=True, loc='upper left')
    
    plt.tight_layout()
    caminho = os.path.join(PASTA_FIG, "fig_benchmark.png")
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print("Gerada:", caminho)

def gerar_figura_bfs_ondas():
    """Gera esquema visual das ondas de propagação da BFS a partir da origem."""
    fig, ax = plt.subplots(figsize=(7.0, 3.8), dpi=300)
    
    # Centro
    ax.scatter(0, 0, color='#c0392b', s=350, zorder=4, edgecolor='#111', lw=1.5)
    ax.text(0, 0, 'Origem\n(Onda 0)', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    
    # Círculos concêntricos de ondas
    raios = [1.0, 2.0, 3.0]
    cores = ['#e67e22', '#f1c40f', '#3498db']
    labels = ['Onda 1 (dist = 1)', 'Onda 2 (dist = 2)', 'Onda 3 (dist = 3)']
    
    for r, cor, lbl in zip(raios, cores, labels):
        circ = plt.Circle((0,0), r, fill=False, color=cor, ls='--', lw=1.8, zorder=1)
        ax.add_patch(circ)
        ax.text(0, r + 0.1, lbl, ha='center', va='bottom', color=cor, fontsize=9, fontweight='bold', backgroundcolor='#ffffff')
        
    # Pontos nas ondas
    np.random.seed(42)
    pontos_x, pontos_y = [0], [0]
    for r, n_pts in zip(raios, [4, 7, 10]):
        angs = np.linspace(0, 2*np.pi, n_pts, endpoint=False) + np.random.uniform(-0.2, 0.2, n_pts)
        for a in angs:
            px = r * np.cos(a)
            py = r * np.sin(a)
            pontos_x.append(px)
            pontos_y.append(py)
            ax.scatter(px, py, color='#2c3e50', s=160, zorder=3, edgecolor='#fff', lw=1)
            # Aresta com o anel anterior
            ax.plot([px*0.65, px], [py*0.65, py], color='#bdc3c7', lw=1.2, zorder=2)
            
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-3.6, 3.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Modelo em Ondas da Busca em Largura (BFS)', pad=10, fontweight='bold')
    
    plt.tight_layout()
    caminho = os.path.join(PASTA_FIG, "fig_bfs_ondas.png")
    plt.savefig(caminho, bbox_inches='tight')
    plt.close()
    print("Gerada:", caminho)

if __name__ == "__main__":
    estilo_base()
    gerar_figura_kuratowski()
    gerar_figura_hall()
    gerar_figura_benchmark()
    gerar_figura_bfs_ondas()
    print("Todas as figuras geradas com sucesso.")
