from .etapa_pedido import Etapa
from .observador import Observador
from .fonte_estado_pedido import FonteEstadoPedido
from .tipos import RegistroDeChamada


class ObservadorDadosAbertos(Observador):

    def __init__(self, sujeito: FonteEstadoPedido, registrar: RegistroDeChamada):
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
