# Plano Geral e Decisões do Projeto — ECM306 (Revisão v1)

## 1. Identificação e Contexto

| Item | Definição |
|---|---|
| **Disciplina** | ECM306 — Tópicos Avançados de Estrutura de Dados (Instituto Mauá de Tecnologia) |
| **Professor** | Prof. Robson Calvetti |
| **Integrantes** | David Sanchez Bittencourt Daniel (RA: 24.00029-9)<br>Kauã Bueno Marcatto Ortega (RA: 24.00031-0) |
| **Data de Entrega e Apresentação** | **12/11/2026** (trabalho em grupo, com submissão individual no CanvasLMS) |
| **Tópicos do Enunciado** | 1. Pesquisa: *"Grafos e suas aplicações"*<br>2. Implementação: *"Resolvendo um problema com Grafo"* (proibido tema clichê como GPS/mapas) |

---

## 2. O Problema Escolhido: "Caso Fake News"

**Tema prático:** Simulação de propagação e contenção (*quarentena*) de boatos (*fake news*) em redes de mensagens instantâneas.

- **Modelagem em Grafo (Aula T25):**
  - **Vértices ($V$):** Pessoas participantes de grupos sociais (`Família`, `Trabalho`, `Faculdade`, `Academia`, `Condomínio`).
  - **Arestas ($E$):** Contato direto mútuo (possibilidade de encaminhar mensagem de $u$ para $v$ e vice-versa).
  - **Tipo e Estrutura:** Grafo simples, **não direcionado** e **não ponderado**, representado em **Lista de Adjacência** ($\mathcal{O}(V + E)$ em memória, ideal para redes sociais esparsas).
- **Algoritmos e Conceitos da Disciplina Integrados:**
  1. **Busca em Largura — BFS (Aula T25, $\mathcal{O}(V + E)$):** Simula a propagação em ondas discretas (Onda 0 = Paciente Zero, Onda 1 = contatos diretos, Onda 2 = contatos de contatos...), reconstruindo o caminho do boato e identificando quem fica isolado.
  2. **Quarentena Exata por Força Bruta (Aula T23, $\mathcal{O}(V \cdot (V + E))$):** Testa isolar cada pessoa elegível $v$, executa a BFS sem $v$ e calcula quantas pessoas deixam de ser contaminadas:
     $$\text{protegidos}(v) = |\text{alcançados}(G)| - |\text{alcançados}(G \setminus \{v\})| - 1$$
  3. **Pontos de Articulação de Tarjan via DFS ($\mathcal{O}(V + E)$) vs. Heurística de Maior Grau (Aula T23):**
     - **Momento-chave didático do projeto:** Na rede principal (28 pessoas, 42 contatos), a pessoa mais "popular" (**Marina**, grau 7, grupo Faculdade) **não protege ninguém (0 protegidos)** quando bloqueada, pois seu grupo é internamente redundante. Já **Diego** (grau 5) e **Fábio** (grau 3) são **Pontos de Articulação (pontes entre grupos)** e seu bloqueio protege **20 e 18 pessoas (até 74% da rede)**.

---

## 3. Mapa dos Planos Separados e Melhorias (v0 → v1)

A partir da avaliação crítica da `v0`, o planejamento foi dividido em **3 planos específicos** mais este documento geral:

| Plano | Arquivo | Problemas diagnosticados na v0 | Solução planejada para a v1 |
|---|---|---|---|
| **1. Pesquisa (Relatório PDF)** | [`plano_pesquisa.md`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/plano/plano_pesquisa.md) | • Comprido demais (21 páginas)<br>• Comandos LaTeX crus (`$K_5$`, `$V$`, `∑_{v ∈ V}`)<br>• Glifos quebrados (`10■`)<br>• Textos sobrepostos em tabelas e gráficos | • Enxugar para **8 a 10 páginas** (seguindo o modelo de 8 págs do Teorema de Hall)<br>• Usar tags nativas do ReportLab (`<sub>`, `<super>`) e fontes TrueType do Windows<br>• Envolver 100% das células de tabela em `Paragraph` (quebra automática de linha) e ajustar rótulos/proporções das figuras |
| **2. Apresentação (Slides PPTX)** | [`plano_slides.md`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/plano/plano_slides.md) | • Excesso de texto por slide (paredões de bullets)<br>• Fonte pequena (11–13 pt)<br>• Pouco intuitivo (explicava topologia com texto)<br>• Zero dinâmico (lâminas estáticas repetitivas) | • **Máximo de 25–35 palavras por slide** e fonte mínima de **20–24 pt**<br>• Substituir parágrafos por **diagramas visuais grandes** e comparativo visual *Intuição vs. Topologia*<br>• Adicionar **animações progressivas por clique** (ondas BFS e corte da ponte) |
| **3. Código (Java + Frontend)** | [`plano_codigo.md`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/plano/plano_codigo.md) | • Polaroids grandes sobrepostas umas às outras<br>• Barra superior confusa com 8 botões e `"Modo Quarentena: OFF"`<br>• Painel lateral poluído com tudo empilhado | • Nós mais compactos + **algoritmo anticolisão** e demarcação visual dos 5 grupos (zero sobreposição)<br>• Interação direta no nó (clique esquerdo = origem / clique direito ou botão rápido = bloquear)<br>• Painel lateral organizado em **2 abas limpas** (*Propagação BFS* e *Quarentena*) |

