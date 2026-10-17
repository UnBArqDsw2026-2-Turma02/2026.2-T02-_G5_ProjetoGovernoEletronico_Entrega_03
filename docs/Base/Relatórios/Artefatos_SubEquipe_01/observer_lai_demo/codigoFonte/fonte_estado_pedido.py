from abc import abstractmethod
from typing import Protocol

from .modelo_pedido import PedidoLAI


class FonteEstadoPedido(Protocol):
    @abstractmethod
    def getEstado(self) -> PedidoLAI:
        raise NotImplementedError("A fonte de estado precisa implementar getEstado().")
