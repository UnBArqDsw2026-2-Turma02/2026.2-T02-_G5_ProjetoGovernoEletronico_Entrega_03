import java.util.List;

public class BuscaTransparencia implements FonteBusca {

    @Override
    public String nome() {
        return "Portal da Transparência";
    }

    @Override
    public ResultadoFonte consultar(String termo) {
        System.out.println("  [BuscaTransparencia] buscando registros de transparência sobre: " + termo);
        // Simulação de "busca sem registros" (fonte disponível, porém sem resultados).
        if (termo.equalsIgnoreCase("inexistente")) {
            return ResultadoFonte.de(nome(), List.of());
        }
        return ResultadoFonte.de(nome(), List.of(
                new ItemResultado("Registro de transparência simulado sobre " + termo,
                        "https://portaldatransparencia.gov.br/")));
    }
}
