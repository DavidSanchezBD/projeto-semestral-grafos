package br.maua.fakenews.algoritmos;

import br.maua.fakenews.modelo.Grafo;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Escolha da melhor pessoa a bloquear (quarentena).
 * Força bruta exata: para cada candidato, remove-o e roda a BFS. Custo O(V * (V + E)).
 * Comparada com duas heurísticas: maior grau e pontos de articulação (aula T23).
 */
public final class Quarentena {
    private Quarentena() {
    }

    /**
     * @param pessoa            candidato
     * @param alcancadosSemEla  quantos receberiam a mensagem se ela fosse bloqueada
     * @param protegidos        quantos deixam de receber (sem contar a própria pessoa)
     */
    public record Candidato(int pessoa, int alcancadosSemEla, int protegidos, int grau, boolean articulacao) {
    }

    public record ResultadoQuarentena(
            int alcancadosAtuais,
            List<Candidato> ranking,
            Candidato melhorForcaBruta,
            Candidato melhorMaiorGrau,
            List<Integer> articulacoes,
            boolean heuristicaAcertou,
            double tempoMs) {
    }

    public static ResultadoQuarentena analisar(Grafo g, int origem, Set<Integer> bloqueados) {
        long t0 = System.nanoTime();
        int base = BuscaEmLargura.contarAlcancados(g, origem, bloqueados);
        List<Integer> arts = PontosDeArticulacao.encontrar(g, bloqueados);
        Set<Integer> artSet = new HashSet<>(arts);

        List<Candidato> ranking = new ArrayList<>();
        int[] distAtual = BuscaEmLargura.executar(g, origem, bloqueados).distancias();
        Set<Integer> teste = new HashSet<>(bloqueados);
        for (int v = 0; v < g.numeroDeVertices(); v++) {
            if (v == origem || bloqueados.contains(v)) continue;
            // só vale testar quem a mensagem alcança hoje
            if (distAtual[v] == -1) continue;
            teste.add(v);
            int sem = BuscaEmLargura.contarAlcancados(g, origem, teste);
            teste.remove(v);
            ranking.add(new Candidato(v, sem, base - sem - 1, g.grau(v), artSet.contains(v)));
        }
        ranking.sort(Comparator.comparingInt(Candidato::protegidos).reversed()
                .thenComparing(Comparator.comparingInt(Candidato::grau).reversed())
                .thenComparingInt(Candidato::pessoa));

        Candidato melhor = ranking.isEmpty() ? null : ranking.get(0);
        Candidato maiorGrau = ranking.stream()
                .max(Comparator.comparingInt(Candidato::grau).thenComparing(c -> -c.pessoa()))
                .orElse(null);
        boolean acertou = melhor != null && maiorGrau != null
                && maiorGrau.protegidos() == melhor.protegidos();
        double ms = (System.nanoTime() - t0) / 1_000_000.0;
        return new ResultadoQuarentena(base, ranking, melhor, maiorGrau, arts, acertou, ms);
    }

}
