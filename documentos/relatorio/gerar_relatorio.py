"""
Gerador do Relatório de Pesquisa em PDF (Revisão v1) — ECM306.
Segue rigorosamente o modelo 'Teorema de Hall Aplicado a Grafos.pdf' e as regras de plano/plano_pesquisa.md:
- Fontes TrueType nativas do Windows (Arial Unicode: zero glifos '■');
- Formatação matemática 100% com tags XML nativas do ReportLab (<i>, <sub>, <super>) — zero '$' ou LaTeX cru;
- Tabelas 100% construídas com objetos Paragraph em todas as células (quebra de linha automática, zero colisão);
- Figuras inseridas com leitura real de (w_px, h_px) via PIL (aspect ratio 100% preservado);
- Extensão enxuta entre 8 e 10 páginas com validação automatizada pós-build via pypdf.
"""

import os
import sys
from PIL import Image as PILImage
from pypdf import PdfReader

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

RAIZ_PROJETO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PASTA_FIG = os.path.join(RAIZ_PROJETO, "documentos", "comum", "figuras")
PASTA_ENTREGA = os.path.join(RAIZ_PROJETO, "Entrega")
os.makedirs(PASTA_ENTREGA, exist_ok=True)
CAMINHO_PDF = os.path.join(PASTA_ENTREGA, "Relatorio_Grafos_e_suas_Aplicacoes.pdf")


SIMBOLOS_MATH_FALLBACK = set("∈∉⊆⊂⊇⊃∪∩≪≫∅∀∃⇒⇔≈∝")


def P(texto, estilo):
    """Cria um Paragraph convertendo automaticamente símbolos matemáticos ausentes na Arial para MathSym."""
    partes = []
    for ch in texto:
        if ch in SIMBOLOS_MATH_FALLBACK:
            partes.append(f"<font name='MathSym'>{ch}</font>")
        else:
            partes.append(ch)
    return Paragraph("".join(partes), estilo)


def registrar_fontes_truetype():
    """Registra a família Arial TrueType do Windows e Segoe UI Symbol para operadores matemáticos Unicode."""
    pasta_win = r"C:\Windows\Fonts"
    mapa = {
        "Arial": os.path.join(pasta_win, "arial.ttf"),
        "Arial-Bold": os.path.join(pasta_win, "arialbd.ttf"),
        "Arial-Italic": os.path.join(pasta_win, "ariali.ttf"),
        "Arial-BoldItalic": os.path.join(pasta_win, "arialbi.ttf"),
        "MathSym": os.path.join(pasta_win, "seguisym.ttf"),
    }
    for nome, arq in mapa.items():
        if not os.path.exists(arq):
            raise FileNotFoundError(f"Fonte TrueType obrigatória não encontrada: {arq}")
        pdfmetrics.registerFont(TTFont(nome, arq))

    pdfmetrics.registerFontFamily(
        "Arial",
        normal="Arial",
        bold="Arial-Bold",
        italic="Arial-Italic",
        boldItalic="Arial-BoldItalic",
    )


