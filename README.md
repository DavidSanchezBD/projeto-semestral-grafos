# Projeto Semestral ECM306 — Teoria dos Grafos
**Instituto Mauá de Tecnologia (IMT) — Engenharia de Computação**
**Disciplina:** ECM306 — Tópicos Avançados de Estrutura de Dados  
**Orientador:** Prof. José Calvetti  
**Semestre:** 2º Semestre de 2026  

---

## 👥 Integrantes do Grupo
- **David Sanchez Bittencourt Daniel** — RA: `24.00029-9`
- **Kauã Bueno Marcatto Ortega** — RA: `24.00031-0`

---

## 📁 Os Três Artefatos de Entrega (Pasta `Entrega/`)

Todos os artefatos solicitados no enunciado estão compilados e prontos para submissão na pasta [`Entrega/`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Entrega/):

| # | Artefato | Arquivo | Descrição |
|---|---|---|---|
| **1a** | **Relatório de Pesquisa (DOCX Editável)** | [`Relatorio_Grafos_e_suas_Aplicacoes.docx`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Entrega/Relatorio_Grafos_e_suas_Aplicacoes.docx) | **Versão editável completa em Word** com formatação rigorosa da ABNT (margens 3/3/2/2, Times New Roman 12, entrelinha 1,5, recuo de 1,25 cm, 6 tabelas estilizadas, 5 figuras em alta resolução e referências NBR 6023). Permite edição livre de textos e dados antes do envio final. |
| **1b** | **Relatório de Pesquisa (PDF Final)** | [`Relatorio_Grafos_e_suas_Aplicacoes.pdf`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Entrega/Relatorio_Grafos_e_suas_Aplicacoes.pdf) | **21 páginas**, padrão ABNT rigoroso (NBR 14724/6023/6024). Cobre fundamentos, lema do aperto de mãos, representações, Euler/Hamilton, Hall/emparelhamentos, Kuratowski/planaridade, coloração, algoritmos (BFS, DFS, Dijkstra, Kahn), técnicas de projeto (Aula T23) e estudo de caso completo com tabelas e gráficos. |
| **2** | **Apresentação do Problema (PPTX)** | [`Apresentacao_Caso_Fake_News.pptx`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Entrega/Apresentacao_Caso_Fake_News.pptx) | **6 slides widescreen (16:9)** sob o tema criativo de **"Jornal Investigativo"** (manchetes, recortes, carimbos). Possui **transições suaves e animações de entrada nativas do PowerPoint** (Zoom e Fade nos carimbos e elementos-chave), design harmonioso sem espaços vazios e **notas de orador** cronometradas para **5 minutos**, divididas entre David e Kauã. |
| **3** | **Demonstração / Solução em Java** | [`Demo_FakeNews_Java.zip`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/Entrega/Demo_FakeNews_Java.zip) e pasta [`demo/`](file:///c:/Users/david/OneDrive/Documents/Faculdade/Tópicos%20Avançados%20de%20Estrutura%20de%20Dados/Projeto%20Semestral/demo/) | Implementação em **Java puro (JDK 21 LTS)** sem dependências externas. Simula a propagação de fake news em ondas por BFS, calcula quarentena por força bruta $O(V \cdot (V+E))$, compara com a heurística de maior grau e identifica pontes com o Algoritmo de Tarjan $O(V+E)$. Servidor HTTP nativo expõe API REST consumida por interface web interativa estilo quadro de cortiça. |

---

## 🚀 Como Executar a Demonstração em Java

### Pré-requisitos
- JDK 21 LTS ou superior instalado e configurado no PATH (`javac -version` e `java -version`).
- Qualquer navegador web moderno (Edge, Chrome, Firefox).

### 1. Iniciar a Demonstração com Interface Web (Recomendado)
Entre na pasta `demo/` e execute:
```cmd
cd demo
executar.bat
```
O script compilará os arquivos fonte (gerando `fakenews.jar`), iniciará o servidor local em `http://localhost:8080/` e abrirá a interface automaticamente no navegador.

### 2. Execução em Modo Console (Plano B em caso de falha no navegador)
```cmd
cd demo
java -jar fakenews.jar --console
```
Imprime no terminal a rede, as ondas de transmissão da BFS, os nós isolados, o ranking de quarentena da força bruta e o diagnóstico da heurística.

### 3. Execução dos Testes Automatizados
```cmd
cd demo
testar.bat
```
Executa a suíte de testes contendo 12 verificações rigorosas (caminho $P_5$, ciclo $C_6$, estrela, grafos desconexos, exemplo da Aula T25, rede do CSV e 200 grafos aleatórios testando a equivalência do algoritmo de Tarjan contra a força bruta).

---

## 🛠️ Como Regerar os Documentos (Relatório e Slides)

Os scripts geradores utilizam Python com ambiente virtual configurado em `%LOCALAPPDATA%\ecm306-venv`:
```powershell
# 1. Regerar as figuras matemáticas e de benchmark
& "$env:LOCALAPPDATA\ecm306-venv\Scripts\python.exe" documentos\comum\tema.py

# 2a. Regerar o Relatório de Pesquisa em DOCX (Word editável)
& "$env:LOCALAPPDATA\ecm306-venv\Scripts\python.exe" documentos\relatorio\gerar_relatorio_docx.py

# 2b. Regerar o Relatório de Pesquisa em PDF (ABNT)
& "$env:LOCALAPPDATA\ecm306-venv\Scripts\python.exe" documentos\relatorio\gerar_relatorio.py

# 3. Regerar a Apresentação PPTX com notas de orador e layout balanceado
& "$env:LOCALAPPDATA\ecm306-venv\Scripts\python.exe" documentos\apresentacao\gerar_apresentacao.py

# 4. Aplicar transições suaves e animações automáticas no PPTX via PowerPoint COM
powershell -ExecutionPolicy Bypass -File documentos\apresentacao\aplicar_animacoes_pptx.ps1
```

---

## 📂 Estrutura Completa do Repositório
```
Projeto Semestral/
├── Entrega/                                      # ARTEFATOS FINAIS PARA ENVIO
│   ├── Relatorio_Grafos_e_suas_Aplicacoes.pdf    # Artefato 1: PDF de Pesquisa ABNT (21 págs)
│   ├── Apresentacao_Caso_Fake_News.pptx          # Artefato 2: Slides PPTX Jornal Investigativo (5 min)
│   └── Demo_FakeNews_Java.zip                    # Artefato 3: Pacote completo da Solução Java
├── demo/                                         # CÓDIGO FONTE DA DEMONSTRAÇÃO
│   ├── src/br/maua/fakenews/
│   │   ├── App.java                              # Ponto de entrada (CLI + inicializador)
│   │   ├── modelo/                               # Pessoa.java e Grafo.java (Lista de Adjacência)
│   │   ├── algoritmos/                           # BuscaEmLargura.java, Quarentena.java, PontosDeArticulacao.java
│   │   ├── dados/                                # LeitorCSV.java, GeradorDeRede.java
│   │   └── web/                                  # ServidorWeb.java (HttpServer nativo), Json.java
│   ├── test/br/maua/fakenews/TestesAlgoritmos.java # 12 testes unitários e de invariantes
│   ├── dados/                                    # pessoas.csv (28 nós) e contatos.csv (42 arestas)
│   ├── web/                                      # index.html, estilo.css, app.js (Quadro de Cortiça)
│   ├── compilar.bat                              # Script de compilação sem Maven/Gradle
│   ├── executar.bat                              # Script de inicialização automática
│   └── testar.bat                                # Script de execução dos testes
├── documentos/                                   # SCRIPTS GERADORES EM PYTHON
│   ├── comum/tema.py                             # Geração de figuras científicas em 300 DPI
│   ├── relatorio/gerar_relatorio.py              # Compilador ReportLab do PDF ABNT
│   ├── apresentacao/gerar_apresentacao.py        # Compilador python-pptx dos slides
│   └── requirements.txt                          # Dependências Python
├── Enunciado/                                    # Instruções originais da disciplina
└── Aulas sobre Grafos/                           # Material didático do Prof. Calvetti (Aulas 17 a 25)
```
