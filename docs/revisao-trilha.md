# Revisão pedagógica da trilha

Revisão das três seções das seis aulas existentes, em 8 de outubro de 2026,
partindo do commit `0c11f1d`. Foram lidos individualmente os **128 itens anteriores**
e confrontados os conteúdos com os enunciados e justificativas das **600 questões**,
mapas mentais, flashcards e quadros do material de apoio. A transcrição enviada
para uma aula futura não foi incorporada nesta revisão.

## Critério aplicado

| Seção | Finalidade | O que foi corrigido |
| --- | --- | --- |
| Resumo da aula | Explicar conceitos, funções, regras, condições e exemplos essenciais | Listas excessivamente resumidas, conceitos disponíveis apenas no feedback/material e falta de explicação de termos |
| Dicas e macetes | Ensinar como memorizar, relacionar ou resolver | Regras isoladas transferidas ao resumo; acrescentadas sequências, associações, fórmulas e roteiros com limites explícitos |
| Pegadinhas | Explicar uma confusão que pode produzir resposta errada | Definições isoladas substituídas por `Armadilha: … Correção: …`, explicando o erro e trazendo exemplos quando úteis |

O mesmo tema pode aparecer nas três seções com tarefas distintas. Isso permite
aprender o conceito, lembrar como aplicá-lo e reconhecer uma confusão. Foram
retiradas repetições literais e consolidados avisos equivalentes. Não houve quota
de itens por seção: os tamanhos refletem a abrangência de cada aula.

As pegadinhas são exemplos de confusão do conteúdo e do banco existente. Não há
evidência de frequência de cobrança nem promessa de que essas frases aparecerão
na prova. Essa distinção também aparece na introdução da seção no painel.

## Resultado por aula

As contagens indicam itens, não linhas, palavras ou assuntos novos.

| Aula | Resumo: antes → depois | Dicas: antes → depois | Pegadinhas: antes → depois |
| --- | --- | --- | --- |
| 1 — SFN | 9 → 11 | 10 → 7 | 8 → 9 |
| 2 — CMN | 7 → 13 | 5 → 6 | 5 → 8 |
| 3 — Banco Central | 7 → 14 | 5 → 7 | 5 → 10 |
| 4 — CVM | 7 → 13 | 6 → 7 | 6 → 10 |
| 5 — Seguros e previdência | 10 → 14 | 8 → 7 | 6 → 9 |
| 6 — Operadores | 10 → 18 | 8 → 8 | 6 → 11 |
| **Total** | **50 → 83** | **42 → 42** | **36 → 57** |

O arquivo [revisao-trilha-itens.json](revisao-trilha-itens.json) guarda cada texto
anterior, sua aula, seção e posição, e o destino no conteúdo atual. Os destinos
`r1`, `d1` e `p1` são posições de itens em `AL`, a partir de 1, dentro da respectiva
aula. Não são IDs de questões. O registro permite verificar também as fusões e
transferências; o aumento de itens não significa inclusão de uma nova aula.

## Conteúdo redistribuído ou recuperado

### Aula 1 — Sistema Financeiro Nacional

- A relação entre risco de inadimplência e spread era apenas uma frase em
  pegadinhas. Agora o resumo explica a relação, a dica ensina o cálculo e a
  pegadinha distingue compensação de perdas de lucro garantido.
- Foram recuperadas a obrigação do emissor do CDB perante o investidor, a
  classificação dos operadores por segmento e a mudança de posição de uma
  empresa entre aplicação e captação. Referências: questões 30, 44, 86, 202,
  203 e 215; quadro dos operadores em `MAT[1]`.
- Os cálculos passaram a distinguir diferença de taxas, margem após custos e
  taxa necessária para obter uma margem. Referências: questões 43, 84, 88,
  198, 211 e 214.
- A identificação do mercado não depende só do prazo: empréstimo de 90 dias
  é crédito e compra de euros é câmbio. Essa comparação substitui o atalho
  demasiado rígido sobre prazos. Referências: questões 81, 86 e 219.
- Consolidada a duplicação da Lei da Usura; a exceção ficou no resumo e ganhou
  uma confusão explicada em pegadinhas. A recomendação de mais de 80% foi
  mantida como método de autoavaliação, distinguida da nota oficial da prova.

