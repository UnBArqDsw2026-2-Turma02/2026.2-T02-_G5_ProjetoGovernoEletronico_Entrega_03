public class TelaBusca {

    private FachadaBuscaPublica fachada = new FachadaBuscaPublica();

    public void solicitarBusca(String termo) {
        fachada.buscar(termo);
        apresentar();
    }

    public void apresentar() {
        System.out.println("Busca simulada concluída.");
    }

    public static void main(String[] args) {
        TelaBusca tela = new TelaBusca();
        tela.solicitarBusca("educação");
    }
}
