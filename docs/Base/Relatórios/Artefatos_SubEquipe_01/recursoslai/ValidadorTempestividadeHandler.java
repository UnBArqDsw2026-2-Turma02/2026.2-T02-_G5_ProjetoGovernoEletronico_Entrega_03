package recursoslai;

public class ValidadorTempestividadeHandler extends InstanciaHandler {

    @Override
    protected boolean tratar(Recurso recurso) {
        if (!recurso.isTempestivo()) {
            recurso.decidir(
                Recurso.Status.INTEMPESTIVO,
                nomeInstancia(),
                "Recurso interposto fora do prazo de 10 dias corridos (art. 15 da Lei 12.527/2011)."
            );
            return true; 
        }
        return false; 
    }

    @Override
    protected String nomeInstancia() {
        return "Validador de Tempestividade";
    }
}
