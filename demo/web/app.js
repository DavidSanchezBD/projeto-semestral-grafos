/**
 * CASO FAKE NEWS — LÓGICA DE APRESENTAÇÃO E CONTROLES (FRONT-END)
 * ECM306 - Tópicos Avançados de Estrutura de Dados
 * Grupo: David Sanchez Daniel & Kauã Bueno Ortega
 * 
 * Filosofia: "Java pensa, o navegador desenha".
 * Toda a busca em largura, cálculo de articulações e força bruta
 * são executados no back-end Java via ServidorWeb (HttpServer nativo).
 */

(function () {
  'use strict';

  // Estado da aplicação
  let rede = null;
  let pacienteZero = 0;
  let bloqueados = new Set();
  let modoQuarentena = false;
  let resultadoBFS = null;
  let passoAtualIndex = 0;
  let animando = false;
  let posicoesNos = new Map(); // id -> {x, y, angulo}

  // Elementos DOM
  const quadro = document.getElementById('quadro');
  const fiosSvg = document.getElementById('fios-svg');
  const nosContainer = document.getElementById('nos-container');
  const selPaciente = document.getElementById('sel-paciente');
  const btnPropagar = document.getElementById('btn-propagar');
  const btnPasso = document.getElementById('btn-passo');
  const btnQuarentena = document.getElementById('btn-quarentena');
  const btnLimpar = document.getElementById('btn-limpar');
  const btnModoBloqueio = document.getElementById('btn-modo-bloqueio');
  const btnRedeAleatoria = document.getElementById('btn-rede-aleatoria');
  const btnRedeOriginal = document.getElementById('btn-rede-original');

  const carimboStatus = document.getElementById('carimbo-status');
  const metAlcancados = document.getElementById('met-alcancados');
  const metRodadas = document.getElementById('met-rodadas');
  const metBloqueados = document.getElementById('met-bloqueados');
  const metProtegidos = document.getElementById('met-protegidos');
  const corpoTabelaBfs = document.getElementById('corpo-tabela-bfs');
  const alertaHeuristica = document.getElementById('alerta-heuristica');
  const listaRanking = document.getElementById('lista-ranking');
  const tagsArticulacoes = document.getElementById('tags-articulacoes');

  // Inicialização
  window.addEventListener('DOMContentLoaded', () => {
    carregarRede();
    configurarEventos();
    window.addEventListener('resize', recalcularLayout);
  });

  // ---------- Comunicação com o Back-end Java ----------

  async function carregarRede() {
    try {
      const resp = await fetch('/api/rede');
      rede = await resp.json();
      bloqueados.clear();
      pacienteZero = 0;
      atualizarOpcoesPaciente();
      posicionarNos();
      desenharFios();
      desenharNos();
      atualizarTagsArticulacoes();
      atualizarMetricasBasicas();
      setCarimboStatus('AGUARDANDO', 'carimbo-aguardando');
    } catch (e) {
      console.error('Falha ao carregar rede:', e);
      alert('Não foi possível conectar ao servidor Java. Verifique se o jar está em execução.');
    }
  }

  async function carregarRedeAleatoria(n = 60) {
    try {
      const resp = await fetch(`/api/rede/aleatoria?n=${n}`, { method: 'POST' });
      rede = await resp.json();
      bloqueados.clear();
      pacienteZero = 0;
      atualizarOpcoesPaciente();
      posicionarNos();
      desenharFios();
      desenharNos();
      atualizarTagsArticulacoes();
      atualizarMetricasBasicas();
      setCarimboStatus('REDE SINTÉTICA', 'carimbo-aguardando');
    } catch (e) {
      console.error('Falha ao carregar rede sintética:', e);
    }
  }

  async function carregarRedeOriginal() {
    try {
      const resp = await fetch('/api/rede/original', { method: 'POST' });
      rede = await resp.json();
      bloqueados.clear();
      pacienteZero = 0;
      atualizarOpcoesPaciente();
      posicionarNos();
      desenharFios();
      desenharNos();
      atualizarTagsArticulacoes();
      atualizarMetricasBasicas();
      setCarimboStatus('REDE ORIGINAL', 'carimbo-aguardando');
    } catch (e) {
      console.error('Falha ao restaurar rede original:', e);
    }
  }

  async function obterBFS() {
    const params = new URLSearchParams({
      origem: pacienteZero,
      bloqueados: Array.from(bloqueados).join(',')
    });
    const resp = await fetch(`/api/bfs?${params}`);
    return await resp.json();
  }

  async function obterQuarentena() {
    const params = new URLSearchParams({
      origem: pacienteZero,
      bloqueados: Array.from(bloqueados).join(',')
    });
    const resp = await fetch(`/api/quarentena?${params}`);
    return await resp.json();
  }

  // ---------- Layout e Desenho do Quadro ----------

  function recalcularLayout() {
    if (!rede) return;
    posicionarNos();
    desenharFios();
    atualizarPosicoesNosDOM();
  }

  function posicionarNos() {
    posicoesNos.clear();
    const w = quadro.clientWidth;
    const h = quadro.clientHeight;
    const margemX = 60;
    const margemY = 60;
    const utilW = w - margemX * 2;
    const utilH = h - margemY * 2;

    if (rede.tipo === 'original' && rede.pessoas.length <= 30) {
      // Layout temático em 5 agrupamentos para a rede CSV (quadro investigativo)
      const centrosGrupos = {
        'Família':    { cx: margemX + utilW * 0.18, cy: margemY + utilH * 0.22 },
        'Trabalho':   { cx: margemX + utilW * 0.50, cy: margemY + utilH * 0.28 },
        'Faculdade':  { cx: margemX + utilW * 0.82, cy: margemY + utilH * 0.35 },
        'Academia':   { cx: margemX + utilW * 0.72, cy: margemY + utilH * 0.78 },
        'Condomínio': { cx: margemX + utilW * 0.24, cy: margemY + utilH * 0.78 }
      };

      // Agrupa pessoas
      const porGrupo = {};
      rede.pessoas.forEach(p => {
        if (!porGrupo[p.grupo]) porGrupo[p.grupo] = [];
        porGrupo[p.grupo].push(p);
      });

      for (const [grupo, lista] of Object.entries(porGrupo)) {
        const centro = centrosGrupos[grupo] || { cx: w / 2, cy: h / 2 };
        const total = lista.length;
        const raio = Math.min(utilW, utilH) * (total > 5 ? 0.14 : 0.10);
        lista.forEach((p, idx) => {
          const ang = (2 * Math.PI * idx) / total;
          const x = centro.cx + raio * Math.cos(ang);
          const y = centro.cy + raio * Math.sin(ang);
          const rot = ((p.id * 7) % 11) - 5; // rotação suave entre -5 e +5 graus
          posicoesNos.set(p.id, { x, y, angulo: rot });
        });
      }
    } else {
      // Layout em anel concêntrico/distribuído para redes sintéticas
      const total = rede.pessoas.length;
      const cx = w / 2;
      const cy = h / 2;
      const raio = Math.min(utilW, utilH) * 0.42;
      rede.pessoas.forEach((p, idx) => {
        const ang = (2 * Math.PI * idx) / total;
        const x = cx + raio * Math.cos(ang);
        const y = cy + raio * Math.sin(ang);
        const rot = ((p.id * 5) % 9) - 4;
        posicoesNos.set(p.id, { x, y, angulo: rot });
      });
    }
  }

  function desenharFios() {
    fiosSvg.innerHTML = '';
    rede.contatos.forEach(([a, b]) => {
      const posA = posicoesNos.get(a);
      const posB = posicoesNos.get(b);
      if (!posA || !posB) return;

      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      const idFio = chaveFio(a, b);
      path.setAttribute('id', idFio);
      path.setAttribute('class', 'fio-rede');

      // Leve arqueamento nos fios estilo varal/teia
      const dx = posB.x - posA.x;
      const dy = posB.y - posA.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const curva = Math.min(25, dist * 0.08);
      const mx = (posA.x + posB.x) / 2 - dy * (curva / dist);
      const my = (posA.y + posB.y) / 2 + dx * (curva / dist);

      path.setAttribute('d', `M ${posA.x} ${posA.y} Q ${mx} ${my} ${posB.x} ${posB.y}`);
      fiosSvg.appendChild(path);
    });
  }

  function desenharNos() {
    nosContainer.innerHTML = '';
    const artSet = new Set(rede.articulacoes || []);

    rede.pessoas.forEach(p => {
      const pos = posicoesNos.get(p.id);
      if (!pos) return;

      const card = document.createElement('div');
      card.className = 'polaroid';
      card.id = `no-${p.id}`;
      card.style.left = `${pos.x}px`;
      card.style.top = `${pos.y}px`;
      card.style.transform = `translate(-50%, -50%) rotate(${pos.angulo}deg)`;

      if (p.id === pacienteZero) card.classList.add('paciente-zero');
      if (bloqueados.has(p.id)) card.classList.add('bloqueado');
      if (artSet.has(p.id)) card.classList.add('articulacao');

      // Alfinete com cor do grupo
      const pinClass = classeAlfinete(p.grupo);

      // Iniciais
      const iniciais = extrairIniciais(p.nome);

      card.innerHTML = `
        <div class="alfinete ${pinClass}"></div>
        <div class="polaroid-foto">
          <span class="polaroid-iniciais">${iniciais}</span>
          <span class="grau-badge" title="Grau de conexões">${p.grau}</span>
          <div class="carimbo-slot"></div>
        </div>
        <div class="polaroid-nome" title="${p.nome}">${p.nome}</div>
        <div class="polaroid-grupo">${p.grupo}</div>
      `;

      card.addEventListener('click', (ev) => manipularCliqueNo(p.id, ev));
      nosContainer.appendChild(card);
    });

    atualizarCarimbosNos();
  }

  function atualizarPosicoesNosDOM() {
    rede.pessoas.forEach(p => {
      const pos = posicoesNos.get(p.id);
      const el = document.getElementById(`no-${p.id}`);
      if (pos && el) {
        el.style.left = `${pos.x}px`;
        el.style.top = `${pos.y}px`;
      }
    });
  }

  function extrairIniciais(nome) {
    if (!nome) return '??';
    const partes = nome.trim().split(/\s+/);
    if (partes.length === 1) return partes[0].substring(0, 2).toUpperCase();
    return (partes[0][0] + partes[partes.length - 1][0]).toUpperCase();
  }

  function classeAlfinete(grupo) {
    const g = (grupo || '').toLowerCase();
    if (g.includes('fam')) return 'pin-familia';
    if (g.includes('trab')) return 'pin-trabalho';
    if (g.includes('fac')) return 'pin-faculdade';
    if (g.includes('acad')) return 'pin-academia';
    if (g.includes('cond')) return 'pin-condominio';
    return 'pin-familia';
  }

  function chaveFio(a, b) {
    const u = Math.min(a, b);
    const v = Math.max(a, b);
    return `fio-${u}-${v}`;
  }

  // ---------- Eventos e Interações ----------

  function configurarEventos() {
    selPaciente.addEventListener('change', () => {
      definirPacienteZero(parseInt(selPaciente.value, 10));
    });

    btnPropagar.addEventListener('click', executarPropagacaoAutomatica);
    btnPasso.addEventListener('click', executarProximoPasso);
    btnQuarentena.addEventListener('click', executarAnaliseQuarentena);
    btnLimpar.addEventListener('click', resetarPropagacao);

    btnModoBloqueio.addEventListener('click', () => {
      modoQuarentena = !modoQuarentena;
      btnModoBloqueio.classList.toggle('ativo', modoQuarentena);
      btnModoBloqueio.textContent = modoQuarentena ? 'Modo Quarentena: ATIVO' : 'Modo Quarentena: OFF';
    });

    btnRedeAleatoria.addEventListener('click', () => carregarRedeAleatoria(60));
    btnRedeOriginal.addEventListener('click', carregarRedeOriginal);
  }

  function definirPacienteZero(id) {
    if (bloqueados.has(id)) {
      alert('Esta pessoa está em quarentena (bloqueada). Desbloqueie-a antes de torná-la Paciente Zero.');
      selPaciente.value = pacienteZero;
      return;
    }
    pacienteZero = id;
    selPaciente.value = id;
    resetarPropagacao();
    desenharNos();
  }

  function manipularCliqueNo(id, ev) {
    if (modoQuarentena || ev.shiftKey) {
      // Alterna quarentena
      if (id === pacienteZero) {
        alert('O Paciente Zero não pode ser colocado em quarentena simultaneamente.');
        return;
      }
      if (bloqueados.has(id)) {
        bloqueados.delete(id);
      } else {
        bloqueados.add(id);
      }
      resetarPropagacao();
      desenharNos();
      atualizarMetricasBasicas();
      return;
    }

    // Clique normal define o Paciente Zero
    definirPacienteZero(id);
  }

  function atualizarOpcoesPaciente() {
    selPaciente.innerHTML = '';
    rede.pessoas.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;
      opt.textContent = `${p.nome} (${p.grupo}) [Grau ${p.grau}]`;
      if (p.id === pacienteZero) opt.selected = true;
      selPaciente.appendChild(opt);
    });
  }

  // ---------- Execução e Animação da BFS ----------

  async function executarPropagacaoAutomatica() {
    if (animando) return;
    animando = true;
    resetarPropagacaoVisual();
    setCarimboStatus('PROPAGANDO...', 'carimbo-propagando');

    resultadoBFS = await obterBFS();
    passoAtualIndex = 0;

    const niveis = resultadoBFS.niveis;
    for (let onda = 0; onda < niveis.length; onda++) {
      const pessoasDaOnda = niveis[onda];
      pessoasDaOnda.forEach(v => {
        carimbarNo(v, onda === 0 ? 'ZERO' : `ONDA ${onda}`, onda === 0 ? 'carimbo-zero' : 'carimbo-recebeu');
        // Acende fios de conexão com o nível anterior
        if (resultadoBFS.anterior[v] !== -1) {
          ativarFio(v, resultadoBFS.anterior[v]);
        }
      });

      // Atualiza métricas em tempo real
      const atingidosAteAgora = niveis.slice(0, onda + 1).reduce((acc, l) => acc + l.length, 0);
      metAlcancados.textContent = atingidosAteAgora;
      metRodadas.textContent = onda;

      await dormir(550);
    }

    // Preenche a tabela completa de passos da fila
    preencherTabelaPassosBFS(resultadoBFS.passos);
    finalizarPropagacao();
    animando = false;
  }

  async function executarProximoPasso() {
    if (!resultadoBFS) {
      resultadoBFS = await obterBFS();
      passoAtualIndex = 0;
      resetarPropagacaoVisual();
      setCarimboStatus('EM ANDAMENTO', 'carimbo-propagando');
    }

    if (passoAtualIndex >= resultadoBFS.passos.length) {
      finalizarPropagacao();
      return;
    }

    const passo = resultadoBFS.passos[passoAtualIndex];
    const u = passo.vertice;
    const distU = resultadoBFS.dist[u];

    // Carimba o vértice retirado
    carimbarNo(u, distU === 0 ? 'ZERO' : `ONDA ${distU}`, distU === 0 ? 'carimbo-zero' : 'carimbo-recebeu');

    // Ilumina fios para os novos descobertos
    passo.novos.forEach(v => {
      ativarFio(u, v);
    });

    // Adiciona linha na tabela
    adicionarLinhaTabelaBFS(passoAtualIndex + 1, passo);
    passoAtualIndex++;

    metAlcancados.textContent = contarCartoesCarimbados();
    metRodadas.textContent = distU;

    if (passoAtualIndex >= resultadoBFS.passos.length) {
      finalizarPropagacao();
    }
  }

  function finalizarPropagacao() {
    const total = rede.pessoas.length;
    const atingidos = resultadoBFS.alcancados.length;
    const isolados = total - atingidos - bloqueados.size;

    metAlcancados.textContent = atingidos;
    metRodadas.textContent = resultadoBFS.rodadas;
    metProtegidos.textContent = isolados > 0 ? isolados : 0;

    if (isolados > 0) {
      setCarimboStatus('CONTIDO PARCIAL', 'carimbo-contido');
    } else {
      setCarimboStatus('SURTO COMPLETO', 'carimbo-propagando');
    }
  }

  function carimbarNo(id, texto, classe) {
    const el = document.getElementById(`no-${id}`);
    if (!el) return;
    el.classList.add('alcancado');
    const slot = el.querySelector('.carimbo-slot');
    if (slot) {
      slot.innerHTML = `<div class="carimbo-foto ${classe}">${texto}</div>`;
    }
  }

  function ativarFio(a, b) {
    const id = chaveFio(a, b);
    const el = document.getElementById(id);
    if (el) el.classList.add('fio-ativo');
  }

  function contarCartoesCarimbados() {
    return document.querySelectorAll('.polaroid.alcancado').length;
  }

  function atualizarCarimbosNos() {
    bloqueados.forEach(id => {
      const el = document.getElementById(`no-${id}`);
      if (el) {
        el.classList.add('bloqueado');
        const slot = el.querySelector('.carimbo-slot');
        if (slot) {
          slot.innerHTML = `<div class="carimbo-foto carimbo-bloqueado-foto">BLOQUEADO</div>`;
        }
      }
    });
  }

  function resetarPropagacaoVisual() {
    document.querySelectorAll('.polaroid').forEach(el => {
      el.classList.remove('alcancado');
      const slot = el.querySelector('.carimbo-slot');
      if (slot) slot.innerHTML = '';
    });
    document.querySelectorAll('.fio-rede').forEach(el => {
      el.classList.remove('fio-ativo');
    });
    atualizarCarimbosNos();
    corpoTabelaBfs.innerHTML = '';
  }

  function resetarPropagacao() {
    resultadoBFS = null;
    passoAtualIndex = 0;
    resetarPropagacaoVisual();
    atualizarMetricasBasicas();
    setCarimboStatus('AGUARDANDO', 'carimbo-aguardando');
  }

  function atualizarMetricasBasicas() {
    metAlcancados.textContent = '0';
    metRodadas.textContent = '0';
    metBloqueados.textContent = bloqueados.size;
    metProtegidos.textContent = '0';
  }

  function setCarimboStatus(texto, classe) {
    carimboStatus.textContent = texto;
    carimboStatus.className = `carimbo carimbo-caso ${classe}`;
  }

  // ---------- Rastreamento da Tabela BFS (Aula T25) ----------

  function preencherTabelaPassosBFS(passos) {
    corpoTabelaBfs.innerHTML = '';
    passos.forEach((p, idx) => adicionarLinhaTabelaBFS(idx + 1, p));
  }

  function adicionarLinhaTabelaBFS(etapa, p) {
    const tr = document.createElement('tr');
    tr.className = 'linha-ativa';

    const filaTxt = p.filaAntes.length === 0 ? '[]' : `[${p.filaAntes.map(nomePessoa).join(', ')}]`;
    const vertTxt = nomePessoa(p.vertice);
    const novosTxt = p.novos.length === 0 ? 'nenhum' : p.novos.map(nomePessoa).join(', ');

    tr.innerHTML = `
      <td>${etapa}</td>
      <td>${filaTxt}</td>
      <td><strong>${vertTxt}</strong></td>
      <td>${novosTxt}</td>
    `;
    corpoTabelaBfs.appendChild(tr);
    tr.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function nomePessoa(id) {
    const p = rede.pessoas[id];
    return p ? p.nome : `P${id}`;
  }

  // ---------- Diagnóstico de Quarentena e Heurística ----------

  async function executarAnaliseQuarentena() {
    setCarimboStatus('ANALISANDO...', 'carimbo-propagando');
    const diag = await obterQuarentena();

    // Atualiza Alerta Didático (Força Bruta vs Maior Grau)
    const melhorFB = diag.melhorForcaBruta;
    const melhorMG = diag.melhorMaiorGrau;

    if (!melhorFB) {
      alertaHeuristica.className = 'alerta-comparacao';
      alertaHeuristica.innerHTML = 'Nenhum candidato elegível para bloqueio neste momento.';
      return;
    }

    const nomeFB = nomePessoa(melhorFB.pessoa);
    const nomeMG = nomePessoa(melhorMG.pessoa);

    if (diag.heuristicaAcertou) {
      alertaHeuristica.className = 'alerta-comparacao sucesso';
      alertaHeuristica.innerHTML = `
        <strong>HEURÍSTICA ACERTOU!</strong><br>
        O candidato com maior grau (<strong>${nomeMG}</strong>, grau ${melhorMG.grau}) coincide com o ótimo da Força Bruta, protegendo <strong>${melhorFB.protegidos}</strong> pessoas (${diag.tempoMs.toFixed(2)} ms).
      `;
    } else {
      alertaHeuristica.className = 'alerta-comparacao erro';
      alertaHeuristica.innerHTML = `
        <strong>ALERTA DIDÁTICO: A HEURÍSTICA ERROU!</strong><br>
        • <strong>Maior Grau (${nomeMG}, grau ${melhorMG.grau}):</strong> protegeu apenas <strong>${melhorMG.protegidos}</strong> pessoas.<br>
        • <strong>Ótimo da Força Bruta (${nomeFB}, grau ${melhorFB.grau}):</strong> protegeu <strong>${melhorFB.protegidos}</strong> pessoas!<br>
        <em>Motivo:</em> ${nomeFB} é uma "ponte" estratégica (ponto de articulação), enquanto ${nomeMG} possui conexões redundantes dentro do próprio grupo.
      `;
    }

    // Preenche lista de ranking
    listaRanking.innerHTML = '';
    diag.ranking.slice(0, 8).forEach((c, idx) => {
      const li = document.createElement('li');
      li.className = `item-ranking ${idx === 0 ? 'top1' : ''} ${c.pessoa === melhorMG.pessoa ? 'maior-grau' : ''}`;
      const nome = nomePessoa(c.pessoa);
      const artTxt = c.articulacao ? ' 🚩 (articulação)' : '';
      const mgTxt = c.pessoa === melhorMG.pessoa ? ' [maior grau]' : '';

      li.innerHTML = `
        <span>#${idx + 1} <strong>${nome}</strong>${artTxt}${mgTxt}</span>
        <span>Protege <strong>${c.protegidos}</strong> (grau ${c.grau})</span>
      `;
      li.title = `Clique para colocar ${nome} em quarentena`;
      li.addEventListener('click', () => {
        bloqueados.add(c.pessoa);
        resetarPropagacao();
        desenharNos();
        atualizarMetricasBasicas();
      });
      listaRanking.appendChild(li);
    });

    setCarimboStatus('AVALIADO', 'carimbo-contido');
  }

  function atualizarTagsArticulacoes() {
    tagsArticulacoes.innerHTML = '';
    if (!rede.articulacoes || rede.articulacoes.length === 0) {
      tagsArticulacoes.innerHTML = '<span class="desc-articulacoes">Nenhuma articulação crítica na rede.</span>';
      return;
    }
    rede.articulacoes.forEach(id => {
      const span = document.createElement('span');
      span.className = 'tag-articulacao';
      span.textContent = nomePessoa(id);
      span.title = 'Clique para colocar em quarentena';
      span.style.cursor = 'pointer';
      span.addEventListener('click', () => {
        bloqueados.add(id);
        resetarPropagacao();
        desenharNos();
        atualizarMetricasBasicas();
      });
      tagsArticulacoes.appendChild(span);
    });
  }

  function dormir(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

})();
