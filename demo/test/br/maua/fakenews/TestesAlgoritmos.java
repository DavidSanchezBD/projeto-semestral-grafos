package br.maua.fakenews;

import br.maua.fakenews.algoritmos.BuscaEmLargura;
import br.maua.fakenews.algoritmos.PontosDeArticulacao;
import br.maua.fakenews.algoritmos.Quarentena;
import br.maua.fakenews.algoritmos.Quarentena.ResultadoQuarentena;
import br.maua.fakenews.algoritmos.ResultadoBFS;
import br.maua.fakenews.dados.GeradorDeRede;
import br.maua.fakenews.dados.LeitorCSV;
import br.maua.fakenews.modelo.Grafo;
import br.maua.fakenews.web.Json;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Set;

/** Testes sem dependências externas: cada caso lança AssertionError se falhar. */
public final class TestesAlgoritmos {
    private static int total = 0;
    private static int falhas = 0;

    public static void main(String[] args) {
        executar("Caminho P5: BFS, articulações e quarentena", TestesAlgoritmos::caminhoP5);
        executar("Ciclo C6: sem articulações", TestesAlgoritmos::cicloC6);
        executar("Estrela: centro é a única articulação", TestesAlgoritmos::estrela);
        executar("Grafo desconexo e vértice isolado", TestesAlgoritmos::desconexo);
        executar("Exemplo da aula T25 (C, B1..B5, X)", TestesAlgoritmos::exemploAula);
        executar("Origem bloqueada não alcança ninguém", TestesAlgoritmos::origemBloqueada);
        executar("Contato repetido e laço são ignorados", TestesAlgoritmos::arestasInvalidas);
        executar("Pessoa inexistente lança exceção", TestesAlgoritmos::pessoaInexistente);
        executar("Rede do CSV: maior grau NÃO é a melhor escolha", TestesAlgoritmos::redeCsv);
        executar("Tarjan confere com força bruta em 200 grafos aleatórios", TestesAlgoritmos::propriedadeTarjan);
        executar("Rede grande não estoura a pilha (n=5000)", TestesAlgoritmos::redeGrande);
        executar("JSON: escape de aspas e acentos", TestesAlgoritmos::json);

        System.out.printf("%n%d testes, %d falha(s)%n", total, falhas);
        if (falhas > 0) System.exit(1);
    }

    // ---------- casos ----------

    private static void caminhoP5() {
        Grafo g = caminho(5);
        ResultadoBFS r = BuscaEmLargura.executar(g, 0, Set.of());
        for (int i = 0; i < 5; i++) igual(i, r.distancia(i), "dist " + i);
        igual(List.of(0, 1, 2, 3, 4), r.caminhoAte(4), "caminho");
        igual(4, r.rodadasDeEncaminhamento(), "rodadas");
        igual(List.of(1, 2, 3), PontosDeArticulacao.encontrar(g, Set.of()), "articulações");
        ResultadoQuarentena q = Quarentena.analisar(g, 0, Set.of());
        igual(5, q.alcancadosAtuais(), "alcançados");
        igual(1, q.melhorForcaBruta().pessoa(), "melhor é bloquear o 1");
        igual(3, q.melhorForcaBruta().protegidos(), "bloquear 1 protege 3");
    }

    private static void cicloC6() {
        Grafo g = vazio(6);
        for (int i = 0; i < 6; i++) g.adicionarContato(i, (i + 1) % 6);
        igual(List.of(), PontosDeArticulacao.encontrar(g, Set.of()), "sem articulações");
        ResultadoQuarentena q = Quarentena.analisar(g, 0, Set.of());
        igual(0, q.melhorForcaBruta().protegidos(), "ninguém é ponte num ciclo");
        igual(3, BuscaEmLargura.executar(g, 0, Set.of()).rodadasDeEncaminhamento(), "rodadas no C6");
    }

    private static void estrela() {
        Grafo g = vazio(6);
        for (int i = 1; i < 6; i++) g.adicionarContato(0, i);
        igual(List.of(0), PontosDeArticulacao.encontrar(g, Set.of()), "centro");
        ResultadoQuarentena q = Quarentena.analisar(g, 1, Set.of());
        igual(0, q.melhorForcaBruta().pessoa(), "bloquear o centro");
        igual(4, q.melhorForcaBruta().protegidos(), "protege os outros 4");
    }

