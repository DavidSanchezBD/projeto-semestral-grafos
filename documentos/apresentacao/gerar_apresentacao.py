"""
Gerador da Apresentação PPTX — "Caso Fake News: Operação Grafos"
Estética de Jornal Investigativo / Dossiê Policial
Tempo total estimado: 5 minutos (6 slides com roteiro de fala nas notas do orador)
ECM306 - Tópicos Avançados de Estrutura de Dados | Instituto Mauá de Tecnologia
Autores: David Sanchez Bittencourt Daniel & Kauã Bueno Marcatto Ortega
Orientador: Prof. Calvetti
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

# Cores da paleta Jornal Investigativo
COR_FUNDO = RGBColor(245, 238, 220)       # #F5EEDB Papel envelhecido
COR_PRETO_TINTA = RGBColor(27, 27, 27)     # #1B1B1B Tinta de jornal
COR_VERMELHO = RGBColor(192, 57, 43)      # #C0392B Fio vermelho / Carimbo
COR_AMARELO_POSTIT = RGBColor(249, 231, 159) # #F9E79F Post-it
COR_CINZA_CLARO = RGBColor(220, 215, 200) # #DCD7C8 Borda papel
COR_BRANCO = RGBColor(255, 255, 255)
COR_AZUL_NOITE = RGBColor(41, 128, 185)

def criar_apresentacao():
    prs = Presentation()
    # Widescreen 16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6] # Layout em branco

    # -------------------------------------------------------------
    # Helper: fundo e cabeçalho padrão de jornal
    # -------------------------------------------------------------
    def aplicar_fundo_jornal(slide, titulo_secao="GAZETA DOS GRAFOS"):
        # Fundo papel
        fundo = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        fundo.fill.solid()
        fundo.fill.fore_color.rgb = COR_FUNDO
        fundo.line.color.rgb = COR_PRETO_TINTA
        fundo.line.width = Pt(3)

        # Tarja superior de jornal
        tarja = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.3), Inches(12.533), Inches(0.45))
        tarja.fill.solid()
        tarja.fill.fore_color.rgb = COR_PRETO_TINTA
        tarja.line.fill.background()
        tf = tarja.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"★ {titulo_secao} — EDIÇÃO ESPECIAL ECM306 — INSTITUTO MAUÁ DE TECNOLOGIA ★"
        p.font.name = "Georgia"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COR_BRANCO
        p.alignment = PP_ALIGN.CENTER

    def adicionar_carimbo(slide, texto, left, top, width, height, cor=COR_VERMELHO, rot= -5):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = cor
        shape.line.width = Pt(3)
        shape.rotation = rot
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = texto
        p.font.name = "Impact"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = cor
        p.alignment = PP_ALIGN.CENTER
        return shape

    # =============================================================
    # SLIDE 1: CAPA — MANCHETE DE JORNAL
    # =============================================================
    s1 = prs.slides.add_slide(slide_layout)
    aplicar_fundo_jornal(s1, "INQUÉRITO ESPECIAL: TEORIA DOS GRAFOS")

    adicionar_carimbo(s1, "CONFIDENCIAL", Inches(10.5), Inches(0.9), Inches(2.2), Inches(0.6), COR_VERMELHO, -6)

    # Manchete principal
    tx_manchete = s1.shapes.add_textbox(Inches(0.6), Inches(0.9), Inches(10.0), Inches(2.0))
    tf1 = tx_manchete.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "CASO FAKE NEWS: OPERAÇÃO GRAFOS"
    p1.font.name = "Georgia"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COR_PRETO_TINTA

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Boato viral atinge 27 pessoas em 4 rodadas: como a Teoria dos Grafos rastreia e contém o contágio"
    p1_sub.font.name = "Courier New"
    p1_sub.font.size = Pt(14)
    p1_sub.font.color.rgb = RGBColor(80, 80, 80)
    p1_sub.space_before = Pt(8)

    # Caixa Dossiê com Autores
    dossie = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.2), Inches(6.0), Inches(3.5))
    dossie.fill.solid()
    dossie.fill.fore_color.rgb = COR_BRANCO
    dossie.line.color.rgb = COR_PRETO_TINTA
    dossie.line.width = Pt(1.5)
    tf_dos = dossie.text_frame
    tf_dos.word_wrap = True
    
    p = tf_dos.paragraphs[0]
    p.text = "DOSSIÊ DE INVESTIGAÇÃO TÉCNICA"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO

    itens_dos = [
        ("Disciplina:", "ECM306 — Tópicos Avançados de Estrutura de Dados"),
        ("Instituição:", "Instituto Mauá de Tecnologia (IMT)"),
        ("Orientador:", "Prof. José Calvetti"),
        ("Investigadores:", "David Sanchez Daniel (RA: 24.00029-9)\nKauã Bueno Ortega (RA: 24.00031-0)"),
        ("Data de Conclusão:", "Novembro de 2026"),
        ("Status do Inquérito:", "Solução em Java pura + Demonstração Web")
    ]
    for rotulo, val in itens_dos:
        p = tf_dos.add_paragraph()
        p.text = f"• {rotulo} {val}"
        p.font.name = "Courier New"
        p.font.size = Pt(10)
        p.font.color.rgb = COR_PRETO_TINTA
        p.space_before = Pt(4)

    # Imagem da capa (redes de ondas)
    caminho_fig_bfs = os.path.join(FIG_DIR, "fig_bfs_ondas.png")
    if os.path.exists(caminho_fig_bfs):
        s1.shapes.add_picture(caminho_fig_bfs, Inches(7.2), Inches(3.2), width=Inches(5.5))

    s1.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 1 | ~45 segundos]\n\n"
        "[DAVID]: Olá a todos, olá professor Calvetti. Hoje apresentamos o nosso projeto semestral de Tópicos Avançados de Estrutura de Dados, "
        "intitulado 'Caso Fake News: Operação Grafos'. Eu sou o David e estou acompanhado do Kauã.\n\n"
        "[KAUÃ]: Fugindo intencionalmente de temas clichês como GPS e rotas de mapas viários, decidimos aplicar a Teoria dos Grafos a um dos problemas "
        "mais urgentes da sociedade moderna: a propagação de desinformação em redes de mensagens. Desenvolvemos uma solução computacional 100% em Java "
        "para rastrear o contágio em ondas e determinar, matematicamente, quem deve ser colocado em quarentena para conter o boato."
    )

    # =============================================================
    # SLIDE 2: O CRIME — A MENSAGEM VIRAL
    # =============================================================
    s2 = prs.slides.add_slide(slide_layout)
    aplicar_fundo_jornal(s2, "OCORRÊNCIA: O DELITO DA DESINFORMAÇÃO")

    adicionar_carimbo(s2, "BOATO FALSO", Inches(10.2), Inches(0.9), Inches(2.5), Inches(0.6), COR_VERMELHO, 4)

    # Título do slide
    tx_tit = s2.shapes.add_textbox(Inches(0.6), Inches(0.9), Inches(9.5), Inches(0.8))
    p = tx_tit.text_frame.paragraphs[0]
    p.text = "O PROBLEMA: 'ENCAMINHADA COM FREQUÊNCIA'"
    p.font.name = "Georgia"
    p.font.size = Pt(24)
    p.font.bold = True

    # Balão estilo mensagem de WhatsApp
    balao = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.8), Inches(2.2))
    balao.fill.solid()
    balao.fill.fore_color.rgb = RGBColor(220, 248, 198) # Verde WhatsApp
    balao.line.color.rgb = RGBColor(160, 200, 140)
    balao.line.width = Pt(1.5)
    tf_b = balao.text_frame
    tf_b.word_wrap = True
    
    p = tf_b.paragraphs[0]
    p.text = "↗ Encaminhada com frequência"
    p.font.name = "Calibri"
    p.font.size = Pt(10)
    p.font.italic = True
    p.font.color.rgb = RGBColor(100, 100, 100)

    p = tf_b.add_paragraph()
    p.text = "\"URGENTE: Nova taxa bancária do PIX entra em vigor amanhã às 8h! Repasse para todos os seus grupos de família e trabalho para cancelar a cobrança automática!\""
    p.font.name = "Calibri"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = RGBColor(20, 20, 20)
    p.space_before = Pt(6)

    # Carimbo "FAKE" em cima do balão
    adicionar_carimbo(s2, "FAKE NEWS", Inches(4.2), Inches(2.8), Inches(2.2), Inches(0.7), COR_VERMELHO, -14)

    # Painel das 3 Perguntas de Investigação
    painel_perg = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), Inches(1.8), Inches(5.6), Inches(4.8))
    painel_perg.fill.solid()
    painel_perg.fill.fore_color.rgb = COR_BRANCO
    painel_perg.line.color.rgb = COR_PRETO_TINTA
    painel_perg.line.width = Pt(2)
    tf_p = painel_perg.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    p.text = "AS 3 PERGUNTAS FUNDAMENTAIS DO INQUÉRITO"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_PRETO_TINTA

    perguntas = [
        ("1. Rastreamento:", "A partir de um Paciente Zero, quem são todas as pessoas que recebem o boato?"),
        ("2. Velocidade:", "Em quantas rodadas de encaminhamento a mensagem contamina toda a rede?"),
        ("3. Contenção (Quarentena):", "Se pudermos conscientizar ou bloquear apenas UMA pessoa, quem deve ser escolhido para proteger o maior número de cidadãos?")
    ]
    for tit, desc in perguntas:
        p = tf_p.add_paragraph()
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COR_VERMELHO
        p.space_before = Pt(10)
        
        p2 = tf_p.add_paragraph()
        p2.text = desc
        p2.font.name = "Courier New"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COR_PRETO_TINTA
        p2.space_before = Pt(2)

    # Post-it inferior esquerdo
    postit = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.4), Inches(5.8), Inches(2.2))
    postit.fill.solid()
    postit.fill.fore_color.rgb = COR_AMARELO_POSTIT
    postit.line.color.rgb = RGBColor(200, 180, 100)
    postit.rotation = -1
    tf_pos = postit.text_frame
    tf_pos.word_wrap = True
    p = tf_pos.paragraphs[0]
    p.text = "NOTA DO INVESTIGADOR:"
    p.font.name = "Georgia"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COR_PRETO_TINTA
    
    p = tf_pos.add_paragraph()
    p.text = "O problema não é geográfico! A distância relevante não é em quilômetros, mas sim em 'graus de separação' e etapas de retransmissão entre contatos diretos."
    p.font.name = "Courier New"
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(40, 40, 40)
    p.space_before = Pt(4)

    s2.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 2 | ~50 segundos]\n\n"
        "[DAVID]: Todos nós já recebemos mensagens alarmistas com o selo 'Encaminhada com frequência' no WhatsApp: notícias falsas sobre saúde, "
        "fraudes financeiras ou supostas taxas bancárias. Quando alguém aperta 'encaminhar', deflagra um contágio em cadeia.\n\n"
        "[KAUÃ]: Diante desse crime informacional, o nosso papel como engenheiros de computação é responder a três perguntas exatas: "
        "Primeiro: quem a notícia alcança? Segundo: em quantas rodadas de repasse? E terceiro, a decisão mais difícil: se tivermos recurso limitado "
        "para intervir e conscientizar apenas uma pessoa para que ela não repasse o boato, quem devemos escolher para salvar o maior número de pessoas?"
    )

    # =============================================================
    # SLIDE 3: A MODELAGEM — O QUADRO DO DETETIVE
    # =============================================================
    s3 = prs.slides.add_slide(slide_layout)
    aplicar_fundo_jornal(s3, "EVIDÊNCIAS: DA REALIDADE AO GRAFO")

    tx_tit = s3.shapes.add_textbox(Inches(0.6), Inches(0.9), Inches(11.0), Inches(0.8))
    p = tx_tit.text_frame.paragraphs[0]
    p.text = "A MODELAGEM: AS 5 PERGUNTAS DE CALVETTI (AULA T25)"
    p.font.name = "Georgia"
    p.font.size = Pt(24)
    p.font.bold = True

    # 4 Cartões tipo Ficha Policial
    cards_mod = [
        ("VÉRTICES (V)", "Pessoas integrantes dos grupos de mensagens.\n\n• ID numérico único (0 a N-1)\n• Nome de exibição\n• Grupo social de origem", COR_AZUL_NOITE),
        ("ARESTAS (E)", "Contatos mútuos diretos salvos na agenda.\n\n• Conexão bidirecional (não direcionada)\n• Sem pesos (custo unitário por repasse)\n• Não admite laços ou repetições", COR_VERMELHO),
        ("REPRESENTAÇÃO", "Lista de Adjacência em Java.\n\n• Memória O(V + E) — ótimo p/ esparsos\n• Varredura de vizinhos em O(grau(v))\n• List<List<Integer>> em memória", COR_PRETO_TINTA),
        ("OBJETIVO DUPLO", "Alcançar & Desconectar.\n\n1. Rastrear alcance máximo por BFS\n2. Encontrar corte ótimo que divide a rede em componentes protegidos", COR_VERMELHO)
    ]
    for idx, (tit, corpo, cor_borda) in enumerate(cards_mod):
        x = Inches(0.6 + idx * 3.1)
        c = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(1.8), Inches(2.9), Inches(3.6))
        c.fill.solid()
        c.fill.fore_color.rgb = COR_BRANCO
        c.line.color.rgb = cor_borda
        c.line.width = Pt(2)
        tf = c.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = cor_borda
        
        p2 = tf.add_paragraph()
        p2.text = corpo
        p2.font.name = "Courier New"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COR_PRETO_TINTA
        p2.space_before = Pt(8)

    # Post-it inferior com resumo do Teorema do Aperto de Mãos
    faixa_inf = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.7), Inches(12.133), Inches(1.2))
    faixa_inf.fill.solid()
    faixa_inf.fill.fore_color.rgb = COR_AMARELO_POSTIT
    faixa_inf.line.color.rgb = COR_PRETO_TINTA
    tf_f = faixa_inf.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "PROPRIEDADE ESTRUTURAL DA REDE DE TESTE (28 PESSOAS, 42 CONTATOS):"
    p.font.name = "Georgia"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COR_PRETO_TINTA

    p = tf_f.add_paragraph()
    p.text = "Pelo Lema do Aperto de Mãos (Teorema 1, Aula T17), ∑ d(v) = 2|E| = 84. A rede possui comunidades internas densas (Família, Trabalho, Faculdade, Academia, Condomínio) conectadas por pouquíssimas pontes estratégicas — exatamente o padrão das redes sociais reais!"
    p.font.name = "Courier New"
    p.font.size = Pt(9.5)
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
    aplicar_fundo_jornal(s4, "INVESTIGAÇÃO: O ALGORITMO DA PERSEGUIÇÃO")

    adicionar_carimbo(s4, "O(V + E)", Inches(10.8), Inches(0.9), Inches(1.8), Inches(0.55), COR_AZUL_NOITE, 0)

    tx_tit = s4.shapes.add_textbox(Inches(0.6), Inches(0.9), Inches(10.0), Inches(0.8))
    p = tx_tit.text_frame.paragraphs[0]
    p.text = "A PROPAGAÇÃO: BUSCA EM LARGURA (BFS)"
    p.font.name = "Georgia"
    p.font.size = Pt(24)
    p.font.bold = True

    # Bloco explicativo da BFS
    bloco_bfs = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(5.6), Inches(5.0))
    bloco_bfs.fill.solid()
    bloco_bfs.fill.fore_color.rgb = COR_BRANCO
    bloco_bfs.line.color.rgb = COR_PRETO_TINTA
    bloco_bfs.line.width = Pt(1.5)
    tf = bloco_bfs.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "MECÂNICA DAS ONDAS DE CONTÁGIO"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_NOITE

    itens_bfs = [
        ("Fila FIFO (Queue):", "Garante que todos os nós à distância 'd' sejam processados rigorosamente antes dos nós à distância 'd + 1'."),
        ("Vetor dist[]:", "Inicializado com -1 para distinguir visitados de inalcançáveis (como no slide 16 da aula T25). dist[origem] = 0."),
        ("Vetor anterior[]:", "Registra o predecessor na árvore BFS, permitindo reconstituir a rota exata de disseminação do boato até qualquer vítima."),
        ("Pessoas Isoladas:", "Vértices que permanecem com dist = -1 revelam cidadãos imunes/desconectados (exemplo: Sônia, id 27, na rede de testes).")
    ]
    for tit, desc in itens_bfs:
        p = tf.add_paragraph()
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COR_PRETO_TINTA
        p.space_before = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Courier New"
        p2.font.size = Pt(9.5)
        p2.space_before = Pt(2)

    # Imagem da Tabela de Rastreamento (ou gráfico da BFS)
    caminho_fig_screen = os.path.join(FIG_DIR, "fig_screenshot_demo.png")
    if os.path.exists(caminho_fig_screen):
        s4.shapes.add_picture(caminho_fig_screen, Inches(6.5), Inches(1.8), width=Inches(6.2))

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
    aplicar_fundo_jornal(s5, "DIAGNÓSTICO: O DILEMA DA QUARENTENA")

    adicionar_carimbo(s5, "AULA T23", Inches(10.8), Inches(0.9), Inches(1.8), Inches(0.55), COR_VERMELHO, 3)

    tx_tit = s5.shapes.add_textbox(Inches(0.6), Inches(0.9), Inches(10.0), Inches(0.8))
    p = tx_tit.text_frame.paragraphs[0]
    p.text = "A QUARENTENA: FORÇA BRUTA VS. HEURÍSTICA DE GRAU"
    p.font.name = "Georgia"
    p.font.size = Pt(24)
    p.font.bold = True

    # Cartão da Força Bruta
    c_fb = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.8))
    c_fb.fill.solid()
    c_fb.fill.fore_color.rgb = COR_BRANCO
    c_fb.line.color.rgb = COR_VERMELHO
    c_fb.line.width = Pt(2)
    tf = c_fb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "FORÇA BRUTA EXATA — O(V · (V + E))"
    p.font.name = "Georgia"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO

    itens_fb = [
        ("Como Funciona:", "Simula a remoção temporária de cada pessoa elegível e roda uma BFS rápida a partir da origem."),
        ("Fórmula de Sucesso:", "protegidos(v) = alcançados_antes − alcançados_sem_v − 1"),
        ("Garantia Matemática:", "Encontra o ótimo global absoluto. Em 28 pessoas executa em menos de 10 ms; em 2.000 pessoas leva apenas 275 ms!")
    ]
    for tit, desc in itens_fb:
        p = tf.add_paragraph()
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COR_PRETO_TINTA
        p.space_before = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Courier New"
        p2.font.size = Pt(9.5)
        p2.space_before = Pt(2)

    # Cartão da Heurística de Grau e Tarjan
    c_heu = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.9), Inches(4.8))
    c_heu.fill.solid()
    c_heu.fill.fore_color.rgb = RGBColor(253, 237, 236) # Fundo rosa alerta
    c_heu.line.color.rgb = COR_VERMELHO
    c_heu.line.width = Pt(2)
    tf = c_heu.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "O EXPERIMENTO DIDÁTICO: A HEURÍSTICA ERROU!"
    p.font.name = "Georgia"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COR_VERMELHO

    p = tf.add_paragraph()
    p.text = "• Intuição Míope (Maior Grau): Marina (id 12, grau 7)"
    p.font.name = "Georgia"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COR_AZUL_NOITE
    p.space_before = Pt(6)

    p2 = tf.add_paragraph()
    p2.text = "Marina tem 7 amigos na Faculdade. Se for bloqueada, protege ZERO pessoas! O grupo da faculdade é tão conectado que o boato apenas contorna Marina por outro colega."
    p2.font.name = "Courier New"
    p2.font.size = Pt(9.5)
    p2.space_before = Pt(2)

    p3 = tf.add_paragraph()
    p3.text = "• Ótimo da Força Bruta: Diego (id 3, grau 5) e Fábio (id 5, grau 3)"
    p3.font.name = "Georgia"
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = COR_VERMELHO
    p3.space_before = Pt(8)

    p4 = tf.add_paragraph()
    p4.text = "Diego e Fábio protegem 20 e 18 pessoas! Por quê? Pelo Algoritmo de Tarjan O(V+E), ambos são Pontos de Articulação (pontes entre a Família e o Trabalho). Cortar a ponte isola o resto do mundo."
    p4.font.name = "Courier New"
    p4.font.size = Pt(9.5)
    p4.space_before = Pt(2)

    adicionar_carimbo(s5, "PONTE VENCE GRAU", Inches(8.5), Inches(5.3), Inches(3.6), Inches(0.6), COR_VERMELHO, -4)

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
    aplicar_fundo_jornal(s6, "VEREDITO: CASO ENCERRADO")

    adicionar_carimbo(s6, "CASO ENCERRADO", Inches(9.8), Inches(0.9), Inches(2.9), Inches(0.65), RGBColor(39, 174, 96), -3)

    tx_tit = s6.shapes.add_textbox(Inches(0.6), Inches(0.9), Inches(9.0), Inches(0.8))
    p = tx_tit.text_frame.paragraphs[0]
    p.text = "SÍNTESE DO INQUÉRITO E DEMONSTRAÇÃO AO VIVO"
    p.font.name = "Georgia"
    p.font.size = Pt(24)
    p.font.bold = True

    # 3 Conclusões Principais
    conclusoes = [
        ("1. O Modelo Correto Vence a Intuição", "Uma modelagem semântica precisa em grafos revela gargalos e pontes que análises simplistas ou gulosas não conseguem antecipar."),
        ("2. Eficiência Polinomial e Escalabilidade", "BFS em O(V+E), Tarjan em O(V+E) e Força Bruta em O(V·(V+E)) executam com facilidade em instâncias de milhares de nós em milissegundos."),
        ("3. Filosofia 'Java Pensa, Navegador Desenha'", "Zero dependências externas: toda a inteligência e os testes unitários residem no JDK 21 puro, com uma interface investigativa que facilita a visualização em aula.")
    ]
    for idx, (tit, desc) in enumerate(conclusoes):
        y = Inches(1.8 + idx * 1.5)
        box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), y, Inches(7.5), Inches(1.3))
        box.fill.solid()
        box.fill.fore_color.rgb = COR_BRANCO
        box.line.color.rgb = COR_PRETO_TINTA
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = tit
        p.font.name = "Georgia"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COR_VERMELHO

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Courier New"
        p2.font.size = Pt(9.5)
        p2.space_before = Pt(3)

    # Chamada para Demonstração (Lado direito)
    box_demo = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.4), Inches(1.8), Inches(4.3), Inches(4.3))
    box_demo.fill.solid()
    box_demo.fill.fore_color.rgb = COR_AMARELO_POSTIT
    box_demo.line.color.rgb = COR_PRETO_TINTA
    box_demo.line.width = Pt(2)
    tf_d = box_demo.text_frame
    tf_d.word_wrap = True

    p = tf_d.paragraphs[0]
    p.text = "PROVA MATERIAL:"
    p.font.name = "Georgia"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COR_PRETO_TINTA
    p.alignment = PP_ALIGN.CENTER

    p = tf_d.add_paragraph()
    p.text = "DEMONSTRAÇÃO EM JAVA AO VIVO"
    p.font.name = "Impact"
    p.font.size = Pt(18)
    p.font.color.rgb = COR_VERMELHO
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(8)

    p = tf_d.add_paragraph()
    p.text = "Vamos agora ao sistema em execução para:\n\n1. Selecionar o Paciente Zero\n2. Assistir à propagação em ondas\n3. Bloquear o Ponto de Articulação\n4. Comprovar a contenção do contágio!"
    p.font.name = "Courier New"
    p.font.size = Pt(10)
    p.font.color.rgb = COR_PRETO_TINTA
    p.space_before = Pt(10)

    s6.notes_slide.notes_text_frame.text = (
        "[ROTEIRO DE FALA — SLIDE 6 | ~50 segundos]\n\n"
        "[DAVID]: Para concluir nossa apresentação de 5 minutos, o Caso Fake News demonstra como a Teoria dos Grafos transforma intuições nebulosas "
        "em decisões matemáticas precisas e eficientes.\n\n"
        "[KAUÃ]: Desenvolvemos um código limpo, rigoroso e testado, integrando os conceitos de BFS, caminhos aumentantes e pontos de articulação de Tarjan. "
        "Agora, passamos à demonstração prática do software implementado em Java, executando os experimentos ao vivo para a turma e para o professor Calvetti. "
        "Muito obrigado!"
    )

    prs.save(SAIDA_PPTX)
    print(f"Apresentação PPTX gerada com sucesso em: {SAIDA_PPTX}")

if __name__ == "__main__":
    criar_apresentacao()
