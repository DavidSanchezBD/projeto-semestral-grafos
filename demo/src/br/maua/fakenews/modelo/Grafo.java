package br.maua.fakenews.modelo;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Grafo não direcionado e sem pesos, em lista de adjacência.
 * Vértices = pessoas; arestas = contato direto (ambos podem repassar mensagens).
 * Lista de adjacência: memória O(V + E), adequada a redes esparsas (aula T25).
 */
public final class Grafo {
    private final List<Pessoa> pessoas = new ArrayList<>();
    private final List<List<Integer>> adj = new ArrayList<>();
    private int arestas = 0;

    public int adicionarPessoa(String nome, String grupo) {
        int id = pessoas.size();
        pessoas.add(new Pessoa(id, nome, grupo));
        adj.add(new ArrayList<>());
        return id;
    }

    /** Ignora laços e contatos repetidos. Retorna true se a aresta foi criada. */
    public boolean adicionarContato(int a, int b) {
        validar(a);
        validar(b);
        if (a == b || adj.get(a).contains(b)) return false;
        adj.get(a).add(b);
        adj.get(b).add(a);
        arestas++;
        return true;
    }

    public List<Integer> vizinhos(int v) {
        validar(v);
        return Collections.unmodifiableList(adj.get(v));
    }

    public int grau(int v) {
        validar(v);
        return adj.get(v).size();
    }

    public Pessoa pessoa(int id) {
        validar(id);
        return pessoas.get(id);
    }

    public List<Pessoa> pessoas() {
        return Collections.unmodifiableList(pessoas);
    }

    public int numeroDeVertices() {
        return pessoas.size();
    }

    public int numeroDeArestas() {
        return arestas;
    }

    private void validar(int v) {
        if (v < 0 || v >= pessoas.size())
            throw new IllegalArgumentException("Pessoa inexistente: " + v);
    }
}
