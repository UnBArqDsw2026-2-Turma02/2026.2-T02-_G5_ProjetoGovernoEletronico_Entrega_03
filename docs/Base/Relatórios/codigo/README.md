# Implementação do Padrão GoF Facade — SubEquipe 02 (v2.0)

Este diretório contém a implementação didática do padrão estrutural **Facade** aplicado ao cenário de busca pública de informações do portal [Informa.BR](https://informabr.cgu.gov.br/).

A busca é simulada e não acessa serviços reais. Os links exibidos são apenas as páginas iniciais dos portais.

## Estrutura dos Arquivos

### Núcleo do padrão

| Arquivo | Papel no Padrão | Descrição | Em relação à v1.0 |
| --- | --- | --- | --- |
| `TelaBusca.java` | Cliente (`<<Cliente>>`) | Ponto de entrada (`main`). Solicita a busca à fachada e apresenta o resultado consolidado (`ResultadoBusca`). | Alterado |
| `FachadaBuscaPublica.java` | Fachada (`<<Facade>>`) | Valida, consulta as fontes, isola falhas, solicita a orientação por IA e devolve um `ResultadoBusca`. | Alterado |
| `ValidadorConsulta.java` | Subsistema (`<<Subsistema>>`) | Valida o termo de entrada e retorna uma `ValidacaoConsulta`. | Alterado |
| `FonteBusca.java` | Interface dos subsistemas de busca | Contrato comum: `nome()` e `consultar(termo)`. | **Novo** |
| `BuscaPedidosLAI.java` | Subsistema (implementa `FonteBusca`) | Simula consulta a pedidos da Lei de Acesso à Informação. | Alterado |
| `BuscaTransparencia.java` | Subsistema (implementa `FonteBusca`) | Simula consulta ao Portal da Transparência. O termo `inexistente` simula fonte sem registros. | Alterado |
| `BuscaDadosAbertos.java` | Subsistema (implementa `FonteBusca`) | Simula consulta ao Portal de Dados Abertos. O termo `falha` simula fonte indisponível. | Alterado |
| `GeradorOrientacaoIA.java` | Subsistema (`<<Subsistema>>`) | Simula a geração de resumo orientativo por IA generativa. | Alterado |

### Estruturas de dados (DTOs)

| Arquivo | Descrição | Em relação à v1.0 |
| --- | --- | --- |
| `ResultadoBusca.java` | Resultado consolidado: validação, resultados por fonte e orientação da IA. | **Novo** |
| `ResultadoFonte.java` | Resultado de uma fonte: nome, status e itens. | **Novo** |
| `ItemResultado.java` | Um registro retornado por uma fonte: título e URL de origem. | **Novo** |
| `ValidacaoConsulta.java` | Resultado da validação do termo: válida ou não, e mensagem. | **Novo** |
| `OrientacaoIA.java` | Texto da IA, mantido separado dos dados oficiais, com aviso de possíveis imprecisões. | **Novo** |
| `StatusFonte.java` | Enum: `SUCESSO`, `VAZIO`, `INDISPONIVEL`. | **Novo** |

## Como Compilar e Executar

Certifique-se de possuir o JDK (Java Development Kit) **17 ou superior** instalado

1. **Compilar todos os arquivos:**
   ```bash
   javac -encoding UTF-8 *.java
   ```

2. **Executar a demonstração:**
   ```bash
   java TelaBusca
   ```

   Se os acentos aparecerem errados no console (comum no Windows), execute com:
   ```bash
   java -Dfile.encoding=UTF-8 TelaBusca
   ```

## Cenários executados pelo `main`

| Termo | Demonstra |
| --- | --- |
| `educação` | Fluxo normal: todas as fontes retornam resultados. |
| `"   "` (em branco) | Validação prévia: a fachada interrompe e nenhuma fonte é consultada. |
| `falha` | Uma fonte indisponível (`INDISPONIVEL`): as demais continuam exibidas. |
| `inexistente` | Uma fonte sem registros (`VAZIO`), distinta de fonte indisponível. |

## Saída esperada no console

Resultado completo da execução (verificado com o JDK 21):

```text
=== Busca: "educação" ===
Analisando sua pergunta...
  [ValidadorConsulta] validando termo
  [BuscaPedidosLAI] buscando pedidos LAI sobre: educação
  [BuscaTransparencia] buscando registros de transparência sobre: educação
  [BuscaDadosAbertos] buscando conjuntos de dados sobre: educação
  [GeradorOrientacaoIA] gerando orientação simulada sobre: educação

[Resumo gerado por IA]
  Simulação: a consulta "educação" parece buscar informações públicas relacionadas ao tema. Consulte as abas de resultados para os registros oficiais.
  (Resumo gerado por IA. Pode conter imprecisões.)

[Aba: Pedidos LAI]
  - Pedido LAI simulado nº 001 sobre educação -> https://informabr.cgu.gov.br/
  - Pedido LAI simulado nº 002 sobre educação -> https://informabr.cgu.gov.br/

[Aba: Portal da Transparência]
  - Registro de transparência simulado sobre educação -> https://portaldatransparencia.gov.br/

[Aba: Portal de Dados Abertos]
  - Conjunto de dados simulado sobre educação -> https://dados.gov.br/

Busca simulada concluída.

=== Busca: "   " ===
Analisando sua pergunta...
  [ValidadorConsulta] validando termo
Aviso: Informe um termo para realizar a busca.

=== Busca: "falha" ===
Analisando sua pergunta...
  [ValidadorConsulta] validando termo
  [BuscaPedidosLAI] buscando pedidos LAI sobre: falha
  [BuscaTransparencia] buscando registros de transparência sobre: falha
  [BuscaDadosAbertos] buscando conjuntos de dados sobre: falha
  [Fachada] falha em 'Portal de Dados Abertos': Portal de Dados Abertos fora do ar (simulado)
  [GeradorOrientacaoIA] gerando orientação simulada sobre: falha

[Resumo gerado por IA]
  Simulação: a consulta "falha" parece buscar informações públicas relacionadas ao tema. Consulte as abas de resultados para os registros oficiais.
  (Resumo gerado por IA. Pode conter imprecisões.)

[Aba: Pedidos LAI]
  - Pedido LAI simulado nº 001 sobre falha -> https://informabr.cgu.gov.br/
  - Pedido LAI simulado nº 002 sobre falha -> https://informabr.cgu.gov.br/

[Aba: Portal da Transparência]
  - Registro de transparência simulado sobre falha -> https://portaldatransparencia.gov.br/

[Aba: Portal de Dados Abertos]
  Fonte indisponível no momento. Tente novamente mais tarde.

Busca simulada concluída.

=== Busca: "inexistente" ===
Analisando sua pergunta...
  [ValidadorConsulta] validando termo
  [BuscaPedidosLAI] buscando pedidos LAI sobre: inexistente
  [BuscaTransparencia] buscando registros de transparência sobre: inexistente
  [BuscaDadosAbertos] buscando conjuntos de dados sobre: inexistente
  [GeradorOrientacaoIA] gerando orientação simulada sobre: inexistente

[Resumo gerado por IA]
  Simulação: a consulta "inexistente" parece buscar informações públicas relacionadas ao tema. Consulte as abas de resultados para os registros oficiais.
  (Resumo gerado por IA. Pode conter imprecisões.)

[Aba: Pedidos LAI]
  - Pedido LAI simulado nº 001 sobre inexistente -> https://informabr.cgu.gov.br/
  - Pedido LAI simulado nº 002 sobre inexistente -> https://informabr.cgu.gov.br/

[Aba: Portal da Transparência]
  Nenhum registro encontrado para esta fonte.

[Aba: Portal de Dados Abertos]
  - Conjunto de dados simulado sobre inexistente -> https://dados.gov.br/

Busca simulada concluída.
```