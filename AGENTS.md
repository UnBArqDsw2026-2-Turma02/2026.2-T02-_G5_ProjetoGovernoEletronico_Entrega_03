# AGENTS.md — Guia anti-erros do G5 (Padrões de Projeto — Entrega 03)

> **Leia antes de editar este repositório.** Este documento consolida os critérios de avaliação da professora e os erros já apontados nas Entregas 01 e 02, aplicados ao escopo da Entrega 03 (Módulo Padrões de Projeto). Vale para pessoas e para agentes de IA (ex.: opencode) que trabalharem no projeto.

---

## 0. Resumo executivo — o que mais derruba nota

1. **Artefato sem código rodando**: padrão só desenhado, sem implementação e sem vídeo de execução.
2. **Notação UML errada** ou modelo do padrão mal rotulado.
3. **Falta de fontes** em qualquer foco ("Sem Fontes" no parecer).
4. **Falta de rastros de trabalho em equipe**: pontos de vista diferentes, debates, consensos, divergências, atas e gravações.
5. **Versionamento fraco**: "única versão", "modelo não histórico de versões", versão do relatório divergente do commit.
6. **Metodologia e senso crítico "pouco revelados"**.
7. **Erros de forma**: acentos/espaços em nomes de classes, falta de estereótipos, associações sem semântica.
8. **IA generativa sem evidência concreta** de uso e sem crítica.
9. **Participações sem comprobatório** (commit ou registro no histórico de versão identificável).

---

## 1. Contexto da Entrega 03

| Item | Valor |
| --- | --- |
| Disciplina | Arquitetura e Desenho de Software (ADS) — Profa. Milene Serrano |
| Instituição | UnB / FCTE (FGA) |
| Semestre / Turma | 2026.2 / Turma 02 |
| Grupo | G5 — Projeto Governo Eletrônico (base: portal Informa.BR / LAI / CGU) |
| Organização | 3 subequipes: `SubEquipe01`, `SubEquipe02`, `SubEquipe03` |
| Repositório | https://github.com/UnBArqDsw2026-2-Turma02/2026.2-T02-_G5_ProjetoGovernoEletronico_Entrega_03 |
| GitPages | https://unbarqdsw2026-2-turma02.github.io/2026.2-T02-_G5_ProjetoGovernoEletronico_Entrega_03/ |
| Contato da profa. | mileneserrano@unb.br — FCTE, sala 27 (UED) |

### Focos da entrega

| Foco | Conteúdo | Entrega mínima |
| --- | --- | --- |
| FOCO_01 | GoFs Criacionais + IA Generativa | 1 padrão criacional com **modelo & código & vídeo rodando** |
| FOCO_02 | GoFs Estruturais + IA Generativa | 1 padrão estrutural com **modelo & código & vídeo rodando** |
| FOCO_03 | GoFs Comportamentais + IA Generativa | 1 padrão comportamental com **modelo & código & vídeo rodando** |

Além disso, **cada membro** deve registrar seu ponto de vista sobre lições aprendidas e uso crítico da IA Generativa.

### Divisão atual (a confirmar)

| SubEquipe | Categoria |
| --- | --- |
| SubEquipe 01 | GoFs Comportamentais |
| SubEquipe 02 e SubEquipe 03 | GoFs Criacionais e Estruturais (definir quem fica com qual) |

### Datas (Módulo Padrões de Projeto)

| Data | Evento |
| --- | --- |
| 16/10/2026 | Dinâmica de Elaboração (Aula 18) |
| **19/10/2026** | **Entrega via Aprender3 (todos os grupos)** + Avaliação Parte I (G1–G4) |
| **23/10/2026** | **Apresentação do G5 — 08:00–08:20, sala 27 UED** (Avaliação Parte II, G5–G8) |

- Se o Aprender3 falhar, enviar por e-mail para a profa. **dentro do prazo**.
- A apresentação é presencial, com os representantes, e os artefatos devem ser salvos com antecedência (internet da UnB). Levar máquina própria.

### Menções individuais

- Entrega mínima cumprida pela equipe → base **MM**.
- Deixar de contribuir em **1 dos 3 focos** → **MI**.
- Deixar de contribuir em **2 dos 3 focos** → **II**.
- Não contribuir em **nenhum foco** → **SR**.
- Confirmar com a profa. se a contribuição esperada é em todos os focos ou apenas no foco do próprio subgrupo.

### Estrutura relevante do repositório (Docsify)