### Aula 2 — Conselho Monetário Nacional

- Os objetivos deixaram de ser apenas quatro verbos: o resumo explica a
  finalidade de cada um; o mnemônico O-P-Z-C permanece nas dicas.
- Recuperadas as competências agrupadas em câmbio, crédito/juros, instituições
  e mercado/orçamento, incluindo o caráter excepcional do monopólio cambial.
  Referências: questões 36–39, 92, 94, 95, 233–239 e mapa de competências.
- Acrescentadas a composição completa da Comoc, contagem de 11 integrantes,
  coordenação, caráter reservado, convocação extraordinária e tarefas da
  Secretaria-Executiva. Referências: questões 97, 98, 105, 248–254, 259 e 276.
- Recuperados os elementos do regime de metas e a diferença entre janela de
  12 meses, comparação mensal e antecedência de 36 meses. Referências:
  questões 35, 240–244 e 270.
- Orçamento monetário virou sequência de resolução; Comoc/Copom e
  ministros/secretários viraram confusões explicadas, sem duplicar definições.

### Aula 3 — Banco Central

- O resumo explica o que corresponde a cada uma das quatro funções, além de
  listar os nomes. A dica usa o destinatário da operação para classificar.
  Referências: questões 74, 107, 114, 320, 325 e 338.
- Recuperados os requisitos dos dirigentes, datas do escalonamento,
  hipóteses de exoneração e a separação entre proposta, aprovação e ato de
  exoneração. Referências: questões 110, 111, 115, 303, 318, 327 e 335.
- Acrescentadas causas, medidas e prazo da comunicação de descumprimento,
  além das condições de nova comunicação. Referências: questões 61, 68,
  296, 324 e flashcards correspondentes.
- Os tetos de compulsórios, antes presentes apenas nos números/material,
  estão explicados no resumo e diferenciados de alíquotas aplicadas.
  Referências: questões 113, 322 e 330.
- As listas de autorizações, normas e exemplos de diretorias foram
  recuperadas do banco/material. Referências: questões 109, 292, 298,
  299, 308–311, 315 e 340.
- Proibição de emitir títulos próprios e distinção histórica entre BC e
  CVM foram transferidas ao resumo. A pegadinha sobre títulos agora mostra
  por que emitir dívida própria difere de negociar títulos públicos.

### Aula 4 — Comissão de Valores Mobiliários

- Recuperados instrumentos que o resumo não enumerava, o enquadramento
  dos contratos de investimento coletivo e a renovação anual do colegiado.
  Referências: questões 346, 357–359, 388 e 400; linha do tempo e flashcards.
- Os cinco blocos de atribuições passaram a ter exemplos; as dicas associam
  ações aos blocos e as pegadinhas mostram trocas plausíveis. Referências:
  questões 135, 136, 148, 160 e 361–366.
- Recuperados os poderes de investigação, os três alcances dos tetos de
  sanções, atenuantes e destinatários de comunicação de ilícitos. Referências:
  questões 137–140, 146, 153, 367–372, 383, 392, 393 e 396.
- Autorregulação ganhou finalidade, fundamentos e pressupostos. A hierarquia
  das normas ficou no resumo; a pegadinha explica por que uma entidade
  supervisora pode também ter competência normativa.

### Aula 5 — Seguros e Previdência

- A composição do CNPC, designação dos representantes e presença de grupos
  não governamentais foram recuperadas no resumo. Referências: questões
  470–472, 477, 483 e 485; mapa e tabela de composição.
- A presença mínima do CNPC e a maioria de integrantes da Previc estão
  explicadas separadamente da regra de decisão. A pegadinha mostra por que
  nove membros não se confundem com cinco presentes, nem a diretoria de
  cinco da Previc exige cinco presentes. Referências: questões 427, 428 e 490.
- Recuperados o Sistema Nacional de Seguros Privados, seus operadores e os
  atos destacados na tabela da Susep. Referências: questões 429, 430 e mapa.
- Autorizações e intervenção da Previc foram transferidas das dicas para
  o resumo; a dica passou a ensinar a resolver um cenário de entidade fechada.
