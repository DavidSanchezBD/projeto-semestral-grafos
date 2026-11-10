# Plano da Pesquisa (Relatório em PDF) — Revisão v1

> **Referência geral:** [`plano_geral.md`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/plano/plano_geral.md)  
> **Modelo de referência da disciplina:** [`Teorema de Hall Aplicado a Grafos.pdf`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Exemplo%20de%20Documento%20de%20Pesquisa/Teorema%20de%20Hall%20Aplicado%20a%20Grafos.pdf) (8 páginas, direto, limpo e sem excessos pré-textuais).

---

## 1. Diagnóstico Crítico da v0 (O que deu errado e por quê)

Na inspeção página a página do PDF gerado na `v0` (21 páginas), foram identificados 3 grupos de problemas:

### 1.1. Erros de Formatação Matemática (LaTeX cru e glifos `■`)
- **Sintaxe LaTeX literal no texto:** O ReportLab não processa LaTeX (`$...$`), mas o script da `v0` passou strings como `"Figura 1 – Grafos não planares canônicos de Kuratowski: $K_5$ e $K_{3,3}$"`, `"diferentes ordens de $V$"` e `"∑_{v ∈ V} d(v) = 2 · |E|"`, fazendo o símbolo `$` e as chaves `_{...}` aparecerem literalmente no PDF (páginas 5, 8, 12 e 19 da `v0`).
- **Quadrados pretos (`■`) em expoentes:** Na Tabela 6 (página 19 da `v0`), foram usados caracteres Unicode de sobrescrito (`10⁴`, `10⁵`, `10⁶`) com a fonte padrão Tipo 1 (`Times-Roman`) do ReportLab, que só suporta codificação *WinAnsi* (Latin-1), renderizando `3,04 × 10■ op.`.

### 1.2. Textos Sobrepostos e Figuras Achatadas
- **Colisão de texto dentro das tabelas (Tabelas 3 e 5 da `v0`):** As células das tabelas foram preenchidas com strings puras (`str`) em vez de objetos `Paragraph` do ReportLab. Quando o texto ultrapassava a largura da coluna, o ReportLab não quebrava linha e desenhava o texto por cima da coluna vizinha (ex.: *"Detecção de Fraude FinanceiraContas bancárias"* e *"Maior Grau (Heurística ERROU!)"* vazando da tabela).
- **Rótulos sobrepostos nos gráficos (`fig_bfs_ondas.png` e `fig_benchmark.png`):**
  - Na Figura 3, o texto `"Onda 1 (dist = 1)"` ficou em cima de um vértice do grafo, e a imagem foi inserida no PDF com `width` e `height` fixos incompatíveis com a proporção real da imagem PNG, deixando os círculos ovais/achatados.
  - Na Figura 5 (benchmark), os textos `"11.1 ms"` ($N=100$) e `"8.5 ms"` ($N=200$) colidiram um sobre o outro.
- **Sumário quebrado:** Números de página desalinhados com as páginas reais (apontava pág. 26 num PDF de 21 páginas) e linhas pontilhadas quebrando em duas linhas.

### 1.3. Pesquisa Muito Comprida (21 páginas vs. 8 páginas do modelo)
- A `v0` tinha **21 páginas**, inflada por 6 páginas pré-textuais (Capa, Folha de Rosto, Resumo, Abstract, Lista de Ilustrações, Lista de Tabelas, Sumário) e 7 capítulos longos com excesso de tabelas e espaçamentos grandes.
- Já o documento de exemplo fornecido na pasta do projeto ([`Teorema de Hall Aplicado a Grafos.pdf`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Exemplo%20de%20Documento%20de%20Pesquisa/Teorema%20de%20Hall%20Aplicado%20a%20Grafos.pdf)) tem apenas **8 páginas** no total:
  - Página 1: Capa limpa;
  - Página 2: Resumo + Palavras-chave;
  - Páginas 3 a 8: `1 INTRODUÇÃO` → `2 DESENVOLVIMENTO DO TEMA` → `3 CONSIDERAÇÕES FINAIS` → `4 REFERÊNCIAS BIBLIOGRÁFICAS`, em fonte Arial/Helvetica limpa, sem folha de rosto redundante, sem listas pré-textuais e sem sumário quebrado.

---

## 2. Diretrizes Técnicas para a v1 (Regras Anti-Erro)