- `docs/index.html`, `docs/_sidebar.md`, `docs/README.md`
- `docs/Base/1.PadroesDeProjeto.md` (intro do módulo + regras)
- `docs/Base/Relatórios/1.1.1.SubEquipe_01.md`, `1.1.2.SubEquipe_02.md`, `1.1.3.SubEquipe_03.md`
- `docs/Base/1.2.ParticipacoesPadroesDeProjeto.md` (quadro de participações)
- `docs/Base/1.3.IniciativasExtras.md`
- `docs/Projeto/Projeto.md`

---

## 2. Como a professora avalia (rubrica)

| Dimensão | O que ela verifica |
| --- | --- |
| Contribuições Gerais (análise) | Análise quantitativa (nº de padrões), escopo, **notação UML correta**, aderência ao padrão escolhido, presença de código e execução |
| Qualidade | Muito Alta / Alta / Média / Baixa / Nula |
| Rastreabilidade & Elos com Outros Artefatos | Relação com os artefatos das Entregas 01 e 02, decisões rastreáveis, commits |
| Senso Crítico | Pontos de vista diferentes, debates, consensos, divergências, o que deu errado e por quê |
| Fontes | Referências com links (GoF, refactoring.guru, sourcemaking, material da professora) |
| Versionamento & Participações | Histórico com data/autor/descrição e **comprobatórios individuais** (commits) |
| Metodologia | Como o grupo trabalhou: reuniões, atas, gravações, checklists, deliberações |

**Menções:** SS (Superior) > MS (Médio Superior) > MM (Médio) > MI (Médio Inferior) > II (Inferior) > SR (Sem Rendimento).

**Participação:** "Todos Participam Conferindo Pontos de Vista" > "Maioria Participa" > "Minoria Participa" > "Sem Destaque".

---

## 3. Histórico dos pareceres (lições das Entregas 01 e 02)

### Entrega 01 — `T02 - G5 - Parecer Entrega_01.pdf`

- Análise real: **MI** nos três subgrupos; **André João: II** (atuou só no FOCO_03 e de forma pontual). Menção final: **PLUS MM** para todos, exceto André João.
- Críticas recorrentes:
  - "Em geral, faltam rastros para trabalho em equipe, coleta de pontos de vista diferentes, versionamentos."
  - "Sem rastros para os insumos usados, a base que gerou os artefatos."
  - "Sem fontes", "Modelo não histórico de versões", "Pouco revelado em geral".
  - IA Generativa: "relatos simples... faltam fontes, versionamentos, trabalho em equipe, senso crítico".
  - Iniciativas Extras: "Faltam rastros, versionamentos, trabalho em equipe, senso crítico, fontes consultadas e embasamento".

### Entrega 02 — `document(3).pdf`

- Menções: SubEquipes 01 e 02 → **MS**; **SubEquipe 03 → MM**; Tiago → **SR** (sem atuação).
- **FOCO_01 (Estático, SubEquipe 03):** "Média+. Capricham pouco nos rastros." Faltou `<<enumeration>>` em `StatusManifestação`; acentos e espaços nos nomes das classes; `Manifestação → Resposta` ("origina") provavelmente é **composição**; associações sem semântica; "pouco senso crítico revelado"; "Metodologia: pouco revelada".
- **FOCO_02 (Dinâmico, SubEquipe 03):** "**Avaliando como diagrama de estados, seria Qualidade Nula, pois não atende a notação UML.**" O artefato era um **BPMN** (verbos/ações, gateways, raias), não uma máquina de estados. "Sem Fontes." "Única versão."
- **FOCO_03 (IA):** pontos de vista presentes, mas "sem evidências claras de uso da IA Generativa"; sem fontes.
- **Iniciativas Extras:** SubEquipe 03 **sem nenhum registro** (as SubEquipes 01 e 02 têm ata + gravação).

### Erros recorrentes → correção obrigatória