---

## 4. Arquitetura do Repositório e Ambiente Técnico

```text
Projeto Semestral/
├── Enunciado/                          (arquivos originais da disciplina)
├── Aulas sobre grafos/                 (slides T17 a T25 do Prof. Calvetti)
├── Exemplo de Documento de Pesquisa/   (modelo PDF de 8 páginas — referência de estilo)
├── plano/                              (documentação de planejamento v1)
│   ├── plano_geral.md                  ← este arquivo
│   ├── plano_pesquisa.md               ← plano do relatório ABNT
│   ├── plano_slides.md                 ← plano da apresentação PPTX
│   └── plano_codigo.md                 ← plano do backend Java + frontend web
├── demo/                               (Entregável 3: Aplicação Java + Interface Web)
│   ├── src/br/maua/fakenews/           (código-fonte Java 21 puro, sem dependências externas)
│   ├── test/br/maua/fakenews/          (suíte de testes automatizados)
│   ├── dados/                          (pessoas.csv e contatos.csv)
│   ├── web/                            (index.html, estilo.css, app.js — 100% offline)
│   └── compilar.bat · executar.bat · testar.bat
├── documentos/                         (Scripts geradores dos documentos)
│   ├── requirements.txt
│   ├── comum/                          (tema visual e gerador de figuras limpas)
│   ├── relatorio/                      (gerador do PDF/DOCX enxuto e sem erros de formatação)
│   └── apresentacao/                   (gerador do PPTX visual e dinâmico)
└── Entrega/                            (Artefatos finais prontos para o CanvasLMS)
    ├── Relatorio_Grafos_e_suas_Aplicacoes.pdf
    ├── Apresentacao_Caso_Fake_News.pptx
    └── Demo_FakeNews_Java.zip
```

### Regras de Ambiente
1. **Java 21 LTS (Eclipse Temurin):** Compilação direta via `javac -encoding UTF-8` empacotando em `fakenews.jar` (sem Maven/Gradle para não depender de internet na sala de aula).
2. **Ambiente Virtual Python fora do OneDrive:** Manter o `.venv` em `%LOCALAPPDATA%\ecm306-venv` para evitar que o OneDrive sincronize milhares de arquivos de biblioteca.
3. **Execução 100% Offline:** Nem o frontend web nem os scripts dependem de CDNs externas ou APIs de terceiros.

---

## 5. Checklist de Entrega Final (12/11/2026)

- [ ] **Relatório PDF (`Entrega/Relatorio_Grafos_e_suas_Aplicacoes.pdf`):** 8–10 páginas, zero strings `$` ou `■`, zero textos sobrepostos nas tabelas e figuras, inspecionado visualmente página por página.
- [ ] **Apresentação PPTX (`Entrega/Apresentacao_Caso_Fake_News.pptx`):** 6 slides visuais, fontes $\ge 20\text{ pt}$, animações de entrada por clique funcionando, notas de fala para 5 minutos.
- [ ] **Aplicação Java (`Entrega/Demo_FakeNews_Java.zip`):** `compilar.bat`, `testar.bat` e `executar.bat` testados; interface web sem sobreposição de nós e com fluxo intuitivo em 3 cliques.
- [ ] **Submissão Individual:** Ambos os integrantes (David e Kauã) enviam os arquivos no CanvasLMS.
