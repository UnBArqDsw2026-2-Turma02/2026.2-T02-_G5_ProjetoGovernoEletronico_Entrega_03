import inspect
import unittest

from simulacao import MotorSimulacao
from codigoFonte.sujeito import Sujeito
from codigoFonte.observador import Observador


class TestesObserver(unittest.TestCase):
    def setUp(self):
        self.demo = MotorSimulacao()

    def criar(self):
        return self.demo.criar("Contratos administrativos", "Órgão de teste", "Quero dados de teste sobre contratos.")

    def test_criacao_notifica_e_observadores_consultam_estado(self):
        estado = self.criar()
        self.assertEqual(estado["pedido"]["estado"], "REGISTRADO")
        self.assertEqual(estado["total_consultas"], 3)
        self.assertTrue(any(e["metodo"] == "getEstado()" for e in estado["ultima_execucao"]))
        self.assertTrue(all(item["consultas"] == 1 for item in estado["observadores"].values()))

    def test_publicacao_somente_apos_etapas(self):
        self.criar()
        with self.assertRaises(ValueError):
            self.demo.avancar("PUBLICADO")
        self.demo.avancar("EM_ANALISE")
        self.demo.avancar("RESPONDIDO", "Resposta demonstrativa.")
        self.demo.avancar("AUTORIZADO")
        estado = self.demo.avancar("PUBLICADO")
        self.assertEqual(estado["total_consultas"], 15)
        self.assertEqual(estado["observadores"]["painel"]["publicados"], 1)
        self.assertEqual(len(estado["observadores"]["busca"]["registros"]), 1)
        self.assertEqual(len(estado["observadores"]["dados"]["registros"]), 1)
        self.assertNotIn("Quero dados de teste", str(estado["observadores"]["busca"]["registros"]))
        self.assertNotIn("Resposta demonstrativa", str(estado["observadores"]["dados"]["registros"]))

    def test_remocao_impede_chamadas_e_reinscricao_sincroniza(self):
        self.criar()
        self.demo.assinatura("busca", False)
        estado = self.demo.avancar("EM_ANALISE")
        self.assertEqual(estado["observadores"]["busca"]["consultas"], 1)
        self.assertEqual(estado["observadores"]["painel"]["consultas"], 2)
        estado = self.demo.assinatura("busca", True)
        self.assertEqual(estado["observadores"]["busca"]["consultas"], 2)
        self.assertEqual(estado["observadores"]["busca"]["ultima_revisao"], 2)

    def test_erro_nao_notifica_observadores(self):
        self.criar()
        antes = self.demo.estado()["total_consultas"]
        with self.assertRaises(ValueError):
            self.demo.avancar("RESPONDIDO", "")
        self.assertEqual(self.demo.estado()["total_consultas"], antes)

    def test_reset(self):
        self.criar()
        estado = self.demo.resetar()
        self.assertIsNone(estado["pedido"])
        self.assertEqual(estado["total_consultas"], 0)
        self.assertTrue(all(v["ativo"] for v in estado["observadores"].values()))

    def test_contratos_abstratos_e_fontes_completas(self):
        with self.assertRaises(TypeError):
            Sujeito()
        with self.assertRaises(TypeError):
            Observador()
        fontes = self.demo.fontes()
        self.assertEqual(len(fontes), 10)
        self.assertIn('codigoFonte/sujeito.py', fontes['Sujeito']['arquivo'])
        self.assertIn('NotImplementedError', fontes['Sujeito']['codigo'])
        self.assertNotIn('...', fontes['Sujeito']['codigo'])
        self.assertIn('self.notificar()', fontes['SujeitoPedidoLAI']['codigo'])
        self.assertIn('self._sujeito.getEstado()', fontes['ObservadorBuscaLAI']['codigo'])
        self.assertIn('def _inicializar', fontes['MotorSimulacao']['codigo'])
        self.assertEqual(fontes['MotorSimulacao']['arquivo'], 'simulacao.py')
        self.assertEqual(fontes['FonteEstadoPedido']['arquivo'], 'codigoFonte/fonte_estado_pedido.py')
        self.assertIn('sujeito: FonteEstadoPedido', fontes['ObservadorBuscaLAI']['codigo'])

    def test_inscricao_duplicada_nao_duplica_atualizacoes(self):
        self.demo.assinatura('busca', True)
        estado = self.criar()
        self.assertEqual(estado['observadores']['busca']['consultas'], 1)
        self.assertEqual(estado['total_consultas'], 3)

    def test_reativacao_apos_publicacao_sincroniza_observador(self):
        self.demo.assinatura('busca', False)
        self.criar()
        self.demo.avancar('EM_ANALISE')
        self.demo.avancar('RESPONDIDO', 'Resposta demonstrativa.')
        self.demo.avancar('AUTORIZADO')
        estado = self.demo.avancar('PUBLICADO')
        self.assertEqual(estado['observadores']['busca']['consultas'], 0)
        self.assertEqual(estado['observadores']['busca']['registros'], [])
        estado = self.demo.assinatura('busca', True)
        self.assertEqual(estado['observadores']['busca']['consultas'], 1)
        self.assertEqual(len(estado['observadores']['busca']['registros']), 1)
        self.assertEqual(estado['observadores']['busca']['ultima_revisao'], 5)


if __name__ == "__main__":
    unittest.main()
