# Implementação do Factory Method — SubEquipe 03 (GoFs Criacionais)

Demonstração do padrão criacional **Factory Method** aplicado à hierarquia `Resposta` do domínio do Informa.BR/LAI: cada decisão da análise do órgão (informação pública, parcial ou negada) é emitida por uma fábrica concreta, que concentra as regras de criação do seu tipo de resposta.

A demonstração roda em Node.js (TypeScript) e se verifica sozinha: são 4 cenários validados com `asserts`, incluindo o caso em que a fábrica barra uma resposta parcial sem base legal.

## Requisitos

- Node.js 18 ou superior

## Como executar

```bash
cd docs/Base/Relatórios/Artefatos_SubEquipe_03/codigo
npm install
npm start
```

Saída esperada (resumo):

```text
[1] 50001.000001/2026-01 → Deferida | status=RESPONDIDO | cabe recurso? false
[2] 50001.000002/2026-02 → Parcialmente Deferida | prazo recursal: 10 dias a contar da ciência (LAI art. 15).
[3] 50001.000003/2026-03 → Indeferida | recurso: Autoridade hierarquicamente superior (1ª instância) — prazo de 10 dias (LAI art. 15).
[4] 50001.000004/2026-04 → criação barrada pela fábrica; status continua EM_ANALISE

Todos os cenários passaram ✔
```

## Estrutura dos Arquivos

| Arquivo | Papel no Padrão | Descrição |
| --- | --- | --- |
| `src/dominio.ts` | — | `PedidoAcesso`, `AgentePublico` e o enum `StatusManifestacao` |
| `src/resposta.ts` | *Product* + *ConcreteProduct* | `Resposta` (abstrata) e as respostas `Deferida`, `ParcialmenteDeferida` e `Indeferida` |
| `src/fabricas.ts` | *Creator* + *ConcreteCreator* | `FabricaResposta` (abstrata): `emitirResposta()` define o processo e `criarResposta()` é o factory method; e as três fábricas concretas |
| `src/main.ts` | Cliente (demonstração) | Executa os 4 cenários e valida com `asserts` |

Relatório completo: [`1.1.3.SubEquipe_03.md`](Base/Relatórios/1.1.3.SubEquipe_03.md)