| Erro | Evidência no parecer | Correção |
| --- | --- | --- |
| Sem fontes | "Sem Fontes", "sem fontes esclarecidas" | Mínimo de 3 fontes por artefato, com links |
| Sem histórico de versões | "única versão" | Tabela de versionamento real (v0.1 → v1.0) |
| Sem rastros de equipe | "faltam rastros... pontos de vista diferentes" | Atas, gravações, debates, consensos, divergências |
| Metodologia fraca | "pouco revelada" | Descrever como o artefato foi produzido, passo a passo |
| Senso crítico fraco | "pouco senso crítico revelado" | Registrar erros, alternativas descartadas e por quê |
| Notação errada | "não atende a notação UML" | Conferir o tipo de diagrama antes de rotular |
| Forma dos nomes | "acentos e termos separados por espaços" | Nomes sem acento e sem espaço |
| Estereótipos ausentes | "indicar que é um `<<enumeration>>`" | Declarar estereótipos de forma explícita |
| IA sem evidência | "sem evidências claras de uso da IA" | Prints, links de chat, prompts, antes/depois |
| Sem iniciativas extras | "Subgrupo 03, sem registros" | Ao menos 1 ata + gravação por entrega |
| Sem código/execução (E3) | exigência da Entrega 03 | Implementar o padrão e gravar vídeo rodando |

---

## 4. Regras de ouro (obrigatórias)

1. **Modelo & código & vídeo rodando** para o padrão do subgrupo — sem isso, a entrega mínima não existe.
2. **Nunca** rotular um diagrama com notação errada. BPMN não é UML.
3. Toda **associação** deve ter semântica (rótulo/papel) e multiplicidade correta; usar composição/agregação quando couber.
4. **Nomes de classes, estados e atividades sem acento e sem espaço** (ex.: `PedidoAcesso`, `RespostaDeferida`).
5. **Estereótipos explícitos**: `<<enumeration>>`, `<<abstract>>`, `<<interface>>` etc.
6. **Fontes em todo foco**, com links (GoF, refactoring.guru, sourcemaking, material da profa., LAI).
7. **Versionamento real**: histórico com versão, data, autor e descrição; nunca "única versão".
8. **Comprobatórios individuais**: commits por membro (não apenas um commit coletivo).
9. **Metodologia explícita**: reunião → ata → gravação → decisão → artefato.
10. **Senso crítico**: documentar o que deu errado, o que mudou de ideia e por quê.
11. **IA generativa com evidência e crítica**: mostrar o uso e o que foi validado/descartado.
12. **Iniciativas extras**: pelo menos uma por entrega, com ata + gravação.
13. **Versionar a fonte e o render**: manter o `.puml` e re-gerar PNG/PDF após qualquer alteração; manter o código do padrão no repositório.

---

## 5. Guia por foco (Entrega 03)

### 5.1 GoFs Criacionais + IA Generativa

Checklist mínimo:
- [ ] Contexto (Problema) descrito com o domínio do Informa.BR/LAI.
- [ ] Padrão escolhido e justificado (ex.: Factory Method, Abstract Factory, Builder, Prototype, Singleton).
- [ ] Modelagem UML (classes/sequência) do padrão.
- [ ] Código implementado, com explicação dos participantes do padrão.
- [ ] Link do código no repositório + **vídeo do padrão rodando**.
- [ ] Fontes, versionamento, metodologia, senso crítico e participações.

### 5.2 GoFs Estruturais + IA Generativa

Checklist mínimo:
- [ ] Contexto (Problema) descrito com o domínio do Informa.BR/LAI.
- [ ] Padrão escolhido e justificado (ex.: Adapter, Facade, Proxy, Decorator, Composite, Bridge, Flyweight).
- [ ] Modelagem UML do padrão.
- [ ] Código implementado, com explicação dos participantes do padrão.
- [ ] Link do código no repositório + **vídeo do padrão rodando**.
- [ ] Fontes, versionamento, metodologia, senso crítico e participações.

### 5.3 GoFs Comportamentais + IA Generativa (SubEquipe 01)

- Mesma estrutura, com padrão comportamental (ex.: Observer, Strategy, State, Command, Iterator).

### 5.4 Estrutura obrigatória do relatório da subequipe

1. `FOCO_0X: [Categoria] & IA Generativa` + entrega mínima.
2. `Participantes no Foco`: Membro | Lições aprendidas | Uso da IA Generativa (senso crítico).
3. `Metodologia do Foco` (reuniões, atas, gravações, debates, divergências).
4. `[Padrão GoF]`: **Contexto (Problema)** → **Modelagem (UML)** → **Implementação (código & vídeo rodando)**.
5. `Versionamentos`: Membro | Contribuição | Data.
6. Observações.

### 5.5 IA Generativa (FOCO_03 de cada subequipe)