### Regra 1 — Tipografia TrueType Unicode e Marcação Nativa (Zero LaTeX / Zero `■`)
1. **Registrar fontes TrueType do Windows no ReportLab (`pdfmetrics.registerFont`):**
   - Usar `Arial` (`C:\Windows\Fonts\arial.ttf`, `arialbd.ttf`, `ariali.ttf`, `arialbi.ttf`) — exatamente como no PDF de exemplo do Teorema de Hall — ou `Times New Roman` (`times.ttf`), garantindo suporte completo a UTF-8 (`∑`, `∈`, `⊆`, `≥`, `≤`, `≠`, `×`, `→`, `∪`, `∩`, `∅`).
2. **Proibição absoluta de `$` e sintaxe LaTeX em strings do ReportLab:**
   - Subscritos e sobrescritos devem usar **exclusivamente** as tags XML nativas do `Paragraph` do ReportLab:
     - $K_5$ e $K_{3,3}$ $\rightarrow$ `<i>K</i><sub>5</sub>` e `<i>K</i><sub>3,3</sub>`
     - $S_0$ $\rightarrow$ `<i>S</i><sub>0</sub>`
     - $\mathcal{O}(V^2)$ $\rightarrow$ `O(<i>V</i><super>2</super>)`
     - $3,04 \times 10^4$ $\rightarrow$ `3,04 × 10<super>4</super>`
     - $\sum_{v \in V} d(v) = 2|E|$ $\rightarrow$ `∑ d(<i>v</i>) = 2|<i>E</i>| (para todo <i>v</i> ∈ <i>V</i>)`
3. **Validação automatizada pós-build:** Um teste no próprio script Python lerá o texto de todas as páginas do PDF gerado via `pypdf` e falhará imediatamente se encontrar qualquer ocorrência de `$`, `_{`, `^{` ou `■`.

### Regra 2 — Zero Sobreposição em Tabelas e Figuras
1. **Tabelas 100% com `Paragraph`:**
   - Criar uma função utilitária `tabela_abnt(cabecalho, linhas, larguras_cm)` que converte **toda** célula (cabeçalho e corpo) em `Paragraph(texto, estilo_celula)`. Assim, qualquer texto longo quebra linha automaticamente dentro da própria célula e a altura da linha se ajusta sozinha.
   - A soma de `larguras_cm` será sempre $\le 16,0\text{ cm}$ (largura útil da folha A4 com margens ABNT de $3\text{ cm}$ à esquerda e $2\text{ cm}$ à direita).
   - Toda tabela mais seu título e fonte serão envolvidos em `KeepTogether([...])` para nunca quebrar no meio entre duas páginas.
2. **Figuras com Proporção Real (*Aspect Ratio* preservado) e Rótulos Limpos:**
   - Ao inserir uma imagem PNG no ReportLab, ler primeiro suas dimensões reais `(w_px, h_px)` com `PIL.Image` e calcular `altura_pt = largura_pt * (h_px / w_px)`. Nunca passar `width` e `height` arbitrários que distorçam a figura.
   - Nas figuras geradas com `matplotlib`:
     - Na figura das ondas BFS (`fig_bfs_ondas.png`), colocar os rótulos `"Onda 1"`, `"Onda 2"`, `"Onda 3"` em ângulos livres de vértices (ex.: $45^\circ$ ou no topo com `bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.9, edgecolor='none')`).
     - No gráfico de desempenho (`fig_benchmark.png`), anotar apenas os marcos principais ($N=100, 500, 1000, 2000$) com `xytext` deslocado verticalmente para nunca sobrepor números próximos.

---

## 3. Nova Estrutura Enxuta do Documento (Meta: 8 a 10 Páginas)

Seguindo exatamente a estrutura limpa e direta do modelo [`Teorema de Hall Aplicado a Grafos.pdf`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Exemplo%20de%20Documento%20de%20Pesquisa/Teorema%20de%20Hall%20Aplicado%20a%20Grafos.pdf):

