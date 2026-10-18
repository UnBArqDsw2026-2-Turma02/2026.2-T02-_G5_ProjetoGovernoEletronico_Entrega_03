public class FachadaBuscaPublica {

    private ValidadorConsulta validador = new ValidadorConsulta();
    private BuscaPedidosLAI pedidosLAI = new BuscaPedidosLAI();
    private BuscaTransparencia transparencia = new BuscaTransparencia();
    private BuscaDadosAbertos dadosAbertos = new BuscaDadosAbertos();
    private GeradorOrientacaoIA orientacaoIA = new GeradorOrientacaoIA();

    public void buscar(String termo) {
        validador.validar(termo);
        pedidosLAI.consultar(termo);
        transparencia.consultar(termo);
        dadosAbertos.consultar(termo);
        orientacaoIA.gerar(termo);
    }
}
