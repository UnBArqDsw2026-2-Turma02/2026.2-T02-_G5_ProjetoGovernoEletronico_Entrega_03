package recursoslai;

import java.util.Scanner;

public class TesteManual {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("=== TESTE MANUAL — GoF Chain of Responsibility — Recursos da LAI ===");
        System.out.println("Responda as perguntas abaixo. A cadeia (Validador -> 1a -> 2a -> CGU -> CMRI)");
        System.out.println("vai processar o recurso EM TEMPO REAL, de acordo com o que for digitado.\n");

        System.out.print("Protocolo do recurso (ex.: REC-0099): ");
        String protocolo = linhaOuPadrao(sc, "REC-0099");

        System.out.print("Nome do cidadão: ");
        String cidadao = linhaOuPadrao(sc, "Cidadão de Teste");

        boolean tempestivo = perguntarSimNao(sc,
            "O recurso foi interposto dentro do prazo de 10 dias corridos (tempestivo)? (s/n): ");
        boolean executivoFederal = perguntarSimNao(sc,
            "O órgão recorrido pertence ao Poder Executivo Federal? (s/n): ");

        Recurso recurso = new Recurso(protocolo, cidadao, tempestivo, executivoFederal);

        boolean deferir1a = false, deferir2a = false, deferirCGU = false, deferirCMRI = false;
        if (tempestivo) {
            deferir1a = perguntarSimNao(sc,
                "A 1ª instância (Autoridade Hierárquica Superior) vai DEFERIR o recurso? (s/n): ");
            if (!deferir1a) {
                deferir2a = perguntarSimNao(sc,
                    "A 2ª instância (Autoridade Máxima do Órgão) vai DEFERIR o recurso? (s/n): ");
                if (!deferir2a) {
                    if (executivoFederal) {
                        deferirCGU = perguntarSimNao(sc,
                            "A 3ª instância (CGU) vai DEFERIR o recurso? (s/n): ");
                    } else {
                        System.out.println("(Órgão fora do Executivo Federal: a CGU não vai conhecer o mérito do recurso.)");
                    }
                    if (!deferirCGU) {
                        deferirCMRI = perguntarSimNao(sc,
                            "A 4ª instância (CMRI) vai DEFERIR o recurso? (s/n): ");
                    }
                }
            }
        }

        InstanciaHandler validador = new ValidadorTempestividadeHandler();
        InstanciaHandler primeira = new AutoridadeHierarquicaSuperiorHandler(deferir1a);
        InstanciaHandler segunda = new AutoridadeMaximaOrgaoHandler(deferir2a);
        InstanciaHandler cgu = new CGUHandler(deferirCGU);
        InstanciaHandler cmri = new CMRIHandler(deferirCMRI);

        validador.encadear(primeira).encadear(segunda).encadear(cgu).encadear(cmri);

        System.out.println("\n--- Iniciando tramitação pela Cadeia de Responsabilidade ---");
        System.out.println("Recurso antes do processamento: " + recurso);
        System.out.println();

        validador.handle(recurso);

        System.out.println();
        System.out.println(">>> RESULTADO FINAL: " + recurso);

        sc.close();
    }

    private static boolean perguntarSimNao(Scanner sc, String pergunta) {
        while (true) {
            System.out.print(pergunta);
            String resp = sc.nextLine().trim().toLowerCase();
            if (resp.equals("s") || resp.equals("sim")) return true;
            if (resp.equals("n") || resp.equals("nao") || resp.equals("não")) return false;
            System.out.println("Resposta inválida. Digite 's' ou 'n'.");
        }
    }

    private static String linhaOuPadrao(Scanner sc, String padrao) {
        String linha = sc.nextLine().trim();
        return linha.isEmpty() ? padrao : linha;
    }
}
