"""
Gerador da Apresentação PPTX — "Caso Fake News: Operação Grafos"
Design Reformulado e Profissional — Tema "Jornal Investigativo / Dossiê Policial"

Correções de Design:
1. Fontes ampliadas para legibilidade de projeção (12pt-14pt corpo, 15pt-18pt subtítulos, 20pt-28pt títulos).
2. Eliminação completa de espaços vazios nos cartões com distribuição vertical balanceada.
3. Proporção exata das imagens e cartões sem transbordamentos.
4. Cores e contraste calibrados (#141414, #282828, #1B365D, #C0392B sobre fundos claros).
5. Notas de fala com roteiro cronometrado para David e Kauã (~5 minutos).

ECM306 - Tópicos Avançados de Estrutura de Dados | Instituto Mauá de Tecnologia
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
FIG_DIR = os.path.join(RAIZ_DIR, "documentos", "comum", "figuras")
SAIDA_PPTX = os.path.join(RAIZ_DIR, "Entrega", "Apresentacao_Caso_Fake_News.pptx")
os.makedirs(os.path.dirname(SAIDA_PPTX), exist_ok=True)

# Paleta refinada
COR_FUNDO = RGBColor(251, 248, 241)          # #FBF8F1 Papel jornal suave
COR_TINTA_ESCURA = RGBColor(20, 20, 20)       # #141414 Preto carvão
COR_TINTA_CORPO = RGBColor(40, 40, 40)        # #282828 Texto escuro nítido
COR_VERMELHO_FIO = RGBColor(192, 57, 43)      # #C0392B Vermelho investigativo
COR_VERMELHO_ESCURO = RGBColor(140, 25, 15)   # #8C190F
COR_VERDE_CARIMBO = RGBColor(39, 174, 96)     # #27AE60 Verde resolvido
COR_AZUL_MARINHO = RGBColor(27, 54, 93)       # #1B365D Azul institucional
COR_AMARELO_POSTIT = RGBColor(254, 249, 231)  # #FEF9E7 Amarelo post-it suave
COR_BORDA_POSTIT = RGBColor(212, 172, 13)     # #D4AC0D
COR_BRANCO = RGBColor(255, 255, 255)
COR_CINZA_BORDA = RGBColor(200, 195, 185)     # #C8C3B9

def criar_apresentacao():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Layout em branco

    # -------------------------------------------------------------
    # Helpers Visuais
    # -------------------------------------------------------------
    def aplicar_fundo(slide, subtitulo_tarja="INQUÉRITO ESPECIAL: TEORIA DOS GRAFOS"):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COR_FUNDO
        bg.line.color.rgb = COR_TINTA_ESCURA
        bg.line.width = Pt(2.5)

        tarja = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.28), Inches(12.533), Inches(0.42))
        tarja.fill.solid()
        tarja.fill.fore_color.rgb = COR_TINTA_ESCURA
        tarja.line.fill.background()
        tf = tarja.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = f"★ {subtitulo_tarja} — ECM306 — INSTITUTO MAUÁ DE TECNOLOGIA ★"
        p.font.name = "Georgia"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COR_BRANCO
        p.alignment = PP_ALIGN.CENTER

    def add_titulo(slide, titulo_texto, largura=9.2, tamanho_pt=22):
        tx = slide.shapes.add_textbox(Inches(0.6), Inches(0.82), Inches(largura), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.text = titulo_texto
        p.font.name = "Georgia"
        p.font.size = Pt(tamanho_pt)
        p.font.bold = True
        p.font.color.rgb = COR_TINTA_ESCURA

    def add_carimbo(slide, texto, left, top, width, height, cor=COR_VERMELHO_FIO, rot=-4):
        s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        s.fill.solid()
        s.fill.fore_color.rgb = COR_BRANCO
        s.line.color.rgb = cor
        s.line.width = Pt(2.5)
        s.rotation = rot
        tf = s.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = texto
        p.font.name = "Trebuchet MS"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = cor
        p.alignment = PP_ALIGN.CENTER
        return s

    def add_card(slide, left, top, width, height, cor_fundo=COR_BRANCO, cor_borda=COR_CINZA_BORDA, largura_borda=1.5):
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = cor_fundo
        card.line.color.rgb = cor_borda
        card.line.width = Pt(largura_borda)
        card.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        card.text_frame.margin_left = Inches(0.2)
        card.text_frame.margin_right = Inches(0.2)
        card.text_frame.margin_top = Inches(0.18)
        card.text_frame.margin_bottom = Inches(0.18)
        return card

    # =============================================================
    # SLIDE 1: CAPA — MANCHETE DE JORNAL
    # =============================================================
    s1 = prs.slides.add_slide(slide_layout)
    aplicar_fundo(s1, "INQUÉRITO ESPECIAL: TEORIA DOS GRAFOS")
    add_carimbo(s1, "CONFIDENCIAL", Inches(10.5), Inches(0.85), Inches(2.2), Inches(0.55), COR_VERMELHO_FIO, -5)

    tx1 = s1.shapes.add_textbox(Inches(0.6), Inches(0.82), Inches(9.8), Inches(1.8))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    tf1.vertical_anchor = MSO_ANCHOR.TOP
    p = tf1.paragraphs[0]
    p.text = "CASO FAKE NEWS: OPERAÇÃO GRAFOS"
    p.font.name = "Georgia"
    p.font.size = Pt(29)
    p.font.bold = True
    p.font.color.rgb = COR_TINTA_ESCURA

    p2 = tf1.add_paragraph()
    p2.text = "Boato viral atinge 27 pessoas em 4 rodadas: rastreamento por BFS e contenção por Quarentena e Pontos de Articulação"
    p2.font.name = "Calibri"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(90, 90, 90)
    p2.space_before = Pt(5)

    # Cartão Dossiê (Esquerda)
    card_dos = add_card(s1, Inches(0.6), Inches(2.6), Inches(6.0), Inches(4.5), COR_BRANCO, COR_TINTA_ESCURA, 2)
    tf_dos = card_dos.text_frame
    tf_dos.word_wrap = True
    p = tf_dos.paragraphs[0]
    p.text = "DOSSIÊ DE INVESTIGAÇÃO TÉCNICA"
    p.font.name = "Georgia"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_FIO

    itens_dossie = [
        ("Disciplina:", "ECM306 — Tópicos Avançados de Estrutura de Dados"),
        ("Instituição:", "Instituto Mauá de Tecnologia (IMT)"),
        ("Orientador:", "Prof. José Calvetti"),
        ("Investigadores:", "David Sanchez Bittencourt Daniel (RA: 24.00029-9)\nKauã Bueno Marcatto Ortega (RA: 24.00031-0)"),
        ("Problema Central:", "Propagação e Quarentena em Redes de Mensagens"),
        ("Abordagem:", "Busca em Largura (BFS), Força Bruta e Algoritmo de Tarjan"),
        ("Implementação:", "100% Java Puro (JDK 21) + Interface Web Investigativa")
    ]
    for rotulo, val in itens_dossie:
        p = tf_dos.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {rotulo} "
        run1.bold = True
        run1.font.name = "Calibri"
        run1.font.size = Pt(12)
        run1.font.color.rgb = COR_TINTA_ESCURA
        
        run2 = p.add_run()
        run2.text = val
        run2.font.name = "Calibri"
        run2.font.size = Pt(12)
        run2.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(4)

    # Imagem à direita perfeitamente contida no cartão
    c_img = add_card(s1, Inches(6.8), Inches(2.6), Inches(5.9), Inches(4.5), COR_BRANCO, COR_CINZA_BORDA, 1.5)
    caminho_fig_bfs = os.path.join(FIG_DIR, "fig_bfs_ondas.png")
    if os.path.exists(caminho_fig_bfs):
        s1.shapes.add_picture(caminho_fig_bfs, Inches(7.25), Inches(2.8), height=Inches(4.1))

    s1.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 1 | ~45 segundos]\n\n"
        "[DAVID]: Olá a todos, olá professor Calvetti. Hoje apresentamos o nosso projeto semestral de Tópicos Avançados de Estrutura de Dados, "
        "intitulado 'Caso Fake News: Operação Grafos'. Eu sou o David e estou acompanhado do Kauã.\n\n"
        "[KAUÃ]: Fugindo intencionalmente de formulações clichês como rotas de GPS e mapas viários, decidimos aplicar a Teoria dos Grafos a um dos problemas "
        "mais urgentes da sociedade moderna: a propagação viral de desinformação em redes de mensagens. Desenvolvemos uma solução computacional 100% em Java "
        "para rastrear o contágio em ondas e determinar, matematicamente, quem deve ser colocado em quarentena para conter o boato."
    )

    # =============================================================
    # SLIDE 2: O CRIME — A MENSAGEM VIRAL
    # =============================================================
    s2 = prs.slides.add_slide(slide_layout)
    aplicar_fundo(s2, "OCORRÊNCIA: O DELITO DA DESINFORMAÇÃO")
    add_titulo(s2, "O PROBLEMA: 'ENCAMINHADA COM FREQUÊNCIA'")
    add_carimbo(s2, "BOATO DETECTADO", Inches(10.2), Inches(0.85), Inches(2.5), Inches(0.55), COR_VERMELHO_FIO, 4)

    # Balão estilo mensagem de WhatsApp
    balao = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.8), Inches(5.8), Inches(2.1))
    balao.fill.solid()
    balao.fill.fore_color.rgb = RGBColor(220, 248, 198)
    balao.line.color.rgb = RGBColor(140, 190, 120)
    balao.line.width = Pt(1.5)
    tf_b = balao.text_frame
    tf_b.word_wrap = True
    tf_b.vertical_anchor = MSO_ANCHOR.TOP
    tf_b.margin_left = Inches(0.2)
    tf_b.margin_right = Inches(0.2)
    tf_b.margin_top = Inches(0.15)
    
    p = tf_b.paragraphs[0]
    p.text = "↗ Encaminhada com frequência"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.italic = True
    p.font.color.rgb = RGBColor(90, 90, 90)

    p = tf_b.add_paragraph()
    p.text = "\"URGENTE: Nova taxa bancária do PIX entra em vigor amanhã às 8h! Repasse imediatamente para todos os seus grupos de família e trabalho para cancelar a cobrança automática!\""
    p.font.name = "Calibri"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COR_TINTA_ESCURA
    p.space_before = Pt(6)

    # Carimbo "FAKE NEWS" logo abaixo do balão
    add_carimbo(s2, "FAKE NEWS", Inches(3.8), Inches(3.6), Inches(2.3), Inches(0.52), COR_VERMELHO_FIO, -7)

    # Post-it inferior esquerdo
    postit = add_card(s2, Inches(0.6), Inches(4.2), Inches(5.8), Inches(2.1), COR_AMARELO_POSTIT, COR_BORDA_POSTIT, 1.5)
    postit.rotation = -1
    tf_pos = postit.text_frame
    tf_pos.word_wrap = True
    p = tf_pos.paragraphs[0]
    p.text = "NOTA METODOLÓGICA & PARADIGMA:"
    p.font.name = "Georgia"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_ESCURO
    
    itens_postit = [
        ("• O problema NÃO é geográfico:", "A distância é em 'graus de separação' e saltos lógicos."),
        ("• Propagação em Ondas Discretas:", "Cada repasse representa uma rodada de contágio (onda BFS)."),
        ("• Escala do Problema:", "Na rede piloto: 27 infectados em 4 rodadas sem intervenção!")
    ]
    for rot, desc in itens_postit:
        p = tf_pos.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{rot} "
        run1.bold = True
        run1.font.name = "Calibri"
        run1.font.size = Pt(11)
        run1.font.color.rgb = COR_TINTA_ESCURA
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = "Calibri"
        run2.font.size = Pt(11)
        run2.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(2)

    # Faixa tática inferior esquerda
    faixa_tat = add_card(s2, Inches(0.6), Inches(6.45), Inches(5.8), Inches(0.55), COR_BRANCO, COR_VERMELHO_FIO, 1.5)
    tf_tat = faixa_tat.text_frame
    tf_tat.word_wrap = True
    tf_tat.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_tat.paragraphs[0]
    p.text = "⚡ DECISÃO TÁTICA: Conter a 1ª onda (Fábio/Diego) blinda até 74% da rede!"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_ESCURO

    # Lado Direito: As 3 Perguntas Fundamentais do Inquérito
    card_perg = add_card(s2, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.2), COR_BRANCO, COR_TINTA_ESCURA, 2)
    tf_p = card_perg.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "AS 3 PERGUNTAS FUNDAMENTAIS DO INQUÉRITO"
    p.font.name = "Georgia"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_MARINHO

    perguntas = [
        ("1. Rastreamento do Contágio (Alcance)", 
         "A partir de um Paciente Zero, quem são todas as pessoas que recebem o boato?",
         "Solução em Grafos: Componente conexa alcançável calculada via BFS O(V + E).",
         COR_AZUL_MARINHO),
        ("2. Velocidade da Difusão (Tempo / Rodadas)", 
         "Em quantas rodadas a mensagem contamina todas as comunidades alcançáveis?",
         "Solução em Grafos: Excentricidade e raio BFS. Na rede piloto: dist_max = 4 rodadas.",
         COR_TINTA_ESCURA),
        ("3. Contenção Ótima (Quarentena)", 
         "Se pudermos conscientizar apenas UMA pessoa, quem protegerá mais cidadãos?",
         "Solução em Grafos: Força Bruta O(V·(V+E)) e Pontos de Articulação de Tarjan O(V+E).",
         COR_VERMELHO_FIO)
    ]
    for tit, desc, solucao, cor_dest in perguntas:
        p = tf_p.add_paragraph()
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = cor_dest
        p.space_before = Pt(10)
        
        p2 = tf_p.add_paragraph()
        p2.text = f"• Pergunta: {desc}"
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.color.rgb = COR_TINTA_CORPO
        p2.space_before = Pt(2)

        p3 = tf_p.add_paragraph()
        run = p3.add_run()
        run.text = f"✔ Resposta: {solucao}"
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(11.5)
        run.font.color.rgb = cor_dest
        p3.space_before = Pt(2)

    s2.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 2 | ~50 segundos]\n\n"
        "[DAVID]: Todos nós já recebemos mensagens alarmistas com o selo 'Encaminhada com frequência' no WhatsApp: notícias falsas sobre saúde, "
        "fraudes financeiras ou falsas taxas bancárias. Quando alguém aperta 'encaminhar', deflagra um contágio em cadeia.\n\n"
        "[KAUÃ]: Diante desse crime informacional, o nosso papel como engenheiros de computação é responder a três perguntas exatas: "
        "Primeiro: quem a notícia alcança? Segundo: em quantas rodadas de repasse? E terceiro, a decisão mais difícil: se tivermos recurso limitado "
        "para intervir e conscientizar apenas uma pessoa para que ela não repasse o boato, quem devemos escolher para salvar o maior número de pessoas?"
    )

    # =============================================================
    # SLIDE 3: A MODELAGEM — AS 5 PERGUNTAS DE CALVETTI
    # =============================================================
    s3 = prs.slides.add_slide(slide_layout)
    aplicar_fundo(s3, "EVIDÊNCIAS: DA REALIDADE AO GRAFO")
    add_titulo(s3, "A MODELAGEM: AS 5 PERGUNTAS DE CALVETTI (AULA T25)", largura=12.0, tamanho_pt=21)

    cards_mod = [
        ("VÉRTICES (V)", 
         "Pessoas da rede social.\n\n"
         "• ID: 0 a N-1 sequencial\n"
         "• Rótulo: Nome e Grupo Social\n"
         "• Grau d(v): Contatos diretos\n"
         "• 5 Grupos: Família, Trabalho, Faculdade, Academia, Condomínio\n"
         "• Estado: Suscetível / Quarentena", 
         COR_AZUL_MARINHO),
        
        ("ARESTAS (E)", 
         "Contatos salvos na agenda.\n\n"
         "• Não direcionada: Conversa mútua\n"
         "• Sem pesos: Cada repasse = 1 salto\n"
         "• Grafo Simples: Sem laços nem paralelas\n"
         "• Topologia: Esparsa (|E| ≪ |V|²)\n"
         "• Total Piloto: |E| = 42 arestas mútuas", 
         COR_VERMELHO_FIO),
        
        ("REPRESENTAÇÃO", 
         "Lista de Adjacência em Java Puro.\n\n"
         "• Memória: O(V + E) ótimo\n"
         "• Varredura: O(d(v)) para vizinhos\n"
         "• Estrutura: List<List<Integer>> nativa\n"
         "• Matriz O(V²): Descartada\n"
         "• Economia: 84 nós vs. 784 células!", 
         COR_TINTA_ESCURA),
        
        ("OBJETIVOS GÊMEOS", 
         "Rastrear Alcance & Conter Fluxo.\n\n"
         "1. Rastrear: BFS calcula menor caminho em saltos lógicos\n"
         "2. Conter: Encontrar corte ótimo que divide a rede em blocos blindados\n"
         "3. Comparar: Heurística gulosa vs. Topologia e Pontos de Articulação", 
         COR_VERMELHO_ESCURO)
    ]
    for idx, (tit, corpo, cor_borda) in enumerate(cards_mod):
        x = Inches(0.6 + idx * 3.1)
        c = add_card(s3, x, Inches(1.8), Inches(2.9), Inches(3.2), COR_BRANCO, cor_borda, 2)
        tf = c.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = cor_borda
        
        for linha in corpo.split("\n"):
            p2 = tf.add_paragraph()
            p2.text = linha
            p2.font.name = "Calibri"
            p2.font.size = Pt(10.5)
            p2.font.color.rgb = COR_TINTA_CORPO
            p2.space_before = Pt(2) if linha else Pt(3)

    # Faixa inferior dashboard com alto contraste e métricas
    faixa_inf = add_card(s3, Inches(0.6), Inches(5.15), Inches(12.133), Inches(1.85), COR_AMARELO_POSTIT, COR_BORDA_POSTIT, 2)
    tf_f = faixa_inf.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "PROPRIEDADES ESTRUTURAIS DA REDE PILOTO (28 PESSOAS, 42 CONTATOS):"
    p.font.name = "Georgia"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_ESCURO

    metricas_rede = [
        ("• Lema do Aperto de Mãos (Teorema 1, Aula T17):", "∑ d(v) = 2|E| = 84 contatos totais na rede. O grau médio dos participantes é exatamente 3,0 contatos/pessoa."),
        ("• Comunidades e Diâmetro:", "A rede divide-se em 5 clusters densos conectados por pontes raras. O diâmetro é de 4 saltos lógicos (excentricidade máxima da BFS)."),
        ("• Gargalos Críticos de Articulação:", "O algoritmo de Tarjan identifica 7 pontos de articulação vitais (Diego, Fábio, Beto, etc.) cuja remoção desconecta componentes inteiros."),
        ("• Fenômeno do 'Mundo Pequeno':", "Espelha com precisão a estrutura das redes sociais reais (modelo de Watts-Strogatz), com alto agrupamento local e caminhos curtos.")
    ]
    for rot, desc in metricas_rede:
        p = tf_f.add_paragraph()
        run1 = p.add_run()
        run1.text = f"{rot} "
        run1.bold = True
        run1.font.name = "Calibri"
        run1.font.size = Pt(11)
        run1.font.color.rgb = COR_TINTA_ESCURA
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = "Calibri"
        run2.font.size = Pt(11)
        run2.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(2)

    s3.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 3 | ~50 segundos]\n\n"
        "[DAVID]: Na aula T25, o professor Calvetti enfatizou que a realidade não determina o grafo sozinha: a pergunta define a modelagem útil. "
        "Aqui, cada vértice é uma pessoa física e cada aresta é um contato mútuo salvo na agenda de mensagens.\n\n"
        "[KAUÃ]: Não usamos arestas direcionadas porque quem conversa pode tanto enviar quanto receber. Também não usamos pesos, porque cada repasse "
        "representa uma rodada lógica discreta. Escolhemos a Lista de Adjacência porque, em redes sociais esparsas, ela consome O(V + E) de memória, "
        "muito superior à Matriz O(V²). Montamos uma rede piloto com 28 pessoas em 5 grupos do cotidiano para validar os algoritmos."
    )

    # =============================================================
    # SLIDE 4: A PERSEGUIÇÃO — BFS EM ONDAS
    # =============================================================
    s4 = prs.slides.add_slide(slide_layout)
    aplicar_fundo(s4, "INVESTIGAÇÃO: O ALGORITMO DA PERSEGUIÇÃO")
    add_titulo(s4, "A PROPAGAÇÃO: BUSCA EM LARGURA (BFS)", largura=9.2, tamanho_pt=22)
    add_carimbo(s4, "CUSTO: O(V + E)", Inches(10.3), Inches(0.85), Inches(2.4), Inches(0.55), COR_AZUL_MARINHO, 0)

    # Bloco explicativo da BFS com alinhamento ao topo perfeito
    bloco_bfs = add_card(s4, Inches(0.6), Inches(1.8), Inches(5.8), Inches(5.2), COR_BRANCO, COR_AZUL_MARINHO, 2)
    tf = bloco_bfs.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "MECÂNICA DAS ONDAS DE CONTÁGIO (AULA T25)"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_MARINHO

    itens_bfs = [
        ("Fila FIFO (ArrayDeque):", "Garante que nós à distância 'd' sejam explorados antes dos nós 'd + 1'."),
        ("Vetor dist[]:", "Iniciado em -1 para distinguir visitados de inalcançáveis. dist[origem] = 0."),
        ("Vetor anterior[]:", "Registra o predecessor na árvore BFS para reconstituir a rota exata do boato."),
        ("Simulação de Quarentena:", "Se um nó está em quarentena, a BFS ignora suas arestas incidentes.")
    ]
    for tit, desc in itens_bfs:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {tit} "
        run1.bold = True
        run1.font.name = "Georgia"
        run1.font.size = Pt(11.5)
        run1.font.color.rgb = COR_TINTA_ESCURA
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = "Calibri"
        run2.font.size = Pt(11)
        run2.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(4)

    # Passo a passo da rede piloto
    p = tf.add_paragraph()
    p.text = "Linha do Tempo da Propagação (Origem: Ana, id 0):"
    p.font.name = "Georgia"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_FIO
    p.space_before = Pt(6)

    passos_tempo = [
        "Onda 0 (t=0): Ana (Família) cria e dispara o boato.",
        "Onda 1 (t=1): Fábio, Bruno, Carla recebem (Família).",
        "Onda 2 (t=2): Diego (Trabalho), Beto, Zeca (Condomínio).",
        "Onda 3 (t=3): Wesley, Yara, João, Karen, Luísa...",
        "Onda 4 (t=4): Marina, Otávio, Pedro, Quênia, Sofia...",
        "Conclusão: 27 de 28 pessoas infectadas. Apenas Sônia (isolada) é imune!",
        "Custo Computacional: O(V + E) = 70 operações na rede piloto (< 0,1 ms)."
    ]
    for pt in passos_tempo:
        p = tf.add_paragraph()
        p.text = f"  › {pt}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = COR_TINTA_ESCURA if ("Conclusão" in pt or "Custo" in pt) else COR_TINTA_CORPO
        if "Conclusão" in pt or "Custo" in pt:
            p.font.bold = True
        p.space_before = Pt(1)

    # Imagem da tela da aplicação à direita com moldura e legenda
    c_img = add_card(s4, Inches(6.8), Inches(1.8), Inches(5.9), Inches(5.2), COR_BRANCO, COR_CINZA_BORDA, 1.5)
    caminho_fig_screen = os.path.join(FIG_DIR, "fig_screenshot_demo.png")
    if os.path.exists(caminho_fig_screen):
        s4.shapes.add_picture(caminho_fig_screen, Inches(7.0), Inches(2.0), width=Inches(5.5))

    # Legenda da figura dentro do cartão
    tx_leg = s4.shapes.add_textbox(Inches(7.0), Inches(5.7), Inches(5.5), Inches(1.2))
    tf_leg = tx_leg.text_frame
    tf_leg.word_wrap = True
    tf_leg.vertical_anchor = MSO_ANCHOR.TOP
    p = tf_leg.paragraphs[0]
    p.text = "Figura: Interface Investigativa Web desenvolvida em HTML5 Canvas/CSS3 puro, conectada ao backend Java 21 via HTTP REST (porta 8080). Permite simular a BFS passo a passo e testar quarentenas ao vivo."
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(90, 90, 90)

    s4.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 4 | ~50 segundos]\n\n"
        "[DAVID]: Para rastrear a propagação, aplicamos a clássica Busca em Largura (BFS). Como todas as conexões têm o mesmo peso lógico, "
        "a BFS é o algoritmo matematicamente ótimo para computar o menor número de passos.\n\n"
        "[KAUÃ]: A fila FIFO funciona como uma onda expansiva: na Onda 0 temos o paciente zero. Na Onda 1, todos os contatos imediatos. "
        "Se alguém estiver bloqueado na quarentena, o algoritmo simplesmente não enfileira seus vizinhos, contendo a onda naquele ponto. "
        "Além disso, a BFS nos entrega o vetor anterior, permitindo rastrear o caminho reverso da mentira até quem a originou."
    )

    # =============================================================
    # SLIDE 5: A QUARENTENA — FORÇA BRUTA VS MAIOR GRAU
    # =============================================================
    s5 = prs.slides.add_slide(slide_layout)
    aplicar_fundo(s5, "DIAGNÓSTICO: O DILEMA DA QUARENTENA")
    add_titulo(s5, "QUARENTENA: FORÇA BRUTA VS. HEURÍSTICA DE GRAU", largura=9.0, tamanho_pt=20)
    add_carimbo(s5, "AULA T23: PARADIGMAS", Inches(9.8), Inches(0.85), Inches(2.9), Inches(0.55), COR_VERMELHO_FIO, 2)

    # Coluna 1: Força Bruta Exata
    c_fb = add_card(s5, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.5), COR_BRANCO, COR_AZUL_MARINHO, 2)
    tf = c_fb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FORÇA BRUTA EXATA — O(V · (V + E))"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_MARINHO

    itens_fb = [
        ("Como Opera:", "Simula a remoção temporária de cada pessoa elegível da rede e executa uma BFS rápida a partir da origem."),
        ("Fórmula de Proteção:", "protegidos(v) = alcançados_base − alcançados_sem_v − 1"),
        ("Garantia Matemática:", "Encontra o ótimo global absoluto com 100% de precisão, sem risco de cair em mínimos locais ou heurísticas míopes."),
        ("Robustez Topológica:", "Não depende de heurísticas nem de grafos planares; funciona com qualquer topologia conexa arbitrária."),
        ("Conclusão Prática:", "A Força Bruta prova quem é o melhor corte sem falsos positivos. Em redes de milhares de nós, seu custo polinomial roda em frações de segundo.")
    ]
    for tit, desc in itens_fb:
        p = tf.add_paragraph()
        run1 = p.add_run()
        run1.text = f"• {tit} "
        run1.bold = True
        run1.font.name = "Georgia"
        run1.font.size = Pt(11.5)
        run1.font.color.rgb = COR_TINTA_ESCURA
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = "Calibri"
        run2.font.size = Pt(11)
        run2.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(4)

    p = tf.add_paragraph()
    p.text = "Escalabilidade Experimental Comprovada:"
    p.font.name = "Georgia"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_MARINHO
    p.space_before = Pt(6)

    benchmark_fb = [
        ("Rede Piloto (N = 28, E = 42):", "< 2 ms (1.960 operações elementares)"),
        ("Rede Média (N = 500):", "14 ms"),
        ("Rede Grande (N = 2.000):", "275 ms (100% viável em tempo real)")
    ]
    for cenario, tempo in benchmark_fb:
        p = tf.add_paragraph()
        p.text = f"  › {cenario} {tempo}"
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(1)

    # Coluna 2: O Experimento Didático
    c_heu = add_card(s5, Inches(6.8), Inches(1.8), Inches(5.9), Inches(4.5), RGBColor(254, 245, 245), COR_VERMELHO_FIO, 2)
    tf_h = c_heu.text_frame
    tf_h.word_wrap = True

    p = tf_h.paragraphs[0]
    p.text = "O EXPERIMENTO DIDÁTICO: A HEURÍSTICA ERROU!"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_ESCURO

    p = tf_h.add_paragraph()
    run = p.add_run()
    run.text = "1. Intuição Míope (Maior Grau): MARINA (id 12, grau 7)"
    run.bold = True
    run.font.name = "Georgia"
    run.font.size = Pt(12)
    run.font.color.rgb = COR_AZUL_MARINHO
    p.space_before = Pt(6)

    p2 = tf_h.add_paragraph()
    p2.text = "• Marina é a mais popular da rede (7 amigos na Faculdade).\n• Ao isolar Marina, seus colegas ainda se comunicam por rotas alternativas internas na clique da faculdade.\n• Resultado: ZERO pessoas protegidas! Eficácia: 0%."
    p2.font.name = "Calibri"
    p2.font.size = Pt(11)
    p2.font.color.rgb = COR_TINTA_CORPO
    p2.space_before = Pt(2)

    p3 = tf_h.add_paragraph()
    run = p3.add_run()
    run.text = "2. Ótimo da Topologia: DIEGO (grau 5) e FÁBIO (grau 3)"
    run.bold = True
    run.font.name = "Georgia"
    run.font.size = Pt(12)
    run.font.color.rgb = COR_VERMELHO_FIO
    p3.space_before = Pt(8)

    p4 = tf_h.add_paragraph()
    p4.text = "• Diego e Fábio possuem grau menor, mas são PONTOS DE ARTICULAÇÃO identificados pelo algoritmo de Tarjan.\n• Eles constituem as únicas pontes ligando a Família ao Trabalho e às demais comunidades.\n• Ao bloquear Diego ou Fábio: até 20 cidadãos são blindados (74% da rede protegida)!"
    p4.font.name = "Calibri"
    p4.font.size = Pt(11)
    p4.font.color.rgb = COR_TINTA_CORPO
    p4.space_before = Pt(2)

    p5 = tf_h.add_paragraph()
    run = p5.add_run()
    run.text = "3. Placar Final da Disputa:"
    run.bold = True
    run.font.name = "Georgia"
    run.font.size = Pt(11.5)
    run.font.color.rgb = COR_VERMELHO_ESCURO
    p5.space_before = Pt(6)

    p6 = tf_h.add_paragraph()
    p6.text = "  › Heurística Gulosa (Marina, grau 7): 0 cidadãos blindados (0%)\n  › Corte de Tarjan / Força Bruta (Diego, grau 5): 20 blindados (74%)"
    p6.font.name = "Calibri"
    p6.font.size = Pt(10.5)
    p6.font.bold = True
    p6.font.color.rgb = COR_TINTA_ESCURA
    p6.space_before = Pt(1)

    # Faixa inferior unificada com Tarjan e Carimbo
    faixa_s5 = add_card(s5, Inches(0.6), Inches(6.45), Inches(8.0), Inches(0.75), COR_AMARELO_POSTIT, COR_BORDA_POSTIT, 1.5)
    tf_s5 = faixa_s5.text_frame
    tf_s5.word_wrap = True
    tf_s5.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_s5.paragraphs[0]
    p.text = "⚡ FILTRO DE TARJAN EM O(V+E): Identifica os 7 pontos de corte em 8 ms para 2.000 nós, comprovando que a topologia global supera o grau local!"
    p.font.name = "Calibri"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_MARINHO

    add_carimbo(s5, "PONTES VENCEM GRAU", Inches(8.9), Inches(6.45), Inches(3.8), Inches(0.6), COR_VERMELHO_FIO, 0)

    s5.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 5 | ~55 segundos]\n\n"
        "[DAVID]: Aqui chegamos ao momento mais fascinante do trabalho, que conecta diretamente com a Aula T23 sobre técnicas de projeto de algoritmos. "
        "A intuição comum diz: 'bloqueie a pessoa mais popular da rede, a que tem maior grau de amizades'.\n\n"
        "[KAUÃ]: Na nossa rede, a pessoa com mais contatos é a Marina, com grau 7 no grupo da faculdade. Mas a nossa análise de Força Bruta "
        "comprovou que bloquear a Marina protege ZERO pessoas adicionais! Porque o grupo dela é hiperconectado por dentro. "
        "Já o Diego e o Fábio, que têm grau menor, protegem 20 e 18 pessoas! Isso acontece porque, pelo Algoritmo de Tarjan, eles são Pontos de Articulação, "
        "as únicas pontes entre comunidades inteiras. A topologia estrutural vence a popularidade isolada."
    )

    # =============================================================
    # SLIDE 6: CASO ENCERRADO — CONCLUSÕES & DEMO
    # =============================================================
    s6 = prs.slides.add_slide(slide_layout)
    aplicar_fundo(s6, "VEREDITO: CASO ENCERRADO")
    add_titulo(s6, "SÍNTESE DO INQUÉRITO E DEMONSTRAÇÃO AO VIVO", largura=8.8, tamanho_pt=20)
    add_carimbo(s6, "CASO ENCERRADO", Inches(9.8), Inches(0.85), Inches(2.9), Inches(0.55), COR_VERDE_CARIMBO, -3)

    conclusoes = [
        ("1. Topologia Estrutural Vence a Intuição Local", 
         "A popularidade de um nó (alto grau) não implica relevância em cortes. Pontes de articulação são os gargalos reais de fluxo na rede.",
         "Evidência: Marina (grau 7) salva 0 pessoas; Diego (grau 5, ponte) salva 20 pessoas (74% da rede protegida).",
         COR_AZUL_MARINHO),
        ("2. Eficiência Polinomial e Escalabilidade Real", 
         "BFS em O(V+E) e Tarjan em O(V+E) rodam em frações de milissegundo. A Força Bruta em O(V·(V+E)) computa o corte global ótimo em tempo hábil.",
         "Evidência: 28 nós em < 2 ms; 500 nós em 14 ms; 2.000 nós em 275 ms (100% aplicável em produção).",
         COR_TINTA_ESCURA),
        ("3. Filosofia 'Java Pensa, Navegador Desenha'", 
         "Zero frameworks pesados: o algoritmo roda no JDK 21 puro via Lista de Adjacência nativa, com visualização pedagógica em HTML5 Canvas.",
         "Evidência: Código desacoplado, suíte de testes unitários passando em 100% e servidor HTTP nativo sem dependências.",
         COR_VERMELHO_FIO)
    ]
    for idx, (tit, desc, evid, cor_tit) in enumerate(conclusoes):
        y = Inches(1.8 + idx * 1.7)
        box = add_card(s6, Inches(0.6), y, Inches(7.5), Inches(1.58), COR_BRANCO, COR_TINTA_ESCURA, 1.5)
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = cor_tit

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Calibri"
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = COR_TINTA_CORPO
        p2.space_before = Pt(3)

        p3 = tf.add_paragraph()
        run = p3.add_run()
        run.text = f"✔ {evid}"
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(11)
        run.font.color.rgb = cor_tit
        p3.space_before = Pt(3)

    # Chamada para Demonstração (Lado direito)
    box_demo = add_card(s6, Inches(8.4), Inches(1.8), Inches(4.3), Inches(5.2), COR_AMARELO_POSTIT, COR_BORDA_POSTIT, 2)
    tf_d = box_demo.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "PROVA MATERIAL:"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_TINTA_ESCURA
    p.alignment = PP_ALIGN.CENTER

    p = tf_d.add_paragraph()
    p.text = "DEMONSTRAÇÃO EM JAVA AO VIVO"
    p.font.name = "Trebuchet MS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_FIO
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(2)

    passos_demo = [
        ("1. Disparo do Boato", "Selecionar Paciente Zero (Ana)"),
        ("2. Ondas de Propagação", "Executar BFS passo a passo"),
        ("3. Falha da Heurística", "Bloquear Marina (grau 7) → 0 salvos"),
        ("4. Corte de Articulação", "Bloquear Diego/Fábio → 20 salvos"),
        ("5. Tarjan Instantâneo", "Conferir cálculo dos pontos de corte")
    ]
    for rot, desc in passos_demo:
        p = tf_d.add_paragraph()
        run1 = p.add_run()
        run1.text = f"✔ {rot}: "
        run1.bold = True
        run1.font.name = "Calibri"
        run1.font.size = Pt(10.5)
        run1.font.color.rgb = COR_TINTA_ESCURA
        
        run2 = p.add_run()
        run2.text = desc
        run2.font.name = "Calibri"
        run2.font.size = Pt(10)
        run2.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(2)

    # Entregáveis anexos
    p = tf_d.add_paragraph()
    p.text = "Artefatos Disponíveis no Repositório:"
    p.font.name = "Georgia"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_MARINHO
    p.space_before = Pt(4)

    entregas = [
        "• Relatório ABNT (.docx e .pdf, 30 pág.)",
        "• Código Java Puro (JDK 21) + Testes",
        "• Interface Web Investigativa (Canvas 2D)"
    ]
    for ent in entregas:
        p = tf_d.add_paragraph()
        p.text = ent
        p.font.name = "Calibri"
        p.font.size = Pt(9.5)
        p.font.color.rgb = COR_TINTA_CORPO
        p.space_before = Pt(1)

    # Box de inicialização rápida
    p = tf_d.add_paragraph()
    p.text = "Comando de Execução Rápida:"
    p.font.name = "Georgia"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO_ESCURO
    p.space_before = Pt(4)

    p = tf_d.add_paragraph()
    p.text = "> compilar.bat && executar.bat\n> Abrir http://localhost:8080"
    p.font.name = "Consolas"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COR_TINTA_ESCURA
    p.space_before = Pt(1)

    p = tf_d.add_paragraph()
    p.text = "Suíte de Testes: br.maua.fakenews.TestesAlgoritmos (OK)"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.color.rgb = COR_VERDE_CARIMBO
    p.font.bold = True
    p.space_before = Pt(3)

    # Assinatura acadêmica
    p = tf_d.add_paragraph()
    p.text = "David Daniel & Kauã Ortega | Prof. José Calvetti (IMT)"
    p.font.name = "Calibri"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COR_TINTA_ESCURA
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(5)

    prs.save(SAIDA_PPTX)
    print(f"Apresentação PPTX reformulada com sucesso em: {SAIDA_PPTX}")

if __name__ == "__main__":
    criar_apresentacao()
