package recursoslai;

public class TesteAutomatizado {

    private static int totalTestes = 0;
    private static int falhas = 0;

    public static void main(String[] args) {

        testeIntempestivoEhBarradoNoValidador();
        testeDeferidoNa1aInstanciaNaoAvancaNaCadeia();
        testeIndeferidoNa1aAvancaParaA2a();
        testeCguNaoConheceMasNaoEncerraCadeia();
        testeCmriEhUltimoElogEEsgotaViaRecursal();
        testeCadeiaSemProximoEloEsgotaAutomaticamente();

        System.out.println();
        System.out.println("=================================================");
        System.out.println("Total de testes: " + totalTestes + " | Falhas: " + falhas);
        if (falhas == 0) {
            System.out.println("TODOS OS TESTES PASSARAM ✔");
        } else {
            System.out.println("HÁ TESTES COM FALHA ✘");
        }
        System.out.println("=================================================");

        if (falhas > 0) {
            System.exit(1);
        }
    }



    private static void testeIntempestivoEhBarradoNoValidador() {
        Recurso r = new Recurso("T01", "Teste", false, true);
        InstanciaHandler cadeia = new ValidadorTempestividadeHandler();
        cadeia.encadear(new CMRIHandler(true)); 
        cadeia.handle(r);

        verificar("Recurso intempestivo deve ser barrado no Validador",
            r.getStatus() == Recurso.Status.INTEMPESTIVO
            && "Validador de Tempestividade".equals(r.getInstanciaResponsavelPelaDecisao()));
    }

    private static void testeDeferidoNa1aInstanciaNaoAvancaNaCadeia() {
        Recurso r = new Recurso("T02", "Teste", true, true);
        InstanciaHandler validador = new ValidadorTempestividadeHandler();
        InstanciaHandler primeira = new AutoridadeHierarquicaSuperiorHandler(true);
        validador.encadear(primeira).encadear(new CMRIHandler(false)); 
        validador.handle(r);

        verificar("Recurso deferido na 1ª instância deve parar ali (não chegar à CMRI)",
            r.getStatus() == Recurso.Status.DEFERIDO
            && r.getInstanciaResponsavelPelaDecisao().contains("1ª Instância"));
    }

    private static void testeIndeferidoNa1aAvancaParaA2a() {
        Recurso r = new Recurso("T03", "Teste", true, true);
        InstanciaHandler primeira = new AutoridadeHierarquicaSuperiorHandler(false);
        InstanciaHandler segunda = new AutoridadeMaximaOrgaoHandler(true);
        primeira.encadear(segunda);
        primeira.handle(r);

        verificar("Recurso indeferido na 1ª instância deve ser decidido na 2ª",
            r.getStatus() == Recurso.Status.DEFERIDO
            && r.getInstanciaResponsavelPelaDecisao().contains("2ª Instância"));
    }

    private static void testeCguNaoConheceMasNaoEncerraCadeia() {
        Recurso r = new Recurso("T04", "Teste", true, false); 
        InstanciaHandler cgu = new CGUHandler(false);
        InstanciaHandler cmri = new CMRIHandler(true);
        cgu.encadear(cmri);
        cgu.handle(r);

        verificar("CGU não conhecer o recurso não deve esgotar a via recursal (deve seguir até a CMRI)",
            r.getStatus() == Recurso.Status.DEFERIDO
            && r.getInstanciaResponsavelPelaDecisao().contains("CMRI"));
    }

    private static void testeCmriEhUltimoElogEEsgotaViaRecursal() {
        Recurso r = new Recurso("T05", "Teste", true, true);
        InstanciaHandler cmri = new CMRIHandler(false);
        cmri.handle(r);

        verificar("CMRI negando deve resultar em INDEFERIDO (fim da via administrativa)",
            r.getStatus() == Recurso.Status.INDEFERIDO
            && r.getInstanciaResponsavelPelaDecisao().contains("CMRI"));
    }

    private static void testeCadeiaSemProximoEloEsgotaAutomaticamente() {
        Recurso r = new Recurso("T06", "Teste", true, true);
        InstanciaHandler semSaida = new AutoridadeHierarquicaSuperiorHandler(false);
        semSaida.handle(r);

        verificar("Handler sem próximo elo e que não decide deve esgotar a via recursal automaticamente",
            r.getStatus() == Recurso.Status.ESGOTADA_VIA_RECURSAL);
    }


    private static void verificar(String descricao, boolean condicao) {
        totalTestes++;
        if (condicao) {
            System.out.println("[OK]    " + descricao);
        } else {
            falhas++;
            System.out.println("[FALHA] " + descricao);
        }
    }
}
