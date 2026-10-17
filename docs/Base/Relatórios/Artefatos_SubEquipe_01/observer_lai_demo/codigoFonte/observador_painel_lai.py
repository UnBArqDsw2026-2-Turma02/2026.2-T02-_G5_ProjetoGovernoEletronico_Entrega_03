from .etapa_pedido import Etapa
from .observador import Observador
from .fonte_estado_pedido import FonteEstadoPedido
from .tipos import RegistroDeChamada


class ObservadorPainelLAI(Observador):

    def __init__(self, sujeito: FonteEstadoPedido, registrar: RegistroDeChamada):
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