- As comparações de ministérios, sedes, reuniões e nomeação deixaram de ser
  fatos isolados em pegadinhas: agora mostram inversões e o motivo da correção.
- O canal de venda de previdência aberta não muda o supervisor do produto;
  a comparação evita confundir banco distribuidor e órgão competente.

### Aula 6 — Operadores

- Recuperados abertura de crédito, desconto de títulos, finalidade do
  capital de giro e operações com depósitos e repasses. Referências:
  questões 511, 512, 529, 530 e 553–560; mapa de operações.
- Acrescentados grupos de atuação, categorias de cooperativas singulares,
  direitos/deveres, cotas-partes, sobras e perdas. Referências: questões
  568–572, 575–580, 587–590 e 592; tabela de classificação.
- A autorização para captar depósitos à vista e a exceção da categoria de
  capital e empréstimo ficaram explícitas. Referências: questões 507,
  564, 566 e 580.
- Recuperadas as diferenças entre atender associados e prestar certos
  serviços a não associados, sem generalização para toda a atuação.
  Referências: questões 581–585 e 600; tabela de atividades.
- Fórmulas da pirâmide cooperativa e exemplo dos 51% foram trazidos para
  dicas, com confusões de unidade e base de cálculo nas pegadinhas.
  Referências: questões 595, 596 e 599.

## Correções de consistência

1. A pegadinha e o mapa mental da aula 6 ainda afirmavam CNPJ independente por
   carteira, embora o resumo, as questões e outros materiais já descrevessem
   contabilidade separada por carteira e possibilidade de balanço único.
   Essas duas referências antigas foram corrigidas em coerência com as questões
   528, 574 e 597 já revistas na rodada anterior.
2. O quadro de números da aula 6 agora diz que **as centrais detêm as ações com
   voto do banco cooperativo**, eliminando a redação que situava as ações “nas
   centrais”. O item do balanço explicita possibilidade, em vez de obrigação.
3. O mapa e a tabela de instituições monetárias qualificam as cooperativas
   pela autorização para depósitos à vista; a categoria de capital e empréstimo
   é explicitamente excluída dessa captação no resumo.
4. A justificativa geral da questão **564** ainda dizia “Só captam prazos mais
   longos”, embora seu feedback específico já dissesse que o prazo não define
   uma instituição não monetária. A justificativa geral foi alinhada ao feedback,
   corrigindo também o texto que pode aparecer na revisão final dos simulados.
   Nenhum enunciado, alternativa, gabarito, ID ou feedback por alternativa mudou
   nesta rodada; foi alterado somente esse campo de justificativa geral em `Q`.

## Validação e padrão futuro

O teste de navegação existente foi ampliado para abrir as **18 seções**, conferir
todos os **182 itens renderizados**, as introduções das seções, a ausência de
repetição literal entre elas e o formato de armadilha/correção. Também foi
conferida a rastreabilidade dos 128 itens anteriores e a preservação das linhas
de questões, com a única exceção documentada da justificativa da questão 564.

Comandos de validação:

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/smoke.py
```

Resultado local: **28 testes aprovados** (6 de estrutura do banco, 5 de qualidade
de alternativas e 17 de navegador), além da auditoria de tamanho. Os testes de
navegador também conferiram os 2.400 vínculos entre alternativas e feedbacks,
histórico, simulados e demais fluxos existentes. Isso não representa confirmação
da execução do GitHub Actions ou da publicação do Pages.

O padrão editorial permanente está em `AGENTS.md`: revisar item por item,
conferir a cobertura com transcrições/slides/questões/material, mostrar um método
real em cada dica, explicar o erro em cada pegadinha e procurar versões antigas
em outros materiais ao corrigir uma contradição.

Esta é uma revisão de organização, cobertura e coerência com o material existente.
Os complementos vêm do banco e dos materiais já presentes; não representam uma
consulta independente às normas vigentes. Composições, datas e regras jurídicas
da aula não foram recertificadas por fontes oficiais nesta etapa. Os testes
confirmam estrutura e funcionamento, não completude pedagógica ou validade legal.
