package br.maua.fakenews.algoritmos;

import br.maua.fakenews.algoritmos.ResultadoBFS.PassoBFS;
import br.maua.fakenews.modelo.Grafo;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Deque;
import java.util.List;
import java.util.Set;

/**
 * Busca em largura (aula T25). Complexidade O(V + E) com lista de adjacência.
 * Pessoas em "quarentena" (bloqueadas) são tratadas como removidas do grafo.
 */
public final class BuscaEmLargura {
    private BuscaEmLargura() {
    }

    public static ResultadoBFS executar(Grafo g, int origem, Set<Integer> bloqueados) {
        int n = g.numeroDeVertices();
        g.pessoa(origem); // valida
        int[] dist = new int[n];
        int[] anterior = new int[n];
        Arrays.fill(dist, -1);
        Arrays.fill(anterior, -1);
        List<PassoBFS> passos = new ArrayList<>();
        if (bloqueados.contains(origem)) return new ResultadoBFS(origem, dist, anterior, passos);

        Deque<Integer> fila = new ArrayDeque<>();
        dist[origem] = 0;
        fila.add(origem);
        while (!fila.isEmpty()) {
            List<Integer> filaAntes = List.copyOf(fila);
            int u = fila.remove();
            List<Integer> novos = new ArrayList<>();
            for (int v : g.vizinhos(u)) {
                if (dist[v] == -1 && !bloqueados.contains(v)) {
                    dist[v] = dist[u] + 1;
                    anterior[v] = u;
                    fila.add(v);
                    novos.add(v);
                }
            }
            passos.add(new PassoBFS(filaAntes, u, novos));
        }
        return new ResultadoBFS(origem, dist, anterior, passos);
    }

    /** Versão rápida (só conta alcançados), sem registrar passos; usada pela força bruta. */
    public static int contarAlcancados(Grafo g, int origem, Set<Integer> bloqueados) {
        if (bloqueados.contains(origem)) return 0;
        boolean[] visto = new boolean[g.numeroDeVertices()];
        Deque<Integer> fila = new ArrayDeque<>();
        visto[origem] = true;
        fila.add(origem);
        int total = 1;
        while (!fila.isEmpty()) {
            int u = fila.remove();
            for (int v : g.vizinhos(u)) {
                if (!visto[v] && !bloqueados.contains(v)) {
                    visto[v] = true;
                    total++;
                    fila.add(v);
                }
            }
        }
        return total;
    }
}
