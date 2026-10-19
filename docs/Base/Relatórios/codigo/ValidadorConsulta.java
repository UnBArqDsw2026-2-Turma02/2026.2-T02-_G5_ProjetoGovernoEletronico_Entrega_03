public class ValidadorConsulta {

    public ValidacaoConsulta validar(String termo) {
        System.out.println("  [ValidadorConsulta] validando termo");
        if (termo == null || termo.isBlank()) {
            return new ValidacaoConsulta(false, "Informe um termo para realizar a busca.");
        }
        return new ValidacaoConsulta(true, "Consulta válida.");
    }
}
