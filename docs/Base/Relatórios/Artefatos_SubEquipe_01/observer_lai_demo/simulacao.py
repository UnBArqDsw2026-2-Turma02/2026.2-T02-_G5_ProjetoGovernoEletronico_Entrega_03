from dataclasses import asdict
from datetime import datetime, timezone
import inspect
from pathlib import Path
from threading import RLock

from padrao import (
    Etapa, FonteEstadoPedido, Observador, ObservadorBuscaLAI,
    ObservadorDadosAbertos, ObservadorPainelLAI, PedidoLAI, Sujeito,
    SujeitoPedidoLAI,
)


CLASSES = [
    Sujeito,
    SujeitoPedidoLAI,
    Observador,
    ObservadorBuscaLAI,
    ObservadorDadosAbertos,
    ObservadorPainelLAI,
    FonteEstadoPedido,
    PedidoLAI,
    Etapa,
]
ROTULOS = {
    "Sujeito": "Sujeito abstrato",
    "SujeitoPedidoLAI": "Sujeito concreto",
    "Observador": "Contrato de atualização",
    "FonteEstadoPedido": "Contrato de consulta ao estado",
    "ObservadorBuscaLAI": "BuscaLAI • observador concreto",
    "ObservadorDadosAbertos": "Dados Abertos • observador concreto",
    "ObservadorPainelLAI": "Painel LAI • observador concreto",
    "PedidoLAI": "Modelo de dados",
    "Etapa": "Estados possíveis do pedido",
    "MotorSimulacao": "Orquestração da aplicação",
}
OBSERVADORES = {
    "busca": "ObservadorBuscaLAI",
    "dados": "ObservadorDadosAbertos",
    "painel": "ObservadorPainelLAI",
}


class MotorSimulacao:
    def __init__(self):
        self._lock = RLock()
        self._inicializar()

    def _inicializar(self):
        self._eventos = []
        self._sequencia = 0
        self._ultimo_evento = []
        self.sujeito = SujeitoPedidoLAI(self._registrar)
        self.observadores = {
            "busca": ObservadorBuscaLAI(self.sujeito, self._registrar),
            "dados": ObservadorDadosAbertos(self.sujeito, self._registrar),
            "painel": ObservadorPainelLAI(self.sujeito, self._registrar),
        }
        for observador in self.observadores.values():
            self.sujeito.adicionar(observador)
        self._ultimo_evento = list(self._eventos)

    def _registrar(self, classe: str, metodo: str, detalhe: str, categoria: str):
        self._sequencia += 1
        self._eventos.append({
            "ordem": self._sequencia,
            "classe": classe,
            "metodo": metodo,
            "detalhe": detalhe,
            "categoria": categoria,
        })

    def resetar(self) -> dict:
        with self._lock:
            self._inicializar()
            return self._estado()

    def criar(self, assunto: str, orgao: str, descricao: str) -> dict:
        with self._lock:
            assunto, orgao, descricao = (x.strip() for x in (assunto, orgao, descricao))
            if not 3 <= len(assunto) <= 100:
                raise ValueError("O assunto deve ter entre 3 e 100 caracteres.")
            if not 2 <= len(orgao) <= 100:
                raise ValueError("Informe um órgão fictício (2 a 100 caracteres).")
            if not 10 <= len(descricao) <= 500:
                raise ValueError("A descrição deve ter entre 10 e 500 caracteres.")
            anterior = len(self._eventos)
            self.sujeito.criarPedido(PedidoLAI(
                protocolo="DEMO-LAI-0001", assunto=assunto, orgao=orgao,
                descricao=descricao,
                criado_em=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ))
            self._ultimo_evento = self._eventos[anterior:]
            return self._estado()

    def avancar(self, etapa: str, resposta: str = "") -> dict:
        with self._lock:
            try:
                proxima = Etapa(etapa)
            except ValueError as exc:
                raise ValueError("Etapa desconhecida.") from exc
            if len(resposta) > 500:
                raise ValueError("A resposta deve ter no máximo 500 caracteres.")
            anterior = len(self._eventos)
            self.sujeito.setEstado(proxima, resposta)
            self._ultimo_evento = self._eventos[anterior:]
            return self._estado()

    def assinatura(self, nome: str, habilitado: bool) -> dict:
        with self._lock:
            if nome not in self.observadores:
                raise ValueError("Observador inexistente.")
            observador = self.observadores[nome]
            anterior = len(self._eventos)
            if habilitado:
                ja_inscrito = observador in self.sujeito.inscritos()
                self.sujeito.adicionar(observador)
                if not ja_inscrito and self.sujeito.estado_atual():
                    observador.atualizar()
            else:
                self.sujeito.remover(observador)
            self._ultimo_evento = self._eventos[anterior:]
            return self._estado()

    def estado(self) -> dict:
        with self._lock:
            return self._estado()

    def fontes(self) -> dict:
        return {
            cls.__name__: {
                "nome": cls.__name__,
                "rotulo": ROTULOS[cls.__name__],
                "herda": [x.__name__ for x in cls.__bases__ if x is not object],
                "codigo": inspect.getsource(cls),
                "arquivo": str(Path(inspect.getfile(cls)).resolve().relative_to(Path(__file__).resolve().parent)),
            }
            for cls in CLASSES
        }

    def _estado(self) -> dict:
        pedido = self.sujeito.estado_atual()
        inscritos = self.sujeito.inscritos()
        busca = self.observadores["busca"]
        dados = self.observadores["dados"]
        painel = self.observadores["painel"]
        return {
            "pedido": {**asdict(pedido), "estado": pedido.estado.value} if pedido else None,
            "total_consultas": self.sujeito.total_consultas,
            "observadores": {
                "busca": {
                    "classe": "ObservadorBuscaLAI", "ativo": busca in inscritos,
                    "consultas": busca.consultas, "ultima_revisao": busca.ultima_revisao,
                    "registros": list(busca.indice_publico),
                },
                "dados": {
                    "classe": "ObservadorDadosAbertos", "ativo": dados in inscritos,
                    "consultas": dados.consultas, "ultima_revisao": dados.ultima_revisao,
                    "registros": list(dados.registros_publicos),
                },
                "painel": {
                    "classe": "ObservadorPainelLAI", "ativo": painel in inscritos,
                    "consultas": painel.consultas, "ultima_revisao": painel.ultima_revisao,
                    "registrados": painel.total_registrados,
                    "respondidos": painel.total_respondidos,
                    "publicados": painel.total_publicados,
                    "situacao": painel.status_visualizado,
                },
            },
            "eventos": list(self._eventos[-120:]),
            "ultima_execucao": list(self._ultimo_evento),
        }
