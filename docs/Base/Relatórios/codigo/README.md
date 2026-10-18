# Implementação do Padrão GoF Facade — SubEquipe 02

Este diretório contém a implementação didática do padrão estrutural **Facade** aplicado ao cenário de busca pública de informações do portal [Informa.BR](https://informabr.cgu.gov.br/).

## Estrutura dos Arquivos

| Arquivo | Papel no Padrão | Descrição |
| --- | --- | --- |
| `TelaBusca.java` | Cliente (`<<Cliente>>`) | Ponto de entrada (`main`) que solicita a busca e apresenta o resultado consolidado. |
| `FachadaBuscaPublica.java` | Fachada (`<<Facade>>`) | Orquestra a execução da validação, consultas aos subsistemas e resumo por IA. |
| `ValidadorConsulta.java` | Subsistema (`<<Subsistema>>`) | Valida termos de busca de entrada. |
| `BuscaPedidosLAI.java` | Subsistema (`<<Subsistema>>`) | Simula consulta a pedidos da Lei de Acesso à Informação. |
| `BuscaTransparencia.java` | Subsistema (`<<Subsistema>>`) | Simula consulta ao Portal da Transparência. |
| `BuscaDadosAbertos.java` | Subsistema (`<<Subsistema>>`) | Simula consulta ao Portal de Dados Abertos. |
| `GeradorOrientacaoIA.java` | Subsistema (`<<Subsistema>>`) | Simula geração de resumo orientativo por IA generativa. |

## Como Compilar e Executar

Certifique-se de possuir o JDK (Java Development Kit) 8 ou superior instalado.

1. **Compilar todos os arquivos:**
   ```bash
   javac *.java
   ```

2. **Executar a demonstração:**
   ```bash
   java TelaBusca
   ```

3. **Saída esperada no console:**
   ```text
   Validando consulta: educação
   Buscando pedidos LAI sobre: educação
   Buscando informações de transparência sobre: educação
   Buscando dados abertos sobre: educação
   Gerando orientação simulada sobre: educação
   Busca simulada concluída.
   ```