    private static void desconexo() {
        Grafo g = vazio(5);
        g.adicionarContato(0, 1);
        g.adicionarContato(1, 2);
        g.adicionarContato(3, 4); // ilha; vértice 4 isolado do resto
        ResultadoBFS r = BuscaEmLargura.executar(g, 0, Set.of());
        igual(List.of(0, 1, 2), r.alcancados(), "alcançados");
        igual(List.of(3, 4), r.naoAlcancados(), "não alcançados");
        igual(-1, r.distancia(4), "dist inalcançável");
        igual(List.of(), r.caminhoAte(4), "caminho inexistente");
        Grafo h = vazio(1);
        igual(List.of(0), BuscaEmLargura.executar(h, 0, Set.of()).alcancados(), "grafo de 1 vértice");
    }

    private static void exemploAula() {
        // slide 13/15 da T25: C-B1, C-B2, B1-B3, B2-B4, B3-B5; X isolado
        // ids: C=0 B1=1 B2=2 B3=3 B4=4 B5=5 X=6
        Grafo g = vazio(7);
        g.adicionarContato(0, 1);
        g.adicionarContato(0, 2);
        g.adicionarContato(1, 3);
        g.adicionarContato(2, 4);
        g.adicionarContato(3, 5);
        ResultadoBFS r = BuscaEmLargura.executar(g, 0, Set.of());
        igual(List.of(List.of(0), List.of(1, 2), List.of(3, 4), List.of(5)), r.niveis(), "níveis");
        igual(List.of(0, 1, 3, 5), r.caminhoAte(5), "caminho C-B1-B3-B5");
        igual(3, r.distancia(5), "3 retransmissões");
        igual(List.of(6), r.naoAlcancados(), "X isolado");
        // rastreamento: etapa 1 fila [C], retira C, descobre B1 e B2
        igual(List.of(0), r.passos().get(0).filaAntes(), "fila etapa 1");
        igual(List.of(1, 2), r.passos().get(0).novos(), "novos etapa 1");
        igual(List.of(1, 2), r.passos().get(1).filaAntes(), "fila etapa 2");
        igual(List.of(3), r.passos().get(1).novos(), "novos etapa 2");
    }

    private static void origemBloqueada() {
        Grafo g = caminho(3);
        ResultadoBFS r = BuscaEmLargura.executar(g, 0, Set.of(0));
        igual(List.of(), r.alcancados(), "ninguém alcançado");
        igual(0, BuscaEmLargura.contarAlcancados(g, 0, Set.of(0)), "contagem rápida");
    }

    private static void arestasInvalidas() {
        Grafo g = vazio(2);
        verdadeiro(g.adicionarContato(0, 1), "primeira aresta");
        verdadeiro(!g.adicionarContato(1, 0), "repetida");
        verdadeiro(!g.adicionarContato(0, 0), "laço");
        igual(1, g.numeroDeArestas(), "arestas");
    }

    private static void pessoaInexistente() {
        Grafo g = vazio(2);
        try {
            g.adicionarContato(0, 5);
        } catch (IllegalArgumentException esperado) {
            return;
        }
        throw new AssertionError("deveria lançar IllegalArgumentException");
    }

    private static void redeCsv() {
        try {
            Path d = Path.of("dados");
            if (!java.nio.file.Files.isDirectory(d)) d = Path.of("demo", "dados");
            Grafo g = LeitorCSV.ler(d.resolve("pessoas.csv"), d.resolve("contatos.csv"));
            igual(28, g.numeroDeVertices(), "28 pessoas");
            igual(0, g.grau(27), "Sônia isolada");
            ResultadoQuarentena q = Quarentena.analisar(g, 0, Set.of());
            verdadeiro(!q.heuristicaAcertou(), "o maior grau deve errar nesta rede");
            igual(12, q.melhorMaiorGrau().pessoa(), "maior grau = Marina");
            igual(0, q.melhorMaiorGrau().protegidos(), "bloquear Marina não protege ninguém");
            igual(3, q.melhorForcaBruta().pessoa(), "melhor = Diego (ponte)");
            igual(20, q.melhorForcaBruta().protegidos(), "Diego protege 20");
            igual(List.of(2, 3, 5, 6, 9, 11, 13, 19, 24), q.articulacoes(), "articulações da rede");
        } catch (java.io.IOException e) {
            throw new AssertionError("não leu o CSV: " + e);
        }
    }

