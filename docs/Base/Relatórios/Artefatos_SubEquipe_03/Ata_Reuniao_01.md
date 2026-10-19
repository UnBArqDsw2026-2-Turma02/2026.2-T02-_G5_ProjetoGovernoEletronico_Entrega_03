# Ata de Reunião — SubEquipe 03 (GoFs Criacionais)

**Entrega:** Módulo Padrões de Projeto — Entrega 03
**Data:** 18/10/2026
**Horário:** (a preencher)
**Local/Plataforma:** (a preencher)
**Gravação:** (link a preencher)

## Participantes

| Nome | Presente |
| --- | --- |
| Isaac Lucas Souza Bezerra | Sim |
| André João Cordeiro Gomes | Sim |
| João Paulo Barros | Sim |
| Rivadalvio Joaquim Da Silva Filho | Sim |

## Pauta

1. Escolha do padrão GoF Criacional (Factory Method, Abstract Factory, Builder ou Singleton).
2. Justificativa do padrão com base no domínio Informa.BR/LAI, nos artefatos das Entregas 01 e 02 e no material da professora (GRASP Criador e Aula de GoFs Criacionais).
3. Organização do trabalho: execução em conjunto por todos os membros (modelagem UML, código e execução).
4. Registro de divergências e consensos.

## Decisões

- **Padrão escolhido:** Factory Method, aplicado à hierarquia `Resposta` (Deferida, Parcialmente Deferida e Indeferida) do Diagrama de Classes da Entrega 02.
- **Justificativa:** cada tipo de resposta tem regras de criação próprias, ligadas à LAI e à privacidade (LGPD). O Factory Method isola essas regras em cada fábrica concreta e mantém o processo comum em `emitirResposta()`. O Abstract Factory foi descartado porque serve para criar famílias de objetos, e cada decisão do órgão gera um único produto.
- **Organização:** todos os membros atuando juntos na modelagem, no código e na execução.
- **Prazo interno:** 19/10/2026 (data de entrega da Entrega 03).

## Divergências e Consensos

- **Divergência:** parte do grupo defendia o Abstract Factory por parecer o mais aderente ao projeto; após a análise das intenções de cada padrão (criar um produto versus criar uma família de produtos), o grupo convergiu.
- **Consenso:** Factory Method — a hierarquia `Resposta` já existia e cada subtipo tem regras próprias de criação; seria o caso clássico do padrão, com menos complexidade.
- **Consenso:** a escolha da fábrica concreta fica em um único ponto do cliente (mapa `Decisao → FabricaResposta`), ligada aos gateways "Admissível?" e "Informação pública?" do BPMN da Entrega 02.

## Encaminhamentos

- Implementar o código em TypeScript, com demonstração que se verifica sozinha (4 cenários).
- Revisar os diagramas (notação UML, nomes sem acento/espaço, estereótipos).
- Registrar as evidências de uso da IA Generativa de cada membro.
- Gravar o vídeo do padrão em execução.

## Comprobatórios

- Ata versionada neste arquivo.
- Gravação: (link a preencher)
