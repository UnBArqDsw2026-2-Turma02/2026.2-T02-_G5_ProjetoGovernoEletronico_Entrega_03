from abc import abstractmethod
from typing import Callable, Protocol
from dataclasses import dataclass, replace
from enum import Enum


RegistroDeChamada = Callable[[str, str, str, str], None]


class Etapa(str, Enum):
    REGISTRADO = "REGISTRADO"
    EM_ANALISE = "EM_ANALISE"
    RESPONDIDO = "RESPONDIDO"
    AUTORIZADO = "AUTORIZADO"
    PUBLICADO = "PUBLICADO"


@dataclass(frozen=True)
class PedidoLAI:
    protocolo: str
    assunto: str
    orgao: str
    descricao: str
    estado: Etapa = Etapa.REGISTRADO
    resposta: str = ""
    autorizado: bool = False
    revisao: int = 1
    criado_em: str = ""


class Observador(Protocol):
    @abstractmethod
    def atualizar(self) -> None:
        raise NotImplementedError("O observador concreto precisa implementar atualizar().")


class Sujeito(Protocol):
    @abstractmethod
    def adicionar(self, observador: Observador) -> None:
        raise NotImplementedError("O sujeito concreto precisa implementar adicionar().")

    @abstractmethod
    def remover(self, observador: Observador) -> None:
        raise NotImplementedError("O sujeito concreto precisa implementar remover().")

    @abstractmethod
    def notificar(self) -> None:
        raise NotImplementedError("O sujeito concreto precisa implementar notificar().")


class SujeitoPedidoLAI(Sujeito):

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


class ObservadorBuscaLAI(Observador):

    def __init__(self, sujeito: SujeitoPedidoLAI, registrar: RegistroDeChamada):
        self._sujeito = sujeito
        self._registrar = registrar
        self.consultas = 0
        self.indice_publico: list[dict] = []
        self.ultima_revisao = 0

    def atualizar(self) -> None:
        self._registrar("ObservadorBuscaLAI", "atualizar()", "Recebeu a notificação; vai consultar o sujeito.", "observador")
        pedido = self._sujeito.getEstado()
        self.consultas += 1
        self.ultima_revisao = pedido.revisao
        if pedido.estado == Etapa.PUBLICADO and pedido.autorizado:
            self.indice_publico = [{"protocolo": pedido.protocolo, "descricao": "Registro demonstrativo de pedido publicado."}]
            mensagem = "Índice público simulado atualizado (sem texto pessoal)."
        else:
            mensagem = "Consultou o estado; nada publicável ainda."
        self._registrar("ObservadorBuscaLAI", "atualizar()", mensagem, "efeito")


class ObservadorDadosAbertos(Observador):

    def __init__(self, sujeito: SujeitoPedidoLAI, registrar: RegistroDeChamada):
        self._sujeito = sujeito
        self._registrar = registrar
        self.consultas = 0
        self.registros_publicos: list[dict] = []
        self.ultima_revisao = 0

    def atualizar(self) -> None:
        self._registrar("ObservadorDadosAbertos", "atualizar()", "Recebeu a notificação; vai consultar o sujeito.", "observador")
        pedido = self._sujeito.getEstado()
        self.consultas += 1
        self.ultima_revisao = pedido.revisao
        if pedido.estado == Etapa.PUBLICADO and pedido.autorizado:
            self.registros_publicos = [{"protocolo": pedido.protocolo, "situacao": "PUBLICADO", "revisao": pedido.revisao}]
            mensagem = "Metadados públicos simulados exportados."
        else:
            mensagem = "Consultou o estado; exportação ainda bloqueada."
        self._registrar("ObservadorDadosAbertos", "atualizar()", mensagem, "efeito")


class ObservadorPainelLAI(Observador):

    def __init__(self, sujeito: SujeitoPedidoLAI, registrar: RegistroDeChamada):
        self._sujeito = sujeito
        self._registrar = registrar
        self.consultas = 0
        self.total_registrados = 0
        self.total_respondidos = 0
        self.total_publicados = 0
        self.status_visualizado = "SEM_PEDIDO"
        self.ultima_revisao = 0

    def atualizar(self) -> None:
        self._registrar("ObservadorPainelLAI", "atualizar()", "Recebeu a notificação; vai consultar o sujeito.", "observador")
        pedido = self._sujeito.getEstado()
        self.consultas += 1
        self.ultima_revisao = pedido.revisao
        self.status_visualizado = pedido.estado.value
        self.total_registrados = 1
        self.total_respondidos = int(pedido.estado in {Etapa.RESPONDIDO, Etapa.AUTORIZADO, Etapa.PUBLICADO})
        self.total_publicados = int(pedido.estado == Etapa.PUBLICADO)
        self._registrar("ObservadorPainelLAI", "atualizar()", f"Indicadores recalculados ({pedido.estado.value}).", "efeito")
