package recursoslai;

public abstract class InstanciaHandler {

    private InstanciaHandler proximo;

    public InstanciaHandler encadear(InstanciaHandler proximo) {
        this.proximo = proximo;
        return proximo;
    }

    public final void handle(Recurso recurso) {
        boolean tratouNestaInstancia = tratar(recurso);
        if (!tratouNestaInstancia) {
            if (proximo != null) {
                System.out.println("   -> " + nomeInstancia() + " não decidiu; repassando para o próximo elo da cadeia...");
                proximo.handle(recurso);
            } else {
                recurso.decidir(
                    Recurso.Status.ESGOTADA_VIA_RECURSAL,
                    nomeInstancia(),
                    "Via recursal administrativa esgotada (não há próxima instância na cadeia)."
                );
            }
        }
    }

    protected abstract boolean tratar(Recurso recurso);

    protected abstract String nomeInstancia();
}
