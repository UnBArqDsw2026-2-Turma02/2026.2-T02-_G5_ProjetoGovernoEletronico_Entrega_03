import java.util.List;

public record ResultadoFonte(String nomeFonte, StatusFonte status, List<ItemResultado> itens) {

    public static ResultadoFonte de(String nomeFonte, List<ItemResultado> itens) {
        StatusFonte status = itens.isEmpty() ? StatusFonte.VAZIO : StatusFonte.SUCESSO;
        return new ResultadoFonte(nomeFonte, status, itens);
    }

    public static ResultadoFonte indisponivel(String nomeFonte) {
        return new ResultadoFonte(nomeFonte, StatusFonte.INDISPONIVEL, List.of());
    }
}
