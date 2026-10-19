# Observer — pedido LAI

Aplicação demonstrativa do padrão comportamental Observer com consulta de estado realizada pelos observadores. Possui interface web, registro de chamadas e auditoria dos objetos em execução.

## Execução

Requer Python 3.10 ou superior, sem dependências externas.

```bash
python3 servidor.py
```

Acesse http://127.0.0.1:8000.

## Organização do código

```text
observer_lai_demo/
├── codigoFonte/
│   ├── __init__.py
│   ├── etapa_pedido.py                Etapa
│   ├── modelo_pedido.py               PedidoLAI
│   ├── sujeito.py                     Sujeito
│   ├── sujeito_pedido_lai.py          SujeitoPedidoLAI
│   ├── observador.py                  Observador
│   ├── fonte_estado_pedido.py         FonteEstadoPedido
│   ├── observador_busca_lai.py        ObservadorBuscaLAI
│   ├── observador_dados_abertos.py    ObservadorDadosAbertos
│   ├── observador_painel_lai.py       ObservadorPainelLAI
│   └── tipos.py                       Tipo de callback de auditoria
├── padrao.py                         Fachada de importação dos tipos do padrão
├── simulacao.py                      Orquestração, transições e auditoria
├── servidor.py                       API HTTP e arquivos estáticos
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── referencias/
│   └── diagrama-original.html
└── tests/
    └── test_observer.py
```

A pasta `codigoFonte/` contém contratos, entidade de domínio e classes concretas em arquivos próprios. A classe `MotorSimulacao`, responsável pela composição e pela interface de aplicação, fica em `simulacao.py`, fora da pasta. `padrao.py` só disponibiliza uma fachada de importação, sem repetir implementações.

## Arquitetura

- `Sujeito` e `Observador` estabelecem os contratos do padrão GoF Observer.
- `SujeitoPedidoLAI` mantém o estado do pedido e gerencia inscrições; chama `notificar()` depois de cada alteração válida.
- `FonteEstadoPedido` é um contrato de leitura implementado pelo sujeito concreto. Os observadores dependem apenas desse contrato, não de `SujeitoPedidoLAI`.
- Cada observador implementa `atualizar()` sem receber dados e consulta `getEstado()` para obter uma cópia imutável do pedido.
- `ObservadorPainelLAI` acompanha todas as etapas; `ObservadorBuscaLAI` e `ObservadorDadosAbertos` produzem registros públicos sintéticos apenas quando o estado é `PUBLICADO` e existe autorização.
- O orquestrador `MotorSimulacao` registra as chamadas e mantém as instâncias; o backend não é acoplado ao frontend.
- Reativar um observador faz uma leitura de sincronização quando já existe pedido. Desativá-lo impede notificações subsequentes.
- Uma transição inválida é rejeitada sem notificar observadores.

A sequência das etapas é `REGISTRADO → EM_ANALISE → RESPONDIDO → AUTORIZADO → PUBLICADO`.

## Interface e API

A aba **Fluxo e atualizações** executa as cinco etapas e mostra as chamadas dos métodos. A aba **Classes e código** obtém de `/api/classes` o código completo das classes a partir de seus arquivos reais; a auditoria permite avançar e reiniciar o pedido.

| Método | Rota | Responsabilidade |
|---|---|---|
| GET | `/api/estado` | Inspecionar o estado atual |
| GET | `/api/classes` | Consultar os códigos-fonte das classes |
| POST | `/api/criar` | Criar o pedido |
| POST | `/api/avancar` | Avançar uma etapa |
| POST | `/api/assinatura` | Ativar ou desativar um observador |
| POST | `/api/resetar` | Reiniciar a demonstração |

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Referência

- https://refactoring.guru/pt-br/design-patterns/observer/python/example
