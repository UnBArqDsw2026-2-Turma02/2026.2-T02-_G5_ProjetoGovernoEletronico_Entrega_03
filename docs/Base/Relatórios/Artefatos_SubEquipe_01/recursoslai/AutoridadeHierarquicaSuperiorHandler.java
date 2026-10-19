package recursoslai;

public class AutoridadeHierarquicaSuperiorHandler extends InstanciaHandler {

    private final boolean vaiDeferir;

    public AutoridadeHierarquicaSuperiorHandler(boolean vaiDeferir) {
        this.vaiDeferir = vaiDeferir;
    }

    @Override
    protected boolean tratar(Recurso recurso) {
        System.out.println("   -> " + nomeInstancia() + " analisando o recurso " + recurso.getProtocolo() + "...");
        if (vaiDeferir) {
            recurso.decidir(Recurso.Status.DEFERIDO, nomeInstancia(),
                "Autoridade hierárquica superior reconheceu o direito de acesso e deferiu o recurso.");
            return true;
        }
        return false;
    }

    @Override
    protected String nomeInstancia() {
        return "1ª Instância (Autoridade Hierárquica Superior)";
    }
}
