/**
 * Demonstração do Factory Method no fluxo de resposta a um Pedido de Acesso (Informa.BR).
 * Executar:  npm install && npm start
 */
import assert from "node:assert/strict";
import { AgentePublico, PedidoAcesso, StatusManifestacao } from "./dominio";
import {
  DadosRespostaInvalidosError,
  FabricaResposta,
  FabricaRespostaDeferida,
  FabricaRespostaIndeferida,
  FabricaRespostaParcial,
} from "./fabricas";
import { RespostaIndeferida, RespostaParcialmenteDeferida } from "./resposta";

/**
 * Decisão da análise do órgão — são os gateways do BPMN da Entrega 02
 * ("Admissível?" e "Informação pública?"). A escolha da fábrica concreta fica
 * em um único ponto; o resto do sistema só conhece a abstração FabricaResposta.
 */
type Decisao = "PUBLICA" | "PARCIAL" | "NEGADA";
const fabricaPara: Record<Decisao, FabricaResposta> = {
  PUBLICA: new FabricaRespostaDeferida(),
  PARCIAL: new FabricaRespostaParcial(),
  NEGADA: new FabricaRespostaIndeferida(),
};

const agente = new AgentePublico("Ana Souza", "SIAPE-123456", "Analista do SIC");

// --- Cenário 1: informação pública → Resposta Deferida
const p1 = new PedidoAcesso("50001.000001/2026-01", "Contratos de TI do órgão em 2025");
const r1 = agente.elaborarResposta(p1, fabricaPara.PUBLICA, {
  texto: "Segue a relação de contratos solicitada.",
  linkAcesso: "https://exemplo.gov.br/contratos-ti-2025.csv",
  formatoArquivo: "CSV",
});
console.log(`[1] ${p1.protocolo} → ${r1.tipo} | status=${p1.status} | cabe recurso? ${r1.cabeRecurso()}`);
assert.equal(r1.tipo, "Deferida");
assert.equal(p1.status, StatusManifestacao.RESPONDIDO);
assert.equal(r1.publicada, true);

// --- Cenário 2: parte da informação tem dado pessoal → Resposta Parcialmente Deferida
const p2 = new PedidoAcesso("50001.000002/2026-02", "Folha de pagamento da unidade X");
const r2 = agente.elaborarResposta(p2, fabricaPara.PARCIAL, {
  texto: "Fornecida a folha com CPF e endereço dos servidores ocultados.",
  partesOcultadas: "CPF, endereço residencial",
  justificativaRestricao: "Informação pessoal relativa à intimidade",
  enquadramentoLGPD: "LAI art. 31; LGPD art. 6º, III (necessidade)",
});
assert.ok(r2 instanceof RespostaParcialmenteDeferida);
console.log(`[2] ${p2.protocolo} → ${r2.tipo} | prazo recursal: ${r2.indicarPrazoRecursal()}`);

// --- Cenário 3: informação sigilosa → Resposta Indeferida
const p3 = new PedidoAcesso("50001.000003/2026-03", "Plano de segurança da sede do órgão");
const r3 = agente.elaborarResposta(p3, fabricaPara.NEGADA, {
  texto: "Pedido negado por se tratar de informação classificada.",
  motivoNegativa: "Informação classificada como reservada",
  dispositivoLegalLAI: "LAI art. 23, VII",
  autoridadeRecursal: "Autoridade hierarquicamente superior (1ª instância)",
});
assert.ok(r3 instanceof RespostaIndeferida);
console.log(`[3] ${p3.protocolo} → ${r3.tipo} | recurso: ${r3.indicarAutoridadeRecursal()}`);

// --- Cenário 4: a fábrica barra a criação de uma resposta parcial sem base legal (privacidade)
const p4 = new PedidoAcesso("50001.000004/2026-04", "Lista de beneficiários com endereço");
assert.throws(
  () => agente.elaborarResposta(p4, fabricaPara.PARCIAL, { texto: "Segue lista.", partesOcultadas: "endereço" }),
  DadosRespostaInvalidosError,
);
assert.equal(p4.status, StatusManifestacao.EM_ANALISE); // nada foi vinculado
console.log(`[4] ${p4.protocolo} → criação barrada pela fábrica; status continua ${p4.status}`);

console.log("\nTodos os cenários passaram ✔");
