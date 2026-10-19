package recursoslai;

public class ChainOfResponsibilityDemo {

    public static void main(String[] args) {

        System.out.println("=== GoF Comportamental: Chain of Responsibility ===");
        System.out.println("=== Fluxo de Recursos da LAI (Informa.BR) ===\n");

        processar(montarCenario1_Intempestivo());
        processar(montarCenario2_DeferidoNa1aInstancia());
        processar(montarCenario3_NaoConhecidoPelaCGU_DeferidoNaCMRI());
        processar(montarCenario4_EsgotaViaRecursal());

        System.out.println("=== Fim da demonstração ===");
    }

    private static void processar(Object[] cenario) {
        String titulo = (String) cenario[0];
        Recurso recurso = (Recurso) cenario[1];
        InstanciaHandler cadeia = (InstanciaHandler) cenario[2];

        System.out.println("---------------------------------------------------------------");
        System.out.println(titulo);
        System.out.println("Recurso inicial: " + recurso);
        cadeia.handle(recurso);
        System.out.println("Resultado final: " + recurso);
        System.out.println();
    }

    private static InstanciaHandler montarCadeiaCompleta(boolean deferir1a, boolean deferir2a, boolean deferirCGU, boolean deferirCMRI) {
        InstanciaHandler validador = new ValidadorTempestividadeHandler();
        InstanciaHandler primeiraInstancia = new AutoridadeHierarquicaSuperiorHandler(deferir1a);
        InstanciaHandler segundaInstancia = new AutoridadeMaximaOrgaoHandler(deferir2a);
        InstanciaHandler cgu = new CGUHandler(deferirCGU);
        InstanciaHandler cmri = new CMRIHandler(deferirCMRI);

        validador.encadear(primeiraInstancia)
                 .encadear(segundaInstancia)
                 .encadear(cgu)
                 .encadear(cmri);

        return validador; 
    }

    private static Object[] montarCenario1_Intempestivo() {
        Recurso recurso = new Recurso("REC-0001", "Maria Oliveira", false, true);
        InstanciaHandler cadeia = montarCadeiaCompleta(false, false, false, false);
        return new Object[] {
            "Cenário 1: Recurso INTEMPESTIVO (barrado antes mesmo da 1ª instância)",
            recurso, cadeia
        };
    }

    private static Object[] montarCenario2_DeferidoNa1aInstancia() {
        Recurso recurso = new Recurso("REC-0002", "João Pereira", true, true);
        InstanciaHandler cadeia = montarCadeiaCompleta( true, false, false, false);
        return new Object[] {
            "Cenário 2: Recurso DEFERIDO já na 1ª instância",
            recurso, cadeia
        };
    }

    private static Object[] montarCenario3_NaoConhecidoPelaCGU_DeferidoNaCMRI() {
        Recurso recurso = new Recurso("REC-0003", "Ana Souza", true,  false);
        InstanciaHandler cadeia = montarCadeiaCompleta(false, false, false, true);
        return new Object[] {
            "Cenário 3: CGU NÃO CONHECE (órgão fora do Executivo Federal) -> segue para a CMRI, que DEFERE",
            recurso, cadeia
        };
    }

    private static Object[] montarCenario4_EsgotaViaRecursal() {
        Recurso recurso = new Recurso("REC-0004", "Carlos Lima", true, true);
        InstanciaHandler cadeia = montarCadeiaCompleta(false, false, false, false);
        return new Object[] {
            "Cenário 4: Negado em TODAS as instâncias -> via administrativa se ESGOTA na CMRI",
            recurso, cadeia
        };
    }
}
