# Plano dos Slides (Apresentação PPTX ≤ 5 min) — Revisão v1

> **Referência geral:** [`plano_geral.md`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/plano/plano_geral.md)  
> **Tempo de apresentação:** Máximo de **5 minutos** (seguido da demonstração ao vivo do código Java).

---

## 1. Diagnóstico Crítico dos Slides da v0

Na revisão das imagens dos 6 slides gerados na `v0`, os seguintes problemas comprometeram a apresentação:

1. **Excesso de texto ("Slidedoc" em vez de Slide):**
   - Cada slide da `v0` tinha entre **150 e 230 palavras** distribuídas em caixas com 6 a 8 frases longas (ex.: Slide 3 tinha 4 colunas de texto + 1 caixa inferior com 4 frases longas; Slide 5 tinha duas colunas inteiras de texto corrido).
2. **Texto muito pequeno:**
   - Para caber tanto texto, o corpo dos slides usou fontes entre **11 pt e 13 pt**, impossíveis de ler rapidamente do fundo da sala de aula.
3. **Pouco intuitivo:**
   - Conceitos essencialmente visuais — como a **transformação de pessoas/contatos em grafo**, a **propagação em ondas da BFS** e o motivo pelo qual **bloquear a ponte (Diego) funciona enquanto bloquear a pessoa mais popular (Marina) falha** — foram explicados com parágrafos de texto técnico em vez de diagramas visuais claros.
4. **Zero dinâmico:**
   - Todos os 6 slides usaram o mesmo layout engessado (caixas retangulares brancas sobre fundo bege), sem progressão visual passo a passo e sem destaque gráfico para o raciocínio durante a fala.

---

## 2. Regras de Ouro do Redesign (v1)

### 2.1. Regra de Tipografia e Densidade ("Pouco Texto, Fonte Grande")
- **Limite estrito de palavras:** Máximo de **25 a 35 palavras visíveis por slide** (toda explicação detalhada fica exclusivamente nas **Notas do Orador**).
- **Tamanhos mínimos de fonte:**
  - Manchete / Título do slide: **34 a 40 pt** (`Georgia Bold` / `Segoe UI Black`)
  - Subtítulos de cartões / blocos: **22 a 26 pt**
  - Texto curto de apoio / palavras-chave: **18 a 20 pt** (**proibido usar fonte menor que 18 pt** em qualquer lugar do slide, exceto rótulos internos de diagramas).
  - Números de destaque (*Big Numbers*): **48 a 64 pt** (ex.: **`20 salvos`** vs. **`0 salvos`**).

### 2.2. Regra de Intuitividade ("Mostre o Grafo, Não Descreva o Grafo")
- Todo slide técnico terá **pelo menos 60% da área ocupada por um diagrama visual grande** (gerado em alta resolução ou desenhado com formas nativas do PowerPoint):
  - Em vez de listar em texto *"Vértices = pessoas, Arestas = contatos"*, desenhar **duas pessoas ligadas por um fio** com setas apontando: `Vértice (Pessoa)` e `Aresta (Contato Mútuo)`.
  - Em vez de explicar com texto por que a heurística de Maior Grau falha, colocar **dois mini-grafos lado a lado**:
    - **Esquerda (❌ Maior Grau — Marina, 7 amigos):** mostra o corte em Marina, mas os fios ao redor continuam levando o boato para todo o grupo (`0 protegidos`).
    - **Direita (✅ Ponte / Tarjan — Diego, ponte única):** mostra uma tesoura/bloqueio cortando a única ponte entre `Família` e `Trabalho`, deixando 20 nós verdes e isolados do boato (`20 protegidos — 74%`).

### 2.3. Regra de Dinamismo (Animações por Clique + Transições)
1. **Animações de entrada progressivas por clique (`On Click` no PowerPoint):**
   - Os elementos de cada slide **não aparecem todos de uma vez**. Ao passar o slide, aparece apenas o título e o elemento base; cada clique do apresentador revela o próximo passo visual sincronizado com a fala:
     - **No Slide 2 (O Problema):** Aparece a mensagem Fake News → *Clique 1:* Pergunta 1 (Alcance) → *Clique 2:* Pergunta 2 (Velocidade) → *Clique 3:* Pergunta 3 (Quarentena).
     - **No Slide 4 (BFS em Ondas):** Aparece o Paciente Zero (Onda 0) → *Clique 1:* Acende Onda 1 + Fila → *Clique 2:* Acende Onda 2 → *Clique 3:* Acende Onda 3 e mostra o alcance total.
     - **No Slide 5 (Maior Grau vs. Ponte):** Aparece o desafio *"Quem bloquear?"* → *Clique 1:* Mostra a tentativa pelo Maior Grau (Marina → `0 salvos ❌`) → *Clique 2:* Mostra a solução por Força Bruta / Ponto de Articulação (Diego → `20 salvos ✅`).
2. **Transições suaves entre slides (`Fade` / `Push` / `Morph`):** Configuradas diretamente no XML dos slides para dar fluidez cinematográfica.

---

## 3. Roteiro Visual Slide a Slide (6 Slides = 5 Minutos)

