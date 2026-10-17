from .sujeito import Sujeito


class SujeitoPedidoLAI(Sujeito):
    _proximas_etapas = {
        "REGISTRADO": "EM_ANALISE",
        "EM_ANALISE": "RESPONDIDO",
        "RESPONDIDO": "AUTORIZADO",
        "AUTORIZADO": "PUBLICADO",
    }

    def __init__(self) -> None:
        super().__init__()
        self._pedido: dict[str, str | int | bool] | None = None

    def criarPedido(self, dados: dict[str, str]) -> None:
        if self._pedido is not None:
            raise ValueError("Já existe um pedido registrado.")

        campos_obrigatorios = (
            "protocolo",
            "assunto",
            "orgao",
            "descricao",
        )

        if any(
            not dados.get(campo, "").strip()
            for campo in campos_obrigatorios
        ):
            raise ValueError(
                "Informe protocolo, assunto, órgão e descrição."
            )

        self._pedido = {
            campo: dados[campo].strip()
            for campo in campos_obrigatorios
        }

        self._pedido.update({
            "estado": "REGISTRADO",
            "resposta": "",
            "autorizado": False,
            "revisao": 1,
        })

        self.notificar()

    def setEstado(
        self,
        novo_estado: str,
        resposta: str = "",
    ) -> None:
        if self._pedido is None:
            raise ValueError("Nenhum pedido foi criado.")

        estado_atual = str(self._pedido["estado"])

        if self._proximas_etapas.get(estado_atual) != novo_estado:
            raise ValueError("Transição de estado inválida.")

        if novo_estado == "RESPONDIDO" and not resposta.strip():
            raise ValueError(
                "É necessário informar a resposta do pedido."
            )

        self._pedido["estado"] = novo_estado
        self._pedido["revisao"] = (
            int(self._pedido["revisao"]) + 1
        )

        if novo_estado == "RESPONDIDO":
            self._pedido["resposta"] = resposta.strip()

        if novo_estado == "AUTORIZADO":
            self._pedido["autorizado"] = True

        self.notificar()

    def getEstado(self) -> dict[str, str | int | bool]:
        if self._pedido is None:
            raise ValueError("Nenhum pedido foi criado.")

        return self._pedido.copy()