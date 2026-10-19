package recursoslai;


public class CGUHandler extends InstanciaHandler {

    private final boolean vaiDeferir;

    public CGUHandler(boolean vaiDeferir) {
        this.vaiDeferir = vaiDeferir;
    }

    @Override
    protected boolean tratar(Recurso recurso) {
        System.out.println("   -> " + nomeInstancia() + " verificando admissibilidade do recurso " + recurso.getProtocolo() + "...");

        if (!recurso.isOrgaoDoPoderExecutivoFederal()) {
            System.out.println("   -> " + nomeInstancia() + " NÃO CONHECE o recurso (órgão recorrido fora do Poder Executivo Federal - art. 16 da LAI e art. 23 do Decreto 7.724/2012); encaminhando à instância final.");
            return false;
        }

        if (vaiDeferir) {
            recurso.decidir(Recurso.Status.DEFERIDO, nomeInstancia(),
                "CGU conheceu o recurso e deferiu o acesso à informação.");
            return true;
        }

        return false; 
    }

    @Override
    protected String nomeInstancia() {
        return "3ª Instância (CGU)";
    }
}
