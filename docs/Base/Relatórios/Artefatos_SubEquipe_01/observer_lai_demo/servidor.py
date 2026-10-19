import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from simulacao import MotorSimulacao

STATIC = Path(__file__).resolve().parent / "static"
MOTOR = MotorSimulacao()
MAX_BODY = 12_000


class Aplicacao(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC), **kwargs)

    def _json(self, status, data):
        conteudo = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(conteudo)

    def do_GET(self):
        if self.path == "/api/estado":
            return self._json(200, MOTOR.estado())
        if self.path == "/api/classes":
            return self._json(200, MOTOR.fontes())
        if self.path.startswith("/api/"):
            return self._json(404, {"erro": "Endpoint desconhecido."})
        return super().do_GET()

    def do_POST(self):
        rotas = {"/api/criar", "/api/avancar", "/api/assinatura", "/api/resetar"}
        if self.path not in rotas:
            return self._json(404, {"erro": "Endpoint desconhecido."})
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if not (0 <= tamanho <= MAX_BODY):
                return self._json(413, {"erro": "Requisição muito grande."})
            dados = json.loads(self.rfile.read(tamanho)) if tamanho else {}
            if not isinstance(dados, dict):
                raise ValueError("É necessário enviar um objeto JSON.")
            if self.path == "/api/criar":
                resultado = MOTOR.criar(str(dados.get("assunto", "")), str(dados.get("orgao", "")), str(dados.get("descricao", "")))
            elif self.path == "/api/avancar":
                resultado = MOTOR.avancar(str(dados.get("etapa", "")), str(dados.get("resposta", "")))
            elif self.path == "/api/assinatura":
                if type(dados.get("ativo")) is not bool:
                    raise ValueError("O campo ativo deve ser booleano.")
                resultado = MOTOR.assinatura(str(dados.get("observador", "")), dados["ativo"])
            else:
                resultado = MOTOR.resetar()
            return self._json(200, resultado)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            return self._json(400, {"erro": str(exc)})


if __name__ == "__main__":
    endereco = ("127.0.0.1", 8000)
    servidor = ThreadingHTTPServer(endereco, Aplicacao)
    print("Observer LAI (demonstração local): http://127.0.0.1:8000")
    print("Para encerrar: Ctrl+C")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    finally:
        servidor.server_close()
