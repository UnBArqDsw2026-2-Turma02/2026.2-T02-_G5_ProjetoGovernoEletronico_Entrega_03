import java.util.List;

public record ResultadoBusca(ValidacaoConsulta validacao,
                             List<ResultadoFonte> fontes,
                             OrientacaoIA orientacao) {

    public static ResultadoBusca invalida(ValidacaoConsulta validacao) {
        return new ResultadoBusca(validacao, List.of(), OrientacaoIA.vazia());
    }
}
