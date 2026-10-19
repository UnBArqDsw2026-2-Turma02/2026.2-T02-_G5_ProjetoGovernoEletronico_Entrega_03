import java.util.ArrayList;
import java.util.List;

public class FachadaBuscaPublica {

    private final ValidadorConsulta validador;
    private final List<FonteBusca> fontes;
    private final GeradorOrientacaoIA orientacaoIA;

    public FachadaBuscaPublica() {
        this(new ValidadorConsulta(),
             List.of(new BuscaPedidosLAI(), new BuscaTransparencia(), new BuscaDadosAbertos()),
             new GeradorOrientacaoIA());
    }

    public FachadaBuscaPublica(ValidadorConsulta validador,
                               List<FonteBusca> fontes,
                               GeradorOrientacaoIA orientacaoIA) {
        this.validador = validador;
        this.fontes = fontes;
        this.orientacaoIA = orientacaoIA;
    }

    public ResultadoBusca buscar(String termo) {
        ValidacaoConsulta validacao = validador.validar(termo);
        if (!validacao.valida()) {
            return ResultadoBusca.invalida(validacao);
        }

        String termoLimpo = termo.strip();
        List<ResultadoFonte> resultados = new ArrayList<>();
        for (FonteBusca fonte : fontes) {
            try {
                resultados.add(fonte.consultar(termoLimpo));
            } catch (RuntimeException e) {
                System.out.println("  [Fachada] falha em '" + fonte.nome() + "': " + e.getMessage());
                resultados.add(ResultadoFonte.indisponivel(fonte.nome()));
            }
        }

        OrientacaoIA orientacao;
        try {
            orientacao = orientacaoIA.gerar(termoLimpo);
        } catch (RuntimeException e) {
            orientacao = OrientacaoIA.indisponivel();
        }

        return new ResultadoBusca(validacao, resultados, orientacao);
    }
}
