# Caso Fake News — Propagação BFS e Quarentena em Grafos (Revisão v1)

**ECM306 — Tópicos Avançados de Estrutura de Dados | Instituto Mauá de Tecnologia (IMT)**

**Integrantes:**
- David Sanchez Bittencourt Daniel — RA: `24.00029-9`
- Kauã Bueno Marcatto Ortega — RA: `24.00031-0`

**Orientador:** Prof. Robson Calvetti

---

## 1. Visão Geral

Este sistema implementa uma simulação interativa de propagação e contenção cirúrgica (*quarentena*) de desinformação (*fake news*) em redes de mensagens instantâneas utilizando **Teoria dos Grafos**.

A arquitetura segue o princípio ***"O Java 21 pensa, o navegador desenha"***:
1. **Modelagem em Grafo (Aula T25):**
   - **Vértices ($V = 28$):** Pessoas distribuídas em 5 grupos sociais (`Família`, `Trabalho`, `Faculdade`, `Academia`, `Condomínio`), incluindo um vértice isolado (`Sônia`, grau 0).
   - **Arestas ($E = 42$):** Canais de contato direto mútuo (grafo simples, não direcionado e não ponderado em **Lista de Adjacência** $\mathcal{O}(V + E)$).
2. **Busca em Largura — BFS (Aula T25, $\mathcal{O}(V + E)$):**
   - Propaga o boato em ondas concêntricas de distância mínima (`Onda 0`, `Onda 1`, `Onda 2`...) e exibe a tabela completa de rastreamento da fila FIFO.
3. **Quarentena Exata por Força Bruta ($\mathcal{O}(V \cdot (V + E))$) vs. Maior Grau e Pontos de Articulação de Tarjan ($\mathcal{O}(V + E)$):**
   - **Heurística de Maior Grau (`Marina`, grau 7, Faculdade):** Protege **0 pessoas (0%)**, pois seu grupo possui rotas internas redundantes.
   - **Ótimo Global / Ponto de Articulação (`Diego`, grau 5, Família):** Protege **20 pessoas (74% dos contaminados)** ao cortar a ponte que liga a Família aos grupos Trabalho, Faculdade e Academia.

---

## 2. Como Executar na Sala de Aula

### Opção 1: Interface Web Interativa (Recomendada)
Dê um duplo clique ou execute no terminal dentro da pasta `demo/`:
```cmd
executar.bat
```
O script compila automaticamente o projeto (caso `fakenews.jar` não exista), inicia o servidor `HttpServer` nativo do JDK 21 em `http://localhost:8080/` e abre o navegador padrão.

### Roteiro de Demonstração ao Vivo em 3 Cliques:
1. **Passo 1 & 2 (Propagar BFS):** Com `Ana (Família)` selecionada como Paciente Zero, clique em **`▶ Propagar em Ondas`** (ou **`⏭ Passo a Passo`**) para ver o contágio atingir **27 de 28 pessoas** e acompanhar a fila FIFO na **Aba 1**.
2. **Passo 3 (Comparar Quarentena):** Clique em **`🛡️ Comparar Quarentena`**. A **Aba 2** se abre comparando lado a lado **Marina (Grau 7 → 0 salvos)** vs. **Diego (Grau 5, Ponte → 20 salvos)** e destacando ambos diretamente no grafo.
3. **Testar Bloqueios em 1 Clique:** Clique em **`Testar no Grafo`** (em Marina) e depois em **`Aplicar Bloqueio Ótimo`** (em Diego) — ou clique com o **botão direito** sobre qualquer nó para bloqueá-lo/desbloqueá-lo instantaneamente!

### Opção 2: Modo Console (Plano B sem navegador)
```cmd
java -Dfile.encoding=UTF-8 -jar fakenews.jar --console
```

### Opção 3: Suíte de Testes Automatizados (12 Casos Unitários e de Propriedade)
```cmd
testar.bat
```
