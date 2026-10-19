from dataclasses import replace

from .etapa_pedido import Etapa
from .modelo_pedido import PedidoLAI
from .observador import Observador
from .sujeito import Sujeito
from .fonte_estado_pedido import FonteEstadoPedido
from .tipos import RegistroDeChamada


class SujeitoPedidoLAI(Sujeito, FonteEstadoPedido):

    def __init__(self, registrar: RegistroDeChamada):
        self._pedido: PedidoLAI | None = None
        self._observadores: list[Observador] = []
        self._registrar = registrar
        self.total_consultas = 0

    def adicionar(self, observador: Observador) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)
            self._registrar("Sujeito", "adicionar()", f"Inscrito: {type(observador).__name__}", "assinatura")

    def remover(self, observador: Observador) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)
            self._registrar("Sujeito", "remover()", f"Removido: {type(observador).__name__}", "assinatura")

    def notificar(self) -> None:
        self._registrar("Sujeito", "notificar()", f"Notificando {len(self._observadores)} observador(es) inscrito(s).", "notificacao")
        for observador in tuple(self._observadores):
            self._registrar("Sujeito", "notificar() → atualizar()", type(observador).__name__, "notificacao")
            observador.atualizar()

    def criarPedido(self, pedido_inicial: PedidoLAI) -> None:
        if self._pedido is not None:
            raise ValueError("Já existe um pedido. Reinicie a simulação para criar outro.")
        self._pedido = pedido_inicial
        self._registrar("SujeitoPedidoLAI", "criarPedido()", f"Pedido {pedido_inicial.protocolo} registrado.", "estado")
        self.notificar()

    def setEstado(self, etapa: Etapa, resposta: str = "") -> None:
        pedido_atual = self._pedido
        if pedido_atual is None:
            raise ValueError("Crie um pedido antes de avançar.")
        transicoes_permitidas = {
            Etapa.REGISTRADO: Etapa.EM_ANALISE,
            Etapa.EM_ANALISE: Etapa.RESPONDIDO,
            Etapa.RESPONDIDO: Etapa.AUTORIZADO,
            Etapa.AUTORIZADO: Etapa.PUBLICADO,
        }
        if transicoes_permitidas.get(pedido_atual.estado) != etapa:
            raise ValueError("Transição inválida. Avance para a próxima etapa indicada.")
        if etapa == Etapa.RESPONDIDO and not resposta.strip():
            raise ValueError("Escreva uma resposta fictícia antes de avançar.")
        pedido_atualizado = replace(
            pedido_atual,
            estado=etapa,
            resposta=resposta.strip() if etapa == Etapa.RESPONDIDO else pedido_atual.resposta,
            autorizado=pedido_atual.autorizado or etapa == Etapa.AUTORIZADO,
            revisao=pedido_atual.revisao + 1,
        )
        self._pedido = pedido_atualizado
        self._registrar("SujeitoPedidoLAI", "setEstado()", f"Estado alterado: {pedido_atual.estado.value} → {etapa.value}.", "estado")
        self.notificar()

    def getEstado(self) -> PedidoLAI:
        if self._pedido is None:
            raise ValueError("Nenhum pedido cadastrado.")
        self.total_consultas += 1
        self._registrar("SujeitoPedidoLAI", "getEstado()", f"Leitura da revisão {self._pedido.revisao}.", "consulta")
        return replace(self._pedido)

    def estado_atual(self) -> PedidoLAI | None:
        return replace(self._pedido) if self._pedido else None

    def inscritos(self) -> list[Observador]:
        return list(self._observadores)
