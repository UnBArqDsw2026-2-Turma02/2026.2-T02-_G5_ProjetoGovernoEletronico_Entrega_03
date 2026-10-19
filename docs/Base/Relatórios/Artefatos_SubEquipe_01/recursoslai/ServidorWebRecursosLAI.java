package recursoslai;

import com.sun.net.httpserver.Headers;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintStream;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executors;

public class ServidorWebRecursosLAI {
    private static final int PORTA_PADRAO = 8080;
    private static final Path HTML = Paths.get("web", "index.html");

    public static void main(String[] args) throws Exception {
        int porta = args.length > 0 ? Integer.parseInt(args[0]) : PORTA_PADRAO;
        if (!Files.exists(HTML)) {
            System.err.println("Não encontrei " + HTML.toAbsolutePath());
            System.err.println("Execute o comando a partir da pasta chainofresponsibility.");
            System.exit(1);
        }
        String host = System.getProperty("server.host", "127.0.0.1");
        HttpServer servidor = HttpServer.create(new InetSocketAddress(host, porta), 0);
        servidor.createContext("/", ServidorWebRecursosLAI::servirPagina);
        servidor.createContext("/api/processar", ServidorWebRecursosLAI::processarRecurso);
        servidor.setExecutor(Executors.newSingleThreadExecutor());
        servidor.start();
        System.out.println("Interface web disponível em: http://localhost:" + porta);
        System.out.println("Mantenha este terminal aberto enquanto usa a interface. Ctrl+C encerra o servidor.");
    }

    private static void servirPagina(HttpExchange exchange) throws IOException {
        if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
            responder(exchange, 405, "text/plain; charset=UTF-8", "Método não permitido");
            return;
        }
        byte[] conteudo = Files.readAllBytes(HTML);
        responder(exchange, 200, "text/html; charset=UTF-8", conteudo);
    }

    private static void processarRecurso(HttpExchange exchange) throws IOException {
        if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
            responder(exchange, 405, "application/json; charset=UTF-8", "{\"erro\":\"Use POST\"}");
            return;
        }
        String corpo = lerCorpo(exchange.getRequestBody());
        Map<String, String> dados = parseForm(corpo);
        String protocolo = valor(dados, "protocolo").trim();
        String cidadao = valor(dados, "cidadao").trim();
        if (protocolo.isEmpty() || cidadao.isEmpty()) {
            responder(exchange, 400, "application/json; charset=UTF-8", "{\"erro\":\"Preencha o protocolo e o nome do cidadão.\"}");
            return;
        }

        boolean tempestivo = "true".equals(valor(dados, "tempestivo"));
        boolean executivoFederal = "true".equals(valor(dados, "executivoFederal"));
        boolean deferir1 = "deferir".equals(valor(dados, "decisao1"));
        boolean deferir2 = "deferir".equals(valor(dados, "decisao2"));
        boolean deferirCGU = "deferir".equals(valor(dados, "decisaoCGU"));
        boolean deferirCMRI = "deferir".equals(valor(dados, "decisaoCMRI"));

        Recurso recurso = new Recurso(protocolo, cidadao, tempestivo, executivoFederal);
        InstanciaHandler cadeia = new ValidadorTempestividadeHandler();
        cadeia.encadear(new AutoridadeHierarquicaSuperiorHandler(deferir1))
              .encadear(new AutoridadeMaximaOrgaoHandler(deferir2))
              .encadear(new CGUHandler(deferirCGU))
              .encadear(new CMRIHandler(deferirCMRI));

        StringBuilder relatorio = new StringBuilder();
        relatorio.append("=== PROCESSAMENTO DO RECURSO ===\n")
                 .append("Protocolo: ").append(protocolo).append('\n')
                 .append("Cidadão: ").append(cidadao).append('\n')
                 .append("Tempestivo: ").append(simNao(tempestivo)).append('\n')
                 .append("Órgão do Executivo Federal: ").append(simNao(executivoFederal)).append("\n\n")
                 .append("--- Log da cadeia de handlers ---\n");

        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        try (PrintStream captura = new PrintStream(buffer, true, "UTF-8")) {
            System.setOut(captura);
            cadeia.handle(recurso);
        } catch (Exception e) {
            responder(exchange, 500, "application/json; charset=UTF-8", "{\"erro\":\"Falha ao processar o recurso.\"}");
            return;
        } finally {
            System.setOut(original);
        }
        relatorio.append(new String(buffer.toByteArray(), StandardCharsets.UTF_8));
        relatorio.append("\n--- RESULTADO FINAL ---\n")
                 .append("Status: ").append(recurso.getStatus()).append('\n')
                 .append("Instância responsável: ")
                 .append(recurso.getInstanciaResponsavelPelaDecisao() == null ? "—" : recurso.getInstanciaResponsavelPelaDecisao()).append('\n')
                 .append("Motivo: ").append(recurso.getMotivoDaDecisao() == null ? "—" : recurso.getMotivoDaDecisao()).append('\n');
        String json = "{\"status\":\"" + escaparJson(recurso.getStatus().toString()) + "\",\"instancia\":\"" + escaparJson(recurso.getInstanciaResponsavelPelaDecisao()) + "\",\"motivo\":\"" + escaparJson(recurso.getMotivoDaDecisao()) + "\",\"relatorio\":\"" + escaparJson(relatorio.toString()) + "\"}";
        responder(exchange, 200, "application/json; charset=UTF-8", json);
    }

    private static String lerCorpo(InputStream input) throws IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buffer = new byte[4096];
        int lido;
        while ((lido = input.read(buffer)) != -1) out.write(buffer, 0, lido);
        return new String(out.toByteArray(), StandardCharsets.UTF_8);
    }

    private static Map<String, String> parseForm(String corpo) throws IOException {
        Map<String, String> resultado = new HashMap<String, String>();
        if (corpo.isEmpty()) return resultado;
        for (String par : corpo.split("&")) {
            String[] partes = par.split("=", 2);
            String chave = URLDecoder.decode(partes[0], "UTF-8");
            String valor = partes.length > 1 ? URLDecoder.decode(partes[1], "UTF-8") : "";
            resultado.put(chave, valor);
        }
        return resultado;
    }

    private static String valor(Map<String, String> dados, String chave) {
        String v = dados.get(chave);
        return v == null ? "" : v;
    }

    private static String simNao(boolean valor) { return valor ? "Sim" : "Não"; }

    private static String escaparJson(String texto) {
        if (texto == null) return "";
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < texto.length(); i++) {
            char c = texto.charAt(i);
            switch (c) {
                case '"': b.append("\\\""); break;
                case '\\': b.append("\\\\"); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                default: if (c < 0x20) b.append(String.format("\\u%04x", (int)c)); else b.append(c);
            }
        }
        return b.toString();
    }

    private static void responder(HttpExchange exchange, int status, String tipo, String corpo) throws IOException {
        responder(exchange, status, tipo, corpo.getBytes(StandardCharsets.UTF_8));
    }

    private static void responder(HttpExchange exchange, int status, String tipo, byte[] corpo) throws IOException {
        Headers headers = exchange.getResponseHeaders();
        headers.set("Content-Type", tipo);
        headers.set("X-Content-Type-Options", "nosniff");
        headers.set("Cache-Control", "no-store");
        exchange.sendResponseHeaders(status, corpo.length);
        try (OutputStream out = exchange.getResponseBody()) { out.write(corpo); }
    }
}
