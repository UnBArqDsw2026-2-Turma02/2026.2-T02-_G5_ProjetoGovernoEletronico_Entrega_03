from dataclasses import dataclass

from .etapa_pedido import Etapa


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
