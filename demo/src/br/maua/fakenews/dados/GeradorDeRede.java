package br.maua.fakenews.dados;

import br.maua.fakenews.modelo.Grafo;

import java.util.Random;

/** Gera redes aleatórias com comunidades (reprodutíveis por semente) para testes de desempenho. */
public final class GeradorDeRede {
    private GeradorDeRede() {
    }

    public static Grafo gerar(int n, long semente) {
        return gerar(n, 10, 0.35, semente);
    }

    /**
     * @param tamanhoComunidade tamanho médio de cada grupo
     * @param pDentro           probabilidade de contato entre duas pessoas do mesmo grupo
     */
    public static Grafo gerar(int n, int tamanhoComunidade, double pDentro, long semente) {
        if (n < 1) throw new IllegalArgumentException("n deve ser >= 1");
        Random rnd = new Random(semente);
        Grafo g = new Grafo();
        int comunidades = Math.max(1, n / tamanhoComunidade);
        int[] comunidadeDe = new int[n];
        for (int i = 0; i < n; i++) {
            comunidadeDe[i] = i % comunidades;
            g.adicionarPessoa("Pessoa " + (i + 1), "Grupo " + (comunidadeDe[i] + 1));
        }
        // dentro de cada grupo: cadeia (garante conexão) + contatos aleatórios
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (comunidadeDe[i] == comunidadeDe[j] && rnd.nextDouble() < pDentro) g.adicionarContato(i, j);
            }
        }
        for (int c = 0; c < comunidades; c++) {
            int anterior = -1;
            for (int i = c; i < n; i += comunidades) {
                if (anterior != -1) g.adicionarContato(anterior, i);
                anterior = i;
            }
        }
        // poucas pontes entre grupos vizinhos
        for (int c = 0; c + 1 < comunidades; c++) {
            int a = c + comunidades * rnd.nextInt(Math.max(1, (n - c + comunidades - 1) / comunidades));
            int b = (c + 1) + comunidades * rnd.nextInt(Math.max(1, (n - c - 1 + comunidades - 1) / comunidades));
            if (a < n && b < n) g.adicionarContato(a, b);
        }
        return g;
    }
}
