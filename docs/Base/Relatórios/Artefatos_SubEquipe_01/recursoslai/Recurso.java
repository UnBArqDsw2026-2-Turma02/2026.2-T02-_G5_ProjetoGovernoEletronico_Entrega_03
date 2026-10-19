package recursoslai;

public class Recurso {

    public enum Status {
        AGUARDANDO_ANALISE,
        INTEMPESTIVO,     
        DEFERIDO,
        INDEFERIDO,
        NAO_CONHECIDO,     
        ESGOTADA_VIA_RECURSAL
    }

    private final String protocolo;
    private final String cidadao;
    private final boolean tempestivo;
    private final boolean orgaoDoPoderExecutivoFederal; 
    private Status status;
    private String instanciaResponsavelPelaDecisao;
    private String motivoDaDecisao;

    public Recurso(String protocolo, String cidadao, boolean tempestivo, boolean orgaoDoPoderExecutivoFederal) {
        this.protocolo = protocolo;
        this.cidadao = cidadao;
        this.tempestivo = tempestivo;
        this.orgaoDoPoderExecutivoFederal = orgaoDoPoderExecutivoFederal;
        this.status = Status.AGUARDANDO_ANALISE;
    }

    public String getProtocolo() { return protocolo; }
    public String getCidadao() { return cidadao; }
    public boolean isTempestivo() { return tempestivo; }
    public boolean isOrgaoDoPoderExecutivoFederal() { return orgaoDoPoderExecutivoFederal; }
    public Status getStatus() { return status; }
    public String getInstanciaResponsavelPelaDecisao() { return instanciaResponsavelPelaDecisao; }
    public String getMotivoDaDecisao() { return motivoDaDecisao; }

    public boolean isDecidido() {
        return status != Status.AGUARDANDO_ANALISE;
    }

    public void decidir(Status status, String instancia, String motivo) {
        this.status = status;
        this.instanciaResponsavelPelaDecisao = instancia;
        this.motivoDaDecisao = motivo;
    }

    @Override
    public String toString() {
        return String.format(
            "Recurso[protocolo=%s, cidadão=%s, status=%s, decidido por=%s, motivo=\"%s\"]",
            protocolo, cidadao, status,
            instanciaResponsavelPelaDecisao == null ? "-" : instanciaResponsavelPelaDecisao,
            motivoDaDecisao == null ? "-" : motivoDaDecisao
        );
    }
}
