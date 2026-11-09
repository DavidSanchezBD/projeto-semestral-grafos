"""
Gerador do Relatório de Pesquisa ABNT em PDF
ECM306 - Tópicos Avançados de Estrutura de Dados | Instituto Mauá de Tecnologia
Autores: David Sanchez Bittencourt Daniel (24.00029-9) & Kauã Bueno Marcatto Ortega (24.00031-0)
Orientador: Prof. Calvetti
"""

import os
import sys
from reportlab.lib import pagesizes, colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
FIG_DIR = os.path.join(RAIZ_DIR, "documentos", "comum", "figuras")
SAIDA_PDF = os.path.join(RAIZ_DIR, "Entrega", "Relatorio_Grafos_e_suas_Aplicacoes.pdf")
os.makedirs(os.path.dirname(SAIDA_PDF), exist_ok=True)

class ABNTCanvas(canvas.Canvas):
    """
    Canvas com numeração ABNT NBR 14724:
    - Folhas pré-textuais não são numeradas visualmente, mas contam na paginação.
    - Numeração aparece a partir da primeira folha do texto (Introdução), no canto superior direito (2cm da borda).
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.pagina_introducao = 1000

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_paginas = len(self.pages)
        for i, page_state in enumerate(self.pages):
            self.__dict__.update(page_state)
            num_pag = i + 1
            if num_pag >= self.pagina_introducao:
                self.setFont("Times-Roman", 10)
                self.drawRightString(pagesizes.A4[0] - 2.0*cm, pagesizes.A4[1] - 1.5*cm, str(num_pag))
            super().showPage()
        super().save()

def construir_relatorio():
    doc = SimpleDocTemplate(
        SAIDA_PDF,
        pagesize=pagesizes.A4,
        leftMargin=3.0*cm,
        rightMargin=2.0*cm,
        topMargin=3.0*cm,
        bottomMargin=2.0*cm
    )

    styles = getSampleStyleSheet()

    # Estilos ABNT
    estilo_capa_inst = ParagraphStyle(
        'CapaInstituicao',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1, # Centro
        textTransform='uppercase'
    )
    estilo_capa_autores = ParagraphStyle(
        'CapaAutores',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textTransform='uppercase'
    )
    estilo_capa_titulo = ParagraphStyle(
        'CapaTitulo',
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        alignment=1,
        textTransform='uppercase'
    )
    estilo_capa_subtitulo = ParagraphStyle(
        'CapaSubtitulo',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=1
    )
    estilo_capa_local = ParagraphStyle(
        'CapaLocal',
        fontName='Times-Roman',
        fontSize=11,
        leading=15,
        alignment=1
    )
    estilo_folha_nota = ParagraphStyle(
        'FolhaNota',
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=4, # Justificado
        leftIndent=7.5*cm
    )

    estilo_titulo_secao = ParagraphStyle(
        'Secao1',
        fontName='Times-Bold',
        fontSize=12,
        leading=18,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )
    estilo_subsecao = ParagraphStyle(
        'Secao2',
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    estilo_subsubsecao = ParagraphStyle(
        'Secao3',
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    estilo_corpo = ParagraphStyle(
        'CorpoTexto',
        fontName='Times-Roman',
        fontSize=12,
        leading=18, # 1.5 linhas
        alignment=4,
        firstLineIndent=1.25*cm,
        spaceAfter=6
    )

    estilo_resumo = ParagraphStyle(
        'ResumoTexto',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=4,
        spaceAfter=8
    )

    estilo_legenda_fig = ParagraphStyle(
        'LegendaFig',
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        alignment=1,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    estilo_fonte_fig = ParagraphStyle(
        'FonteFig',
        fontName='Times-Roman',
        fontSize=10,
        leading=13,
        alignment=1,
        spaceBefore=3,
        spaceAfter=12
    )

    estilo_codigo = ParagraphStyle(
        'Codigo',
        fontName='Courier',
        fontSize=9,
        leading=12,
        leftIndent=1.0*cm,
        spaceAfter=6
    )

    estilo_ref = ParagraphStyle(
        'Referencias',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=4,
        spaceAfter=10
    )

    story = []

    # =========================================================================
    # 1. CAPA
    # =========================================================================
    story.append(Spacer(1, 1.0*cm))
    story.append(Paragraph("INSTITUTO MAUÁ DE TECNOLOGIA<br/>CENTRO UNIVERSITÁRIO", estilo_capa_inst))
    story.append(Paragraph("ENGENHARIA DE COMPUTAÇÃO", estilo_capa_inst))
    story.append(Spacer(1, 3.5*cm))

    story.append(Paragraph("DAVID SANCHEZ BITTENCOURT DANIEL — RA: 24.00029-9<br/>KAUÃ BUENO MARCATTO ORTEGA — RA: 24.00031-0", estilo_capa_autores))
    story.append(Spacer(1, 4.5*cm))

    story.append(Paragraph("GRAFOS E SUAS APLICAÇÕES:<br/>FUNDAMENTOS, ALGORITMOS E ESTUDO DE CASO NA CONTENÇÃO DE DESINFORMAÇÃO EM REDES SOCIAIS", estilo_capa_titulo))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Implementação de rastreamento em ondas com Busca em Largura e mitigação de Fake News por Quarentena e Pontos de Articulação", estilo_capa_subtitulo))

    story.append(Spacer(1, 6.0*cm))
    story.append(Paragraph("SÃO CAETANO DO SUL<br/>2026", estilo_capa_local))
    story.append(PageBreak())

    # =========================================================================
    # 2. FOLHA DE ROSTO
    # =========================================================================
    story.append(Spacer(1, 1.0*cm))
    story.append(Paragraph("DAVID SANCHEZ BITTENCOURT DANIEL<br/>KAUÃ BUENO MARCATTO ORTEGA", estilo_capa_autores))
    story.append(Spacer(1, 4.0*cm))

    story.append(Paragraph("GRAFOS E SUAS APLICAÇÕES:<br/>FUNDAMENTOS, ALGORITMOS E ESTUDO DE CASO NA CONTENÇÃO DE DESINFORMAÇÃO EM REDES SOCIAIS", estilo_capa_titulo))
    story.append(Spacer(1, 2.5*cm))

    texto_nota = (
        "Trabalho acadêmico semestral apresentado à disciplina ECM306 — "
        "Tópicos Avançados de Estrutura de Dados do Instituto Mauá de Tecnologia, "
        "como requisito parcial para avaliação do 2º semestre.<br/><br/>"
        "<strong>Orientador:</strong> Prof. José Calvetti."
    )
    story.append(Paragraph(texto_nota, estilo_folha_nota))

    story.append(Spacer(1, 6.0*cm))
    story.append(Paragraph("SÃO CAETANO DO SUL<br/>2026", estilo_capa_local))
    story.append(PageBreak())

    # =========================================================================
    # 3. RESUMO
    # =========================================================================
    story.append(Paragraph("RESUMO", estilo_titulo_secao))
    texto_resumo = (
        "Este trabalho apresenta um estudo aprofundado sobre a Teoria dos Grafos, abrangendo desde os seus fundamentos "
        "matemáticos e representações computacionais até estruturas clássicas e paradigmas de projeto de algoritmos. "
        "Revisam-se propriedades estruturais como graus de vértices, lema do aperto de mãos, conexidade, grafos eulerianos "
        "e hamiltonianos, emparelhamentos em grafos bipartidos com o Teorema de Hall, planaridade com o Teorema de Kuratowski "
        "e coloração. No campo algorítmico, detalham-se os métodos de Busca em Largura (BFS), Busca em Profundidade (DFS), "
        "o algoritmo de Dijkstra para caminhos mínimos e o algoritmo de Kahn para ordenação topológica. Com base nesse arcabouço, "
        "desenvolve-se uma solução computacional completa e original em Java puro (JDK 21) voltada à simulação, rastreamento "
        "e contenção da disseminação de desinformação (fake news) em grupos de mensagens. A propagação do boato a partir de "
        "um paciente zero é modelada por ondas discretas via BFS em complexidade O(V + E). Para a mitigação, implementa-se "
        "um algoritmo exato de quarentena por força bruta em O(V·(V + E)), comparando seu resultado com a heurística gulosa de "
        "maior grau e com o algoritmo de Tarjan para identificação de pontos de articulação em O(V + E). Os experimentos práticos "
        "evidenciam um fenômeno didático central: o vértice de maior grau nem sempre é a intervenção ótima, sendo superado por "
        "vértices com menor conectividade que atuam como pontes estruturais entre comunidades. Uma interface interativa "
        "baseada na estética de quadro investigativo valida a viabilidade operacional e didática da proposta."
    )
    story.append(Paragraph(texto_resumo, estilo_resumo))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("<strong>Palavras-chave:</strong> Teoria dos Grafos; Busca em Largura; Fake News; Quarentena; Pontos de Articulação; Algoritmo de Tarjan.", estilo_resumo))
    story.append(PageBreak())

    # =========================================================================
    # 4. ABSTRACT
    # =========================================================================
    story.append(Paragraph("ABSTRACT", estilo_titulo_secao))
    texto_abstract = (
        "This work presents an in-depth study of Graph Theory, spanning from mathematical foundations and computational "
        "representations to classical structures and algorithm design paradigms. Structural properties such as vertex degrees, "
        "the handshaking lemma, connectivity, Eulerian and Hamiltonian graphs, matchings in bipartite graphs with Hall's "
        "Marriage Theorem, planarity with Kuratowski's Theorem, and graph coloring are comprehensively reviewed. Regarding "
        "algorithms, Breadth-First Search (BFS), Depth-First Search (DFS), Dijkstra's shortest path, and Kahn's topological "
        "sorting are analyzed. Grounded in this framework, a complete and original computational solution is developed in pure "
        "Java (JDK 21) focused on simulating, tracking, and containing misinformation (fake news) spreading across messaging "
        "groups. Spreading from a patient zero is modeled as discrete waves via BFS in O(V + E) time. For mitigation, an exact "
        "brute-force quarantine algorithm in O(V·(V + E)) is implemented and contrasted against both the highest-degree greedy "
        "heuristic and Tarjan's bridge-finding algorithm in O(V + E). Practical experiments demonstrate that the highest-degree "
        "node is not always the optimal quarantine target, often superseded by lower-degree vertices acting as structural bridges "
        "between communities. An interactive web interface styled as an investigative board confirms the operational and pedagogical "
        "validity of the approach."
    )
    story.append(Paragraph(texto_abstract, estilo_resumo))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("<strong>Keywords:</strong> Graph Theory; Breadth-First Search; Misinformation; Quarantine; Articulation Points; Tarjan's Algorithm.", estilo_resumo))
    story.append(PageBreak())

    # =========================================================================
    # 5. LISTA DE ILUSTRAÇÕES E TABELAS
    # =========================================================================
    story.append(Paragraph("LISTA DE ILUSTRAÇÕES", estilo_titulo_secao))
    story.append(Paragraph("Figura 1 – Grafos não planares canônicos de Kuratowski: $K_5$ e $K_{3,3}$", estilo_corpo))
    story.append(Paragraph("Figura 2 – Emparelhamento máximo em grafo bipartido e condição de Hall", estilo_corpo))
    story.append(Paragraph("Figura 3 – Modelo de propagação em ondas da Busca em Largura (BFS)", estilo_corpo))
    story.append(Paragraph("Figura 4 – Interface do software 'Caso Fake News: Operação Grafos' em execução", estilo_corpo))
    story.append(Paragraph("Figura 5 – Benchmark de desempenho da análise de quarentena por força bruta", estilo_corpo))
    story.append(Spacer(1, 1.0*cm))

    story.append(Paragraph("LISTA DE TABELAS", estilo_titulo_secao))
    story.append(Paragraph("Tabela 1 – Comparação de complexidade: Lista vs. Matriz de Adjacência", estilo_corpo))
    story.append(Paragraph("Tabela 2 – Síntese comparativa entre trilhas eulerianas e ciclos hamiltonianos", estilo_corpo))
    story.append(Paragraph("Tabela 3 – Mapeamento de problemas cotidianos e estruturas de grafos", estilo_corpo))
    story.append(Paragraph("Tabela 4 – Rastreamento da fila BFS na rede de teste do estudo de caso", estilo_corpo))
    story.append(Paragraph("Tabela 5 – Ranking de candidatos à quarentena: Força Bruta vs. Maior Grau", estilo_corpo))
    story.append(Paragraph("Tabela 6 – Benchmark de tempo de execução da força bruta para diferentes ordens de $V$", estilo_corpo))
    story.append(PageBreak())

    # =========================================================================
    # 6. SUMÁRIO
    # =========================================================================
    story.append(Paragraph("SUMÁRIO", estilo_titulo_secao))
    itens_sumario = [
        ("1 INTRODUÇÃO", "7"),
        ("2 FUNDAMENTOS TEÓRICOS DE GRAFOS", "8"),
        ("  2.1 Definições Formais e Grau de Vértices", "8"),
        ("  2.2 Representações Computacionais em Memória", "9"),
        ("  2.3 Caminhos, Ciclos e Conexidade", "10"),
        ("3 ESTRUTURAS ESPECIAIS E PROPRIEDADES CLÁSSICAS", "11"),
        ("  3.1 Grafos Eulerianos e Hamiltonianos", "11"),
        ("  3.2 Emparelhamentos Bipartidos e Teorema de Hall", "12"),
        ("  3.3 Planaridade e Coloração de Grafos", "13"),
        ("4 ALGORITMOS FUNDAMENTAIS E PARADIGMAS DE PROJETO", "14"),
        ("  4.1 Buscas em Grafos: BFS e DFS", "14"),
        ("  4.2 Caminhos Mínimos e Ordenação Topológica", "15"),
        ("  4.3 Técnicas de Projeto: Força Bruta, Gulosos e Programação Dinâmica", "16"),
        ("5 PANORAMA DE APLICAÇÕES COMPUTACIONAIS", "17"),
        ("6 ESTUDO DE CASO: RASTREAMENTO E QUARENTENA DE FAKE NEWS", "18"),
        ("  6.1 Formulação do Problema e Perguntas de Modelagem", "18"),
        ("  6.2 Modelagem Formal e Estrutura dos Dados", "19"),
        ("  6.3 Propagação em Ondas via Busca em Largura (BFS)", "20"),
        ("  6.4 Mitigação Exata por Força Bruta vs. Heurística de Grau", "21"),
        ("  6.5 Diagnóstico Estrutural por Pontos de Articulação (Tarjan)", "22"),
        ("  6.6 Arquitetura de Software e Interface com o Usuário", "23"),
        ("  6.7 Resultados Experimentais e Análise de Escalabilidade", "24"),
        ("7 CONCLUSÃO", "25"),
        ("REFERÊNCIAS", "26")
    ]
    for tit, pag in itens_sumario:
        p_txt = f"{tit} {'.' * (68 - len(tit))} {pag}"
        story.append(Paragraph(p_txt, estilo_corpo))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 1: INTRODUÇÃO
    # =========================================================================
    story.append(Paragraph("1 INTRODUÇÃO", estilo_titulo_secao))
    story.append(Paragraph(
        "A Teoria dos Grafos constitui um dos ramos mais férteis e aplicados da Ciência da Computação e da Matemática Discreta. "
        "Surgida formalmente em 1736 com a resolução do célebre problema das Pontes de Königsberg por Leonhard Euler, a disciplina "
        "evoluiu de uma curiosidade topológica para a linguagem fundamental de modelagem de sistemas complexos, redes de transporte, "
        "circuitos eletrônicos, estruturas moleculares e mídias sociais contemporâneas.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "No ambiente digital moderno, a interconexão ubíqua propiciada por aplicativos de mensagens instantâneas estabeleceu "
        "redes de relacionamento de altíssima capilaridade. Se, por um lado, tal infraestrutura potencializa a circulação veloz de dados, "
        "por outro, propicia o fenômeno deletério da disseminação em massa de desinformação (fake news). A propagação viral de boatos "
        "opera de maneira estritamente relacional: uma informação falsa inserida por um emissor inicial alcança seus contatos imediatos, "
        "os quais, ao retransmiti-la, deflagram ondas subsequentes de contágio informacional.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "Diante desse panorama, o presente trabalho atende às diretrizes da disciplina ECM306 — Tópicos Avançados de Estrutura de Dados, "
        "desenvolvendo uma pesquisa abrangente intitulada 'Grafos e suas Aplicações' e implementando um projeto autoral sob o lema "
        "'Resolvendo um Problema com Grafo'. Rejeitando formulações clichês baseadas em sistemas de navegação por GPS ou mapas viários, "
        "o estudo propõe a formalização matemática e algorítmica do problema de contenção de boatos em redes de mensagens.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "O trabalho estrutura-se em sete capítulos: os Capítulos 2 a 4 cobrem com rigor os conceitos fundamentais, estruturas clássicas "
        "e famílias algorítmicas lecionadas pelo Prof. Calvetti; o Capítulo 5 compila um panorama abrangente de aplicações práticas no cotidiano; "
        "o Capítulo 6 detalha a engenharia do estudo de caso, formalizando o modelo, as classes Java, a simulação em ondas por BFS, "
        "a mitigação exata por força bruta em contraste com heurísticas de grau e os pontos de articulação de Tarjan; por fim, o Capítulo 7 "
        "sintetiza as conclusões obtidas.",
        estilo_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 2: FUNDAMENTOS TEÓRICOS DE GRAFOS
    # =========================================================================
    story.append(Paragraph("2 FUNDAMENTOS TEÓRICOS DE GRAFOS", estilo_titulo_secao))
    
    story.append(Paragraph("2.1 Definições Formais e Grau de Vértices", estilo_subsecao))
    story.append(Paragraph(
        "Formalmente, um grafo G é definido como um par ordenado G = (V, E), no qual V = {v1, v2, ..., vn} representa um conjunto não vazio "
        "de elementos denominados <em>vértices</em> (ou nós), e E = {e1, e2, ..., em} denota um conjunto de <em>arestas</em> (ou arcos), "
        "sendo cada aresta e ∈ E associada a um par não ordenado (ou ordenado, no caso de digrafos) de vértices {u, v} ⊆ V (NICOLETTI; HRUSCHKA, 2017).",
        estilo_corpo
    ))
    story.append(Paragraph(
        "Dois vértices u e v unidos por uma aresta são ditos adjacentes ou vizinhos. O conjunto de vizinhos de um vértice v é denominado sua "
        "vizinhança aberta, denotada por N(v). O grau de um vértice v, expresso por d(v) ou grau(v), corresponde ao número de arestas incidentes "
        "em v. Um vértice é classificado como par se d(v) for par, e ímpar caso contrário. Um resultado fundamental da teoria clássica é "
        "o Teorema da Soma dos Graus, frequentemente chamado de <em>Lema do Aperto de Mãos</em> (Handshaking Lemma):",
        estilo_corpo
    ))
    story.append(Paragraph(
        "<strong>Teorema 1 (Soma dos Graus).</strong> Seja G = (V, E) um grafo não direcionado com n vértices e m arestas. Então: "
        "<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>∑_{v ∈ V} d(v) = 2 · |E|</strong><br/><br/>"
        "<em>Demonstração.</em> Cada aresta e = {u, v} conecta exatamente dois vértices, contribuindo com uma unidade no cômputo de d(u) "
        "e uma unidade em d(v). Consequentemente, ao somar os graus de todos os vértices de V, cada aresta é contabilizada exatamente duas vezes. Q.E.D.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "<strong>Corolário 1.</strong> Em todo grafo não direcionado, a quantidade de vértices de grau ímpar é obrigatoriamente par. "
        "De fato, se dividirmos a soma dos graus em vértices pares e ímpares, a soma total é par (2|E|); como a soma dos pares é par, "
        "a soma dos ímpares também deve ser par, o que só ocorre se houver um número par de parcelas ímpares.",
        estilo_corpo
    ))

    story.append(Paragraph("2.2 Representações Computacionais em Memória", estilo_subsecao))
    story.append(Paragraph(
        "A escolha da estrutura de dados para armazenar G em memória impacta criticamente a eficiência temporal dos algoritmos "
        "(CORMEN et al., 2012). As duas abordagens canônicas são a <em>Matriz de Adjacência</em> e a <em>Lista de Adjacência</em>:",
        estilo_corpo
    ))
    story.append(Paragraph(
        "• <strong>Matriz de Adjacência:</strong> matriz bidimensional M de dimensões |V| × |V|, onde M[u][v] = 1 se {u, v} ∈ E e 0 caso contrário. "
        "Possui custo de memória quadrático O(V²), permitindo consultar a existência de arestas em tempo O(1), mas penalizando a iteração sobre "
        "a vizinhança de um nó em O(V). É indicada primordialmente para grafos densos, onde |E| se aproxima de |V|².<br/>"
        "• <strong>Lista de Adjacência:</strong> arranjo de |V| listas encadeadas ou dinâmicas, onde a lista associada ao vértice u armazena todos "
        "os seus vizinhos N(u). Consome espaço proporcional a O(V + E), viabilizando enumerar vizinhos em tempo ótimo O(grau(u)). "
        "É a representação padrão para grafos esparsos, como redes de telecomunicações e redes sociais.",
        estilo_corpo
    ))

    # Tabela 1
    story.append(Paragraph("Tabela 1 – Comparação de complexidade: Lista vs. Matriz de Adjacência", estilo_legenda_fig))
    tabela_rep_dados = [
        ["Operação / Critério", "Lista de Adjacência", "Matriz de Adjacência"],
        ["Espaço em Memória", "O(V + E) — Ótimo p/ esparsos", "O(V²) — Excessivo p/ esparsos"],
        ["Consultar aresta (u, v)", "O(d(u))", "O(1) — Acesso direto"],
        ["Listar vizinhos de u", "O(d(u)) — Imediato", "O(V) — Varredura completa"],
        ["Adicionar vértice", "O(1) amortizado", "O(V²) — Realocação"],
        ["Perfil mais indicado", "Redes sociais, web, esparsas", "Grafos densos, algébricos"]
    ]
    tab_rep = Table(tabela_rep_dados, colWidths=[5.0*cm, 5.0*cm, 5.5*cm])
    tab_rep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2d7be')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888'))
    ]))
    story.append(tab_rep)
    story.append(Paragraph("Fonte: Adaptado de Cormen et al. (2012) e Nicoletti e Hruschka (2017).", estilo_fonte_fig))

    story.append(Paragraph("2.3 Caminhos, Ciclos e Conexidade", estilo_subsecao))
    story.append(Paragraph(
        "A formalização das sequências de vértices e arestas é indispensável para a teoria algorítmica:<br/>"
        "• <strong>Passeio (Walk):</strong> sequência alternada v0, e1, v1, e2, ..., vk de vértices e arestas conectadas.<br/>"
        "• <strong>Trilha (Trail):</strong> passeio no qual todas as arestas são distintas duas a duas.<br/>"
        "• <strong>Caminho (Path):</strong> trilha na qual todos os vértices são distintos (com exceção eventual do início e término).<br/>"
        "• <strong>Ciclo:</strong> caminho fechado de comprimento k ≥ 3, cuja origem coincide com o destino.<br/>"
        "Um grafo é dito <em>conexo</em> se existir ao menos um caminho entre qualquer par de seus vértices. Quando não é conexo, "
        "ele se decompõe em subgrafos conexos maximais denominados <em>componentes conexos</em> (BOAVENTURA NETTO, 2014).",
        estilo_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 3: ESTRUTURAS ESPECIAIS E PROPRIEDADES CLÁSSICAS
    # =========================================================================
    story.append(Paragraph("3 ESTRUTURAS ESPECIAIS E PROPRIEDADES CLÁSSICAS", estilo_titulo_secao))
    
    story.append(Paragraph("3.1 Grafos Eulerianos e Hamiltonianos", estilo_subsecao))
    story.append(Paragraph(
        "A distinção entre cobrir todas as conexões ou visitar todas as entidades constitui uma das fronteiras conceituais "
        "mais relevantes da teoria computacional:<br/>"
        "• <strong>Grafo Euleriano:</strong> grafo conexo que admite um circuito fechado contendo cada aresta de E exatamente uma vez. "
        "Pelo Teorema de Euler (1736), um grafo conexo é euleriano se e somente se todos os seus vértices possuírem grau par. "
        "Se admitir exatamente dois vértices de grau ímpar, existe uma trilha euleriana aberta iniciando em um ímpar e terminando no outro.<br/>"
        "• <strong>Grafo Hamiltoniano:</strong> grafo que possui um ciclo simples fechado que visita cada vértice de V exatamente uma vez. "
        "Diferentemente do caso euleriano, não se conhece um critério estrutural simples e de verificação polinomial que caracterize todos "
        "os grafos hamiltonianos; as condições clássicas conhecidas (Teorema de Dirac: d(v) ≥ n/2; Teorema de Ore: d(u)+d(v) ≥ n) são apenas "
        "suficientes. A decisão de hamiltonicidade é um problema NP-completo clássico.",
        estilo_corpo
    ))

    # Tabela 2
    story.append(Paragraph("Tabela 2 – Síntese comparativa entre trilhas eulerianas e ciclos hamiltonianos", estilo_legenda_fig))
    tab_eh_dados = [
        ["Critério", "Problema Euleriano", "Problema Hamiltoniano"],
        ["Objeto a ser coberto", "Todas as arestas (E)", "Todos os vértices (V)"],
        ["Repetição de vértices", "Permitida ao longo da trilha", "Proibida (exceto retorno à origem)"],
        ["Critério de existência", "Todos os graus pares (exato)", "Condições parciais (Dirac, Ore)"],
        ["Complexidade de decisão", "Polinomial P — Alg. Hierholzer O(E)", "NP-completo — Explosão fatorial"],
        ["Exemplo prático", "Varrição de ruas, leitura de hidrômetros", "Visita a clientes (Caixeiro Viajante)"]
    ]
    tab_eh = Table(tab_eh_dados, colWidths=[4.2*cm, 5.5*cm, 5.8*cm])
    tab_eh.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2d7be')),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888'))
    ]))
    story.append(tab_eh)
    story.append(Paragraph("Fonte: Elaborado pelos autores a partir do material de aula (Calvetti, 2026).", estilo_fonte_fig))

    story.append(Paragraph("3.2 Emparelhamentos Bipartidos e Teorema de Hall", estilo_subsecao))
    story.append(Paragraph(
        "Um grafo G = (V, E) é <em>bipartido</em> se V puder ser particionado em dois subconjuntos disjuntos X e Y tais que toda aresta em E "
        "ligue um elemento de X a um de Y. Um conjunto M ⊆ E é dito um <em>emparelhamento</em> (matching) se duas arestas quaisquer de M "
        "não compartilharem vértices em comum. Diz-se que M satura o conjunto X se todo vértice x ∈ X for extremidade de alguma aresta de M.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "<strong>Teorema de Hall (Philip Hall, 1935).</strong> Seja G um grafo bipartido com bipartição (X, Y). Existe um emparelhamento "
        "que satura X se, e somente se, para todo subconjunto S ⊆ X, a cardinalidade de sua vizinhança satisfizer: "
        "<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>|N(S)| ≥ |S|</strong><br/><br/>"
        "A condição de Hall formaliza a barreira fundamental de alocação: se um subconjunto de solicitantes S demandar mais parceiros do que "
        "o total conjunto de opções que lhes são compatíveis (|N(S)| < |S|), o atendimento pleno torna-se estruturalmente impossível. "
        "Pelo Teorema de Berge (1957), um emparelhamento é máximo se e somente se não contiver caminhos M-aumentantes.",
        estilo_corpo
    ))

    # Figura 2
    caminho_fig_hall = os.path.join(FIG_DIR, "fig_hall_emparelhamento.png")
    if os.path.exists(caminho_fig_hall):
        story.append(Paragraph("Figura 2 – Emparelhamento máximo em grafo bipartido e condição de Hall", estilo_legenda_fig))
        story.append(Image(caminho_fig_hall, width=13.0*cm, height=7.0*cm))
        story.append(Paragraph("Fonte: Elaborado pelos autores (2026).", estilo_fonte_fig))

    story.append(Paragraph("3.3 Planaridade e Coloração de Grafos", estilo_subsecao))
    story.append(Paragraph(
        "Um grafo é dito <em>plano</em> se estiver desenhado sobre uma superfície bidimensional de modo que suas arestas não se interceptem "
        "a não ser em suas extremidades. Um grafo é <em>planar</em> se for isomorfo a um grafo plano. Para qualquer grafo planar conexo, "
        "vale a <em>Fórmula Poliedral de Euler</em>: <strong>|V| - |E| + |F| = 2</strong>, onde F representa o conjunto de faces (regiões delimitadas).",
        estilo_corpo
    ))
    story.append(Paragraph(
        "<strong>Teorema de Kuratowski (1930).</strong> Um grafo G é planar se, e somente se, não contiver nenhum subgrafo homeomorfo "
        "(obtido por subdivisão de arestas) aos grafos canônicos K5 (grafo completo de 5 vértices) ou K3,3 (grafo bipartido completo das 3 casas e 3 serviços).",
        estilo_corpo
    ))

    # Figura 1
    caminho_fig_kur = os.path.join(FIG_DIR, "fig_kuratowski.png")
    if os.path.exists(caminho_fig_kur):
        story.append(Paragraph("Figura 1 – Grafos não planares canônicos de Kuratowski: $K_5$ e $K_{3,3}$", estilo_legenda_fig))
        story.append(Image(caminho_fig_kur, width=14.0*cm, height=6.2*cm))
        story.append(Paragraph("Fonte: Elaborado pelos autores (2026).", estilo_fonte_fig))

    story.append(Paragraph(
        "A planaridade conecta-se diretamente ao clássico <em>Problema da Coloração de Vértices</em>: atribuir cores aos vértices de modo que nós adjacentes "
        "recebam cores distintas. Pelo célebre <em>Teorema das Quatro Cores</em> (Appel & Haken, 1976), qualquer grafo planar pode ser colorido com no máximo "
        "4 cores. Em grafos gerais, encontrar o número cromático χ(G) é NP-difícil, demandando algoritmos gulosos de ordenação de graus como Welsh-Powell e DSatur.",
        estilo_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 4: ALGORITMOS FUNDAMENTAIS E PARADIGMAS DE PROJETO
    # =========================================================================
    story.append(Paragraph("4 ALGORITMOS FUNDAMENTAIS E PARADIGMAS DE PROJETO", estilo_titulo_secao))
    
    story.append(Paragraph("4.1 Buscas em Grafos: BFS e DFS", estilo_subsecao))
    story.append(Paragraph(
        "As estratégias de travessia sistemática formam a espinha dorsal dos algoritmos sobre grafos:<br/>"
        "• <strong>Busca em Largura (BFS - Breadth-First Search):</strong> explora a rede em 'ondas concêntricas' utilizando uma fila FIFO (First-In, First-Out). "
        "A partir de uma raiz s, todos os vértices à distância 1 são visitados antes dos vértices à distância 2, garantindo que o caminho encontrado "
        "seja o de menor número de arestas em grafos não ponderados. O custo assintótico é O(V + E).<br/>"
        "• <strong>Busca em Profundidade (DFS - Depth-First Search):</strong> avança o mais profundamente possível ao longo de cada ramificação "
        "antes de retroceder (backtracking), operando sobre uma pilha LIFO (ou pilha de recursão). Permite classificar as arestas em árvore, "
        "retorno, avanço e cruzamento, constituindo a base para detecção de componentes fortemente conexos e pontos de corte.",
        estilo_corpo
    ))

    # Figura 3
    caminho_fig_bfs = os.path.join(FIG_DIR, "fig_bfs_ondas.png")
    if os.path.exists(caminho_fig_bfs):
        story.append(Paragraph("Figura 3 – Modelo de propagação em ondas da Busca em Largura (BFS)", estilo_legenda_fig))
        story.append(Image(caminho_fig_bfs, width=13.0*cm, height=7.0*cm))
        story.append(Paragraph("Fonte: Elaborado pelos autores (2026).", estilo_fonte_fig))

    story.append(Paragraph("4.2 Caminhos Mínimos e Ordenação Topológica", estilo_subsecao))
    story.append(Paragraph(
        "Quando as arestas possuem pesos não negativos representando tempos, custos ou distâncias, a BFS deixa de garantir a otimização, "
        "exigindo o algoritmo guloso de <strong>Dijkstra (1959)</strong>. Mantendo uma fila de prioridades (PriorityQueue), o algoritmo "
        "extrai reiteradamente o nó u de menor distância provisória e relaxa suas arestas incidentes: se dist[u] + w(u, v) < dist[v], "
        "atualiza dist[v] e anterior[v]. O custo com heap binário é O((V + E) log V). Pesos negativos invalidam a escolha gulosa, demandando Bellman-Ford.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "Em Grafos Direcionados Acíclicos (DAGs), a <strong>Ordenação Topológica</strong> estabelece uma sequência linear dos vértices compatível "
        "com todas as dependências direcionadas (u → v implica u antes de v). O <strong>Algoritmo de Kahn (1962)</strong> computa iterativamente "
        "os graus de entrada (in-degree); vértices com in-degree zero entram em uma fila, e ao serem processados, decrementam os contadores de seus sucessores. "
        "Se a ordenação final contiver menos de |V| elementos, conclui-se a existência de dependência circular (ciclo).",
        estilo_corpo
    ))

    story.append(Paragraph("4.3 Técnicas de Projeto de Algoritmos (Aula T23)", estilo_subsecao))
    story.append(Paragraph(
        "A disciplina abordou os quatro grandes paradigmas de projeto (GOODRICH; TAMASSIA, 2015):<br/>"
        "1. <strong>Força Bruta:</strong> enumeração exaustiva do espaço de busca. Garante a solução ótima absoluta, com custo frequentemente exponencial, "
        "porém viável e indispensável para validação de instâncias moderadas.<br/>"
        "2. <strong>Algoritmos Gulosos (Greedy):</strong> tomada de decisões míopes locais na esperança de atingir o ótimo global. Ex.: Dijkstra, Kruskal, Prim.<br/>"
        "3. <strong>Divisão e Conquista:</strong> decomposição do problema em subproblemas independentes, resolução recursiva e fusão das respostas. Ex.: MergeSort O(n log n).<br/>"
        "4. <strong>Programação Dinâmica:</strong> memorização de subproblemas sobrepostos com subestrutura ótima. Ex.: algoritmo de Held-Karp para o Caixeiro Viajante O(n² 2^n).",
        estilo_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 5: PANORAMA DE APLICAÇÕES COMPUTACIONAIS
    # =========================================================================
    story.append(Paragraph("5 PANORAMA DE APLICAÇÕES COMPUTACIONAIS", estilo_titulo_secao))
    story.append(Paragraph(
        "A utilidade prática dos grafos reside na sua capacidade de abstrair entidades heterogêneas e suas interações semânticas. "
        "Seguindo as orientações do Prof. Calvetti, o Quadro 1 consolida dez cenários reais onde a Teoria dos Grafos soluciona desafios contemporâneos "
        "sem recorrer ao clichê de mapas geográficos ou roteamento de tráfego viário.",
        estilo_corpo
    ))

    # Tabela 3
    story.append(Paragraph("Tabela 3 – Mapeamento de problemas cotidianos e estruturas de grafos", estilo_legenda_fig))
    tab_app_dados = [
        ["Domínio / Problema", "Vértices (V)", "Arestas (E)", "Algoritmo / Técnica"],
        ["Escalonamento de Provas", "Disciplinas", "Conflito (alunos comuns)", "Coloração de Grafos (Welsh-Powell)"],
        ["Compilação de Pacotes", "Módulos de software", "Dependência direta (A → B)", "Ordenação Topológica (Kahn)"],
        ["Alocação de Plantões", "Médicos e Turnos", "Habilitação / Disponibilidade", "Emparelhamento Bipartido (Hopcroft-Karp)"],
        ["Detecção de Fraude Financeira", "Contas bancárias", "Transações financeiras mútuas", "Componentes Fortemente Conexos (Tarjan)"],
        ["Bioinformática (DNA)", "k-mers (fragmentos)", "Sobreposição de k-1 bases", "Trilha Euleriana em Grafo de De Bruijn"],
        ["Residência Médica", "Candidatos e Hospitais", "Preferências ordenadas", "Algoritmo de Gale-Shapley (Estabilidade)"],
        ["Quadro de Conexões Elétricas", "Postes e Subestações", "Cabos de transmissão", "Árvore Geradora Mínima (Kruskal/Prim)"],
        ["Auditoria de Permissões IAM", "Usuários e Recursos", "Privilégios de acesso", "Busca em Largura (Alcançabilidade)"],
        ["Alocação de Roteadores", "Portas de entrada e saída", "Pacotes enfileirados", "Teorema de Hall em Grafos Bipartidos"],
        ["Contenção de Fake News", "Pessoas em grupos", "Contatos de mensagens", "BFS por Ondas + Pontos de Articulação"]
    ]
    tab_app = Table(tab_app_dados, colWidths=[3.8*cm, 3.5*cm, 4.2*cm, 4.0*cm])
    tab_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2d7be')),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(tab_app)
    story.append(Paragraph("Fonte: Elaborado pelos autores com base na literatura clássica e aulas de ECM306.", estilo_fonte_fig))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 6: ESTUDO DE CASO: RASTREAMENTO E QUARENTENA DE FAKE NEWS
    # =========================================================================
    story.append(Paragraph("6 ESTUDO DE CASO: RASTREAMENTO E QUARENTENA DE FAKE NEWS", estilo_titulo_secao))
    
    story.append(Paragraph("6.1 Formulação do Problema e Perguntas de Modelagem", estilo_subsecao))
    story.append(Paragraph(
        "Apresentada a fundamentação teórica, desenvolve-se a solução do problema prático escolhido: a simulação e contenção da propagação "
        "de desinformação em redes de contatos. Conforme preconizado na Aula T25 (Aplicações Computacionais de Grafos com Java), a modelagem orientada "
        "ao problema deve responder rigorosamente a cinco perguntas diretrizes:",
        estilo_corpo
    ))
    story.append(Paragraph(
        "1. <strong>Quais entidades se tornam vértices?</strong> As pessoas físicas integrantes dos círculos de convivência e grupos de mensagens.<br/>"
        "2. <strong>O que caracteriza uma conexão?</strong> O contato direto mútuo entre duas pessoas através do qual mensagens podem ser retransmitidas.<br/>"
        "3. <strong>A conexão possui direção?</strong> Não. Modela-se como grafo não direcionado, pois o compartilhamento opera bidirecionalmente entre contatos salvos.<br/>"
        "4. <strong>Existe custo, tempo, distância ou capacidade?</strong> Trata-se de grafo não ponderado: cada retransmissão possui o mesmo custo lógico unitário (1 passo).<br/>"
        "5. <strong>A solução procura alcançar, ordenar, cobrir ou atribuir?</strong> O problema visa <em>alcançar</em> (rastrear a onda de contágio) e simultaneamente <em>desconectar estrategicamente</em> (proteger a rede isolando o menor subconjunto crítico).",
        estilo_corpo
    ))

    story.append(Paragraph("6.2 Modelagem Formal e Estrutura dos Dados", estilo_subsecao))
    story.append(Paragraph(
        "A rede representativa desenvolvida para os testes do projeto compreende 28 pessoas (vértices numerados de 0 a 27) e 42 conexões (arestas), "
        "organizadas em cinco comunidades semânticas do cotidiano: Família, Trabalho, Faculdade, Academia e Condomínio. "
        "A rede inclui intencionalmente propriedades topológicas ricas: comunidades internas densas, pontes esparsas entre grupos, "
        "um vértice totalmente isolado (Sônia, id 27) para testar componentes desconexos e uma pessoa com altíssimo número de conexões internas (Marina, id 12, grau 7).",
        estilo_corpo
    ))

    story.append(Paragraph("6.3 Propagação em Ondas via Busca em Largura (BFS)", estilo_subsecao))
    story.append(Paragraph(
        "A difusão do boato a partir do <em>Paciente Zero</em> (origem s) é computada pela classe <code>BuscaEmLargura</code> em Java. "
        "A fila FIFO garante que todos os contatos diretos (distância 1) recebam a mensagem na Onda 1 antes de qualquer retransmissão secundária. "
        "A Tabela 4 ilustra o rastreamento exato da fila para as primeiras etapas da propagação com origem em Ana (id 0), espelhando o formato "
        "didático consagrado pelo Prof. Calvetti na Aula T25.",
        estilo_corpo
    ))

    # Tabela 4
    story.append(Paragraph("Tabela 4 – Rastreamento da fila BFS na rede de teste do estudo de caso", estilo_legenda_fig))
    tab_bfs_dados = [
        ["Etapa", "Fila Antes", "Vértice Retirado", "Novos Vértices Descobertos"],
        ["1", "[Ana]", "Ana (0)", "Bruno (1), Carla (2), Diego (3)"],
        ["2", "[Bruno, Carla, Diego]", "Bruno (1)", "nenhum (já descobertos)"],
        ["3", "[Carla, Diego]", "Carla (2)", "Zeca (24)"],
        ["4", "[Diego, Zeca]", "Diego (3)", "Elisa (4), Fábio (5)"],
        ["5", "[Zeca, Elisa, Fábio]", "Zeca (24)", "Alice (25), Beto (26)"],
        ["6", "[Elisa, Fábio, Alice, Beto]", "Elisa (4)", "nenhum"],
        ["7", "[Fábio, Alice, Beto]", "Fábio (5)", "Gabi (6) — Ponte p/ Trabalho!"]
    ]
    tab_bfs = Table(tab_bfs_dados, colWidths=[2.2*cm, 5.0*cm, 3.8*cm, 4.5*cm])
    tab_bfs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2d7be')),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888'))
    ]))
    story.append(tab_bfs)
    story.append(Paragraph("Fonte: Dados gerados pela execução do software desenvolvido.", estilo_fonte_fig))

    story.append(Paragraph("6.4 Mitigação Exata por Força Bruta vs. Heurística de Grau", estilo_subsecao))
    story.append(Paragraph(
        "Para conter a desinformação, a plataforma deve identificar qual usuário, se colocado em <em>quarentena</em> (bloqueio de repasse), "
        "minimiza o impacto global do boato. Implementou-se um algoritmo exato de Força Bruta: para cada candidato v ∈ V \\ {s}, "
        "simula-se a sua remoção temporária e executa-se uma contagem rápida de alcançados a partir de s. "
        "O número de pessoas protegidas é dado formalmente por: "
        "<br/><br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong>protegidos(v) = alcancados(G) - alcancados(G \\ {v}) - 1</strong><br/><br/>"
        "Com custo O(V · (V + E)), o algoritmo avalia todos os nós e entrega o ótimo absoluto. Paralelamente, computa-se a heurística clássica de maior grau.",
        estilo_corpo
    ))

    # Tabela 5
    story.append(Paragraph("Tabela 5 – Ranking de candidatos à quarentena: Força Bruta vs. Maior Grau", estilo_legenda_fig))
    tab_rank_dados = [
        ["Posição", "Candidato", "Grupo", "Grau", "Protegidos", "Ponto de Articulação?", "Classificação"],
        ["#1", "Diego (id 3)", "Família", "5", "20", "Sim (Tarjan)", "Ótimo Força Bruta"],
        ["#2", "Fábio (id 5)", "Família", "3", "18", "Sim (Tarjan)", "Excelente ponte"],
        ["#3", "Gabi (id 6)", "Trabalho", "3", "17", "Sim (Tarjan)", "Excelente ponte"],
        ["#4", "João (id 9)", "Trabalho", "4", "7", "Sim (Tarjan)", "Ponte Faculdade"],
        ["#5", "Nuno (id 13)", "Faculdade", "4", "6", "Sim (Tarjan)", "Ponte Faculdade"],
        ["—", "Marina (id 12)", "Faculdade", "7", "0", "Não", "Maior Grau (Heurística ERROU!)"]
    ]
    tab_rank = Table(tab_rank_dados, colWidths=[1.8*cm, 3.2*cm, 2.5*cm, 1.5*cm, 2.2*cm, 2.8*cm, 3.5*cm])
    tab_rank.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2d7be')),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888')),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#fce4ec')) # Destaque erro
    ]))
    story.append(tab_rank)
    story.append(Paragraph("Fonte: Saída do módulo Quarentena.java executado sobre a rede do projeto.", estilo_fonte_fig))

    story.append(Paragraph(
        "<strong>O Experimento Didático Central:</strong> Como evidenciado na Tabela 5, a heurística de Maior Grau aponta Marina (id 12, grau 7). "
        "No entanto, bloquear Marina protege <em>zero</em> pessoas adicionais, pois o grupo da Faculdade é densamente interconectado internamente. "
        "Em contrapartida, Diego (id 3) e Fábio (id 5) atuam como pontes de articulação exclusivas, protegendo 20 e 18 pessoas, respectivamente. "
        "Este resultado comprova empiricamente que o maior grau não reflete a importância topológica de estrangulamento de fluxo.",
        estilo_corpo
    ))

    story.append(Paragraph("6.5 Diagnóstico Estrutural por Pontos de Articulação (Tarjan)", estilo_subsecao))
    story.append(Paragraph(
        "Um vértice v é um <em>ponto de articulação</em> (ou de corte) se a sua remoção desconectar o grafo ou elevar o número de componentes conexos. "
        "O algoritmo de <strong>Robert Tarjan (1972)</strong> detecta todos os pontos de corte em uma única passagem DFS em tempo ótimo O(V + E). "
        "Para cada vértice u, mantêm-se dois registros temporais: disc[u] (tempo de descoberta) e low[u] (menor tempo de descoberta alcançável via "
        "arestas de árvore e no máximo uma aresta de retorno). Um vértice não raiz u é articulação se possuir um filho v na árvore DFS tal que "
        "low[v] ≥ disc[u]. No projeto, implementou-se uma versão <em>iterativa</em> com pilha explícita em <code>PontosDeArticulacao.java</code>, "
        "garantindo imunidade a estouros de pilha (StackOverflowError) em grafos massivos.",
        estilo_corpo
    ))

    story.append(Paragraph("6.6 Arquitetura de Software e Interface com o Usuário", estilo_subsecao))
    story.append(Paragraph(
        "O sistema foi concebido sob a premissa arquitetural 'Java Pensa, Navegador Desenha':<br/>"
        "• <strong>Back-end em Java Puro (JDK 21):</strong> composto pelas classes <code>Pessoa</code>, <code>Grafo</code>, <code>BuscaEmLargura</code>, "
        "<code>PontosDeArticulacao</code>, <code>Quarentena</code>, <code>LeitorCSV</code>, <code>GeradorDeRede</code>, <code>Json</code> e <code>ServidorWeb</code>. "
        "O servidor HTTP embutido <code>com.sun.net.httpserver.HttpServer</code> expõe uma API REST leve sem qualquer dependência externa.<br/>"
        "• <strong>Front-end Web Investigativo:</strong> interface rica estilizada como um Quadro de Cortiça policial (polaroids inclinadas, alfinetes coloridos "
        "por grupo, fios vermelhos de varal em SVG, carimbos vintage de 'RECEBEU' e 'BLOQUEADO' e dossiê datilografado).",
        estilo_corpo
    ))

    # Figura 4 - Screenshot
    caminho_fig_screen = os.path.join(FIG_DIR, "fig_screenshot_demo.png")
    if os.path.exists(caminho_fig_screen):
        story.append(Paragraph("Figura 4 – Interface do software 'Caso Fake News: Operação Grafos' em execução", estilo_legenda_fig))
        story.append(Image(caminho_fig_screen, width=15.0*cm, height=9.0*cm))
        story.append(Paragraph("Fonte: Captura de tela gerada automaticamente pelo sistema em execução.", estilo_fonte_fig))

    story.append(Paragraph("6.7 Resultados Experimentais e Análise de Escalabilidade", estilo_subsecao))
    story.append(Paragraph(
        "Para aferir a escalabilidade da força bruta O(V·(V + E)), executou-se a rotina de benchmark da classe <code>ServidorWeb</code> "
        "com o <code>GeradorDeRede</code> sobre instâncias sintéticas variando de 100 a 2000 vértices com comunidades semi-esparsas. "
        "Os tempos foram medidos em ambiente Windows 64-bit sobre a JVM OpenJDK 21 LTS.",
        estilo_corpo
    ))

    # Tabela 6
    story.append(Paragraph("Tabela 6 – Benchmark de tempo de execução da força bruta para diferentes ordens de $V$", estilo_legenda_fig))
    tab_bench_dados = [
        ["Vértices (V)", "Arestas (E)", "Candidatos Avaliados", "Tempo Real (ms)", "Complexidade Teórica V(V+E)"],
        ["100", "204", "99", "11.1 ms", "3,04 × 10⁴ op."],
        ["200", "423", "199", "8.5 ms", "1,24 × 10⁵ op."],
        ["500", "1.115", "499", "30.9 ms", "8,07 × 10⁵ op."],
        ["1.000", "2.207", "999", "62.5 ms", "3,20 × 10⁶ op."],
        ["2.000", "4.433", "1.999", "275.7 ms", "1,28 × 10⁷ op."]
    ]
    tab_bench = Table(tab_bench_dados, colWidths=[2.5*cm, 2.5*cm, 3.5*cm, 3.0*cm, 4.0*cm])
    tab_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2d7be')),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888'))
    ]))
    story.append(tab_bench)
    story.append(Paragraph("Fonte: Medições extraídas do endpoint /api/desempenho da JVM.", estilo_fonte_fig))

    # Figura 5 - Gráfico Benchmark
    caminho_fig_bench = os.path.join(FIG_DIR, "fig_benchmark.png")
    if os.path.exists(caminho_fig_bench):
        story.append(Paragraph("Figura 5 – Benchmark de desempenho da análise de quarentena por força bruta", estilo_legenda_fig))
        story.append(Image(caminho_fig_bench, width=13.0*cm, height=7.2*cm))
        story.append(Paragraph("Fonte: Elaborado pelos autores (2026).", estilo_fonte_fig))

    story.append(Paragraph(
        "Como ilustrado na Figura 5, mesmo para uma rede de 2.000 pessoas e mais de 4.400 conexões mútuas, a análise completa de força bruta "
        "executa em apenas 275 milissegundos na JVM moderna, viabilizando respostas interativas em tempo real. "
        "A concordância com a curva teórica assintótica O(V·(V + E)) confirma a excelência da implementação baseada em lista de adjacência.",
        estilo_corpo
    ))
    story.append(PageBreak())

    # =========================================================================
    # CAPÍTULO 7: CONCLUSÃO
    # =========================================================================
    story.append(Paragraph("7 CONCLUSÃO", estilo_titulo_secao))
    story.append(Paragraph(
        "O presente trabalho de graduação consolidou os principais tópicos da Teoria dos Grafos ministrados na disciplina ECM306, "
        "articulando rigor teórico, análise de complexidade computacional e implementação de engenharia de software funcional.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "A transição da teoria para a prática permitiu demonstrar que a modelagem cuidadosa das entidades e relações é o passo determinante "
        "para o sucesso algorítmico. Ao resolver o problema da contenção de desinformação em redes de contatos, o projeto comprovou de forma "
        "concreta as limitações das heurísticas intuitivas: priorizar o vértice de maior grau em mídias sociais falha frequentemente em conter "
        "epidemias e boatos quando tais nós possuem conexões redundantes intraclasse. Em contrapartida, a combinação entre a Busca em Largura "
        "para propagação em níveis, a Força Bruta para decisão ótima exata e o Algoritmo de Tarjan para identificação de pontes estruturais "
        "forneceu uma ferramenta precisa, didática e de alta eficiência operacional.",
        estilo_corpo
    ))
    story.append(Paragraph(
        "A arquitetura desprovida de frameworks externos ('Java Pensa, Navegador Desenha') demonstrou a robustez do JDK 21 LTS e a portabilidade "
        "do software acadêmico, viabilizando tanto demonstrações gráficas interativas quanto modos de execução resilientes em console. "
        "Como trabalhos futuros, vislumbra-se a incorporação de modelos estocásticos de transmissão (probabilidades de repasse por aresta, simulando "
        "o modelo SIR/SIS epidemiológico) e a introdução de pesos associados ao nível de autoridade e credibilidade dos emissores.",
        estilo_corpo
    ))
    story.append(Spacer(1, 1.0*cm))

    # =========================================================================
    # REFERÊNCIAS
    # =========================================================================
    story.append(Paragraph("REFERÊNCIAS", estilo_titulo_secao))
    referencias = [
        "APPEL, K.; HAKEN, W. Every planar map is four colorable. <strong>Bulletin of the American Mathematical Society</strong>, v. 82, n. 5, p. 711-712, 1976.",
        "BERZTISS, A. T. <strong>Data Structures: Theory and Practice</strong>. 2. ed. New York: Academic Press, 1975.",
        "BOAVENTURA NETTO, P. O. <strong>Grafos: Teoria, Modelos, Algoritmos</strong>. 5. ed. São Paulo: Blucher, 2014.",
        "CALVETTI, J. <strong>Material Didático de ECM306 — Tópicos Avançados de Estrutura de Dados</strong>. São Caetano do Sul: Instituto Mauá de Tecnologia (IMT), 2026. Aulas 17 a 25.",
        "CLARK, J.; HOLTON, D. A. <strong>A First Look at Graph Theory</strong>. Singapore: World Scientific, 1998.",
        "CORMEN, T. H. et al. <strong>Algoritmos: Teoria e Prática</strong>. 3. ed. Rio de Janeiro: Elsevier, 2012.",
        "DIESTEL, R. <strong>Graph Theory</strong>. 5. ed. Berlin: Springer, 2017.",
        "GOLDBARG, M.; GOLDBARG, E. <strong>Grafos: Conceitos, Algoritmos e Aplicações</strong>. Rio de Janeiro: Campus, 2012.",
        "GOODRICH, M. T.; TAMASSIA, R. <strong>Algorithm Design and Applications</strong>. Hoboken: Wiley, 2015.",
        "HALL, P. On representatives of subsets. <strong>Journal of the London Mathematical Society</strong>, v. 10, n. 1, p. 26-30, 1935.",
        "KAHN, A. B. Topological sorting of large networks. <strong>Communications of the ACM</strong>, v. 5, n. 11, p. 558-562, 1962.",
        "KURATOWSKI, K. Sur le problème des courbes gauches en topologie. <strong>Fundamenta Mathematicae</strong>, v. 15, n. 1, p. 271-283, 1930.",
        "NICOLETTI, M. C.; HRUSCHKA JR., E. R. <strong>Fundamentos da Teoria dos Grafos para Computação</strong>. 3. ed. Rio de Janeiro: LTC, 2017.",
        "ROSEN, K. H. <strong>Discrete Mathematics and its Applications</strong>. 7. ed. New York: McGraw-Hill, 2012.",
        "TARJAN, R. Depth-first search and linear graph algorithms. <strong>SIAM Journal on Computing</strong>, v. 1, n. 2, p. 146-160, 1972.",
        "WEST, D. B. <strong>Introduction to Graph Theory</strong>. 2. ed. Upper Saddle River: Prentice Hall, 2001.",
        "WILSON, R. J. <strong>Introduction to Graph Theory</strong>. 4. ed. Harlow: Prentice Hall, 1996."
    ]
    for ref in referencias:
        story.append(Paragraph(ref, estilo_ref))

    # Configuração de início de numeração (Capítulo 1 = Introdução)
    # A Introdução é a página 7 (após Capa, Folha de Rosto, Resumo, Abstract, Listas, Sumário)
    def marcar_canvas(canvas_obj, doc_obj):
        canvas_obj.pagina_introducao = 7

    doc.build(story, canvasmaker=ABNTCanvas, onFirstPage=marcar_canvas)
    print(f"Relatório ABNT gerado com sucesso em: {SAIDA_PDF}")

if __name__ == "__main__":
    construir_relatorio()
