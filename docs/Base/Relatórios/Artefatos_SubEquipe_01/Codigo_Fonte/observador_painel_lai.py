from collections.abc import Callable

from .observador import Observador


class ObservadorPainelLAI(Observador):
    def __init__(
        self,
        consultar_estado: Callable[
            [], dict[str, str | int | bool]
        ],
    ) -> None:
        self._consultar_estado = consultar_estado

        self.indicadores: dict[str, str | int] = {
            "estado": "SEM_PEDIDO",
            "pedidos_registrados": 0,
            "pedidos_respondidos": 0,
            "pedidos_publicados": 0,
        }

    def atualizar(self) -> None:
        pedido = self._consultar_estado()
        estado = str(pedido["estado"])

        self.indicadores = {
            "estado": estado,
            "pedidos_registrados": 1,
            "pedidos_respondidos": int(
                estado in {
                    "RESPONDIDO",
                    "AUTORIZADO",
                    "PUBLICADO",
                }
            ),
            "pedidos_publicados": int(
                estado == "PUBLICADO"
            ),
        }