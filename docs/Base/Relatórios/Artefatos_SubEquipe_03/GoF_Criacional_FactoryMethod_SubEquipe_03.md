# SubEquipe_03 — GoF Criacional: Factory Method

<!-- Versão revisada em 18/10/2026: ajustes de notação nos diagramas, vídeo e referências. -->

## Participantes

| Nome do Membro | Contribuição |
| --- | --- |
| Isaac Lucas Souza Bezerra | <!-- TODO --> |
| André João Cordeiro Gomes | <!-- TODO --> |
| Rivadalvio Joaquim da Silva Filho | <!-- TODO --> |
| João Paulo Barros | <!-- TODO --> |

## Metodologia

1. **Escolha da família:** a SubEquipe 03 ficou com os padrões **criacionais**. O ponto de partida foi o artefato que ela mesma produziu na Entrega 02, o [Diagrama de Classes (Herança)](https://github.com/UnBArqDsw2026-2-Turma02/2026.2-T02-_G5_ProjetoGovernoEletronico_Entrega_02/blob/main/docs/Base/Relat%C3%B3rios/ExtrasSubEquipe_03/Diagrama_de_Classes_Heranca_V01.puml), pois é o único modelo do grupo com classes, atributos e métodos.
2. **Busca do problema de criação:** cada hierarquia do diagrama foi analisada perguntando *"quem cria esses objetos, e com que regras?"*. A hierarquia `Resposta` (Deferida, Parcialmente Deferida e Indeferida) foi escolhida porque cada subtipo tem regras de criação próprias, ligadas à LAI e à privacidade de dados (ênfase do projeto G5).
3. **Escolha do padrão:** comparamos Simple Factory, **Factory Method** e Abstract Factory (ver [Senso crítico](#senso-crítico)).
4. **Modelagem:** diagrama de classes do padrão e diagrama de sequência da execução, em **PlantUML**, com a fonte (`.puml`) versionada no repositório.
5. **Implementação:** código em **TypeScript**, a mesma linguagem do protótipo `NovoPedido.tsx` da SubEquipe 01, com uma demonstração que se verifica sozinha (asserts).
6. **Revisão coletiva:** <!-- TODO: data da reunião, link da ata/gravação e commits. -->

## O problema

No Diagrama de Classes da Entrega 02, `Agente Público` tem o método `elaborarResposta(r : Resposta)`. Mas o diagrama não diz **quem cria a resposta concreta** nem **onde ficam as regras de cada tipo**. Sem um padrão, a tendência é concentrar tudo no cliente:

```ts
// ANTES — o cliente conhece todas as subclasses e todas as regras
function elaborarResposta(pedido: PedidoAcesso, decisao: string, d: Dados) {
  let r: Resposta;
  if (decisao === "PUBLICA") {
    r = new RespostaDeferida(d.texto, d.link, d.formato);
  } else if (decisao === "PARCIAL") {
    if (!d.partesOcultadas || !d.enquadramentoLGPD) throw new Error("...");
    r = new RespostaParcialmenteDeferida(/* ... */);
  } else if (decisao === "NEGADA") {
    if (!d.dispositivoLegalLAI) throw new Error("...");
    r = new RespostaIndeferida(/* ... */);
  }
  pedido.vincularResposta(r);
  r.publicar();
}
```

Problemas dessa abordagem:

- **Acoplamento:** o cliente depende de todas as classes concretas de `Resposta`.
- **Violação do Princípio Aberto/Fechado:** um novo tipo de resposta, como a *Resposta de Informação Inexistente*, obriga a editar o `if/else`.
- **Risco à privacidade:** a validação da base legal de uma resposta parcial fica misturada com o fluxo. Basta esquecer um `if` para publicar uma resposta sem justificar o que foi ocultado.

## O padrão: Factory Method

> **Intenção (GoF):** definir uma interface para criar um objeto, mas deixar as subclasses decidirem qual classe instanciar. O Factory Method permite adiar a instanciação para as subclasses (GAMMA et al., 1994).

| Papel no GoF | Classe no Informa.BR |
| --- | --- |
| **Product** | `Resposta` (abstrata) |
| **ConcreteProduct** | `RespostaDeferida`, `RespostaParcialmenteDeferida`, `RespostaIndeferida` |
| **Creator** | `FabricaResposta` (abstrata): `emitirResposta()` define o processo e `criarResposta()` é o *factory method* |
| **ConcreteCreator** | `FabricaRespostaDeferida`, `FabricaRespostaParcial`, `FabricaRespostaIndeferida` |
| **Cliente** | `AgentePublico.elaborarResposta()` |

### Modelagem estática: Diagrama de Classes do padrão

![Factory Method — Diagrama de Classes](GoF_Criacional_FactoryMethod_V01.png)

Fonte editável: [GoF_Criacional_FactoryMethod_V01.puml](GoF_Criacional_FactoryMethod_V01.puml)

**Leitura do modelo:**

- `FabricaResposta.emitirResposta()` contém os passos **comuns** a toda resposta: validar o texto, criar, vincular ao pedido (o status vai para `RESPONDIDO`) e publicar.
- O único passo que **varia** é `criarResposta()`, o factory method. Cada fábrica concreta valida as próprias regras e instancia o seu produto.
- As classes de produto são **as mesmas** do Diagrama de Classes da Entrega 02. O padrão não muda o domínio, só organiza quem cria cada objeto.

### Modelagem dinâmica: o padrão em execução

![Factory Method — Diagrama de Sequência](GoF_Criacional_FactoryMethod_Sequencia_V01.png)

Fonte editável: [GoF_Criacional_FactoryMethod_Sequencia_V01.puml](GoF_Criacional_FactoryMethod_Sequencia_V01.puml)

O cenário mostra uma resposta **parcialmente deferida**. A fábrica impede a criação quando faltam a parte ocultada ou a base legal, e o pedido continua `EM_ANALISE`.

## Implementação

O código fica em [`codigo/`](codigo/). Para executar:

```bash
cd codigo
npm install
npm start
```

**Trecho central: o Creator e uma fábrica concreta** (`codigo/src/fabricas.ts`):

```ts
export abstract class FabricaResposta {
  /** Processo de emissão: igual para todos os tipos de resposta. */
  emitirResposta(pedido: PedidoAcesso, agente: AgentePublico, dados: DadosResposta): Resposta {
    exigir(dados, ["texto"], "Resposta");
    const resposta = this.criarResposta(dados, agente); // ← factory method
    pedido.vincularResposta(resposta);
    resposta.publicar();
    return resposta;
  }

  /** FACTORY METHOD: cada subclasse decide qual Resposta concreta instanciar. */
  protected abstract criarResposta(dados: DadosResposta, agente: AgentePublico): Resposta;
}

export class FabricaRespostaParcial extends FabricaResposta {
  /** Privacidade: o acesso parcial só pode ser criado com a parte ocultada e a base legal (LAI art. 7º §2º; LGPD). */
  protected criarResposta(d: DadosResposta, agente: AgentePublico): Resposta {
    exigir(d, ["partesOcultadas", "justificativaRestricao", "enquadramentoLGPD"], "Resposta parcialmente deferida");
    return new RespostaParcialmenteDeferida(
      d.texto, agente.nome, d.partesOcultadas!, d.justificativaRestricao!, d.enquadramentoLGPD!,
    );
  }
}
```

**Cliente: não conhece nenhuma subclasse concreta** (`codigo/src/dominio.ts`):

```ts
elaborarResposta(pedido: PedidoAcesso, fabrica: FabricaResposta, dados: DadosResposta): Resposta {
  return fabrica.emitirResposta(pedido, this, dados);
}
```

**Saída da demonstração** (`npm start`):

```text
[1] 50001.000001/2026-01 → Deferida | status=RESPONDIDO | cabe recurso? false
[2] 50001.000002/2026-02 → Parcialmente Deferida | prazo recursal: 10 dias a contar da ciência (LAI art. 15).
[3] 50001.000003/2026-03 → Indeferida | recurso: Autoridade hierarquicamente superior (1ª instância) — prazo de 10 dias (LAI art. 15).
[4] 50001.000004/2026-04 → criação barrada pela fábrica; status continua EM_ANALISE

Todos os cenários passaram ✔
```

- **Vídeo:** (link a definir, demonstrando o código em execução).

## Rastreabilidade & Elos com Outros Artefatos

| Artefato anterior | Elo com o Factory Method |
| --- | --- |
| **Entrega 02: Diagrama de Classes (Herança), SubEquipe 03** | A hierarquia `Resposta` é o *Product* do padrão. Atributos e métodos foram mantidos. |
| **Entrega 02: BPMN do pedido (raia Órgão Público), SubEquipe 03** | Os gateways *"Admissível?"* e *"Informação pública?"* são a decisão que escolhe a fábrica concreta. |
| **Entrega 02: Enum `StatusManifestação`** | `emitirResposta()` leva o pedido de `EM_ANALISE` para `RESPONDIDO`. |
| **Entrega 02: Diagrama de Sequência, SubEquipe 01** | Continua o fluxo depois do envio do pedido e da geração do protocolo. |
| **Entrega 02: Protótipo `NovoPedido.tsx`, SubEquipe 01** | A implementação usa a mesma linguagem (TypeScript), o que facilita a integração. |
| **Entrega 01: SIG de Segurança (Confidencialidade/ABAC), SubEquipe 01** | A `FabricaRespostaParcial` garante que nenhuma resposta com ocultação seja criada sem base legal. |
| **Entrega 01: SIG de Confiabilidade (Rastreabilidade da fonte), SubEquipes 02 e 03** | Toda resposta criada carrega o agente responsável e, quando restringe acesso, o dispositivo legal. |

## Senso crítico

**Por que Factory Method, e não as alternativas?**

- **Simple Factory** (um método com `switch` que devolve a resposta certa): resolve o acoplamento do cliente, mas **não é um padrão GoF** e mantém o `switch`. Um novo tipo de resposta ainda obriga a editar a mesma classe.
- **Abstract Factory:** serve para criar **famílias** de objetos relacionados, por exemplo resposta + notificação + documento PDF de um mesmo "estilo". Hoje só criamos **um** produto por decisão, então seria complexidade sem ganho. Ela passa a fazer sentido se cada tipo de resposta tiver de gerar também a notificação ao cidadão e o comprovante.
- **Factory Method:** é a opção que se encaixa na estrutura que já existia. A hierarquia de produtos já estava modelada, e cada tipo tem **regras de criação próprias**, o caso clássico do padrão.

**Ganhos:**

- O Princípio Aberto/Fechado: uma nova *Resposta de Informação Inexistente* entra como um novo par (fábrica + produto), sem tocar no código existente.
- As regras de privacidade (LAI/LGPD) ficam **em um lugar só** por tipo de resposta, o que facilita a auditoria.
- O processo comum (`emitirResposta`) fica protegido: nenhuma fábrica consegue esquecer de vincular ou publicar.

**Custos e limitações:**

- **Mais classes:** cada produto ganha uma fábrica paralela. Com 3 tipos é aceitável. Com dezenas de tipos, as hierarquias paralelas pesam.
- **A escolha da fábrica não some, só se concentra.** Na demonstração, um mapa `Decisao → FabricaResposta` faz isso em um ponto único. Esse mapa **não faz parte do GoF** e foi uma decisão nossa.
- `DadosResposta` é um objeto com campos opcionais, validados em tempo de execução. Uma melhoria seria tipar os dados de cada fábrica separadamente (*generics*) e validar em tempo de compilação.
- O método `emitirResposta()` lembra o padrão comportamental **Template Method**. É comum os dois aparecerem juntos, e o próprio GoF cita essa relação.

## Uso de IA generativa

<!-- TODO (cada membro): ponto de vista individual, no mesmo formato da tabela do FOCO_03 da Entrega 02. -->

| Nome do Membro | Lições Aprendidas | Uso da IA Generativa (Senso Crítico) |
| --- | --- | --- |
| Isaac Lucas Souza Bezerra | | |
| André João Cordeiro Gomes | | |
| Rivadalvio Joaquim da Silva Filho | | |
| João Paulo Barros | | |

## Referências

- GAMMA, E.; HELM, R.; JOHNSON, R.; VLISSIDES, J. *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley, 1994. Capítulo 3: Creational Patterns, Factory Method.
- [Refactoring.Guru — Factory Method](https://refactoring.guru/pt-br/design-patterns/factory-method)
- [SourceMaking — Factory Method](https://sourcemaking.com/design_patterns/factory_method)
- [Especificação OMG UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/)
- [Material da disciplina — Profa. Milene Serrano](https://sites.google.com/view/unb-fcte-arqdsw)
- [PlantUML — Class Diagram](https://plantuml.com/class-diagram) e [Sequence Diagram](https://plantuml.com/sequence-diagram)
- [Lei de Acesso à Informação — Lei 12.527/2011](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm) (art. 7º §2º, 11 §1º, 15, 23 e 31)
- [Lei Geral de Proteção de Dados — Lei 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)
- [Portal Informa.BR](https://informabr.cgu.gov.br)

## Versionamento

| Versão | Data | Descrição | Autor(es) |
| --- | --- | --- | --- |
| 1.0 | <!-- TODO --> | Modelagem (classes + sequência), implementação e relatório do Factory Method | <!-- TODO --> |
| 1.1 | 18/10/2026 | Revisão de notação nos diagramas (nomes sem acento/espaço, composição, `DadosResposta` e `StatusManifestacao`), vídeo e referências complementados | Revisão SubEquipe 03 | |
