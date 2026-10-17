from collections.abc import Callable

from .observador import Observador


class ObservadorDadosAbertos(Observador):
    def __init__(
        self,
        consultar_estado: Callable[
            [], dict[str, str | int | bool]
        ],
    ) -> None:
        self._consultar_estado = consultar_estado

        self.registros_publicos: list[
            dict[str, str | int]
        ] = []

    def atualizar(self) -> None:
        pedido = self._consultar_estado()

        if (
            pedido["estado"] == "PUBLICADO"
            and pedido["autorizado"]
        ):
            self.registros_publicos = [{
                "protocolo": str(pedido["protocolo"]),
                "estado": str(pedido["estado"]),
                "revisao": int(pedido["revisao"]),
            }]