| Slide | Tempo | Título Curto | Layout Visual (Zero Paredão de Texto) | Dinâmica (Cliques) |
|---|---|---|---|---|
| **1. Capa** | 30 s | **CASO FAKE NEWS**<br>*Rastreando e contendo boatos com Grafos* | • Visual de capa de dossiê investigativo moderno<br>• Diagrama central grande da rede conectada com carimbo `FAKE NEWS`<br>• 3 *Big Badges*: **`28 Pessoas`** · **`5 Grupos`** · **`Java 21 Puro`**<br>• Rodapé limpo: David Daniel & Kauã Ortega · Prof. Robson Calvetti | Entrada com transição suave |
| **2. O Problema** | 50 s | **O PROBLEMA: "ENCAMINHADA COM FREQUÊNCIA"** | • **Esquerda:** Balão grande de mensagem de celular com boato do PIX e carimbo vermelho `FAKE`<br>• **Direita:** 3 cartões grandes numerados (máx. 6 palavras cada):<br>  1️⃣ **Quem recebe?** *(Alcance)*<br>  2️⃣ **Em quantas ondas?** *(Distância)*<br>  3️⃣ **Quem bloquear?** *(Quarentena)* | • Base: Balão do boato<br>• **Clique 1:** Cartão 1️⃣<br>• **Clique 2:** Cartão 2️⃣<br>• **Clique 3:** Cartão 3️⃣ |
| **3. Modelagem** | 50 s | **DO CHAT PARA O GRAFO** | • **Centro (70% da tela):** Diagrama visual grande transformando um grupo de mensagens em grafo:<br>  - Círculos = **Vértices $V$ (28 Pessoas)**<br>  - Fios = **Arestas $E$ (42 Contatos Mútuos)**<br>• **Base:** 3 pílulas visuais grandes:<br>  `Não Direcionado` · `Sem Pesos (1 repasse = 1 salto)` · `Lista de Adjacência O(V+E)` | • Base: Diagrama central<br>• **Clique 1:** Pílulas de propriedades da modelagem |
| **4. Propagação (BFS)** | 60 s | **COMO O BOATO CORRE: BUSCA EM LARGURA (BFS)** | • **Esquerda (65% da tela):** Diagrama grande de **Ondas Concêntricas** (Onda 0 Vermelha → Onda 1 Laranja → Onda 2 Amarela → Onda 3 Azul + 1 nó cinza isolado: *Sônia*)<br>• **Direita (35%):** Visual gráfico de **Fila FIFO** mostrando blocos entrando e saindo + badge gigante: **`27 de 28 atingidos em 4 ondas`** | • Base: Onda 0 (Ana)<br>• **Clique 1:** Onda 1 + Fila<br>• **Clique 2:** Ondas 2 a 4 + Badge `27/28 atingidos` |
| **5. Quarentena** | 70 s | **QUEM BLOQUEAR? INTUIÇÃO vs. TOPOLOGIA** | • Layout comparativo **VERSUS** com 2 diagramas visuais grandes lado a lado:<br>  - **Card Esquerdo (❌ Heurística Maior Grau):** Desenho do grupo Faculdade mostrando **Marina (Grau 7)** bloqueada, mas o boato contornando pelos vizinhos $\rightarrow$ Número gigante **`0 SALVOS (0%)`**<br>  - **Card Direito (✅ Força Bruta + Tarjan):** Desenho mostrando **Diego (Ponte)** bloqueado entre Família e Trabalho, cortando o fluxo $\rightarrow$ Número gigante **`20 SALVOS (74%)`** | • Base: Pergunta central<br>• **Clique 1:** Lado Esquerdo (Maior Grau falha)<br>• **Clique 2:** Lado Direito (Ponte vence!) |
| **6. Conclusão + Demo** | 40 s | **VEREDITO & DEMONSTRAÇÃO AO VIVO** | • **Topo:** 3 cartões-resumo ultra-curtos:<br>  1. **Pontes > Popularidade** *(Articulação supera Maior Grau)*<br>  2. **Rápido na Prática** *(2.000 nós em 0,27 s em Java)*<br>  3. **"Java Pensa, Navegador Desenha"**<br>• **Centro/Base:** Chamada visual grande **`▶ AO VIVO NO NAVEGADOR`** com os 3 passos da demo (`1. Propagar` $\rightarrow$ `2. Testar Marina` $\rightarrow$ `3. Bloquear Diego`) | • Base: 3 conclusões<br>• **Clique 1:** Chamada da Demo ao vivo |

---

## 4. Implementação Técnica e Verificação Visual

1. **`documentos/apresentacao/gerar_apresentacao.py`:**
   - Gerar diagramas dedicados de alta legibilidade com `matplotlib`/`PIL` especificamente para os slides (com fundo transparente/integrado, fontes grandes e zero textos pequenos).
   - Construir os slides em `16:9` ($13,333'' \times 7,5''$) com tipografia grande ($\ge 20\text{ pt}$), alto contraste e poucos elementos por tela.
   - Embutir as **Notas do Orador** detalhadas em cada slide (roteiro completo falado para David e Kauã, permitindo que o slide fique visualmente limpo enquanto os apresentadores têm todo o apoio de fala).
2. **`documentos/apresentacao/aplicar_animacoes_pptx.ps1` (ou injeção XML direta no Python):**
   - Configurar animações `On Click` para os grupos de formas de cada slide e transições suaves entre slides, exportando em seguida cada slide como imagem JPG/PNG via PowerPoint COM para inspeção visual obrigatória.
