package br.maua.fakenews.web;

import java.util.Collection;
import java.util.Map;

/** Serializador JSON mínimo (mapas, listas, vetores, números, booleanos e strings). */
public final class Json {
    private Json() {
    }

    public static String escrever(Object o) {
        StringBuilder sb = new StringBuilder();
        escrever(o, sb);
        return sb.toString();
    }

    private static void escrever(Object o, StringBuilder sb) {
        if (o == null) {
            sb.append("null");
        } else if (o instanceof String s) {
            string(s, sb);
        } else if (o instanceof Double d) {
            sb.append(d.isNaN() || d.isInfinite() ? "null" : d.toString());
        } else if (o instanceof Number || o instanceof Boolean) {
            sb.append(o);
        } else if (o instanceof Map<?, ?> m) {
            sb.append('{');
            boolean primeiro = true;
            for (Map.Entry<?, ?> e : m.entrySet()) {
                if (!primeiro) sb.append(',');
                primeiro = false;
                string(String.valueOf(e.getKey()), sb);
                sb.append(':');
                escrever(e.getValue(), sb);
            }
            sb.append('}');
        } else if (o instanceof Collection<?> c) {
            sb.append('[');
            boolean primeiro = true;
            for (Object x : c) {
                if (!primeiro) sb.append(',');
                primeiro = false;
                escrever(x, sb);
            }
            sb.append(']');
        } else if (o instanceof int[] a) {
            sb.append('[');
            for (int i = 0; i < a.length; i++) {
                if (i > 0) sb.append(',');
                sb.append(a[i]);
            }
            sb.append(']');
        } else {
            throw new IllegalArgumentException("Tipo não suportado em JSON: " + o.getClass());
        }
    }

    private static void string(String s, StringBuilder sb) {
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"' -> sb.append("\\\"");
                case '\\' -> sb.append("\\\\");
                case '\n' -> sb.append("\\n");
                case '\r' -> sb.append("\\r");
                case '\t' -> sb.append("\\t");
                default -> {
                    if (c < 0x20) sb.append(String.format("\\u%04x", (int) c));
                    else sb.append(c);
                }
            }
        }
        sb.append('"');
    }
}
