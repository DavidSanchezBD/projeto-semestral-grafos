package br.maua.fakenews.web;

import br.maua.fakenews.algoritmos.BuscaEmLargura;
import br.maua.fakenews.algoritmos.PontosDeArticulacao;
import br.maua.fakenews.algoritmos.Quarentena;
import br.maua.fakenews.algoritmos.Quarentena.Candidato;
import br.maua.fakenews.algoritmos.Quarentena.ResultadoQuarentena;
import br.maua.fakenews.algoritmos.ResultadoBFS;
import br.maua.fakenews.dados.GeradorDeRede;
import br.maua.fakenews.dados.LeitorCSV;
import br.maua.fakenews.modelo.Grafo;
import br.maua.fakenews.modelo.Pessoa;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Servidor HTTP nativo do JDK. Toda a lógica de grafos fica em Java;
 * a página web apenas desenha o que a API devolve.
 */
public final class ServidorWeb {
    private final Path pastaWeb;
    private final Path pastaDados;
    private volatile Grafo grafo;
    private volatile String origemDaRede = "original";
    private HttpServer servidor;

    public ServidorWeb(Path pastaWeb, Path pastaDados) throws IOException {
        this.pastaWeb = pastaWeb;
        this.pastaDados = pastaDados;
        this.grafo = carregarOriginal();
    }

    private Grafo carregarOriginal() throws IOException {
        return LeitorCSV.ler(pastaDados.resolve("pessoas.csv"), pastaDados.resolve("contatos.csv"));
    }

    public void iniciar(int porta) throws IOException {
        servidor = HttpServer.create(new InetSocketAddress("127.0.0.1", porta), 0);
        servidor.createContext("/api/rede/aleatoria", this::redeAleatoria);
        servidor.createContext("/api/rede/original", this::redeOriginal);
        servidor.createContext("/api/rede", this::rede);
        servidor.createContext("/api/bfs", this::bfs);
        servidor.createContext("/api/quarentena", this::quarentena);
        servidor.createContext("/api/desempenho", this::desempenho);
        servidor.createContext("/", this::estatico);
        servidor.start();
    }

    public void parar() {
        if (servidor != null) servidor.stop(0);
    }

    // ---------- handlers da API ----------

    private void rede(HttpExchange ex) throws IOException {
        responder(ex, () -> descreverRede());
    }

    private void redeOriginal(HttpExchange ex) throws IOException {
        responder(ex, () -> {
            grafo = carregarOriginal();
            origemDaRede = "original";
            return descreverRede();
        });
    }

    private void redeAleatoria(HttpExchange ex) throws IOException {
        responder(ex, () -> {
            int n = inteiro(parametros(ex), "n", 60);
            if (n < 2 || n > 5000) throw new IllegalArgumentException("n deve estar entre 2 e 5000");
            grafo = GeradorDeRede.gerar(n, 42);
            origemDaRede = "aleatoria";
            return descreverRede();
        });
    }

    private void bfs(HttpExchange ex) throws IOException {
        responder(ex, () -> {
            Grafo g = grafo;
            Map<String, String> p = parametros(ex);
            int origem = inteiro(p, "origem", 0);
            Set<Integer> bloqueados = conjunto(p.get("bloqueados"));
            ResultadoBFS r = BuscaEmLargura.executar(g, origem, bloqueados);
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("origem", origem);
            m.put("bloqueados", new ArrayList<>(bloqueados));
            m.put("niveis", r.niveis());
            m.put("dist", r.distancias());
            m.put("anterior", r.anteriores());
            List<Object> passos = new ArrayList<>();
            for (ResultadoBFS.PassoBFS s : r.passos()) {
                Map<String, Object> ps = new LinkedHashMap<>();
                ps.put("filaAntes", s.filaAntes());
                ps.put("vertice", s.vertice());
                ps.put("novos", s.novos());
                passos.add(ps);
            }
            m.put("passos", passos);
            m.put("alcancados", r.alcancados());
            m.put("naoAlcancados", r.naoAlcancados());
            m.put("rodadas", r.rodadasDeEncaminhamento());
            return m;
        });
    }

    private void quarentena(HttpExchange ex) throws IOException {
        responder(ex, () -> {
            Grafo g = grafo;
            Map<String, String> p = parametros(ex);
            int origem = inteiro(p, "origem", 0);
            Set<Integer> bloqueados = conjunto(p.get("bloqueados"));
            g.pessoa(origem);
            ResultadoQuarentena r = Quarentena.analisar(g, origem, bloqueados);
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("alcancadosAtuais", r.alcancadosAtuais());
            List<Object> ranking = new ArrayList<>();
            for (Candidato c : r.ranking()) ranking.add(candidato(c));
            m.put("ranking", ranking);
            m.put("melhorForcaBruta", r.melhorForcaBruta() == null ? null : candidato(r.melhorForcaBruta()));
            m.put("melhorMaiorGrau", r.melhorMaiorGrau() == null ? null : candidato(r.melhorMaiorGrau()));
            m.put("articulacoes", r.articulacoes());
            m.put("heuristicaAcertou", r.heuristicaAcertou());
            m.put("tempoMs", r.tempoMs());
            return m;
        });
    }

