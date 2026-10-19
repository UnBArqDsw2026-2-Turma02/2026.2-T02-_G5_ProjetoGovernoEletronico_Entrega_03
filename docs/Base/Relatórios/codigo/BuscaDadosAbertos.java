import java.util.List;

public class BuscaDadosAbertos implements FonteBusca {

    @Override
    public String nome() {
        return "Portal de Dados Abertos";
    }

    @Override
    public ResultadoFonte consultar(String termo) {
        System.out.println("  [BuscaDadosAbertos] buscando conjuntos de dados sobre: " + termo);
        // Simulação de indisponibilidade da fonte (falha técnica, diferente de busca vazia).
        if (termo.equalsIgnoreCase("falha")) {
            throw new IllegalStateException("Portal de Dados Abertos fora do ar (simulado)");
        }
        return ResultadoFonte.de(nome(), List.of(
                new ItemResultado("Conjunto de dados simulado sobre " + termo,
                        "https://dados.gov.br/")));
    }
}
