from .etapa_pedido import Etapa
from .observador import Observador
from .fonte_estado_pedido import FonteEstadoPedido
from .tipos import RegistroDeChamada


class ObservadorBuscaLAI(Observador):

    def __init__(self, sujeito: FonteEstadoPedido, registrar: RegistroDeChamada):
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
