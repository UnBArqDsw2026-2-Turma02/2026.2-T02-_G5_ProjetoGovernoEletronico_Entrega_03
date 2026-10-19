public record OrientacaoIA(String texto, String aviso) {

    private static final String AVISO_PADRAO = "Resumo gerado por IA. Pode conter imprecisões.";

    public static OrientacaoIA gerada(String texto) {
        return new OrientacaoIA(texto, AVISO_PADRAO);
    }

    public static OrientacaoIA indisponivel() {
        return new OrientacaoIA("", "Orientação por IA indisponível no momento.");
    }

    public static OrientacaoIA vazia() {
        return new OrientacaoIA("", "");
    }
}