def criar_estilos():
    """Cria a folha de estilos inspirada no documento modelo (Arial 11.5/12 pt, espaçamento limpo)."""
    base = getSampleStyleSheet()

    estilos = {
        "capa_inst": ParagraphStyle(
            "capa_inst",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111111"),
        ),
        "capa_autor": ParagraphStyle(
            "capa_autor",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=11.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111111"),
        ),
        "capa_titulo": ParagraphStyle(
            "capa_titulo",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=13,
            leading=18,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111111"),
        ),
        "resumo_titulo": ParagraphStyle(
            "resumo_titulo",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "secao": ParagraphStyle(
            "secao",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=12,
            leading=15,
            alignment=TA_LEFT,
            spaceBefore=11,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "subsecao": ParagraphStyle(
            "subsecao",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=11.2,
            leading=14.5,
            alignment=TA_LEFT,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "corpo": ParagraphStyle(
            "corpo",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=11,
            leading=15.5,
            alignment=TA_JUSTIFY,
            spaceAfter=5.5,
        ),
        "destaque_bloco": ParagraphStyle(
            "destaque_bloco",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=10.5,
            leading=14.5,
            alignment=TA_JUSTIFY,
            leftIndent=0.8 * cm,
            rightIndent=0.5 * cm,
            spaceBefore=2,
            spaceAfter=5.5,
        ),
        "item_lista": ParagraphStyle(
            "item_lista",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=10.6,
            leading=14.5,
            alignment=TA_JUSTIFY,
            leftIndent=0.6 * cm,
            firstLineIndent=-0.35 * cm,
            spaceAfter=4,
        ),
        "legenda_topo": ParagraphStyle(
            "legenda_topo",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=10,
            leading=13,
            alignment=TA_CENTER,
            spaceBefore=4,
            spaceAfter=3,
            keepWithNext=True,
        ),
        "legenda_fonte": ParagraphStyle(
            "legenda_fonte",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=9.5,
            leading=12,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=6,
        ),
        "celula_cab": ParagraphStyle(
            "celula_cab",
            parent=base["Normal"],
            fontName="Arial-Bold",
            fontSize=9.3,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111111"),
        ),
        "celula_esq": ParagraphStyle(
            "celula_esq",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=9.0,
            leading=12,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#111111"),
        ),
        "celula_centro": ParagraphStyle(
            "celula_centro",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=9.0,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111111"),
        ),
        "referencia": ParagraphStyle(
            "referencia",
            parent=base["Normal"],
            fontName="Arial",
            fontSize=9.8,
            leading=13,
            alignment=TA_LEFT,
            spaceAfter=3.5,
        ),
    }
    return estilos


def tabela_abnt(titulo, cabecalho, linhas, larguras_cm, estilos, alinhamentos=None, linha_destaque=None):
    """
    Constrói uma tabela padrão ABNT onde 100% das células são objetos Paragraph.
    Garante quebra de linha automática e zero sobreposição de texto entre colunas.
    """
    soma_cm = sum(larguras_cm)
    if soma_cm > 16.01:
        raise ValueError(f"Largura total da tabela ({soma_cm:.2f} cm) excede os 16,0 cm úteis da página A4.")

    if alinhamentos is None:
        alinhamentos = ["esq"] * len(cabecalho)

    matriz = []
    # Cabeçalho
    linha_cab = [P(col, estilos["celula_cab"]) for col in cabecalho]
    matriz.append(linha_cab)

    # Corpo
    for linha in linhas:
        linha_p = []
        for idx, texto in enumerate(linha):
            est = estilos["celula_centro"] if alinhamentos[idx] == "centro" else estilos["celula_esq"]
            linha_p.append(P(texto, est))
        matriz.append(linha_p)

    larguras_pt = [w * cm for w in larguras_cm]
    t = Table(matriz, colWidths=larguras_pt, repeatRows=1, hAlign="CENTER")

    comandos = [
        ("LINEABOVE", (0, 0), (-1, 0), 1.1, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 1.1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]

    # Listras suaves inspiradas no modelo do Teorema de Hall
    for idx_l in range(1, len(matriz)):
        if linha_destaque is not None and idx_l == linha_destaque:
            comandos.append(("BACKGROUND", (0, idx_l), (-1, idx_l), colors.HexColor("#e2e8f0")))
        elif idx_l % 2 == 0:
            comandos.append(("BACKGROUND", (0, idx_l), (-1, idx_l), colors.HexColor("#f8fafc")))

    t.setStyle(TableStyle(comandos))

    return KeepTogether([
        Paragraph(titulo, estilos["legenda_topo"]),
        t,
        Paragraph("Fonte: elaborado pelos autores (2026).", estilos["legenda_fonte"]),
    ])


def figura_abnt(titulo, nome_arquivo, largura_cm, estilos):
    """
    Insere figura PNG lendo suas dimensões reais via PIL para preservar 100% do aspect ratio.
    """
    caminho = os.path.join(PASTA_FIG, nome_arquivo)
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Figura não encontrada: {caminho}")

    with PILImage.open(caminho) as im:
        w_px, h_px = im.size

    largura_pt = largura_cm * cm
    altura_pt = largura_pt * (float(h_px) / float(w_px))

    img = Image(caminho, width=largura_pt, height=altura_pt)
    img.hAlign = "CENTER"

    return KeepTogether([
        Paragraph(titulo, estilos["legenda_topo"]),
        img,
        Paragraph("Fonte: elaborado pelos autores (2026).", estilos["legenda_fonte"]),
    ])


def cabecalho_numeracao(canvas, doc):
    """Numeração discreta no canto superior direito a partir da página 3 (ABNT NBR 14724)."""
    if doc.page >= 3:
        canvas.saveState()
        canvas.setFont("Arial", 9.5)
        canvas.setFillColor(colors.HexColor("#333333"))
        canvas.drawRightString(A4[0] - 2.0 * cm, A4[1] - 2.0 * cm, str(doc.page))
        canvas.restoreState()


def cabecalho_vazio(canvas, doc):
    """Páginas pré-textuais (Capa e Resumo) sem número de página impresso."""
    pass


def construir_relatorio():
    registrar_fontes_truetype()
    estilos = criar_estilos()

    doc = BaseDocTemplate(
        CAMINHO_PDF,
        pagesize=A4,
        leftMargin=3.0 * cm,
        rightMargin=2.0 * cm,
        topMargin=3.0 * cm,
        bottomMargin=2.0 * cm,
        title="Grafos e suas Aplicações: Fundamentos, Algoritmos e Estudo de Caso em Redes de Mensagens",
        author="David Sanchez Bittencourt Daniel; Kauã Bueno Marcatto Ortega",
    )

    largura_util = A4[0] - 5.0 * cm
    altura_util = A4[1] - 5.0 * cm
    frame_padrao = Frame(3.0 * cm, 2.0 * cm, largura_util, altura_util, id="frame_padrao",
                         leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="PreTextual", frames=[frame_padrao], onPage=cabecalho_vazio),
        PageTemplate(id="Textual", frames=[frame_padrao], onPage=cabecalho_numeracao),
    ])

    story = []

    # =========================================================================
    # PÁGINA 1 — CAPA (Seguindo o padrão limpo do modelo Teorema de Hall)
    # =========================================================================
    story.append(Spacer(1, 0.5 * cm))
    story.append(P("INSTITUTO MAUÁ DE TECNOLOGIA", estilos["capa_inst"]))
    story.append(Spacer(1, 1.8 * cm))
    story.append(P("DAVID SANCHEZ BITTENCOURT DANIEL (RA: 24.00029-9)", estilos["capa_autor"]))
    story.append(Spacer(1, 0.25 * cm))
    story.append(P("KAUÃ BUENO MARCATTO ORTEGA (RA: 24.00031-0)", estilos["capa_autor"]))
    story.append(Spacer(1, 0.45 * cm))
    story.append(P("Prof. Orientador: Prof. Robson Calvetti", estilos["capa_autor"]))
    story.append(Spacer(1, 6.2 * cm))
    story.append(P(
        "GRAFOS E SUAS APLICAÇÕES:<br/>FUNDAMENTOS, ALGORITMOS E ESTUDO DE CASO EM REDES DE MENSAGENS",
        estilos["capa_titulo"]
    ))
    story.append(Spacer(1, 9.2 * cm))
    story.append(P("São Paulo<br/>2026", estilos["capa_autor"]))
    story.append(PageBreak())

    # =========================================================================
    # PÁGINA 2 — RESUMO (Parágrafo único + Palavras-chave, idêntico ao modelo)
    # =========================================================================
    story.append(Spacer(1, 0.5 * cm))
    story.append(P("RESUMO", estilos["resumo_titulo"]))
    story.append(P(
        "Este trabalho apresenta uma pesquisa sobre a Teoria dos Grafos e suas aplicações computacionais, "
        "articulando a fundamentação matemática vista na disciplina de Tópicos Avançados de Estrutura de Dados "
        "(ECM306) com um estudo de caso prático voltado à propagação e contenção de desinformação (<i>fake news</i>) "
        "em redes de mensagens instantâneas. Na primeira parte, revisam-se as representações computacionais em "
        "lista e matriz de adjacência, os problemas clássicos de caminhos eulerianos e hamiltonianos, o "
        "emparelhamento em grafos bipartidos pelo Teorema de Hall, a planaridade pelo Teorema de Kuratowski e a "
        "coloração de vértices, além dos algoritmos de busca em largura (BFS), busca em profundidade (DFS), "
        "identificação de pontos de articulação de Tarjan e o contraste entre força bruta e heurísticas gulosas. "
        "Na segunda parte, modela-se uma rede social de 28 pessoas distribuídas em 5 grupos comunitários com 42 "
        "contatos mútuos, implementada integralmente em Java 21 puro. Os experimentos demonstram que a heurística "
        "gulosa de isolar o vértice de maior grau (Marina, grau 7) falha ao proteger zero pessoas adicionais, ao "
        "passo que a quarentena exata por força bruta combinada à detecção de pontos de articulação identifica as "
        "pontes estruturais da rede (Diego e Fábio), bloqueando até 74% da contaminação com execução inferior a "
        "0,3 segundo mesmo em redes de 2.000 vértices.",
        estilos["corpo"]
    ))
    story.append(Spacer(1, 0.3 * cm))
    story.append(P(
        "<b>Palavras-chave:</b> Teoria dos Grafos; Busca em Largura; Pontos de Articulação; Teorema de Hall; "
        "Contenção de Fake News.",
        estilos["corpo"]
    ))
    story.append(NextPageTemplate("Textual"))
    story.append(PageBreak())

    # =========================================================================
    # SEÇÃO 1 — INTRODUÇÃO
    # =========================================================================
    story.append(P("1 INTRODUÇÃO", estilos["secao"]))
    story.append(P(
        "Inúmeros sistemas do mundo real caracterizam-se não apenas pelos elementos que os compõem, mas sobretudo "
        "pelas relações estabelecidas entre pares desses elementos. Desde a resolução do problema das Sete Pontes "
        "de Königsberg por Leonhard Euler em 1736 — marco inaugural da Teoria dos Grafos —, abstrair entidades "
        "como <i>vértices</i> e suas interações como <i>arestas</i> permitiu transformar problemas geométricos e "
        "logísticos aparentemente intratáveis em estruturas algébricas e combinatórias rigorosas (DIESTEL, 2017; "
        "BOAVENTURA NETTO, 2014).",
        estilos["corpo"]
    ))
    story.append(P(
        "Embora o cálculo de rotas em mapas e sistemas de GPS seja o exemplo mais popularizado de grafos, o "
        "alcance prático dessa estrutura de dados na Ciência da Computação é muito mais amplo. Compiladores e "
        "gerenciadores de pacotes resolvem dependências por ordenação topológica em grafos acíclicos dirigidos; "
        "hospitais e sistemas operacionais alocam recursos e turnos por emparelhamento bipartido fundamentado no "
        "Teorema de Hall; instituições financeiras rastreiam lavagem de dinheiro detectando ciclos em grafos de "
        "transações; e operadoras de energia identificam subestações críticas por meio de pontos de articulação "
        "(CORMEN et al., 2012; SZWWIERCZYNSKI; GOLDBARG; GOLDBARG, 2012).",
        estilos["corpo"]
    ))
    story.append(P(
        "Nesse contexto, um desafio contemporâneo de alta relevância social é compreender e conter a difusão de "
        "boatos (<i>fake news</i>) em plataformas de mensagens instantâneas. Quando uma mensagem falsa é "
        "repassada entre grupos familiares, profissionais e acadêmicos, a velocidade de contágio e o impacto de "
        "uma eventual medida de contenção (<i>quarentena</i>) dependem diretamente da topologia da rede. Este "
        "trabalho sintetiza os fundamentos teóricos e algorítmicos dos grafos, mapeia aplicações reais não "
        "triviais no cotidiano e apresenta a modelagem e validação experimental de uma ferramenta computacional "
        "em Java 21 capaz de simular a propagação por ondas e determinar o bloqueio ótimo de desinformação.",
        estilos["corpo"]
    ))

    # =========================================================================
    # SEÇÃO 2 — FUNDAMENTOS E ALGORITMOS EM GRAFOS
    # =========================================================================
    story.append(P("2 FUNDAMENTOS E ALGORITMOS EM GRAFOS", estilos["secao"]))
    story.append(P("2.1. Conceitos Preliminares e Representações Computacionais", estilos["subsecao"]))
    story.append(P(
        "Um grafo simples não direcionado é definido formalmente pelo par ordenado <i>G</i> = (<i>V</i>, <i>E</i>), "
        "em que <i>V</i> é um conjunto finito e não vazio de vértices (ou nós) de ordem |<i>V</i>|, e <i>E</i> é um "
        "conjunto de pares não ordenados {<i>u</i>, <i>v</i>} denominados arestas, de tamanho |<i>E</i>|, sem laços "
        "nem arestas múltiplas (WEST, 2001). Dois vértices <i>u</i> e <i>v</i> ligados por uma aresta são ditos "
        "<i>adjacentes</i>, e o conjunto vizinhança <i>N</i>(<i>v</i>) reúne todos os vértices adjacentes a <i>v</i>. "
        "A cardinalidade dessa vizinhança define o grau do vértice, <i>d</i>(<i>v</i>) = |<i>N</i>(<i>v</i>)|. Como "
        "cada aresta incide exatamente em duas extremidades, a soma dos graus de todos os vértices satisfaz o "
        "<b>Lema do Aperto de Mãos</b>:",
        estilos["corpo"]
    ))
    story.append(P(
        "<b>Lema do Aperto de Mãos (Euler, 1736).</b> Em qualquer grafo não direcionado <i>G</i> = (<i>V</i>, <i>E</i>), "
        "tem-se ∑ <i>d</i>(<i>v</i>) = 2|<i>E</i>| para todo <i>v</i> ∈ <i>V</i>. Como consequência imediata, a "
        "quantidade de vértices de grau ímpar em qualquer grafo é obrigatoriamente um número par.",
        estilos["destaque_bloco"]
    ))
    story.append(P(
        "Um <i>caminho</i> de comprimento <i>k</i> entre dois vértices é uma sequência de vértices distintos "
        "(<i>v</i><sub>0</sub>, <i>v</i><sub>1</sub>, …, <i>v</i><sub><i>k</i></sub>) tal que cada par consecutivo "
        "forma uma aresta em <i>E</i>; se <i>v</i><sub>0</sub> = <i>v</i><sub><i>k</i></sub> com <i>k</i> ≥ 3, "
        "tem-se um <i>ciclo</i>. Um grafo é <i>conexo</i> quando existe ao menos um caminho entre qualquer par de "
        "vértices; caso contrário, decompõe-se em subgrafos conexos maximais denominados <i>componentes conexos</i>. "
        "Computacionalmente, a escolha entre representar <i>G</i> por <b>Lista de Adjacência</b> ou <b>Matriz de "
        "Adjacência</b> governa o consumo de memória e o custo assintótico dos algoritmos (Tabela 1). Em redes "
        "sociais esparsas, onde |<i>E</i>| ≪ |<i>V</i>|<super>2</super>, a lista de adjacência é estritamente "
        "superior por exigir memória linear O(|<i>V</i>| + |<i>E</i>|).",
        estilos["corpo"]
    ))

    story.append(tabela_abnt(
        "Tabela 1 – Comparação assintótica entre Lista de Adjacência e Matriz de Adjacência",
        ["Critério / Operação", "Lista de Adjacência", "Matriz de Adjacência", "Estrutura Indicada"],
        [
            ["Espaço em memória", "O(|<i>V</i>| + |<i>E</i>|)", "O(|<i>V</i>|<super>2</super>)", "Lista para grafos esparsos"],
            ["Verificar adjacência (<i>u</i>, <i>v</i>)", "O(<i>d</i>(<i>u</i>))", "O(1)", "Matriz para consultas diretas"],
            ["Percorrer vizinhos <i>N</i>(<i>u</i>)", "O(<i>d</i>(<i>u</i>))", "O(|<i>V</i>|)", "Lista (proporcional ao grau)"],
            ["Travessia completa (BFS / DFS)", "O(|<i>V</i>| + |<i>E</i>|)", "O(|<i>V</i>|<super>2</super>)", "Lista para redes reais"],
        ],
        [4.4, 3.6, 3.6, 4.4],
        estilos,
        alinhamentos=["esq", "centro", "centro", "esq"],
    ))

    story.append(P("2.2. Problemas Clássicos: Eulerianos, Emparelhamentos, Planaridade e Coloração", estilos["subsecao"]))
    story.append(P(
        "<b>Trilhas Eulerianas vs. Ciclos Hamiltonianos.</b> Uma trilha euleriana percorre todas as <i>arestas</i> "
        "de um grafo conexo exatamente uma vez; pelo Teorema de Euler-Hierholzer, um grafo conexo possui circuito "
        "euleriano (fechado) se, e somente se, todos os seus vértices têm grau par, e possui trilha euleriana aberta "
        "se possui exatamente 2 vértices de grau ímpar — condição verificável em tempo linear O(|<i>V</i>| + |<i>E</i>|). "
        "Em contraste, decidir se um grafo possui um <i>ciclo hamiltoniano</i> (que visita todos os <i>vértices</i> "
        "uma única vez) é um problema NP-completo sem caracterização local simples, ilustrando como pequenas "
        "mudanças na especificação (arestas vs. vértices) alteram drasticamente a tratabilidade computacional.",
        estilos["corpo"]
    ))
    story.append(P(
        "<b>Grafos Bipartidos e o Teorema de Hall.</b> Um grafo <i>G</i> = (<i>X</i> ∪ <i>Y</i>, <i>E</i>) é "
        "bipartido quando seu conjunto de vértices admite partição em dois subconjuntos disjuntos <i>X</i> e "
        "<i>Y</i> sem arestas internas a um mesmo subconjunto (equivalentemente, quando <i>G</i> não contém ciclos "
        "de comprimento ímpar). Um <i>emparelhamento</i> <i>M</i> ⊆ <i>E</i> é um conjunto de arestas sem "
        "extremidades em comum. O <b>Teorema de Hall (1935)</b> estabelece a condição necessária e suficiente para "
        "que exista um emparelhamento que sature todos os elementos de <i>X</i>:",
        estilos["corpo"]
    ))
    story.append(P(
        "<b>Teorema de Hall (1935).</b> Seja <i>G</i> um grafo bipartido com bipartição (<i>X</i>, <i>Y</i>). "
        "Existe um emparelhamento que satura <i>X</i> se, e somente se, |<i>N</i>(<i>S</i>)| ≥ |<i>S</i>| para todo "
        "subconjunto <i>S</i> ⊆ <i>X</i> (onde <i>N</i>(<i>S</i>) é a união das vizinhanças dos vértices de <i>S</i>).",
        estilos["destaque_bloco"]
    ))
    story.append(P(
        "<b>Planaridade e Coloração.</b> Um grafo é planar quando pode ser desenhado no plano sem cruzamento de "
        "arestas, satisfazendo a relação de Euler |<i>V</i>| − |<i>E</i>| + |<i>F</i>| = 2 (para grafos conexos, "
        "implicando |<i>E</i>| ≤ 3|<i>V</i>| − 6 quando |<i>V</i>| ≥ 3). Pelo <b>Teorema de Kuratowski (1930)</b>, "
        "um grafo finito é planar se, e somente se, não contém subgrafo que seja subdivisão do grafo completo "
        "<i>K</i><sub>5</sub> ou do grafo bipartido completo <i>K</i><sub>3,3</sub> (Figura 1). Já o problema de "
        "<b>coloração de vértices</b> consiste em atribuir o menor número cromático χ(<i>G</i>) de cores aos "
        "vértices de modo que vértices adjacentes recebam cores distintas; pelo Teorema das Quatro Cores, todo "
        "grafo planar satisfaz χ(<i>G</i>) ≤ 4.",
        estilos["corpo"]
    ))

    story.append(figura_abnt(
        "Figura 1 – Grafos não planares proibidos do Teorema de Kuratowski: <i>K</i><sub>5</sub> e <i>K</i><sub>3,3</sub>",
        "fig_kuratowski.png",
        11.6,
        estilos,
    ))

    story.append(P("2.3. Algoritmos de Travessia e Paradigmas de Projeto", estilos["subsecao"]))
    story.append(P(
        "A exploração sistemática de um grafo apoia-se em duas buscas fundamentais em tempo linear O(|<i>V</i>| + |<i>E</i>|): "
        "a <b>Busca em Largura (BFS)</b> e a <b>Busca em Profundidade (DFS)</b>. A BFS utiliza uma fila <i>FIFO</i> "
        "(<i>First-In, First-Out</i>) para visitar os vértices em camadas concêntricas de distância (ondas) a partir "
        "de uma origem <i>s</i>: primeiro descobre todos os vizinhos a distância 1, depois os de distância 2, e "
        "assim sucessivamente, garantindo a árvore de caminhos mínimos em número de arestas para grafos não "
        "ponderados. Quando as arestas possuem pesos não negativos, o algoritmo guloso de <b>Dijkstra</b> generaliza "
        "essa frente de expansão com uma fila de prioridades, enquanto em grafos acíclicos dirigidos (DAGs) o "
        "algoritmo de <b>Kahn</b> utiliza a fila de vértices com grau de entrada zero para produzir uma "
        "<b>ordenação topológica</b> linear.",
        estilos["corpo"]
    ))
    story.append(P(
        "A <b>Busca em Profundidade (DFS)</b>, por sua vez, avança recursivamente (ou por pilha LIFO) o mais fundo "
        "possível antes de retroceder (<i>backtracking</i>). Uma aplicação clássica da DFS é o <b>Algoritmo de "
        "Tarjan (1972)</b> para encontrar <b>Pontos de Articulação</b> (vértices de corte cuja remoção desconecta "
        "o grafo). Numerando os vértices pela ordem de descoberta <i>disc</i>[<i>u</i>] e calculando o menor tempo "
        "alcançável por até uma aresta de retorno <i>low</i>[<i>u</i>], um vértice não raiz <i>u</i> é ponto de "
        "articulação se, e somente se, possui algum filho <i>v</i> na árvore DFS tal que <i>low</i>[<i>v</i>] ≥ "
        "<i>disc</i>[<i>u</i>] (ou, sendo raiz, se possui dois ou mais filhos na árvore DFS).",
        estilos["corpo"]
    ))
    story.append(P(
        "Por fim, conforme discutido nas técnicas de projeto de algoritmos (Aula T23), é essencial contrastar "
        "<b>Algoritmos Gulosos</b> (que tomam decisões localmente ótimas baseadas num critério míope, como escolher "
        "o vértice de maior grau local) com algoritmos de <b>Força Bruta Exata</b> (que enumeram todo o espaço de "
        "candidatos para garantir o ótimo global). Como demonstraremos no estudo de caso da Seção 4, em problemas "
        "de contenção em redes com estrutura comunitária, a heurística gulosa de maior grau pode falhar "
        "completamente por ignorar a topologia global das pontes.",
        estilos["corpo"]
    ))

    # =========================================================================
    # SEÇÃO 3 — APLICAÇÕES NO COTIDIANO
    # =========================================================================
    story.append(P("3 APLICAÇÕES NO COTIDIANO (ALÉM DE MAPAS E GPS)", estilos["secao"]))
    story.append(P(
        "Para evidenciar a versatilidade da Teoria dos Grafos fora do domínio clichê de rotas rodoviárias, a "
        "Tabela 2 sintetiza sete problemas reais de engenharia e computação, especificando o significado dos "
        "vértices, das arestas e o modelo algorítmico que os soluciona.",
        estilos["corpo"]
    ))

    story.append(tabela_abnt(
        "Tabela 2 – Mapeamento de aplicações reais de grafos no cotidiano (excluindo mapas e GPS)",
        ["Domínio / Aplicação", "Vértices (V)", "Arestas (E)", "Algoritmo / Modelo em Grafo"],
        [
            ["1. Escalonamento de Horários e Exames", "Disciplinas ou provas da universidade", "Conflito (alunos matriculados em ambas)", "Coloração de Vértices (cada cor = 1 horário sem choque)"],
            ["2. Gerenciadores de Pacotes e Build", "Bibliotecas / módulos de software (npm, Maven)", "Relação dirigida 'depende de'", "Ordenação Topológica (Kahn / DFS) e detecção de ciclos em DAG"],
            ["3. Alocação de Turnos e Tarefas", "Conjunto X (técnicos) e Conjunto Y (chamados)", "Habilitação técnica para o serviço", "Emparelhamento Bipartido Máximo e Teorema de Hall"],
            ["4. Detecção de Fraude Financeira", "Contas bancárias e chaves de pagamento", "Transferências financeiras dirigidas", "Busca de ciclos dirigidos (lavagem circular) e centralidade"],
            ["5. Montagem de Genomas (Bioinformática)", "Prefixos e sufixos de comprimento <i>k</i> − 1", "Fragmentos sequenciados (<i>k-mers</i>)", "Trilha Euleriana no grafo de De Bruijn em tempo O(|<i>E</i>|)"],
            ["6. Confiabilidade de Redes Elétricas", "Subestações, roteadores e transformadores", "Linhas de transmissão física", "Pontos de Articulação e Pontes de Tarjan via DFS"],
            ["7. Difusão e Quarentena em Redes Sociais", "Usuários em grupos de mensagens", "Contatos diretos de reenvio mútuo", "Busca em Largura (BFS) em ondas + Quarentena de Vértices"],
        ],
        [3.6, 3.6, 3.8, 5.0],
        estilos,
        alinhamentos=["esq", "esq", "esq", "esq"],
        linha_destaque=7,
    ))

    story.append(P(
        "Observa-se um padrão estrutural claro: problemas de <i>incompatibilidade</i> reduzem-se à coloração "
        "(aplicação 1); problemas de <i>precedência temporal</i> reduzem-se a DAGs (aplicação 2); problemas de "
        "<i>atribuição exclusiva</i> apoiam-se em grafos bipartidos e na condição de Hall (aplicação 3); e "
        "problemas de <i>vulnerabilidade estrutural e contágio</i> dependem diretamente de buscas em largura/profundidade "
        "e da identificação de vértices de corte (aplicações 6 e 7).",
        estilos["corpo"]
    ))

    # =========================================================================
    # SEÇÃO 4 — ESTUDO DE CASO: PROPAGAÇÃO E QUARENTENA DE FAKE NEWS
    # =========================================================================
    story.append(P("4 ESTUDO DE CASO: PROPAGAÇÃO E QUARENTENA DE FAKE NEWS", estilos["secao"]))
    story.append(P("4.1. Modelagem do Problema (As 5 Perguntas da Aula T25)", estilos["subsecao"]))
    story.append(P(
        "Para investigar na prática a propagação de boatos e o impacto de estratégias de bloqueio, construiu-se o "
        "sistema <b>Caso Fake News</b> em Java 21 puro. Seguindo o roteiro metodológico da Aula T25 (Prof. Robson "
        "Calvetti), a modelagem responde às cinco questões fundamentais de projeto em grafos:",
        estilos["corpo"]
    ))
    story.append(P(
        "• <b>1. Quem são os vértices (<i>V</i>)?</b> Cada vértice representa uma pessoa cadastrada no aplicativo "
        "de mensagens. A rede principal possui |<i>V</i>| = 28 pessoas distribuídas em 5 grupos comunitários "
        "(<i>Família</i> com 6 membros, <i>Trabalho</i> com 6, <i>Faculdade</i> com 7, <i>Academia</i> com 5 e "
        "<i>Condomínio</i> com 4), incluindo um vértice isolado (Sônia, id 27) para validação de componentes desconexos.",
        estilos["item_lista"]
    ))
    story.append(P(
        "• <b>2. Quem são as arestas (<i>E</i>)?</b> Cada aresta {<i>u</i>, <i>v</i>} representa um canal de "
        "contato direto mútuo pelo qual uma pessoa pode encaminhar mensagens à outra, totalizando |<i>E</i>| = 42 "
        "conexões ativas.",
        estilos["item_lista"]
    ))
    story.append(P(
        "• <b>3. O grafo é direcionado ou não direcionado?</b> <b>Não direcionado</b>, pois no aplicativo de "
        "mensagens o canal de conversa entre dois contatos conhecidos permite o repasse recíproco.",
        estilos["item_lista"]
    ))
    story.append(P(
        "• <b>4. Existem pesos nas arestas?</b> <b>Não ponderado</b>: cada reenvio da mensagem corresponde a "
        "1 salto discreto (1 onda de transmissão), tornando a distância em arestas a métrica exata de velocidade.",
        estilos["item_lista"]
    ))
    story.append(P(
        "• <b>5. Qual estrutura de dados e algoritmos utilizar?</b> Representação em <b>Lista de Adjacência</b> "
        "(classe <font name='Arial-Bold'>Grafo</font>), combinando <b>Busca em Largura (BFS)</b> para simular as "
        "ondas de contágio, <b>Força Bruta Exata</b> para determinar a quarentena ótima e o <b>Algoritmo de "
        "Tarjan</b> para destacar os pontos de articulação.",
        estilos["item_lista"]
    ))

    story.append(P("4.2. Rastreamento por BFS em Ondas e Equação de Quarentena", estilos["subsecao"]))
    story.append(P(
        "Iniciando o boato no <i>Paciente Zero</i> Ana (id 0, grupo Família), a Busca em Largura (BFS) propaga a "
        "mensagem em ondas concêntricas (Figura 2). Sem bloqueios, o boato atinge 27 das 28 pessoas da rede ao "
        "longo de 9 ondas (apenas Sônia, grau 0, permanece inalcançável). A Tabela 3 apresenta o rastreamento "
        "dos 5 primeiros passos da fila FIFO na execução, evidenciando a expansão em camadas da Família para o "
        "Condomínio (Zeca) e para a ponte rumo ao grupo Trabalho (Fábio → Gabi).",
        estilos["corpo"]
    ))

    story.append(figura_abnt(
        "Figura 2 – Modelo de propagação em ondas concêntricas da Busca em Largura (BFS)",
        "fig_bfs_ondas.png",
        8.4,
        estilos,
    ))

    story.append(tabela_abnt(
        "Tabela 3 – Rastreamento dos 5 primeiros passos da fila FIFO na BFS a partir de Ana (id 0)",
        ["Etapa", "Fila FIFO Antes da Retirada", "Vértice Retirado", "Novos Vértices Descobertos (Enfileirados)"],
        [
            ["1", "[Ana]", "Ana (0)", "Bruno (1), Carla (2), Diego (3) — <i>Onda 1</i>"],
            ["2", "[Bruno, Carla, Diego]", "Bruno (1)", "nenhum (vizinhos já descobertos)"],
            ["3", "[Carla, Diego]", "Carla (2)", "Zeca (24) — <i>Ponte p/ Condomínio (Onda 2)</i>"],
            ["4", "[Diego, Zeca]", "Diego (3)", "Elisa (4), Fábio (5) — <i>Ponte p/ Trabalho (Onda 2)</i>"],
            ["5", "[Zeca, Elisa, Fábio]", "Zeca (24)", "Alice (25), Beto (26) — <i>Onda 3</i>"],
        ],
        [1.4, 5.0, 3.0, 6.6],
        estilos,
        alinhamentos=["centro", "esq", "centro", "esq"],
        linha_destaque=4,
    ))

    story.append(P(
        "Para conter a desinformação preventivamente colocando um único indivíduo <i>v</i> ∈ <i>V</i> \\ {<i>s</i>} "
        "em quarentena (removendo temporariamente <i>v</i> e suas arestas incidentes), o ganho de proteção é dado "
        "pela redução líquida de terceiros contaminados:",
        estilos["corpo"]
    ))
    story.append(P(
        "<b>Equação de Proteção por Quarentena:</b> protegidos(<i>v</i>) = |alcançados(<i>G</i>, <i>s</i>)| − "
        "|alcançados(<i>G</i> \\ {<i>v</i>}, <i>s</i>)| − 1 (para todo <i>v</i> previamente alcançado por <i>s</i>). "
        "O algoritmo de força bruta executa uma BFS independente para cada candidato elegível <i>v</i>, com "
        "complexidade de pior caso O(|<i>V</i>| · (|<i>V</i>| + |<i>E</i>|)).",
        estilos["destaque_bloco"]
    ))

    story.append(P("4.3. Resultados Experimentais: Força Bruta vs. Maior Grau", estilos["subsecao"]))
    story.append(P(
        "A Tabela 4 confronta os melhores candidatos encontrados pela Força Bruta com a escolha da heurística "
        "gulosa de Maior Grau. O resultado central do estudo de caso é revelador: a pessoa mais conectada de toda "
        "a rede é <b>Marina (id 12, grau 7, grupo Faculdade)</b>; contudo, colocá-la em quarentena protege "
        "<b>exatamente 0 pessoas adicionais</b>. Isso ocorre porque o grupo da Faculdade possui múltiplas rotas "
        "internas redundantes (ciclos entre Nuno, Olívia, Pedro, Quésia, Rafael e Sofia), de modo que o boato "
        "contorna Marina sem perder alcance.",
        estilos["corpo"]
    ))
    story.append(P(
        "Em contrapartida, <b>Diego (id 3, grau 5)</b> e <b>Fábio (id 5, grau 3)</b> possuem graus menores que "
        "Marina, mas são identificados pelo Algoritmo de Tarjan como <b>Pontos de Articulação</b> que separam o "
        "núcleo inicial da Família dos grupos Trabalho, Faculdade e Academia. Ao bloquear Diego, o alcance cai de "
        "27 para apenas 6 pessoas, salvando <b>20 indivíduos (74,1% das pessoas atingidas)</b>.",
        estilos["corpo"]
    ))

    story.append(tabela_abnt(
        "Tabela 4 – Comparação experimental entre o Top 4 da Força Bruta e a Heurística de Maior Grau",
        ["Rank", "Candidato (ID)", "Grupo", "Grau d(v)", "Protegidos", "Articulação (Tarjan)", "Diagnóstico Estratégico"],
        [
            ["#1", "Diego (id 3)", "Família", "5", "<b>20 (74%)</b>", "Sim (Ponte)", "Ótimo Global (isola Elisa, Fábio e 3 grupos)"],
            ["#2", "Fábio (id 5)", "Família", "3", "<b>18 (67%)</b>", "Sim (Ponte)", "Ponte exclusiva entre Família e Trabalho"],
            ["#3", "Gabi (id 6)", "Trabalho", "3", "<b>17 (63%)</b>", "Sim (Ponte)", "Porta de entrada única do grupo Trabalho"],
            ["#4", "João (id 9)", "Trabalho", "4", "7 (26%)", "Sim (Ponte)", "Ponte entre Trabalho e Faculdade"],
            ["#9", "<b>Marina (id 12)</b>", "Faculdade", "<b>7 (Máx.)</b>", "<b>0 (0%)</b>", "Não", "<b>Falha da Heurística de Maior Grau</b> (rotas internas)"],
        ],
        [1.2, 2.5, 2.0, 1.6, 2.1, 2.5, 4.1],
        estilos,
        alinhamentos=["centro", "esq", "centro", "centro", "centro", "centro", "esq"],
        linha_destaque=5,
    ))

    story.append(P(
        "A Figura 3 apresenta a interface web interativa desenvolvida para a demonstração em sala de aula (arquitetura "
        "<i>“O Java pensa, o navegador desenha”</i> via <font name='Arial-Bold'>HttpServer</font> nativo do JDK 21). "
        "Os 28 nós são dispostos em 5 territórios demarcados com algoritmo anticolisão (zero sobreposição), "
        "permitindo visualizar em tempo real tanto as ondas da fila BFS (Aba 1) quanto o contraste entre bloquear "
        "Marina e bloquear a ponte Diego (Aba 2).",
        estilos["corpo"]
    ))

    story.append(figura_abnt(
        "Figura 3 – Interface web interativa do sistema Caso Fake News (5 grupos demarcados e comparativo de quarentena)",
        "fig_screenshot_demo.png",
        11.4,
        estilos,
    ))

    story.append(P(
        "Por fim, para comprovar a viabilidade computacional do algoritmo de força bruta O(|<i>V</i>| · (|<i>V</i>| + |<i>E</i>|)) "
        "em grafos maiores, executou-se um benchmark automatizado em redes comunitárias sintéticas de |<i>V</i>| = 100 "
        "até |<i>V</i>| = 2.000 vértices (4.433 arestas, cerca de 8,89 × 10<super>6</super> operações elementares). "
        "Como mostra a Figura 4, mesmo para 2.000 pessoas a análise completa conclui em apenas <b>275,7 ms</b> "
        "(&lt; 0,3 s), acompanhando fielmente a curva assintótica teórica.",
        estilos["corpo"]
    ))

    story.append(figura_abnt(
        "Figura 4 – Escalabilidade empírica da quarentena por força bruta em Java 21 (<i>N</i> = 100 a 2.000 vértices)",
        "fig_benchmark.png",
        9.0,
        estilos,
    ))

    # =========================================================================
    # SEÇÕES 5 E 6 — CONSIDERAÇÕES FINAIS E REFERÊNCIAS BIBLIOGRÁFICAS
    # =========================================================================
    story.append(P("5 CONSIDERAÇÕES FINAIS", estilos["secao"]))
    story.append(P(
        "A pesquisa desenvolvida demonstra que a Teoria dos Grafos constitui um arcabouço indispensável para "
        "modelar sistemas relacionais complexos muito além do cálculo de rotas em mapas. Ao conectar propriedades "
        "estruturais — como bipartição e condição de Hall, graus pares em trilhas eulerianas, obstruções planares "
        "de Kuratowski e vértices de corte — a algoritmos lineares em listas de adjacência, problemas aparentemente "
        "intratáveis passam a contar com soluções elegantes e formalmente verificáveis.",
        estilos["corpo"]
    ))
    story.append(P(
        "No estudo de caso sobre propagação de <i>fake news</i>, a combinação entre Busca em Largura (BFS), "
        "Quarentena por Força Bruta e Pontos de Articulação de Tarjan evidenciou uma lição prática fundamental "
        "sobre projeto de algoritmos: <b>centralidade local (popularidade/grau) não equivale a importância "
        "topológica global</b>. Enquanto a heurística gulosa de bloquear o indivíduo mais conectado (Marina, grau 7) "
        "produziu efeito nulo devido à redundância interna de seu grupo, a identificação das pontes intergrupos "
        "(Diego e Fábio) reduziu a contaminação da rede em até 74%.",
        estilos["corpo"]
    ))
    story.append(P(
        "Em termos de engenharia de software, a implementação em Java 21 puro com listas de adjacência comprovou "
        "que mesmo uma abordagem exata de complexidade quadrática O(|<i>V</i>| · (|<i>V</i>| + |<i>E</i>|)) "
        "executa em frações de segundo para redes de milhares de vértices, oferecendo precisão matemática absoluta "
        "e visualização interativa imediata para apoio à tomada de decisão.",
        estilos["corpo"]
    ))

    story.append(P("6 REFERÊNCIAS BIBLIOGRÁFICAS", estilos["secao"]))
    referencias = [
        "BOAVENTURA NETTO, P. O. <i>Grafos: Teoria, Modelos, Algoritmos</i>. 5. ed. São Paulo: Blucher, 2014.",
        "CALVETTI, R. <i>Notas de Aula de ECM306 – Tópicos Avançados de Estrutura de Dados (Aulas T17 a T25)</i>. São Caetano do Sul: Instituto Mauá de Tecnologia, 2026.",
        "CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. <i>Algoritmos: Teoria e Prática</i>. 3. ed. Rio de Janeiro: Elsevier, 2012.",
        "DIESTEL, R. <i>Graph Theory</i>. 5. ed. Berlim: Springer, 2017.",
        "GOLDBARG, M.; GOLDBARG, E. <i>Grafos: Conceitos, Algoritmos e Aplicações</i>. Rio de Janeiro: Elsevier / Campus, 2012.",
        "HALL, P. On representatives of subsets. <i>Journal of the London Mathematical Society</i>, v. s1-10, n. 1, p. 26-30, 1935.",
        "HOPCROFT, J. E.; KARP, R. M. An <i>n</i><super>5/2</super> algorithm for maximum matchings in bipartite graphs. <i>SIAM Journal on Computing</i>, v. 2, n. 4, p. 225-231, 1973.",
        "KURATOWSKI, K. Sur le problème des courbes gauches en topologie. <i>Fundamenta Mathematicae</i>, v. 15, p. 271-283, 1930.",
        "TARJAN, R. E. Depth-first search and linear graph algorithms. <i>SIAM Journal on Computing</i>, v. 1, n. 2, p. 146-160, 1972.",
        "WEST, D. B. <i>Introduction to Graph Theory</i>. 2. ed. Upper Saddle River: Prentice Hall / Pearson, 2001.",
    ]
    for ref in referencias:
        story.append(P(ref, estilos["referencia"]))

    doc.build(story)
    print(f"PDF gerado com sucesso em: {CAMINHO_PDF}")


def validar_pdf(caminho_pdf):
    """
    Validação automatizada pós-build (Regra 1.3 e Seção 4 do plano_pesquisa.md):
    1. Verifica se o número total de páginas está entre 8 e 10 (8 <= págs <= 10);
    2. Lê o texto de todas as páginas via pypdf e falha se encontrar '$', '_{', '^{' ou '■'.
    """
    leitor = PdfReader(caminho_pdf)
    num_paginas = len(leitor.pages)
    print(f"Total de páginas do PDF gerado: {num_paginas}")

    if not (8 <= num_paginas <= 10):
        raise AssertionError(f"Meta de páginas violada: esperado entre 8 e 10 páginas, mas gerou {num_paginas} páginas.")

    proibidos = ["$", "_{", "^{", "■", "\ufffd"]
    erros = []
    for idx, pagina in enumerate(leitor.pages, start=1):
        texto = pagina.extract_text() or ""
        for token in proibidos:
            if token in texto:
                erros.append(f"Página {idx}: encontrado token proibido '{token}'")

    if erros:
        raise AssertionError("Erros de formatação matemática/Unicode detectados:\n" + "\n".join(erros))

    print("[OK] Validação pós-build concluída: 0 ocorrências de '$', '_{', '^{' ou '■' e número de páginas dentro da meta (8-10)!")


if __name__ == "__main__":
    construir_relatorio()
    validar_pdf(CAMINHO_PDF)
