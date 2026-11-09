package br.maua.fakenews.dados;

import br.maua.fakenews.modelo.Grafo;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** Lê a rede a partir de pessoas.csv (id;nome;grupo) e contatos.csv (origem;destino), UTF-8. */
public final class LeitorCSV {
    private LeitorCSV() {
    }

    public static Grafo ler(Path pessoas, Path contatos) throws IOException {
        Grafo g = new Grafo();
        List<String> linhasP = Files.readAllLines(pessoas, StandardCharsets.UTF_8);
        int esperado = 0;
        for (int i = 1; i < linhasP.size(); i++) {
            String l = linhasP.get(i).trim();
            if (l.isEmpty()) continue;
            String[] c = l.split(";");
            if (c.length < 3) throw new IOException("Linha inválida em pessoas.csv: " + l);
            if (Integer.parseInt(c[0].trim()) != esperado)
                throw new IOException("Os ids devem ser sequenciais a partir de 0. Esperado " + esperado + " em: " + l);
            g.adicionarPessoa(c[1].trim(), c[2].trim());
            esperado++;
        }
        List<String> linhasC = Files.readAllLines(contatos, StandardCharsets.UTF_8);
        for (int i = 1; i < linhasC.size(); i++) {
            String l = linhasC.get(i).trim();
            if (l.isEmpty()) continue;
            String[] c = l.split(";");
            if (c.length < 2) throw new IOException("Linha inválida em contatos.csv: " + l);
            g.adicionarContato(Integer.parseInt(c[0].trim()), Integer.parseInt(c[1].trim()));
        }
        return g;
    }
}
