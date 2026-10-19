# Chain of Responsibility — Recursos da LAI (Informa.BR)

Implementação acadêmica em Java do padrão comportamental **Chain of Responsibility**, com interface web local. O navegador apresenta os campos e o log; o servidor Java executa os handlers reais do projeto.

## Requisitos

- JDK 8 ou superior.
- Navegador moderno.

## Compilar

Execute a partir desta pasta:

```bash
javac -encoding UTF-8 -d out recursoslai/*.java
```

## Executar no desktop local

```bash
java -Dfile.encoding=UTF-8 -cp out recursoslai.ServidorWebRecursosLAI
```

Acesse `http://localhost:8080/`. Por padrão, o servidor escuta apenas em `127.0.0.1`.

## Executar no WSL quando o navegador do Windows não alcança localhost do WSL

```bash
java -Dfile.encoding=UTF-8 -Dserver.host=0.0.0.0 -cp out recursoslai.ServidorWebRecursosLAI
```

Depois acesse `http://localhost:8080/` no navegador do Windows. **A opção `0.0.0.0` escuta em todas as interfaces de rede disponíveis; use apenas em ambiente de demonstração confiável e encerre o servidor após a gravação.** Para uso local normal, omita `-Dserver.host=0.0.0.0`.

## O que a interface permite

- Informar protocolo e nome do cidadão.
- Configurar se o recurso é tempestivo e se o órgão pertence ao Poder Executivo Federal.
- Selecionar decisões simuladas das quatro instâncias.
- Ver status, instância responsável, motivo e log de encaminhamento gerados pelos handlers Java.

## Testes automatizados

```bash
java -Dfile.encoding=UTF-8 -cp out recursoslai.TesteAutomatizado
```

## Demonstrações alternativas

```bash
java -Dfile.encoding=UTF-8 -cp out recursoslai.ChainOfResponsibilityDemo
java -Dfile.encoding=UTF-8 -cp out recursoslai.TesteManual
```

## Papéis no padrão GoF

| Papel | Classe | Responsabilidade |
|---|---|---|
| `Handler` | `InstanciaHandler` | Mantém `proximo`; `handle()` tenta tratar e encaminha quando `tratar()` retorna `false`. |
| `ConcreteHandler` | `ValidadorTempestividadeHandler` | Interrompe o fluxo quando o recurso é configurado como intempestivo. |
| `ConcreteHandler` | `AutoridadeHierarquicaSuperiorHandler` | Simula a decisão da primeira instância. |
| `ConcreteHandler` | `AutoridadeMaximaOrgaoHandler` | Simula a decisão da segunda instância. |
| `ConcreteHandler` | `CGUHandler` | Simula a etapa da CGU e a condição de admissibilidade configurada. |
| `ConcreteHandler` | `CMRIHandler` | Simula a decisão final da cadeia. |
| `Request` | `Recurso` | Carrega os dados e o resultado do processamento. |
| `Client` | `ChainOfResponsibilityDemo`, `TesteManual`, `InterfaceRecursosLAI`, `ServidorWebRecursosLAI` | Monta a cadeia e inicia o processamento. |

## Limitações

Esta é uma simulação didática, não um sistema oficial de protocolo ou julgamento. As decisões de mérito são entradas de teste; não há consulta a banco de dados ou serviço governamental. A regra de encaminhamento após o não conhecimento pela CGU é simplificada para demonstrar a propagação da cadeia e não deve ser tomada como parecer jurídico.

## Diagrama

Consulte `diagramas/diagrama_classes_chain_of_responsibility.png` e `.svg`. A fonte PlantUML está em `diagramas/diagrama_classes_chain_of_responsibility.puml`; o script original de geração do diagrama também está incluído.
