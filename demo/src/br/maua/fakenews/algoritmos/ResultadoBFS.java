package br.maua.fakenews.algoritmos;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Resultado de uma BFS: distâncias, predecessores e o rastreamento passo a passo. */
public final class ResultadoBFS {

    /** Um passo da BFS: fila antes, vértice retirado e vértices recém-descobertos. */
    public record PassoBFS(List<Integer> filaAntes, int vertice, List<Integer> novos) {
    }

    private final int origem;
    private final int[] dist;
    private final int[] anterior;
    private final List<PassoBFS> passos;

    ResultadoBFS(int origem, int[] dist, int[] anterior, List<PassoBFS> passos) {
        this.origem = origem;
        this.dist = dist;
        this.anterior = anterior;
        this.passos = passos;
    }

    public int origem() { return origem; }

    /** Distância em número de arestas; -1 se não alcançado. */
    public int distancia(int v) { return dist[v]; }

    public int[] distancias() { return dist.clone(); }

    public int[] anteriores() { return anterior.clone(); }

    public List<PassoBFS> passos() { return passos; }

    public boolean alcancou(int v) { return dist[v] != -1; }

    /** Pessoas alcançadas (inclui a origem). */
    public List<Integer> alcancados() {
        List<Integer> r = new ArrayList<>();
        for (int v = 0; v < dist.length; v++) if (dist[v] != -1) r.add(v);
        return r;
    }

    /** Pessoas não alcançadas (inclui bloqueadas, pois nunca são visitadas). */
    public List<Integer> naoAlcancados() {
        List<Integer> r = new ArrayList<>();
        for (int v = 0; v < dist.length; v++) if (dist[v] == -1) r.add(v);
        return r;
    }

    /** Pessoas agrupadas por "onda" (nível 0 = origem). */
    public List<List<Integer>> niveis() {
        int max = rodadasDeEncaminhamento();
        List<List<Integer>> r = new ArrayList<>();
        for (int i = 0; i <= max; i++) r.add(new ArrayList<>());
        if (dist[origem] == -1) return r;
        for (int v = 0; v < dist.length; v++) if (dist[v] != -1) r.get(dist[v]).add(v);
        return r;
    }

    /** Maior distância encontrada = quantidade de retransmissões até o último alcançado. */
    public int rodadasDeEncaminhamento() {
        int max = 0;
        for (int d : dist) max = Math.max(max, d);
        return max;
    }

    /** Reconstrói o caminho origem -> destino; lista vazia se inalcançável. */
    public List<Integer> caminhoAte(int destino) {
        List<Integer> rota = new ArrayList<>();
        if (dist[destino] == -1) return rota;
        for (int v = destino; v != -1; v = anterior[v]) rota.add(v);
        Collections.reverse(rota);
        return rota;
    }
}