- [ ] Cada membro tem seu próprio ponto de vista (lições aprendidas + uso crítico).
- [ ] Evidência concreta de uso: print do chat, link compartilhável, prompts usados, versão gerada vs versão final.
- [ ] Crítica: o que a IA errou, o que foi validado na literatura e o que foi descartado.
- [ ] Fontes e versionamento.

### 5.6 Iniciativas Extras

- [ ] Pelo menos uma por entrega (ex.: reunião de deliberação, revisão por pares, checklist de padrões).
- [ ] Ata + gravação + decisões.
- [ ] Registrar na página `docs/Base/1.3.IniciativasExtras.md` com links.

---

## 6. Convenções do repositório

- **Docsify:** ao criar página, adicionar em `docs/_sidebar.md` e usar links relativos consistentes.
- **Artefatos:** colocar em `docs/Base/Relatórios/ExtrasSubEquipe_XX/`; manter a fonte (`.puml`) ao lado do render (`.png`/`.pdf`/`.svg`) e o código do padrão.
- **Git:** trabalhar na branch `SubEquipeXX`; abrir PR para `main`; commits atômicos com escopo (`docs(subequipe-03): ...`).
- **Mensagens de commit:** diretas, sem parentéticos/explicações desnecessárias.
- **Participações:** atualizar `docs/Base/1.2.ParticipacoesPadroesDeProjeto.md` com contribuição + significância + comprobatório por membro.

---

## 7. Checklist final antes de entregar

**Artefato (por subequipe)**
- [ ] Modelo UML do padrão (notação correta, nomes sem acento/espaço, estereótipos).
- [ ] Código implementado e versionado no repositório.
- [ ] Vídeo com o padrão **rodando**.
- [ ] Contexto/Problema, Modelagem, Implementação explicados no relatório.
- [ ] Fontes (mín. 3) com links.

**Equipe**
- [ ] Histórico de versões com data/autor/descrição.
- [ ] Participações com commit individual comprobatório (foco + qualidade).
- [ ] Metodologia descrita (reunião → ata → gravação → decisão).
- [ ] Senso crítico registrado.
- [ ] Ponto de vista de IA de todos os membros, com evidência.
- [ ] Iniciativas extras registradas com ata/gravação.

**Publicação**
- [ ] `.puml` + PNG/PDF re-gerados e código no repositório.
- [ ] Links do GitPages funcionando.
- [ ] Entrega enviada via Aprender3 no prazo (**19/10**), com backup local para a apresentação (**23/10, 08:00–08:20**).

---

## 8. Templates

### 8.1 Versionamento

| Nome do Membro | Contribuição | Versão | Data |
| --- | --- | --- | --- |
| Nome | O que fez | v0.1 | dd/mm/aaaa |

### 8.2 Fontes

- [Título da fonte](URL) — como foi usada no artefato.

### 8.3 Metodologia por foco

1. Reunião (data, participantes, link da gravação, ata).
2. Definição do padrão e justificativa.
3. Divisão de responsabilidades.
4. Iterações (v0.1 → v1.0) e o que mudou.
5. Revisão coletiva e deliberação.
6. Rastreabilidade com as Entregas 01 e 02.

### 8.4 Ata de reunião

- Data, horário, participantes, pauta, decisões, divergências, encaminhamentos e link da gravação.

---

## 9. Citações da professora (referência)

- "Avaliando como diagrama de estados, seria Qualidade Nula, pois não atende a notação UML."
- "Não é modelo de estados. Procure tratar como modelo de atividades, para conferir alguma menção e não prejudicar o SubGrupo."
- "Indicar usando <<stereotype>> que 'StatusManifestacao' é um <<enumeration>>."
- "Evitar acentos e termos separados por espaços nos nomes das classes."
- "Sem fontes consultadas." / "Sem Fontes."
- "Metodologia: pouco revelada."
- "Pouco senso crítico revelado."
- "Em geral, faltam rastros para trabalho em equipe, coleta de pontos de vista diferentes, versionamentos."

---

## 10. Comandos úteis

```bash
# ver o site localmente (Docsify)
npx docsify-cli serve docs

# renderizar PlantUML local (se tiver plantuml.jar)
java -jar plantuml.jar -tpng arquivo.puml

# conferir branches e sincronizar com a main
git fetch --all --prune
git log --oneline main..HEAD

# exportar a sessão de IA (opencode)
opencode export <sessionID>
```

> Em caso de dúvida de notação, consulte a especificação OMG UML 2.5.1 e o material da professora antes de finalizar o artefato.