| Pág. Estimada | Seção | Conteúdo Essencial (Direto ao Ponto) |
|---|---|---|
| **Pág. 1** | **Capa** | Instituto Mauá de Tecnologia · Nomes dos autores · Professor: Prof. Robson Calvetti · Título: *GRAFOS E SUAS APLICAÇÕES: FUNDAMENTOS, ALGORITMOS E ESTUDO DE CASO EM REDES DE MENSAGENS* · São Paulo, 2026. |
| **Pág. 2** | **Resumo** | Resumo em parágrafo único (150–200 palavras) + Palavras-chave (padrão idêntico à pág. 2 do modelo do Teorema de Hall). |
| **Pág. 3** | **1 INTRODUÇÃO** | Contextualização da Teoria dos Grafos (de Königsberg às redes modernas), relevância prática além de mapas/GPS e apresentação do estudo de caso (propagação e quarentena de *fake news*). |
| **Págs. 3–5** | **2 FUNDAMENTOS E ALGORITMOS EM GRAFOS** | **2.1. Conceitos e Representações:** Grafo $G=(V,E)$, vizinhança $N(v)$, grau $d(v)$, Lema do Aperto de Mãos ($\sum d(v) = 2|E|$), caminhos/conexidade e **Tabela 1** compacta (*Lista vs. Matriz de Adjacência*).<br>**2.2. Problemas Clássicos:** Trilhas Eulerianas (graus pares) vs. Ciclos Hamiltonianos; Grafos Bipartidos, Emparelhamento e **Teorema de Hall** ($\lvert N(S)\rvert \ge \lvert S\rvert$); Planaridade (**Teorema de Kuratowski**: $K_5$ e $K_{3,3}$, com **Figura 1** limpa) e Coloração.<br>**2.3. Algoritmos de Travessia e Paradigmas:** Busca em Largura (BFS, fila FIFO, menor caminho em saltos), Busca em Profundidade (DFS e Pontos de Articulação de Tarjan), caminhos mínimos (Dijkstra), ordenação topológica (Kahn) e contraste entre **Força Bruta e Algoritmos Gulosos** (Aula T23). |
| **Pág. 6** | **3 APLICAÇÕES NO COTIDIANO** | **Tabela 2** (com `Paragraph` em todas as células, zero sobreposição) mapeando 7 aplicações reais sem mapas/GPS (Escalonamento de horários, Dependências de pacotes, Alocação de tarefas/Hall, Fraudes financeiras, Montagem de DNA, Redes elétricas e Propagação em redes sociais) + comentários concisos em tópicos. |
| **Págs. 7–9** | **4 ESTUDO DE CASO: PROPAGAÇÃO E QUARENTENA DE FAKE NEWS** | **4.1. Modelagem do Problema (5 Perguntas da Aula T25):** Definição formal da rede de 28 pessoas em 5 grupos (`Família`, `Trabalho`, `Faculdade`, `Academia`, `Condomínio`) com 42 contatos.<br>**4.2. Rastreamento por BFS e Quarentena (Força Bruta vs. Maior Grau vs. Tarjan):** Explicação da propagação em ondas (**Figura 2**: ondas BFS + **Tabela 3** enxuta com os 5 primeiros passos da fila) e da equação de proteção.<br>**4.3. Resultados e Validação Experimental:** **Tabela 4** comparando o Top 3 da Força Bruta (Diego protege 20, Fábio protege 18) contra a falha da heurística de Maior Grau (Marina, grau 7, protege 0); **Figura 3** (print da nova interface web limpa) e **Figura 4** (gráfico compacto de tempo da força bruta de $N=100$ a $N=2000$, rodando em $<0,3\text{ s}$). |
| **Pág. 9–10** | **5 CONSIDERAÇÕES FINAIS**<br>**6 REFERÊNCIAS BIBLIOGRÁFICAS** | Síntese dos aprendizados teóricos e práticos (3 parágrafos objetivos) seguida das referências bibliográficas padronizadas (ABNT NBR 6023) na mesma página final. |

---

## 4. Arquivos que Serão Modificados / Criados

1. `documentos/comum/tema.py`:
   - Atualizar geradores das figuras (`fig_kuratowski.png`, `fig_bfs_ondas.png`, `fig_benchmark.png`) com espaçamento amplo, `bbox` nos rótulos e alta resolução sem colisão de textos.
2. `documentos/relatorio/gerar_relatorio.py`:
   - Reescrever usando fontes TrueType (`Arial`), função segura de tabelas com `Paragraph`, preservação automática de *aspect ratio* das figuras e texto enxuto de **8 a 10 páginas**.
   - Incluir validador automático que extrai texto via `pypdf`, verifica o número total de páginas ($8 \le \text{págs} \le 10$) e garante zero ocorrências de `$`, `_{` ou `■`.
3. `Entrega/Relatorio_Grafos_e_suas_Aplicacoes.pdf`:
   - Gerar o PDF final e inspecionar visualmente **todas as páginas** renderizadas como imagem.
