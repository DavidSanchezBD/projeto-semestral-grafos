/**
 * CASO FAKE NEWS — FRONTEND INTERATIVO v1 ("O JAVA PENSA, O NAVEGADOR DESENHA")
 * ECM306 - Tópicos Avançados de Estrutura de Dados | Instituto Mauá de Tecnologia
 * Autores: David Sanchez Bittencourt Daniel & Kauã Bueno Marcatto Ortega
 */

(function () {
  'use strict';

  // Configuração visual dos 5 Territórios (Grupos Sociais) em coordenadas normalizadas [0..1]
  const TERRITORIOS_28 = [
    { grupo: 'Família',    titulo: 'FAMÍLIA (6)',    x: 0.025, y: 0.045, w: 0.305, h: 0.455, fill: '#fef2f2', stroke: '#ef4444' },
    { grupo: 'Condomínio', titulo: 'CONDOMÍNIO (4)', x: 0.025, y: 0.545, w: 0.305, h: 0.415, fill: '#f8fafc', stroke: '#64748b' },
    { grupo: 'Trabalho',   titulo: 'TRABALHO (6)',   x: 0.355, y: 0.045, w: 0.315, h: 0.455, fill: '#fffbeb', stroke: '#f59e0b' },
    { grupo: 'Academia',   titulo: 'ACADEMIA (5)',   x: 0.355, y: 0.545, w: 0.315, h: 0.415, fill: '#f0fdf4', stroke: '#10b981' },
    { grupo: 'Faculdade',  titulo: 'FACULDADE (7)',  x: 0.695, y: 0.045, w: 0.280, h: 0.915, fill: '#eff6ff', stroke: '#3b82f6' }
  ];

  // Coordenadas normalizadas base para os 28 vértices (projetadas para zero cruzamento desnecessário e zero colisão)
  const COORDS_BASE_28 = {
    // Família (0..5)
    0:  { nx: 0.080, ny: 0.180 }, // Ana (Paciente Zero padrão)
    1:  { nx: 0.080, ny: 0.385 }, // Bruno
    2:  { nx: 0.175, ny: 0.415 }, // Carla (ponte p/ Condomínio)
    3:  { nx: 0.185, ny: 0.180 }, // Diego (ponte p/ Elisa e Fábio)
    4:  { nx: 0.275, ny: 0.385 }, // Elisa
    5:  { nx: 0.285, ny: 0.220 }, // Fábio (ponte p/ Trabalho)

    // Condomínio (24..27)
    24: { nx: 0.165, ny: 0.665 }, // Zeca
    25: { nx: 0.085, ny: 0.855 }, // Alice
    26: { nx: 0.205, ny: 0.855 }, // Beto
    27: { nx: 0.280, ny: 0.720 }, // Sônia (Isolada, grau 0)

    // Trabalho (6..11)
    6:  { nx: 0.405, ny: 0.235 }, // Gabi
    7:  { nx: 0.495, ny: 0.145 }, // Heitor
    8:  { nx: 0.475, ny: 0.375 }, // Iara
    9:  { nx: 0.615, ny: 0.165 }, // João (ponte p/ Faculdade)
    10: { nx: 0.620, ny: 0.325 }, // Karen
    11: { nx: 0.560, ny: 0.430 }, // Lucas (ponte p/ Academia)

    // Academia (19..23)
    19: { nx: 0.525, ny: 0.650 }, // Tiago
    20: { nx: 0.415, ny: 0.720 }, // Úrsula
    21: { nx: 0.515, ny: 0.795 }, // Vitor
    22: { nx: 0.425, ny: 0.885 }, // Wesley
    23: { nx: 0.615, ny: 0.855 }, // Yara

    // Faculdade (12..18)
    13: { nx: 0.755, ny: 0.205 }, // Nuno
    18: { nx: 0.915, ny: 0.225 }, // Sofia
    14: { nx: 0.755, ny: 0.430 }, // Olívia
    12: { nx: 0.845, ny: 0.495 }, // Marina (Maior Grau = 7, centro da Faculdade)
    17: { nx: 0.925, ny: 0.545 }, // Rafael
    15: { nx: 0.765, ny: 0.725 }, // Pedro
    16: { nx: 0.895, ny: 0.795 }  // Quésia
  };

  const CORES_GRUPO = {
    'Família': '#ef4444',
    'Trabalho': '#f59e0b',
    'Faculdade': '#3b82f6',
    'Academia': '#10b981',
    'Condomínio': '#64748b'
  };

  // Estado da Aplicação
  const estado = {
    rede: null,
    mapaPessoas: new Map(),
    posicoesPx: new Map(),
    origem: 0,
    bloqueados: new Set(),
    bfs: null,
    bfsSemBloqueioTotal: 27,
    quarentena: null,
    ondaVisivelMax: Infinity,
    etapaPassoAPasso: -1,
    timerAnimacao: null,
    destacarTarjan: false,
    abaAtiva: 'bfs',
    mostrarCalloutsQuarentena: false
  };

  // Referências DOM
  const dom = {
    selOrigem: document.getElementById('sel-origem'),
    selCenario: document.getElementById('sel-cenario'),
    btnPropagar: document.getElementById('btn-propagar'),
    btnPasso: document.getElementById('btn-passo'),
    btnLimpar: document.getElementById('btn-limpar'),
    btnQuarentena: document.getElementById('btn-quarentena'),
    btnToggleTarjan: document.getElementById('btn-toggle-tarjan'),
    countTarjan: document.getElementById('count-tarjan'),
    textoStatus: document.getElementById('texto-status'),

    palco: document.getElementById('palco-grafo'),
    svgTerritorios: document.getElementById('grupo-territorios'),
    svgArestas: document.getElementById('grupo-arestas'),
    camadaNos: document.getElementById('camada-nos'),
    tooltip: document.getElementById('node-tooltip'),

    kpiAlcancados: document.getElementById('kpi-alcancados'),
    kpiAlcancadosSub: document.getElementById('kpi-alcancados-sub'),
    kpiOndas: document.getElementById('kpi-ondas'),
    kpiOndasSub: document.getElementById('kpi-ondas-sub'),
    kpiBloqueados: document.getElementById('kpi-bloqueados'),
    kpiBloqueadosSub: document.getElementById('kpi-bloqueados-sub'),
    kpiProtegidos: document.getElementById('kpi-protegidos'),
    kpiProtegidosSub: document.getElementById('kpi-protegidos-sub'),

    tabBtnBfs: document.getElementById('tab-btn-bfs'),
    tabBtnQuarentena: document.getElementById('tab-btn-quarentena'),
    tabPaneBfs: document.getElementById('tab-pane-bfs'),
    tabPaneQuarentena: document.getElementById('tab-pane-quarentena'),

    badgeNaoAlcancados: document.getElementById('badge-nao-alcancados'),
    listaNaoAlcancados: document.getElementById('lista-nao-alcancados'),
    listaOndas: document.getElementById('lista-ondas'),
    badgeEtapasBfs: document.getElementById('badge-etapas-bfs'),
    tbodyBfs: document.getElementById('tbody-bfs'),

    mgNome: document.getElementById('mg-nome'),
    mgMeta: document.getElementById('mg-meta'),
    mgSalvos: document.getElementById('mg-salvos'),
    mgDesc: document.getElementById('mg-desc'),
    btnTestarMg: document.getElementById('btn-testar-mg'),

    fbNome: document.getElementById('fb-nome'),
    fbMeta: document.getElementById('fb-meta'),
    fbSalvos: document.getElementById('fb-salvos'),
    fbDesc: document.getElementById('fb-desc'),
    btnAplicarFb: document.getElementById('btn-aplicar-fb'),

    badgeTempoFb: document.getElementById('badge-tempo-fb'),
    listaRankingFb: document.getElementById('lista-ranking-fb'),
    listaArticulacoes: document.getElementById('lista-articulacoes'),
    btnBenchmark: document.getElementById('btn-benchmark'),
    boxBenchmark: document.getElementById('box-benchmark'),
    tbodyBenchmark: document.getElementById('tbody-benchmark'),
    benchStatus: document.getElementById('bench-status')
  };

  // =========================================================================
  // 1. COMUNICAÇÃO COM O SERVIDOR JAVA 21 (API REST JSON)
  // =========================================================================
  async function apiGet(url) {
    const resp = await fetch(url, { cache: 'no-store' });
    if (!resp.ok) {
      const txt = await resp.text();
      throw new Error(`Erro HTTP ${resp.status}: ${txt}`);
    }
    return resp.json();
  }

  async function carregarRedeInicial() {
    const dadosRede = await apiGet('/api/rede');
    registrarRede(dadosRede);
    const params = new URLSearchParams(window.location.search);
    const cenarioParam = params.get('cenario');
    const abaParam = params.get('aba');
    if (cenarioParam && ['original', 'marina', 'diego', 'sintetica'].includes(cenarioParam)) {
      dom.selCenario.value = cenarioParam;
      await aplicarCenario(cenarioParam);
    } else {
      await atualizarSimulacaoCompleta({
        animarOndas: false,
        abrirAbaQuarentena: abaParam === 'quarentena'
      });
    }
  }

  function registrarRede(dadosRede) {
    pararAnimacao();
    estado.rede = dadosRede;
    estado.mapaPessoas.clear();
    dadosRede.pessoas.forEach(p => estado.mapaPessoas.set(p.id, p));

    // Preenche seletor de Paciente Zero
    dom.selOrigem.innerHTML = '';
    dadosRede.pessoas.forEach(p => {
      const opt = document.createElement('option');
      opt.value = String(p.id);
      opt.textContent = `${p.nome} (${p.grupo} · g=${p.grau})`;
      dom.selOrigem.appendChild(opt);
    });

    if (!estado.mapaPessoas.has(estado.origem)) {
      estado.origem = 0;
    }
    dom.selOrigem.value = String(estado.origem);
    dom.countTarjan.textContent = String((dadosRede.articulacoes || []).length);
  }

  async function atualizarSimulacaoCompleta(opcoes = {}) {
    const { animarOndas = false, abrirAbaQuarentena = false } = opcoes;
    pararAnimacao();

    const bloqCsv = Array.from(estado.bloqueados).join(',');
    const urlBfsBase = `/api/bfs?origem=${estado.origem}&bloqueados=`;
    const urlBfsAtual = `/api/bfs?origem=${estado.origem}&bloqueados=${encodeURIComponent(bloqCsv)}`;
    const urlQuar = `/api/quarentena?origem=${estado.origem}&bloqueados=${encodeURIComponent(bloqCsv)}`;

    const [bfsBase, bfsAtual, quarentenaAtual] = await Promise.all([
      apiGet(urlBfsBase),
      apiGet(urlBfsAtual),
      apiGet(urlQuar)
    ]);

    estado.bfsSemBloqueioTotal = (bfsBase.alcancados || []).length;
    estado.bfs = bfsAtual;
    estado.quarentena = quarentenaAtual;
    estado.etapaPassoAPasso = -1;

    if (abrirAbaQuarentena) {
      alternarAba('quarentena');
      estado.mostrarCalloutsQuarentena = true;
    }

    if (animarOndas) {
      iniciarAnimacaoOndas();
    } else {
      estado.ondaVisivelMax = Infinity;
      renderizarTudo();
    }
  }

  // =========================================================================
  // 2. CÁLCULO GEOMÉTRICO + ALGORITMO ANTICOLISÃO (ZERO SOBREPOSIÇÃO)
  // =========================================================================
  function calcularPosicoesSemColisao() {
    const rect = dom.palco.getBoundingClientRect();
    const W = Math.max(rect.width || 900, 620);
    const H = Math.max(rect.height || 580, 420);
    const n = estado.rede.pessoas.length;

    const coords = new Map();

    if (estado.rede.tipo === 'original' && n === 28) {
      // Mapeia coordenadas normalizadas para pixels dentro de cada território
      estado.rede.pessoas.forEach(p => {
        const base = COORDS_BASE_28[p.id] || { nx: 0.5, ny: 0.5 };
        coords.set(p.id, {
          x: base.nx * W,
          y: base.ny * H,
          grupo: p.grupo
        });
      });

      // Passo determinístico de relaxamento anticolisão mantendo cada nó no seu território
      const minDist = W < 860 ? 64 : 78;
      const mapaTerritorio = new Map();
      TERRITORIOS_28.forEach(t => mapaTerritorio.set(t.grupo, t));

      const ids = estado.rede.pessoas.map(p => p.id);
      for (let iter = 0; iter < 40; iter++) {
        let moveu = false;
        for (let i = 0; i < ids.length; i++) {
          for (let j = i + 1; j < ids.length; j++) {
            const a = coords.get(ids[i]);
            const b = coords.get(ids[j]);
            let dx = b.x - a.x;
            let dy = b.y - a.y;
            let dist = Math.hypot(dx, dy);
            if (dist < 0.01) {
              dx = 1;
              dy = 0;
              dist = 1;
            }
            if (dist < minDist) {
              const empurrao = (minDist - dist) * 0.52;
              const ux = dx / dist;
              const uy = dy / dist;
              a.x -= ux * empurrao;
              a.y -= uy * empurrao;
              b.x += ux * empurrao;
              b.y += uy * empurrao;
              moveu = true;
            }
          }
        }

        // Restringe cada nó aos limites internos do seu território
        ids.forEach(id => {
          const pos = coords.get(id);
          const t = mapaTerritorio.get(pos.grupo);
          if (t) {
            const padX = 32;
            const padTop = 34;
            const padBottom = 30;
            const minX = t.x * W + padX;
            const maxX = (t.x + t.w) * W - padX;
            const minY = t.y * H + padTop;
            const maxY = (t.y + t.h) * H - padBottom;
            pos.x = Math.max(minX, Math.min(maxX, pos.x));
            pos.y = Math.max(minY, Math.min(maxY, pos.y));
          }
        });

        if (!moveu) break;
      }
    } else {
      // Layout em 5 clusters comunitários com relaxamento para a Rede Sintética (N=60)
      const gruposUnicos = Array.from(new Set(estado.rede.pessoas.map(p => p.grupo)));
      const centrosGrupo = new Map();
      gruposUnicos.forEach((g, idx) => {
        const ang = (2 * Math.PI * idx) / gruposUnicos.length - Math.PI / 2;
        centrosGrupo.set(g, {
          cx: W * 0.5 + Math.cos(ang) * (W * 0.30),
          cy: H * 0.5 + Math.sin(ang) * (H * 0.28)
        });
      });

      const porGrupo = new Map();
      estado.rede.pessoas.forEach(p => {
        if (!porGrupo.has(p.grupo)) porGrupo.set(p.grupo, []);
        porGrupo.get(p.grupo).push(p);
      });

      porGrupo.forEach((lista, grp) => {
        const centro = centrosGrupo.get(grp) || { cx: W / 2, cy: H / 2 };
        const rGrupo = Math.min(W, H) * 0.14;
        lista.forEach((p, idx) => {
          const ang = (2 * Math.PI * idx) / lista.length;
          const rVar = idx % 2 === 0 ? rGrupo : rGrupo * 0.62;
          coords.set(p.id, {
            x: centro.cx + Math.cos(ang) * rVar,
            y: centro.cy + Math.sin(ang) * rVar,
            grupo: p.grupo
          });
        });
      });

      const minDist = n <= 35 ? 68 : 50;
      const ids = estado.rede.pessoas.map(p => p.id);
      for (let iter = 0; iter < 55; iter++) {
        for (let i = 0; i < ids.length; i++) {
          for (let j = i + 1; j < ids.length; j++) {
            const a = coords.get(ids[i]);
            const b = coords.get(ids[j]);
            let dx = b.x - a.x;
            let dy = b.y - a.y;
            let d = Math.hypot(dx, dy) || 1;
            if (d < minDist) {
              const push = (minDist - d) * 0.5;
              a.x -= (dx / d) * push;
              a.y -= (dy / d) * push;
              b.x += (dx / d) * push;
              b.y += (dy / d) * push;
            }
          }
        }
        ids.forEach(id => {
          const pos = coords.get(id);
          pos.x = Math.max(36, Math.min(W - 36, pos.x));
          pos.y = Math.max(32, Math.min(H - 36, pos.y));
        });
      }
    }

    estado.posicoesPx = coords;
  }

  // =========================================================================
  // 3. RENDERIZAÇÃO DO GRAFO (TERRITÓRIOS SVG + ARESTAS + NÓS CIRCULARES)
  // =========================================================================
  function renderizarTudo() {
    if (!estado.rede || !estado.bfs) return;
    calcularPosicoesSemColisao();
    renderizarTerritoriosSvg();
    renderizarArestasSvg();
    renderizarNosHtml();
    atualizarPainelLateral();
    atualizarBannerStatus();
  }

  function renderizarTerritoriosSvg() {
    dom.svgTerritorios.innerHTML = '';
    if (estado.rede.tipo !== 'original' || estado.rede.pessoas.length !== 28) return;

    const rect = dom.palco.getBoundingClientRect();
    const W = Math.max(rect.width || 900, 620);
    const H = Math.max(rect.height || 580, 420);

    TERRITORIOS_28.forEach(t => {
      const x = t.x * W;
      const y = t.y * H;
      const w = t.w * W;
      const h = t.h * H;

      const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      r.setAttribute('x', x.toFixed(1));
      r.setAttribute('y', y.toFixed(1));
      r.setAttribute('width', w.toFixed(1));
      r.setAttribute('height', h.toFixed(1));
      r.setAttribute('fill', t.fill);
      r.setAttribute('stroke', t.stroke);
      r.setAttribute('class', 'territory-box');
      dom.svgTerritorios.appendChild(r);

      const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      lbl.setAttribute('x', (x + 12).toFixed(1));
      lbl.setAttribute('y', (y + 18).toFixed(1));
      lbl.setAttribute('fill', t.stroke);
      lbl.setAttribute('class', 'territory-label');
      lbl.textContent = t.titulo;
      dom.svgTerritorios.appendChild(lbl);
    });
  }

  function renderizarArestasSvg() {
    dom.svgArestas.innerHTML = '';
    const dist = estado.bfs.dist || [];
    const ant = estado.bfs.anterior || [];

    estado.rede.contatos.forEach(([u, v]) => {
      const pu = estado.posicoesPx.get(u);
      const pv = estado.posicoesPx.get(v);
      if (!pu || !pv) return;

      const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      line.setAttribute('x1', pu.x.toFixed(1));
      line.setAttribute('y1', pu.y.toFixed(1));
      line.setAttribute('x2', pv.x.toFixed(1));
      line.setAttribute('y2', pv.y.toFixed(1));
      line.dataset.u = String(u);
      line.dataset.v = String(v);

      const classes = ['edge-line'];
      const pObjU = estado.mapaPessoas.get(u);
      const pObjV = estado.mapaPessoas.get(v);
      if (pObjU && pObjV && pObjU.grupo !== pObjV.grupo) {
        classes.push('edge-bridge');
      }

      if (estado.bloqueados.has(u) || estado.bloqueados.has(v)) {
        classes.push('edge-blocked');
      } else {
        const du = dist[u];
        const dv = dist[v];
        const ehArestaArvoreBfs = (ant[v] === u && dv <= estado.ondaVisivelMax) ||
                                  (ant[u] === v && du <= estado.ondaVisivelMax);
        if (ehArestaArvoreBfs) {
          classes.push('edge-tree');
        } else if (du === -1 && dv === -1 && estado.bloqueados.size > 0) {
          classes.push('edge-saved-path');
        }
      }

      line.setAttribute('class', classes.join(' '));
      dom.svgArestas.appendChild(line);
    });
  }

  function obterIniciais(nome) {
    return nome.slice(0, 2).toUpperCase();
  }

  function renderizarNosHtml() {
    dom.camadaNos.innerHTML = '';
    const dist = estado.bfs.dist || [];
    const artSet = new Set((estado.quarentena && estado.quarentena.articulacoes) || estado.rede.articulacoes || []);

    const idMaiorGrau = estado.quarentena && estado.quarentena.melhorMaiorGrau
      ? estado.quarentena.melhorMaiorGrau.pessoa
      : -1;
    const idMelhorFb = estado.quarentena && estado.quarentena.melhorForcaBruta
      ? estado.quarentena.melhorForcaBruta.pessoa
      : -1;

    estado.rede.pessoas.forEach(p => {
      const pos = estado.posicoesPx.get(p.id);
      if (!pos) return;

      const el = document.createElement('div');
      el.className = 'graph-node';
      el.style.left = `${pos.x.toFixed(1)}px`;
      el.style.top = `${pos.y.toFixed(1)}px`;
      el.dataset.id = String(p.id);

      const d = dist[p.id];
      const estaBloqueado = estado.bloqueados.has(p.id);
      const visivelNaOnda = d !== -1 && d <= estado.ondaVisivelMax;

      let textoTagOnda = '';
      let corTagBg = '';

      if (estaBloqueado) {
        el.classList.add('state-bloq');
        textoTagOnda = '🚫 BLOQ';
        corTagBg = '#7c3aed';
      } else if (visivelNaOnda) {
        if (d === 0) {
          el.classList.add('state-onda-0');
          textoTagOnda = '🎯 Onda 0';
          corTagBg = '#dc2626';
        } else if (d === 1) {
          el.classList.add('state-onda-1');
          textoTagOnda = 'Onda 1';
          corTagBg = '#ea580c';
        } else if (d === 2) {
          el.classList.add('state-onda-2');
          textoTagOnda = 'Onda 2';
          corTagBg = '#d97706';
        } else {
          el.classList.add('state-onda-3');
          textoTagOnda = `Onda ${d}`;
          corTagBg = '#2563eb';
        }
      } else if (d === -1 && p.grau === 0) {
        el.classList.add('state-isolado');
        textoTagOnda = 'Isolada';
        corTagBg = '#64748b';
      } else if (d === -1 && estado.bloqueados.size > 0) {
        el.classList.add('state-salvo');
        textoTagOnda = '🛡️ Salvo';
        corTagBg = '#16a34a';
      }

      if (artSet.has(p.id)) {
        el.classList.add('is-articulacao');
        if (estado.destacarTarjan) {
          el.classList.add('tarjan-highlight');
        }
      }

      // Callout flutuante direto no grafo para Marina vs Diego quando Quarentena está em foco
      if (estado.mostrarCalloutsQuarentena && estado.rede.pessoas.length <= 35) {
        if (p.id === idMaiorGrau && !estaBloqueado) {
          const callout = document.createElement('div');
          callout.className = 'node-callout callout-bad';
          callout.textContent = `❌ Maior Grau (g=${p.grau}) → ${estado.quarentena.melhorMaiorGrau.protegidos} salvos`;
          el.appendChild(callout);
        } else if (p.id === idMelhorFb && !estaBloqueado) {
          const callout = document.createElement('div');
          callout.className = 'node-callout callout-good';
          callout.textContent = `✅ Melhor Ponte (g=${p.grau}) → ${estado.quarentena.melhorForcaBruta.protegidos} salvos`;
          el.appendChild(callout);
        }
      }

      // Círculo principal do nó
      const circle = document.createElement('div');
      circle.className = 'node-circle';
      if (!estaBloqueado && !visivelNaOnda && d !== -1) {
        circle.style.borderColor = CORES_GRUPO[p.grupo] || '#64748b';
      }
      circle.textContent = obterIniciais(p.nome);

      // Badge numérico de grau
      const degBadge = document.createElement('span');
      degBadge.className = 'node-deg-badge';
      degBadge.textContent = `g${p.grau}`;
      circle.appendChild(degBadge);

      // Botão rápido de bloquear/desbloquear no hover
      if (p.id !== estado.origem) {
        const quickBlock = document.createElement('button');
        quickBlock.type = 'button';
        quickBlock.className = 'node-quick-block';
        quickBlock.title = estaBloqueado ? 'Retirar da Quarentena' : 'Colocar em Quarentena (Bloquear)';
        quickBlock.textContent = estaBloqueado ? '↺' : '🚫';
        quickBlock.addEventListener('click', ev => {
          ev.stopPropagation();
          alternarBloqueioPessoa(p.id);
        });
        circle.appendChild(quickBlock);
      }

      el.appendChild(circle);

      // Pill com o nome da pessoa
      const pill = document.createElement('div');
      pill.className = 'node-label-pill';
      pill.textContent = p.nome;
      el.appendChild(pill);

      // Sub-etiqueta de onda ou status (apenas na rede principal para manter limpeza)
      if (textoTagOnda && estado.rede.pessoas.length <= 35) {
        const wTag = document.createElement('div');
        wTag.className = 'node-wave-tag';
        wTag.style.background = corTagBg;
        wTag.style.color = '#ffffff';
        wTag.textContent = textoTagOnda;
        el.appendChild(wTag);
      }

      // Eventos de Interação Direta
      el.addEventListener('click', () => selecionarNovaOrigem(p.id));
      el.addEventListener('contextmenu', ev => {
        ev.preventDefault();
        if (p.id !== estado.origem) {
          alternarBloqueioPessoa(p.id);
        }
      });
      el.addEventListener('mouseenter', ev => destacarVizinhancaNo(p.id, ev));
      el.addEventListener('mousemove', ev => posicionarTooltip(ev));
      el.addEventListener('mouseleave', () => limparDestaqueHover());

      dom.camadaNos.appendChild(el);
    });
  }

  // =========================================================================
  // 4. HOVER INTERATIVO E RECONSTRUÇÃO DO CAMINHO MÍNIMO BFS
  // =========================================================================
  function reconstruirCaminhoBfs(idDestino) {
    if (!estado.bfs || !estado.bfs.dist) return [];
    if (estado.bfs.dist[idDestino] === -1) return [];
    const caminho = [];
    let atual = idDestino;
    let guarda = 0;
    while (atual !== -1 && guarda < 200) {
      const p = estado.mapaPessoas.get(atual);
      caminho.push(p ? p.nome : `#${atual}`);
      atual = estado.bfs.anterior[atual];
      guarda++;
    }
    return caminho.reverse();
  }

  function destacarVizinhancaNo(idFoco, ev) {
    const p = estado.mapaPessoas.get(idFoco);
    if (!p) return;

    const vizinhos = new Set([idFoco]);
    const linhas = dom.svgArestas.querySelectorAll('line');
    linhas.forEach(l => {
      const u = Number(l.dataset.u);
      const v = Number(l.dataset.v);
      if (u === idFoco || v === idFoco) {
        l.classList.add('edge-hover');
        l.classList.remove('edge-dimmed');
        vizinhos.add(u);
        vizinhos.add(v);
      } else {
        l.classList.add('edge-dimmed');
      }
    });

    const nos = dom.camadaNos.querySelectorAll('.graph-node');
    nos.forEach(no => {
      const id = Number(no.dataset.id);
      if (!vizinhos.has(id)) {
        no.classList.add('node-dimmed');
      }
    });

    // Monta Tooltip Rico
    const d = estado.bfs.dist[idFoco];
    const artSet = new Set((estado.quarentena && estado.quarentena.articulacoes) || []);
    const ehPonte = artSet.has(idFoco);
    const caminho = reconstruirCaminhoBfs(idFoco);

    let statusHtml = '';
    if (estado.bloqueados.has(idFoco)) {
      statusHtml = '<span style="color:#c084fc;font-weight:700;">🚫 Em Quarentena (Bloqueado)</span>';
    } else if (d === 0) {
      statusHtml = '<span style="color:#f87171;font-weight:700;">🎯 Paciente Zero (Onda 0)</span>';
    } else if (d > 0) {
      statusHtml = `<span style="color:#fb923c;font-weight:700;">🔥 Contaminado na Onda ${d} (${d} salto${d > 1 ? 's' : ''})</span>`;
    } else if (p.grau === 0) {
      statusHtml = '<span style="color:#94a3b8;font-weight:700;">⚪ Vértice Isolado (dist = ∞)</span>';
    } else {
      statusHtml = '<span style="color:#4ade80;font-weight:700;">🛡️ Protegido pela Quarentena!</span>';
    }

    dom.tooltip.innerHTML = `
      <div style="font-size:0.86rem;font-weight:800;margin-bottom:3px;">
        ${p.nome} <span style="color:#94a3b8;font-weight:600;">(id ${p.id} · ${p.grupo})</span>
      </div>
      <div>Grau: <strong>${p.grau} contato(s)</strong> ${ehPonte ? '· <span style="color:#facc15;font-weight:800;">★ Ponto de Articulação</span>' : ''}</div>
      <div>Status: ${statusHtml}</div>
      ${caminho.length > 1 ? `<div style="margin-top:4px;font-size:0.72rem;color:#cbd5e1;">Rota do boato: <strong>${caminho.join(' → ')}</strong></div>` : ''}
    `;
    dom.tooltip.classList.remove('hidden');
    posicionarTooltip(ev);
  }

  function posicionarTooltip(ev) {
    if (dom.tooltip.classList.contains('hidden')) return;
    const rect = dom.palco.getBoundingClientRect();
    let x = ev.clientX - rect.left + 14;
    let y = ev.clientY - rect.top + 14;
    if (x + 250 > rect.width) x -= 265;
    if (y + 110 > rect.height) y -= 115;
    dom.tooltip.style.left = `${Math.max(8, x)}px`;
    dom.tooltip.style.top = `${Math.max(8, y)}px`;
  }

  function limparDestaqueHover() {
    dom.tooltip.classList.add('hidden');
    dom.svgArestas.querySelectorAll('line').forEach(l => {
      l.classList.remove('edge-hover', 'edge-dimmed');
    });
    dom.camadaNos.querySelectorAll('.graph-node').forEach(n => {
      n.classList.remove('node-dimmed');
    });
  }

  function destacarOndaNoGrafo(nivelOnda) {
    const dist = estado.bfs.dist || [];
    dom.camadaNos.querySelectorAll('.graph-node').forEach(no => {
      const id = Number(no.dataset.id);
      if (dist[id] === nivelOnda) {
        no.classList.remove('node-dimmed');
      } else {
        no.classList.add('node-dimmed');
      }
    });
  }

  // =========================================================================
  // 5. ATUALIZAÇÃO DO PAINEL LATERAL (4 KPIs + ABA 1 BFS + ABA 2 QUARENTENA)
  // =========================================================================
  function atualizarPainelLateral() {
    const totalVertices = estado.rede.pessoas.length;
    const alcancados = (estado.bfs.alcancados || []).length;
    const rodadas = estado.bfs.rodadas || 0;
    const qtdBloq = estado.bloqueados.size;

    // Cálculo de pessoas protegidas (descontando os próprios bloqueados)
    const protegidosLiquidos = Math.max(0, estado.bfsSemBloqueioTotal - alcancados - qtdBloq);
    const baseAlcancaveis = Math.max(1, estado.bfsSemBloqueioTotal - 1);
    const pctProtegidos = Math.round((protegidosLiquidos / baseAlcancaveis) * 100);

    // 1. KPIs Superiores
    dom.kpiAlcancados.textContent = `${alcancados} / ${totalVertices}`;
    dom.kpiAlcancadosSub.textContent = `${Math.round((alcancados / totalVertices) * 100)}% da rede`;

    dom.kpiOndas.textContent = `${rodadas} onda${rodadas === 1 ? '' : 's'}`;
    dom.kpiOndasSub.textContent = rodadas > 0 ? `Distância máx = ${rodadas}` : 'Sem contágio';

    if (qtdBloq === 0) {
      dom.kpiBloqueados.textContent = 'Nenhum';
      dom.kpiBloqueadosSub.textContent = 'Clique dir. p/ bloquear';
    } else if (qtdBloq === 1) {
      const idUnico = Array.from(estado.bloqueados)[0];
      const pUnico = estado.mapaPessoas.get(idUnico);
      dom.kpiBloqueados.textContent = pUnico ? pUnico.nome : `#${idUnico}`;
      dom.kpiBloqueadosSub.textContent = `Grau ${pUnico ? pUnico.grau : '-'}`;
    } else {
      dom.kpiBloqueados.textContent = `${qtdBloq} pessoas`;
      dom.kpiBloqueadosSub.textContent = 'Em quarentena';
    }

    dom.kpiProtegidos.textContent = `${protegidosLiquidos} (${pctProtegidos}%)`;
    dom.kpiProtegidosSub.textContent = protegidosLiquidos > 0 ? 'Salvos do boato!' : 'Sem contenção ativa';

    // 2. ABA 1: Pessoas Fora de Alcance / Salvas + Ondas + Tabela FIFO
    renderizarAbaBfs();

    // 3. ABA 2: Comparativo Maior Grau vs Força Bruta + Ranking + Articulações
    renderizarAbaQuarentena();
  }

  function renderizarAbaBfs() {
    const naoAlcancados = (estado.bfs.naoAlcancados || []).filter(id => !estado.bloqueados.has(id));
    dom.badgeNaoAlcancados.textContent = `${naoAlcancados.length} pessoa${naoAlcancados.length === 1 ? '' : 's'}`;
    dom.listaNaoAlcancados.innerHTML = '';

    if (naoAlcancados.length === 0) {
      dom.listaNaoAlcancados.innerHTML = '<span class="card-subtext">Ninguém ficou protegido nesta configuração.</span>';
    } else {
      naoAlcancados.forEach(id => {
        const p = estado.mapaPessoas.get(id);
        if (!p) return;
        const chip = document.createElement('span');
        chip.className = p.grau === 0 ? 'person-chip' : 'person-chip chip-saved';
        chip.textContent = p.grau === 0 ? `${p.nome} (Isolada)` : `🛡️ ${p.nome} (${p.grupo})`;
        chip.addEventListener('mouseenter', ev => destacarVizinhancaNo(id, ev));
        chip.addEventListener('mouseleave', () => limparDestaqueHover());
        dom.listaNaoAlcancados.appendChild(chip);
      });
    }

    // Lista de Ondas por Nível
    dom.listaOndas.innerHTML = '';
    const niveis = estado.bfs.niveis || [];
    const coresOnda = ['#dc2626', '#ea580c', '#d97706', '#2563eb', '#0284c7'];

    niveis.forEach((listaIds, idxOnda) => {
      if (idxOnda > estado.ondaVisivelMax) return;
      const row = document.createElement('div');
      row.className = 'wave-row';
      row.addEventListener('mouseenter', () => destacarOndaNoGrafo(idxOnda));
      row.addEventListener('mouseleave', () => limparDestaqueHover());

      const badge = document.createElement('span');
      badge.className = 'wave-badge';
      badge.style.background = coresOnda[Math.min(idxOnda, coresOnda.length - 1)];
      badge.textContent = idxOnda === 0 ? 'Onda 0' : `Onda ${idxOnda}`;
      row.appendChild(badge);

      const wrap = document.createElement('div');
      wrap.className = 'chips-wrap';
      listaIds.forEach(id => {
        const p = estado.mapaPessoas.get(id);
        const chip = document.createElement('span');
        chip.className = 'person-chip';
        chip.textContent = p ? `${p.nome}` : `#${id}`;
        wrap.appendChild(chip);
      });
      row.appendChild(wrap);
      dom.listaOndas.appendChild(row);
    });

    // Tabela de Rastreamento da Fila FIFO (Aula T25)
    const passos = estado.bfs.passos || [];
    dom.badgeEtapasBfs.textContent = `${passos.length} etapas`;
    dom.tbodyBfs.innerHTML = '';

    const limitePassos = estado.etapaPassoAPasso >= 0 ? estado.etapaPassoAPasso + 1 : passos.length;
    passos.slice(0, limitePassos).forEach((ps, idx) => {
      const tr = document.createElement('tr');
      if (idx === estado.etapaPassoAPasso) {
        tr.classList.add('row-active');
      }
      const nomeVertice = nomeCurto(ps.vertice);
      const filaStr = (ps.filaAntes || []).map(nomeCurto).join(', ');
      const novosStr = (ps.novos && ps.novos.length > 0)
        ? ps.novos.map(nomeCurto).join(', ')
        : '—';

      tr.innerHTML = `
        <td><strong>${idx + 1}</strong></td>
        <td>[${filaStr}]</td>
        <td><strong>${nomeVertice}</strong></td>
        <td>${novosStr}</td>
      `;
      dom.tbodyBfs.appendChild(tr);
    });
  }

  function renderizarAbaQuarentena() {
    if (!estado.quarentena) return;
    const q = estado.quarentena;
    const baseAlcancaveis = Math.max(1, (q.alcancadosAtuais || 1) - 1);

    // Card Esquerdo: Heurística de Maior Grau
    if (q.melhorMaiorGrau) {
      const pMg = estado.mapaPessoas.get(q.melhorMaiorGrau.pessoa);
      const pctMg = Math.round((q.melhorMaiorGrau.protegidos / baseAlcancaveis) * 100);
      dom.mgNome.textContent = pMg ? `${pMg.nome} (${pMg.grupo})` : `#${q.melhorMaiorGrau.pessoa}`;
      dom.mgMeta.textContent = `Grau ${q.melhorMaiorGrau.grau} (Mais popular da rede)`;
      dom.mgSalvos.textContent = `${q.melhorMaiorGrau.protegidos} protegidos (${pctMg}%)`;
      dom.mgDesc.textContent = q.melhorMaiorGrau.protegidos === 0
        ? 'Grupo possui rotas internas redundantes; o boato dá a volta!'
        : `Reduz o alcance para ${q.melhorMaiorGrau.alcancadosSemEla} pessoas.`;
      dom.btnTestarMg.onclick = () => {
        estado.bloqueados.clear();
        estado.bloqueados.add(q.melhorMaiorGrau.pessoa);
        atualizarSimulacaoCompleta({ animarOndas: false, abrirAbaQuarentena: true });
      };
    }

    // Card Direito: Ótimo da Força Bruta
    if (q.melhorForcaBruta) {
      const pFb = estado.mapaPessoas.get(q.melhorForcaBruta.pessoa);
      const pctFb = Math.round((q.melhorForcaBruta.protegidos / baseAlcancaveis) * 100);
      dom.fbNome.textContent = pFb ? `${pFb.nome} (${pFb.grupo})` : `#${q.melhorForcaBruta.pessoa}`;
      dom.fbMeta.textContent = `Grau ${q.melhorForcaBruta.grau} · ${q.melhorForcaBruta.articulacao ? 'Ponto de Articulação' : 'Candidato Ótimo'}`;
      dom.fbSalvos.textContent = `${q.melhorForcaBruta.protegidos} protegidos (${pctFb}%)`;
      dom.fbDesc.textContent = q.melhorForcaBruta.articulacao
        ? 'Corta a ponte intergrupos identificada pelo Algoritmo de Tarjan!'
        : `Melhor corte global encontrado pela Força Bruta.`;
      dom.btnAplicarFb.onclick = () => {
        estado.bloqueados.clear();
        estado.bloqueados.add(q.melhorForcaBruta.pessoa);
        atualizarSimulacaoCompleta({ animarOndas: false, abrirAbaQuarentena: true });
      };
    }

    // Tempo de execução medido no Java
    dom.badgeTempoFb.textContent = `Java: ${(q.tempoMs || 0).toFixed(2)} ms`;

    // Lista de Ranking (Top 5 + Maior Grau se estiver fora do Top 5)
    dom.listaRankingFb.innerHTML = '';
    const ranking = q.ranking || [];
    const topItens = ranking.slice(0, 5);
    if (q.melhorMaiorGrau && !topItens.some(c => c.pessoa === q.melhorMaiorGrau.pessoa)) {
      topItens.push(q.melhorMaiorGrau);
    }

    const maxProt = Math.max(1, ranking.length > 0 ? ranking[0].protegidos : 1);

    topItens.forEach((cand) => {
      const posReal = ranking.findIndex(r => r.pessoa === cand.pessoa) + 1;
      const p = estado.mapaPessoas.get(cand.pessoa);
      const pctBarra = Math.max(4, Math.round((cand.protegidos / maxProt) * 100));
      const jaBloq = estado.bloqueados.has(cand.pessoa);

      const item = document.createElement('div');
      item.className = 'rank-item';
      item.innerHTML = `
        <span class="rank-pos">#${posReal}</span>
        <div class="rank-info">
          <span class="rank-name">${p ? p.nome : '#' + cand.pessoa} <small style="color:#64748b;">(${p ? p.grupo : ''})</small></span>
          <span class="rank-sub">Grau ${cand.grau} ${cand.articulacao ? '· <strong style="color:#b45309;">★ Ponte (Tarjan)</strong>' : '· Sem corte'}</span>
        </div>
        <div class="rank-bar-wrap">
          <div class="rank-bar-track">
            <div class="rank-bar-fill" style="width:${pctBarra}%;background:${cand.protegidos > 0 ? '#16a34a' : '#ef4444'};"></div>
          </div>
          <span class="rank-bar-label" style="color:${cand.protegidos > 0 ? '#15803d' : '#dc2626'};">${cand.protegidos} salvos</span>
        </div>
      `;

      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `btn-rank-block ${jaBloq ? 'is-blocked' : ''}`;
      btn.textContent = jaBloq ? 'Bloqueado' : 'Bloquear';
      btn.addEventListener('click', () => alternarBloqueioPessoa(cand.pessoa));
      item.appendChild(btn);

      item.addEventListener('mouseenter', ev => destacarVizinhancaNo(cand.pessoa, ev));
      item.addEventListener('mouseleave', () => limparDestaqueHover());
      dom.listaRankingFb.appendChild(item);
    });

    // Chips de Pontos de Articulação (Tarjan)
    dom.listaArticulacoes.innerHTML = '';
    const arts = q.articulacoes || [];
    dom.countTarjan.textContent = String(arts.length);

    if (arts.length === 0) {
      dom.listaArticulacoes.innerHTML = '<span class="card-subtext">Nenhum ponto de articulação restante.</span>';
    } else {
      arts.forEach(idArt => {
        const p = estado.mapaPessoas.get(idArt);
        const chip = document.createElement('span');
        chip.className = 'person-chip chip-bridge';
        chip.textContent = p ? `★ ${p.nome} (${p.grupo} · g=${p.grau})` : `#${idArt}`;
        chip.title = 'Clique para bloquear esta ponte';
        chip.addEventListener('click', () => alternarBloqueioPessoa(idArt));
        chip.addEventListener('mouseenter', ev => destacarVizinhancaNo(idArt, ev));
        chip.addEventListener('mouseleave', () => limparDestaqueHover());
        dom.listaArticulacoes.appendChild(chip);
      });
    }
  }

  function nomeCurto(id) {
    const p = estado.mapaPessoas.get(id);
    return p ? p.nome : `#${id}`;
  }

  function atualizarBannerStatus() {
    const pOrigem = estado.mapaPessoas.get(estado.origem);
    const nomeOrig = pOrigem ? pOrigem.nome : `#${estado.origem}`;
    const total = estado.rede.pessoas.length;
    const alc = (estado.bfs.alcancados || []).length;

    if (estado.bloqueados.size > 0) {
      const nomesBloq = Array.from(estado.bloqueados).map(nomeCurto).join(', ');
      const salvos = Math.max(0, estado.bfsSemBloqueioTotal - alc - estado.bloqueados.size);
      dom.textoStatus.innerHTML = `Origem: <strong>${nomeOrig}</strong> · Quarentena ativa em <strong>${nomesBloq}</strong> → Alcance caiu para <strong>${alc}/${total}</strong> (<strong>${salvos} pessoas salvas!</strong>)`;
    } else if (estado.ondaVisivelMax < Infinity) {
      dom.textoStatus.innerHTML = `Simulando Busca em Largura (BFS) a partir de <strong>${nomeOrig}</strong>: exibindo até a <strong>Onda ${estado.ondaVisivelMax}</strong>...`;
    } else {
      dom.textoStatus.innerHTML = `Origem: <strong>${nomeOrig}</strong> · Boato atinge <strong>${alc} de ${total} pessoas</strong> em <strong>${estado.bfs.rodadas} ondas</strong>. Clique em <strong>🛡️ Comparar Quarentena</strong>!`;
    }
  }

  // =========================================================================
  // 6. ANIMAÇÃO EM ONDAS E PASSO A PASSO DA FILA FIFO
  // =========================================================================
  function pararAnimacao() {
    if (estado.timerAnimacao) {
      clearInterval(estado.timerAnimacao);
      estado.timerAnimacao = null;
    }
  }

  function iniciarAnimacaoOndas() {
    pararAnimacao();
    alternarAba('bfs');
    estado.ondaVisivelMax = 0;
    estado.etapaPassoAPasso = -1;
    renderizarTudo();

    const maxOnda = estado.bfs ? estado.bfs.rodadas : 0;
    estado.timerAnimacao = setInterval(() => {
      if (estado.ondaVisivelMax < maxOnda) {
        estado.ondaVisivelMax++;
        renderizarTudo();
      } else {
        pararAnimacao();
        estado.ondaVisivelMax = Infinity;
        renderizarTudo();
      }
    }, 520);
  }

  function avancarPassoBfs() {
    pararAnimacao();
    alternarAba('bfs');
    if (!estado.bfs || !estado.bfs.passos) return;
    const passos = estado.bfs.passos;
    if (passos.length === 0) return;

    estado.etapaPassoAPasso = (estado.etapaPassoAPasso + 1) % passos.length;
    const passoAtual = passos[estado.etapaPassoAPasso];
    const dVertice = estado.bfs.dist[passoAtual.vertice];
    estado.ondaVisivelMax = Math.max(0, dVertice + (passoAtual.novos.length > 0 ? 1 : 0));
    renderizarTudo();
  }

  // =========================================================================
  // 7. AÇÕES DO USUÁRIO E ATALHOS DE DEMONSTRAÇÃO EM SALA DE AULA
  // =========================================================================
  function selecionarNovaOrigem(idPessoa) {
    if (estado.bloqueados.has(idPessoa)) {
      estado.bloqueados.delete(idPessoa);
    }
    estado.origem = idPessoa;
    dom.selOrigem.value = String(idPessoa);
    atualizarSimulacaoCompleta({ animarOndas: false });
  }

  function alternarBloqueioPessoa(idPessoa) {
    if (idPessoa === estado.origem) return;
    if (estado.bloqueados.has(idPessoa)) {
      estado.bloqueados.delete(idPessoa);
    } else {
      estado.bloqueados.add(idPessoa);
    }
    atualizarSimulacaoCompleta({ animarOndas: false });
  }

  function alternarAba(qual) {
    estado.abaAtiva = qual;
    const ehBfs = qual === 'bfs';
    dom.tabBtnBfs.classList.toggle('active', ehBfs);
    dom.tabBtnQuarentena.classList.toggle('active', !ehBfs);
    dom.tabPaneBfs.classList.toggle('active', ehBfs);
    dom.tabPaneQuarentena.classList.toggle('active', !ehBfs);
  }

  async function aplicarCenario(valor) {
    pararAnimacao();
    if (valor === 'sintetica') {
      const dados = await apiGet('/api/rede/aleatoria?n=60');
      estado.bloqueados.clear();
      estado.origem = 0;
      estado.mostrarCalloutsQuarentena = false;
      registrarRede(dados);
      alternarAba('bfs');
      await atualizarSimulacaoCompleta({ animarOndas: false });
      return;
    }

    // Garante que estamos na rede original de 28 pessoas
    if (!estado.rede || estado.rede.tipo !== 'original') {
      const dadosOrig = await apiGet('/api/rede/original');
      registrarRede(dadosOrig);
    }

    estado.origem = 0;
    dom.selOrigem.value = '0';
    estado.bloqueados.clear();

    if (valor === 'marina') {
      estado.bloqueados.add(12); // Marina (id 12, Grau 7)
      estado.mostrarCalloutsQuarentena = true;
      await atualizarSimulacaoCompleta({ animarOndas: false, abrirAbaQuarentena: true });
    } else if (valor === 'diego') {
      estado.bloqueados.add(3); // Diego (id 3, Ponte Ótima)
      estado.mostrarCalloutsQuarentena = true;
      await atualizarSimulacaoCompleta({ animarOndas: false, abrirAbaQuarentena: true });
    } else {
      estado.mostrarCalloutsQuarentena = false;
      alternarAba('bfs');
      await atualizarSimulacaoCompleta({ animarOndas: false });
    }
  }

  async function executarBenchmarkEscala() {
    dom.boxBenchmark.classList.remove('hidden');
    dom.benchStatus.textContent = 'Executando no Java 21...';
    dom.tbodyBenchmark.innerHTML = '<tr><td colspan="4">Medindo N = 100 a 2.000 vértices...</td></tr>';

    try {
      const res = await apiGet('/api/desempenho');
      dom.tbodyBenchmark.innerHTML = '';
      (res.medicoes || []).forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><strong>${m.n}</strong></td>
          <td>${m.arestas}</td>
          <td>${m.candidatos}</td>
          <td><strong style="color:#16a34a;">${m.tempoMs.toFixed(2)} ms</strong></td>
        `;
        dom.tbodyBenchmark.appendChild(tr);
      });
      dom.benchStatus.textContent = 'Concluído (< 0,3s em N=2000)';
    } catch (err) {
      dom.benchStatus.textContent = 'Erro ao medir';
    }
  }

  // =========================================================================
  // 8. INICIALIZAÇÃO DE EVENTOS
  // =========================================================================
  function configurarEventos() {
    dom.selOrigem.addEventListener('change', () => {
      selecionarNovaOrigem(Number(dom.selOrigem.value));
    });

    dom.btnPropagar.addEventListener('click', () => {
      iniciarAnimacaoOndas();
    });

    dom.btnPasso.addEventListener('click', () => {
      avancarPassoBfs();
    });

    dom.btnLimpar.addEventListener('click', () => {
      estado.bloqueados.clear();
      estado.mostrarCalloutsQuarentena = false;
      dom.selCenario.value = estado.rede && estado.rede.tipo === 'aleatoria' ? 'sintetica' : 'original';
      alternarAba('bfs');
      atualizarSimulacaoCompleta({ animarOndas: false });
    });

    dom.btnQuarentena.addEventListener('click', () => {
      estado.mostrarCalloutsQuarentena = true;
      alternarAba('quarentena');
      renderizarTudo();
    });

    dom.btnToggleTarjan.addEventListener('click', () => {
      estado.destacarTarjan = !estado.destacarTarjan;
      dom.btnToggleTarjan.classList.toggle('active', estado.destacarTarjan);
      renderizarNosHtml();
    });

    dom.selCenario.addEventListener('change', () => {
      aplicarCenario(dom.selCenario.value);
    });

    dom.tabBtnBfs.addEventListener('click', () => alternarAba('bfs'));
    dom.tabBtnQuarentena.addEventListener('click', () => {
      estado.mostrarCalloutsQuarentena = true;
      alternarAba('quarentena');
      renderizarNosHtml();
    });

    dom.btnBenchmark.addEventListener('click', () => {
      executarBenchmarkEscala();
    });

    let resizeTimeout = null;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => renderizarTudo(), 100);
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    configurarEventos();
    carregarRedeInicial();
  });
})();
