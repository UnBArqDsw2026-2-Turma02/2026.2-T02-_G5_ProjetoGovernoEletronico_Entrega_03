/**
 * CREATOR e CONCRETE CREATORS do Factory Method (GoF, padrão criacional).
 *
 * FabricaResposta.emitirResposta() guarda o processo que vale para qualquer resposta:
 * criar, vincular ao pedido e publicar.
 * O passo que muda — QUAL resposta criar e QUAIS regras validar — fica no método
 * fábrica criarResposta(), implementado por cada subclasse.
 */
import { AgentePublico, PedidoAcesso } from "./dominio";
import {
  Resposta,
  RespostaDeferida,
  RespostaIndeferida,
  RespostaParcialmenteDeferida,
} from "./resposta";

/** Dados que o agente informa ao elaborar a resposta. Cada fábrica exige os seus campos. */
export interface DadosResposta {
  texto: string;
  linkAcesso?: string;
  formatoArquivo?: string;
  partesOcultadas?: string;
  justificativaRestricao?: string;
  enquadramentoLGPD?: string;
  motivoNegativa?: string;
  dispositivoLegalLAI?: string;
  autoridadeRecursal?: string;
}

export class DadosRespostaInvalidosError extends Error {}

function exigir(dados: DadosResposta, campos: (keyof DadosResposta)[], contexto: string): void {
  const faltando = campos.filter((c) => !dados[c] || String(dados[c]).trim() === "");
  if (faltando.length > 0) {
    throw new DadosRespostaInvalidosError(`${contexto}: campos obrigatórios ausentes → ${faltando.join(", ")}`);
  }
}

// ---------------------------------------------------------------- Creator
export abstract class FabricaResposta {
  /** Processo de emissão: igual para todos os tipos de resposta. */
  emitirResposta(pedido: PedidoAcesso, agente: AgentePublico, dados: DadosResposta): Resposta {
    exigir(dados, ["texto"], "Resposta");
    const resposta = this.criarResposta(dados, agente); // ← factory method
    pedido.vincularResposta(resposta);
    resposta.publicar();
    return resposta;
  }

  /** FACTORY METHOD: cada subclasse decide qual Resposta concreta instanciar. */
  protected abstract criarResposta(dados: DadosResposta, agente: AgentePublico): Resposta;
}

// ------------------------------------------------------- Concrete Creators
export class FabricaRespostaDeferida extends FabricaResposta {
  protected criarResposta(d: DadosResposta, agente: AgentePublico): Resposta {
    exigir(d, ["linkAcesso", "formatoArquivo"], "Resposta deferida");
    return new RespostaDeferida(d.texto, agente.nome, d.linkAcesso!, d.formatoArquivo!);
  }
}

export class FabricaRespostaParcial extends FabricaResposta {
  /** Privacidade: o acesso parcial só pode ser criado com a parte ocultada e a base legal (LAI art. 7º §2º; LGPD). */
  protected criarResposta(d: DadosResposta, agente: AgentePublico): Resposta {
    exigir(d, ["partesOcultadas", "justificativaRestricao", "enquadramentoLGPD"], "Resposta parcialmente deferida");
    return new RespostaParcialmenteDeferida(
      d.texto,
      agente.nome,
      d.partesOcultadas!,
      d.justificativaRestricao!,
      d.enquadramentoLGPD!,
    );
  }
}

export class FabricaRespostaIndeferida extends FabricaResposta {
  /** Negativa precisa de fundamento legal e de autoridade recursal (LAI art. 11 §1º, II e art. 15). */
  protected criarResposta(d: DadosResposta, agente: AgentePublico): Resposta {
    exigir(d, ["motivoNegativa", "dispositivoLegalLAI", "autoridadeRecursal"], "Resposta indeferida");
    return new RespostaIndeferida(
      d.texto,
      agente.nome,
      d.motivoNegativa!,
      d.dispositivoLegalLAI!,
      d.autoridadeRecursal!,
    );
  }
}
