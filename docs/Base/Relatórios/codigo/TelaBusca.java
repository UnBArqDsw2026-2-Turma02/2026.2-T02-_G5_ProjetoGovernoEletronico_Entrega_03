public class TelaBusca {

    private final FachadaBuscaPublica fachada = new FachadaBuscaPublica();

    public void solicitarBusca(String termo) {
        System.out.println("\n=== Busca: \"" + termo + "\" ===");
        System.out.println("Analisando sua pergunta...");
        ResultadoBusca resultado = fachada.buscar(termo);
        apresentar(resultado);
    }

    public void apresentar(ResultadoBusca resultado) {
        if (!resultado.validacao().valida()) {
            System.out.println("Aviso: " + resultado.validacao().mensagem());
            return;
        }

        OrientacaoIA ia = resultado.orientacao();
        System.out.println("\n[Resumo gerado por IA]");
        if (!ia.texto().isBlank()) {
            System.out.println("  " + ia.texto());
        }
        System.out.println("  (" + ia.aviso() + ")");

        for (ResultadoFonte fonte : resultado.fontes()) {
            System.out.println("\n[Aba: " + fonte.nomeFonte() + "]");
            switch (fonte.status()) {
                case SUCESSO -> fonte.itens().forEach(item ->
                        System.out.println("  - " + item.titulo() + " -> " + item.urlOrigem()));
                case VAZIO -> System.out.println("  Nenhum registro encontrado para esta fonte.");
                case INDISPONIVEL -> System.out.println("  Fonte indisponível no momento. Tente novamente mais tarde.");
            }
        }
        System.out.println("\nBusca simulada concluída.");
    }

    public static void main(String[] args) {
        TelaBusca tela = new TelaBusca();
        tela.solicitarBusca("educação");     // fluxo normal
        tela.solicitarBusca("   ");          // termo em branco (validação)
        tela.solicitarBusca("falha");        // uma fonte indisponível
        tela.solicitarBusca("inexistente");  // uma fonte sem registros
    }
}