    private static void propriedadeTarjan() {
        Random rnd = new Random(7);
        for (int rodada = 0; rodada < 200; rodada++) {
            int n = 2 + rnd.nextInt(14);
            Grafo g = vazio(n);
            double p = 0.1 + rnd.nextDouble() * 0.3;
            for (int i = 0; i < n; i++)
                for (int j = i + 1; j < n; j++) if (rnd.nextDouble() < p) g.adicionarContato(i, j);
            Set<Integer> bloq = new HashSet<>();
            if (rnd.nextInt(3) == 0) bloq.add(rnd.nextInt(n));
            Set<Integer> esperado = new HashSet<>();
            int base = componentes(g, bloq);
            for (int v = 0; v < n; v++) {
                if (bloq.contains(v)) continue;
                Set<Integer> mais = new HashSet<>(bloq);
                mais.add(v);
                // removendo v, um componente "some" se v era isolado; articulação = aumenta o nº de componentes
                int depois = componentes(g, mais);
                int antes = base;
                if (g.vizinhos(v).stream().allMatch(bloq::contains)) antes = base - 1; // v era componente sozinho
                if (depois > antes) esperado.add(v);
            }
            Set<Integer> obtido = new HashSet<>(PontosDeArticulacao.encontrar(g, bloq));
            igual(esperado, obtido, "rodada " + rodada + " n=" + n);
        }
    }

    private static void redeGrande() {
        Grafo g = GeradorDeRede.gerar(5000, 1);
        PontosDeArticulacao.encontrar(g, Set.of());
        verdadeiro(BuscaEmLargura.contarAlcancados(g, 0, Set.of()) > 1, "BFS na rede grande");
    }

    private static void json() {
        String s = Json.escrever(Map.of("nome", "Ana \"A\" Müller\n", "n", 3));
        verdadeiro(s.contains("\"Ana \\\"A\\\" Müller\\n\""), s);
        igual("[1,2]", Json.escrever(new int[]{1, 2}), "vetor");
        igual("null", Json.escrever(Double.NaN), "NaN vira null");
    }

    // ---------- utilidades ----------

    private static Grafo vazio(int n) {
        Grafo g = new Grafo();
        for (int i = 0; i < n; i++) g.adicionarPessoa("P" + i, "G");
        return g;
    }

    private static Grafo caminho(int n) {
        Grafo g = vazio(n);
        for (int i = 0; i + 1 < n; i++) g.adicionarContato(i, i + 1);
        return g;
    }

    /** Componentes conexos ignorando os bloqueados. */
    private static int componentes(Grafo g, Set<Integer> bloq) {
        boolean[] visto = new boolean[g.numeroDeVertices()];
        int c = 0;
        for (int v = 0; v < visto.length; v++) {
            if (visto[v] || bloq.contains(v)) continue;
            c++;
            List<Integer> pilha = new ArrayList<>(List.of(v));
            visto[v] = true;
            while (!pilha.isEmpty()) {
                int u = pilha.remove(pilha.size() - 1);
                for (int w : g.vizinhos(u))
                    if (!visto[w] && !bloq.contains(w)) {
                        visto[w] = true;
                        pilha.add(w);
                    }
            }
        }
        return c;
    }

    private static void executar(String nome, Runnable caso) {
        total++;
        try {
            caso.run();
            System.out.println("[OK]    " + nome);
        } catch (Throwable t) {
            falhas++;
            System.out.println("[FALHA] " + nome + " -> " + t);
        }
    }

    private static void igual(Object esperado, Object obtido, String msg) {
        if (!esperado.equals(obtido))
            throw new AssertionError(msg + ": esperado " + esperado + " mas foi " + obtido);
    }

    private static void verdadeiro(boolean cond, String msg) {
        if (!cond) throw new AssertionError(msg);
    }
}
