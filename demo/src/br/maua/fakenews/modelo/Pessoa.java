package br.maua.fakenews.modelo;

/** Vértice do grafo: uma pessoa em um ou mais grupos de mensagens. */
public record Pessoa(int id, String nome, String grupo) {
}
