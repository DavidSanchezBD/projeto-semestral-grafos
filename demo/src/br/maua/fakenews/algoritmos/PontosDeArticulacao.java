package br.maua.fakenews.algoritmos;

import br.maua.fakenews.modelo.Grafo;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

/**
 * Pontos de articulação (algoritmo de Tarjan, baseado em DFS), versão iterativa
 * para não estourar a pilha de chamadas em redes grandes. Complexidade O(V + E).
 * Um ponto de articulação é uma pessoa cuja remoção desconecta parte da rede.
 */
public final class PontosDeArticulacao {
    private PontosDeArticulacao() {
    }

    public static List<Integer> encontrar(Grafo g, Set<Integer> bloqueados) {
        int n = g.numeroDeVertices();
        int[] disc = new int[n];
        int[] low = new int[n];
        int[] pai = new int[n];
        int[] prox = new int[n]; // índice do próximo vizinho a examinar
        boolean[] art = new boolean[n];
        Arrays.fill(pai, -1);
        int tempo = 0;

        for (int raiz = 0; raiz < n; raiz++) {
            if (disc[raiz] != 0 || bloqueados.contains(raiz)) continue;
            int filhosDaRaiz = 0;
            int[] pilha = new int[n];
            int topo = 0;
            pilha[topo++] = raiz;
            disc[raiz] = low[raiz] = ++tempo;
            while (topo > 0) {
                int u = pilha[topo - 1];
                List<Integer> viz = g.vizinhos(u);
                if (prox[u] < viz.size()) {
                    int v = viz.get(prox[u]++);
                    if (bloqueados.contains(v)) continue;
                    if (disc[v] == 0) {
                        pai[v] = u;
                        if (u == raiz) filhosDaRaiz++;
                        disc[v] = low[v] = ++tempo;
                        pilha[topo++] = v;
                    } else if (v != pai[u]) {
                        low[u] = Math.min(low[u], disc[v]);
                    }
                } else {
                    topo--;
                    int p = pai[u];
                    if (p != -1) {
                        low[p] = Math.min(low[p], low[u]);
                        if (p != raiz && low[u] >= disc[p]) art[p] = true;
                    }
                }
            }
            if (filhosDaRaiz >= 2) art[raiz] = true;
        }
        List<Integer> r = new ArrayList<>();
        for (int v = 0; v < n; v++) if (art[v]) r.add(v);
        return r;
    }
}
