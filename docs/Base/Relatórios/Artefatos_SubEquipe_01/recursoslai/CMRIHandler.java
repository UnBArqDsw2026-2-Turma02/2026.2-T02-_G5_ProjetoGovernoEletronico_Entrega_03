package recursoslai;

public class CMRIHandler extends InstanciaHandler {

    private final boolean vaiDeferir;

    public CMRIHandler(boolean vaiDeferir) {
        this.vaiDeferir = vaiDeferir;
    }

    @Override
    protected boolean tratar(Recurso recurso) {
        System.out.println("   -> " + nomeInstancia() + " julgando em última instância administrativa o recurso " + recurso.getProtocolo() + "...");
        if (vaiDeferir) {
            recurso.decidir(Recurso.Status.DEFERIDO, nomeInstancia(),
                "CMRI deferiu o acesso à informação em última instância administrativa.");
        } else {
            recurso.decidir(Recurso.Status.INDEFERIDO, nomeInstancia(),
                "CMRI manteve a negativa de acesso em última instância administrativa.");
        }
        return true; 
    }

    @Override
    protected String nomeInstancia() {
        return "4ª Instância (CMRI)";
    }
}
