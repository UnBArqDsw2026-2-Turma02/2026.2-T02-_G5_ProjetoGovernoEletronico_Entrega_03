from collections.abc import Callable

from .observador import Observador


class ObservadorBuscaLAI(Observador):
    def __init__(
        self,
        consultar_estado: Callable[
            [], dict[str, str | int | bool]
        ],
    ) -> None:
        self._consultar_estado = consultar_estado
        self.indice_publico: list[dict[str, str]] = []

    def atualizar(self) -> None:
        pedido = self._consultar_estado()

        if (
            pedido["estado"] == "PUBLICADO"
            and pedido["autorizado"]
        ):
            self.indice_publico = [{
                "protocolo": str(pedido["protocolo"]),
                "assunto": str(pedido["assunto"]),
                "resposta": str(pedido["resposta"]),
            }]