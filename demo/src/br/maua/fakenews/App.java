package br.maua.fakenews;

import br.maua.fakenews.algoritmos.BuscaEmLargura;
import br.maua.fakenews.algoritmos.Quarentena;
import br.maua.fakenews.algoritmos.Quarentena.Candidato;
import br.maua.fakenews.algoritmos.Quarentena.ResultadoQuarentena;
import br.maua.fakenews.algoritmos.ResultadoBFS;
import br.maua.fakenews.dados.LeitorCSV;
import br.maua.fakenews.modelo.Grafo;
import br.maua.fakenews.web.ServidorWeb;

import java.awt.Desktop;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Set;

/**
 * Caso Fake News: propagação de boatos em grupos de mensagens (BFS + quarentena).
 * Uso: java -jar fakenews.jar [--console] [--porta 8080] [--sem-navegador]
 */
public final class App {
    public static void main(String[] args) throws Exception {
        boolean console = false;
        boolean navegador = true;
        int porta = 8080;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--console" -> console = true;
                case "--sem-navegador" -> navegador = false;
                case "--porta" -> porta = Integer.parseInt(args[++i]);
                default -> {
                    System.err.println("Argumento desconhecido: " + args[i]);
                    System.exit(1);
                }
            }
        }
        Path base = Files.isDirectory(Path.of("web")) ? Path.of(".") : Path.of("demo");
        Path web = base.resolve("web").toAbsolutePath().normalize();
        Path dados = base.resolve("dados").toAbsolutePath().normalize();

        if (console) {
            modoConsole(dados);
            return;
        }
        ServidorWeb servidor = new ServidorWeb(web, dados);
        servidor.iniciar(porta);
        String url = "http://localhost:" + porta + "/";
        System.out.println("Caso Fake News rodando em " + url + "  (Ctrl+C para encerrar)");
        if (navegador && Desktop.isDesktopSupported() && Desktop.getDesktop().isSupported(Desktop.Action.BROWSE)) {
            Desktop.getDesktop().browse(URI.create(url));
        }
    }

    /** Plano B: mesma análise, em texto, caso o navegador falhe. */
    private static void modoConsole(Path dados) throws Exception {
        Grafo g = LeitorCSV.ler(dados.resolve("pessoas.csv"), dados.resolve("contatos.csv"));
        int origem = 0;
        System.out.printf("Rede: %d pessoas, %d contatos. Paciente zero: %s%n%n",
                g.numeroDeVertices(), g.numeroDeArestas(), g.pessoa(origem).nome());
        ResultadoBFS r = BuscaEmLargura.executar(g, origem, Set.of());
        var niveis = r.niveis();
        for (int i = 0; i < niveis.size(); i++) {
            StringBuilder sb = new StringBuilder();
            for (int v : niveis.get(i)) sb.append(g.pessoa(v).nome()).append(' ');
            System.out.printf("Onda %d: %s%n", i, sb.toString().trim());
        }
        StringBuilder ni = new StringBuilder();
        for (int v : r.naoAlcancados()) ni.append(g.pessoa(v).nome()).append(' ');
        System.out.println("Não alcançados: " + (ni.length() == 0 ? "ninguém" : ni.toString().trim()));

        ResultadoQuarentena q = Quarentena.analisar(g, origem, Set.of());
        System.out.printf("%nQuarentena (força bruta, %.2f ms) - top 5:%n", q.tempoMs());
        for (Candidato c : q.ranking().stream().limit(5).toList()) {
            System.out.printf("  %-8s protege %2d | grau %d%s%n", g.pessoa(c.pessoa()).nome(), c.protegidos(),
                    c.grau(), c.articulacao() ? " | ponto de articulação" : "");
        }
        Candidato mg = q.melhorMaiorGrau();
        System.out.printf("Maior grau: %s protege %d -> heurística %s%n", g.pessoa(mg.pessoa()).nome(),
                mg.protegidos(), q.heuristicaAcertou() ? "acertou" : "ERROU");
    }
}