    private void desempenho(HttpExchange ex) throws IOException {
        responder(ex, () -> {
            List<Object> linhas = new ArrayList<>();
            for (int n : new int[]{100, 200, 500, 1000, 2000}) {
                Grafo g = GeradorDeRede.gerar(n, 42);
                Quarentena.analisar(g, 0, Set.of()); // aquecimento da JVM
                ResultadoQuarentena r = Quarentena.analisar(g, 0, Set.of());
                Map<String, Object> l = new LinkedHashMap<>();
                l.put("n", n);
                l.put("arestas", g.numeroDeArestas());
                l.put("candidatos", r.ranking().size());
                l.put("tempoMs", r.tempoMs());
                linhas.add(l);
            }
            return Map.of("medicoes", linhas);
        });
    }

    // ---------- arquivos estáticos ----------

    private void estatico(HttpExchange ex) throws IOException {
        String caminho = ex.getRequestURI().getPath();
        if (caminho.equals("/")) caminho = "/index.html";
        if (caminho.startsWith("/web/")) caminho = caminho.substring(4);
        Path arquivo = pastaWeb.resolve(caminho.substring(1)).normalize();
        if (!arquivo.startsWith(pastaWeb) || !Files.isRegularFile(arquivo)) {
            enviar(ex, 404, "text/plain; charset=utf-8", "Não encontrado".getBytes(StandardCharsets.UTF_8));
            return;
        }
        enviar(ex, 200, tipo(arquivo.getFileName().toString()), Files.readAllBytes(arquivo));
    }

    private static String tipo(String nome) {
        if (nome.endsWith(".html")) return "text/html; charset=utf-8";
        if (nome.endsWith(".css")) return "text/css; charset=utf-8";
        if (nome.endsWith(".js")) return "text/javascript; charset=utf-8";
        if (nome.endsWith(".svg")) return "image/svg+xml";
        if (nome.endsWith(".png")) return "image/png";
        return "application/octet-stream";
    }

    // ---------- utilidades ----------

    private interface Acao {
        Object executar() throws Exception;
    }

    private void responder(HttpExchange ex, Acao acao) throws IOException {
        try {
            byte[] corpo = Json.escrever(acao.executar()).getBytes(StandardCharsets.UTF_8);
            enviar(ex, 200, "application/json; charset=utf-8", corpo);
        } catch (IllegalArgumentException e) {
            Map<String, Object> erro = Map.of("erro", String.valueOf(e.getMessage()));
            enviar(ex, 400, "application/json; charset=utf-8", Json.escrever(erro).getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            Map<String, Object> erro = Map.of("erro", "Falha interna: " + e);
            enviar(ex, 500, "application/json; charset=utf-8", Json.escrever(erro).getBytes(StandardCharsets.UTF_8));
        }
    }

    private static void enviar(HttpExchange ex, int status, String tipo, byte[] corpo) throws IOException {
        ex.getResponseHeaders().set("Content-Type", tipo);
        ex.getResponseHeaders().set("Cache-Control", "no-store");
        ex.sendResponseHeaders(status, corpo.length);
        try (OutputStream os = ex.getResponseBody()) {
            os.write(corpo);
        }
    }

    private Map<String, Object> descreverRede() {
        Grafo g = grafo;
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("tipo", origemDaRede);
        List<Object> pessoas = new ArrayList<>();
        List<Object> contatos = new ArrayList<>();
        for (Pessoa p : g.pessoas()) {
            Map<String, Object> o = new LinkedHashMap<>();
            o.put("id", p.id());
            o.put("nome", p.nome());
            o.put("grupo", p.grupo());
            o.put("grau", g.grau(p.id()));
            pessoas.add(o);
            for (int v : g.vizinhos(p.id())) if (p.id() < v) contatos.add(List.of(p.id(), v));
        }
        m.put("pessoas", pessoas);
        m.put("contatos", contatos);
        m.put("articulacoes", PontosDeArticulacao.encontrar(g, Set.of()));
        m.put("vertices", g.numeroDeVertices());
        m.put("arestas", g.numeroDeArestas());
        return m;
    }

    private static Map<String, Object> candidato(Candidato c) {
        Map<String, Object> o = new LinkedHashMap<>();
        o.put("pessoa", c.pessoa());
        o.put("alcancadosSemEla", c.alcancadosSemEla());
        o.put("protegidos", c.protegidos());
        o.put("grau", c.grau());
        o.put("articulacao", c.articulacao());
        return o;
    }

    private static Map<String, String> parametros(HttpExchange ex) {
        Map<String, String> r = new HashMap<>();
        String q = ex.getRequestURI().getRawQuery();
        if (q == null) return r;
        for (String par : q.split("&")) {
            int i = par.indexOf('=');
            String k = i < 0 ? par : par.substring(0, i);
            String v = i < 0 ? "" : par.substring(i + 1);
            r.put(URLDecoder.decode(k, StandardCharsets.UTF_8), URLDecoder.decode(v, StandardCharsets.UTF_8));
        }
        return r;
    }

    private static int inteiro(Map<String, String> p, String chave, int padrao) {
        String v = p.get(chave);
        if (v == null || v.isBlank()) return padrao;
        try {
            return Integer.parseInt(v.trim());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("Parâmetro '" + chave + "' deve ser inteiro");
        }
    }

    private static Set<Integer> conjunto(String csv) {
        Set<Integer> s = new HashSet<>();
        if (csv == null || csv.isBlank()) return s;
        for (String x : csv.split(",")) {
            try {
                s.add(Integer.parseInt(x.trim()));
            } catch (NumberFormatException e) {
                throw new IllegalArgumentException("Lista de bloqueados inválida: " + csv);
            }
        }
        return s;
    }
}
