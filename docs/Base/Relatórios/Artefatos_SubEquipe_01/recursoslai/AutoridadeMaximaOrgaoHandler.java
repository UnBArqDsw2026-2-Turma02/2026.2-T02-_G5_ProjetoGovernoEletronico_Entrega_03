package recursoslai;

public class AutoridadeMaximaOrgaoHandler extends InstanciaHandler {

    private final boolean vaiDeferir;

    public AutoridadeMaximaOrgaoHandler(boolean vaiDeferir) {
        this.vaiDeferir = vaiDeferir;
    }

    @Override
    protected boolean tratar(Recurso recurso) {
        System.out.println("   -> " + nomeInstancia() + " analisando o recurso " + recurso.getProtocolo() + "...");
        if (vaiDeferir) {
            recurso.decidir(Recurso.Status.DEFERIDO, nomeInstancia(),
                "Autoridade máxima do órgão reformou a decisão anterior e deferiu o acesso.");
            return true;
        }
        return false;
    }

    @Override
    protected String nomeInstancia() {
        return "2ª Instância (Autoridade Máxima do Órgão)";
    }
}
