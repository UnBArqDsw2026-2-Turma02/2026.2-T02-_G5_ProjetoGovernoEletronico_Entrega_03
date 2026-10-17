import ast
import inspect
from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest

from codigoFonte.etapa_pedido import Etapa
from codigoFonte.modelo_pedido import PedidoLAI
from codigoFonte.observador_busca_lai import ObservadorBuscaLAI
from codigoFonte.observador_dados_abertos import ObservadorDadosAbertos
from codigoFonte.observador_painel_lai import ObservadorPainelLAI
from simulacao import MotorSimulacao


class FontePedidoAlternativa:
    def __init__(self, pedido):
        self.pedido = pedido
        self.consultas = 0

    def getEstado(self):
        self.consultas += 1
        return self.pedido


class TestesArquitetura(unittest.TestCase):
    def setUp(self):
        self.pedido = PedidoLAI(
            protocolo="TESTE-001",
            assunto="Dados de teste",
            orgao="Órgão de teste",
            descricao="Pedido fictício para verificar a arquitetura.",
        )
        self.eventos = []

    def registrar(self, classe, metodo, detalhe, categoria):
        self.eventos.append((classe, metodo, detalhe, categoria))

    def test_observadores_aceitam_fonte_alternativa(self):
        fonte = FontePedidoAlternativa(self.pedido)
        classes = (ObservadorBuscaLAI, ObservadorDadosAbertos, ObservadorPainelLAI)
        for observador_concreto in classes:
            with self.subTest(classe=observador_concreto.__name__):
                instancia = observador_concreto(fonte, self.registrar)
                instancia.atualizar()
                self.assertEqual(instancia.consultas, 1)
        self.assertEqual(fonte.consultas, 3)

    def test_contrato_de_leitura_sem_dependencia_do_sujeito_concreto(self):
        for classe in (ObservadorBuscaLAI, ObservadorDadosAbertos, ObservadorPainelLAI):
            with self.subTest(classe=classe.__name__):
                codigo = inspect.getsource(classe)
                self.assertIn("sujeito: FonteEstadoPedido", codigo)
                self.assertNotIn("SujeitoPedidoLAI", codigo)
                self.assertIn("self._sujeito.getEstado()", codigo)

    def test_modelo_imutavel(self):
        with self.assertRaises(FrozenInstanceError):
            self.pedido.estado = Etapa.PUBLICADO

    def test_orquestracao_fora_de_codigo_fonte(self):
        fontes = MotorSimulacao().fontes()
        self.assertEqual(fontes["MotorSimulacao"]["arquivo"], "simulacao.py")
        for nome, dados in fontes.items():
            with self.subTest(tipo=nome):
                caminho = Path(__file__).resolve().parents[1] / dados["arquivo"]
                self.assertTrue(caminho.exists(), nome)
                codigo_real = caminho.read_text(encoding="utf-8")
                self.assertIn(f"class {nome}", codigo_real)
                self.assertIn(f"class {nome}", dados["codigo"])
                ast.parse(codigo_real)

    def test_pastas_sem_arquivos_de_orquestracao(self):
        diretorio = Path(__file__).resolve().parents[1] / "codigoFonte"
        self.assertFalse((diretorio / "padrao.py").exists())
        self.assertFalse((diretorio / "simulacao.py").exists())


if __name__ == "__main__":
    unittest.main()
