# Caso Fake News: Operação Grafos
**ECM306 — Tópicos Avançados de Estrutura de Dados | Instituto Mauá de Tecnologia (IMT)**

**Integrantes:**
- David Sanchez Bittencourt Daniel — RA: 24.00029-9
- Kauã Bueno Marcatto Ortega — RA: 24.00031-0

**Orientador:** Prof. Calvetti

---

## 1. Visão Geral
Este projeto implementa uma simulação interativa de rastreamento e contenção de desinformação (fake news) em redes de mensagens utilizando **Teoria dos Grafos**.

A solução aborda:
1. **Modelagem:** Vértices = pessoas, Arestas = contatos diretos mútuos (grafo não direcionado e não ponderado em lista de adjacência, $O(V + E)$).
2. **Propagação (Busca em Largura - BFS):** Rastreia as "ondas" de transmissão, distância mínima em retransmissões e caminhos de contágio a partir do *Paciente Zero* ($O(V + E)$).
3. **Contenção (Quarentena por Força Bruta vs Heurísticas):**
   - **Força Bruta Exata ($O(V \cdot (V + E))$):** Simula a remoção de cada vértice e calcula exatamente quantas pessoas deixam de ser contaminadas.
   - **Heurística de Maior Grau:** Demonstra em aula casos onde isolar a pessoa mais conectada falha, pois suas conexões são redundantes dentro de uma mesma comunidade.
   - **Pontos de Articulação (Algoritmo de Tarjan, $O(V + E)$):** Identifica pontes críticas entre comunidades.
4. **Arquitetura "Java Pensa, Navegador Desenha":**
   - Todo o processamento algorítmico é feito em **Java puro (JDK 21)** sem frameworks externos.
   - Um servidor HTTP nativo (`com.sun.net.httpserver.HttpServer`) expõe os endpoints REST em JSON.
   - A interface web apresenta a rede sob uma estética de **Quadro de Investigação / Dossiê Policial** (fundo de cortiça, fotos polaroid, fios vermelhos esticados, carimbos vintage).

---

## 2. Requisitos
- **Java SE Development Kit (JDK 21 LTS ou superior)** instalado e no PATH (`java -version` e `javac -version`).
- Qualquer navegador moderno (Edge, Chrome, Firefox).

---

## 3. Como Executar

### Execução Direta (Recomendada)
Dê um duplo clique ou execute no terminal:
```cmd
executar.bat
```
O script compilará o projeto automaticamente (caso o `.jar` ainda não exista), iniciará o servidor local em `http://localhost:8080/` e abrirá a interface no seu navegador padrão.

### Execução em Modo Console (Plano B para Apresentação)
Caso o computador da apresentação não suporte navegador:
```cmd
java -jar fakenews.jar --console
```

### Executar a Suíte de Testes Automatizados
```cmd
testar.bat
```
Verifica 12 casos de teste unitários e de propriedades invariantes (incluindo teste com 200 grafos aleatórios validando Tarjan contra força bruta).

---

## 4. Endpoints da API REST
| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/rede` | Retorna lista de pessoas, conexões e pontos de articulação |
| `GET` | `/api/bfs?origem=X&bloqueados=Y,Z` | Executa a BFS a partir da origem com vértices em quarentena |
| `GET` | `/api/quarentena?origem=X&bloqueados=Y` | Executa a análise de força bruta e comparação de heurísticas |
| `GET` | `/api/desempenho` | Benchmark de tempo para redes de $n = 100$ a $2000$ vértices |
| `POST`| `/api/rede/aleatoria?n=60` | Gera dinamicamente uma rede sintética de teste de estresse |
| `POST`| `/api/rede/original` | Restaura a rede do arquivo `pessoas.csv` |
