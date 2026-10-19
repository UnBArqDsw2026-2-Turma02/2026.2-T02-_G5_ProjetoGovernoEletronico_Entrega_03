export interface PedidoState {
    enviar(pedido: PedidoContext): void;
    cancelar(pedido: PedidoContext): void;
    recorrer(pedido: PedidoContext): void;
    getStatus(): 'draft' | 'analysis' | 'answered';
}

export class PedidoContext {
    private estadoAtual: PedidoState;

    constructor(estadoInicial: PedidoState) {
        this.estadoAtual = estadoInicial;
    }

    setEstado(novoEstado: PedidoState) {
        this.estadoAtual = novoEstado;
    }

    enviar() { this.estadoAtual.enviar(this); }
    cancelar() { this.estadoAtual.cancelar(this); }
    recorrer() { this.estadoAtual.recorrer(this); }
    getStatus() { return this.estadoAtual.getStatus(); }
}

export class RascunhoState implements PedidoState {
    enviar(pedido: PedidoContext): void {
        console.log("Enviando pedido...");
        pedido.setEstado(new AnaliseState());
    }
    cancelar(pedido: PedidoContext): void {
        console.log("Rascunho cancelado.");
    }
    recorrer(pedido: PedidoContext): void {
        console.log("Erro: Não é possível recorrer de um rascunho.");
    }
    getStatus(): 'draft' { return 'draft'; }
}

export class AnaliseState implements PedidoState {
    enviar(pedido: PedidoContext): void {
        console.log("Aviso: Já está em análise.");
    }
    cancelar(pedido: PedidoContext): void {
        console.log("Pedido em análise cancelado.");
    }
    recorrer(pedido: PedidoContext): void {
        console.log("Aviso: Aguarde a resposta.");
    }
    getStatus(): 'analysis' { return 'analysis'; }
}

export class RespondidoState implements PedidoState {
    enviar(pedido: PedidoContext): void {
        console.log("Erro: Já respondido.");
    }
    cancelar(pedido: PedidoContext): void {
        console.log("Erro: Não é possível cancelar agora.");
    }
    recorrer(pedido: PedidoContext): void {
        console.log("Recorrendo... Voltando para análise.");
        pedido.setEstado(new AnaliseState());
    }
    getStatus(): 'answered' { return 'answered'; }
}