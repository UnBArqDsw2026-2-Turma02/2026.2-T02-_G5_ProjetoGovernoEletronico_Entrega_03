import java.util.List;

public class BuscaPedidosLAI implements FonteBusca {

    @Override
    public String nome() {
        return "Pedidos LAI";
    }

    @Override
    public ResultadoFonte consultar(String termo) {
        System.out.println("  [BuscaPedidosLAI] buscando pedidos LAI sobre: " + termo);
        return ResultadoFonte.de(nome(), List.of(
                new ItemResultado("Pedido LAI simulado nº 001 sobre " + termo,
                        "https://informabr.cgu.gov.br/"),
                new ItemResultado("Pedido LAI simulado nº 002 sobre " + termo,
                        "https://informabr.cgu.gov.br/")));
    }
}
