public class GeradorOrientacaoIA {

    public OrientacaoIA gerar(String termo) {
        System.out.println("  [GeradorOrientacaoIA] gerando orientação simulada sobre: " + termo);
        return OrientacaoIA.gerada("Simulação: a consulta \"" + termo
                + "\" parece buscar informações públicas relacionadas ao tema. "
                + "Consulte as abas de resultados para os registros oficiais.");
    }
}
