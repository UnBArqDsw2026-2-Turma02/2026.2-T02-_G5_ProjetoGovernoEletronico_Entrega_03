/**
 * Classes de domínio mínimas, vindas do Diagrama de Classes (Herança) da Entrega 02.
 * Só foi mantido o necessário para demonstrar o Factory Method.
 */

export enum StatusManifestacao {
  EM_ELABORACAO = "EM_ELABORACAO",
  PROTOCOLADO = "PROTOCOLADO",
  EM_ANALISE = "EM_ANALISE",
  AGUARDANDO_COMPLEMENTACAO = "AGUARDANDO_COMPLEMENTACAO",
  RESPONDIDO = "RESPONDIDO",
  EM_RECURSO_1 = "EM_RECURSO_1",
  EM_RECURSO_2 = "EM_RECURSO_2",
  ENCERRADO = "ENCERRADO",
  CANCELADO = "CANCELADO",
}

// Import apenas de tipo: evita dependência circular em tempo de execução.
import type { Resposta } from "./resposta";
import type { FabricaResposta, DadosResposta } from "./fabricas";

export class PedidoAcesso {
  private _status: StatusManifestacao = StatusManifestacao.EM_ANALISE;
  private _resposta?: Resposta;

  constructor(
    public readonly protocolo: string,
    public readonly descricao: string,
  ) {}

  get status(): StatusManifestacao {
    return this._status;
  }

  get resposta(): Resposta | undefined {
    return this._resposta;
  }

  vincularResposta(resposta: Resposta): void {
    if (this._status !== StatusManifestacao.EM_ANALISE) {
      throw new Error(`Pedido ${this.protocolo} não está em análise (status atual: ${this._status}).`);
    }
    this._resposta = resposta;
    this._status = StatusManifestacao.RESPONDIDO;
  }
}

export class AgentePublico {
  constructor(
    public readonly nome: string,
    public readonly matricula: string,
    public readonly cargo: string,
  ) {}

  /**
   * CLIENTE do padrão: o agente não conhece nenhuma subclasse concreta de Resposta.
   * Ele só recebe uma FabricaResposta (escolhida pela decisão da análise) e pede a emissão.
   */
  elaborarResposta(pedido: PedidoAcesso, fabrica: FabricaResposta, dados: DadosResposta): Resposta {
    return fabrica.emitirResposta(pedido, this, dados);
  }
}
