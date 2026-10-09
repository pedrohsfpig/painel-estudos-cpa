# Desenvolvimento do painel CPA

Use o checkout existente: as tarefas de nuvem já são isoladas. Não crie worktrees
sem solicitação explícita do usuário. O aplicativo é uma página independente em
`index.html`; não introduza dependências de servidor para funcionalidades locais.

## Regra permanente de feedback

O usuário exige feedback da alternativa correta e das três incorretas em TODAS
as questões, após a resposta, exceto nos simulados. Isso inclui Estudo, Hardcore,
estudo diário, prática por aula, revisão de erros e futuras aulas ou conteúdos.

- Toda questão de `Q` precisa de `q[11]`: quatro explicações em texto, na ordem
  original das alternativas `q[4]`, `q[5]`, `q[6]`, `q[7]`.
- A primeira justifica a resposta correta. Cada outra explica o erro específico
  daquela opção; não substitua por quatro cópias da justificativa geral.
- Em perguntas que pedem INCORRETA, NÃO, exceções ou combinações de afirmações,
  explique por que a opção atende ou não ao enunciado. Não chame uma afirmação
  verdadeira de falsa só porque ela não é a resposta pedida.
- Em contas, indique a operação ou o abatimento omitido. Em associações, indique
  os papéis ou posições trocados. Evite apenas repetir que a resposta está errada.
- O feedback acompanha o índice original da opção, inclusive após embaralhar.
  Nunca derive seu vínculo de A/B/C/D nem do lugar da opção na tela.
- Não exiba os feedbacks antes da resposta. Mostre os quatro depois de acertar
  OU errar, inclusive das alternativas eliminadas pelas ajudas.
- Nos simulados, preserve o avanço sem feedback imediato e a revisão geral já
  existente no resultado; não acrescente o bloco de quatro feedbacks ao simulado.
- Adicione questões ao final de `Q`; não reordene os IDs já usados em `cpaH`.
  Preserve o histórico existente e as ajudas/opções originais ao evoluir o esquema.

Antes de publicar alterações em questões ou feedbacks, execute:

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/smoke.py
```

A validação de conteúdo é feita também na inicialização. Nenhuma questão nova
deve ser publicada com explicação faltando, vazia ou repetida para todas as opções.
Os testes automáticos verificam estrutura e comportamento; confira também o
conteúdo pedagógico de cada nova explicação com as aulas e referências fornecidas.

## Qualidade permanente das alternativas

- Redija as quatro opções com o mesmo tipo de resposta e estruturas comparáveis.
  Em números, use as mesmas unidades; em associações, o mesmo número de posições.
- Não deixe explicações, ressalvas ou listas completas exclusivamente na correta.
  Informação para ensinar a resposta deve ficar no feedback depois da escolha.
- Use distratores plausíveis do tema: confusão de competências, troca de etapas,
  inversão de termos ou erros de cálculo. Evite assuntos alheios e opções absurdas.
- Revise o conjunto inteiro para ter uma única resposta defensável. Se a pergunta
  é sobre um mínimo, diga mínimo; se exige uma ordem, explicite a ordem.
- Ao reescrever uma opção, confira seu feedback, a dica e o material de apoio.
  Distinga regra legal, simplificação da aula e mnemônico; não trate macete como lei.
- Audite as quatro posições de tamanho, por caracteres e palavras, com empates.
  Não transforme a menor ou uma posição intermediária em nova pista.
- Use `shuffle` (Fisher–Yates) para embaralhar opções, sem perder o índice de
  origem; não use `sort` com comparador aleatório, que favorece certas posições.
- Os limites automáticos são alertas editoriais, não quotas de autoria. Não use
  preenchimento artificial para atingir métricas nem nomes falsos para igualar
  o tamanho de nomes reais. O teste de tamanho não substitui revisão pedagógica.

O site publicado usa `main` no GitHub Pages. Quando o usuário pedir atualizações
para vê-las no site, valide, envie os commits e informe o resultado real do envio.
Não confunda envio ao GitHub com confirmação de que o Pages já publicou.

## Padrão permanente da trilha, para TODAS as aulas

O usuário exige revisão individual de cada item das três seções de `AL`, inclusive
nas aulas futuras. Siga a finalidade pedagógica, sem preencher seções por quota:

- Priorize **efetividade e consulta rápida**. O usuário quer bater o olho e lembrar
  conceitos, não reler a aula. Use frases diretas e destaque o essencial. Não há
  quota de itens ou palavras; não aumente o texto só para explicar tudo.
- `r` / Resumo da aula: conceitos, funções e regras essenciais, na forma mais
  curta que preserve o sentido. Um fato isolado sobre composição, competência,
  início de mandato ou fluxo de exoneração pertence aqui, não em pegadinhas.
- `d` / Dicas e macetes: associações mentais, mnemônicos, sequências, fórmulas e
  orientações úteis à aprendizagem. Seja direto; não imponha passos ou exemplos
  quando a associação por si já cumpre o objetivo.
- `p` / Pegadinhas: ambiguidades, conceitos confundíveis, ressalvas ou pontos de
  atenção para não errar. Compare o que pode ser trocado ou marque a condição que
  muda a resposta. Uma definição isolada deve voltar ao resumo.
- **Não use os prefixos “Armadilha” ou “Correção”. Não imponha feedback.** Só
  explique o motivo ou use um exemplo se for necessário à compreensão. Não
  prometa que uma distinção aparecerá na prova.
- Um mesmo tema pode aparecer nas três seções se cumprir funções diferentes:
  conceito no resumo, associação na dica, ambiguidade na pegadinha. Não copie o
  mesmo texto entre seções nem repita avisos com redações equivalentes.
- Antes de incluir uma aula, confira a transcrição e os slides fornecidos, os
  tópicos de todas as questões e o material de apoio. Faça uma lista de cobertura:
  conceitos importantes precisam estar acessíveis no resumo; números, exceções
  e competências precisam ser consistentes com dicas, pegadinhas e feedbacks.
- Transcrições podem ter erros de reconhecimento. Confira nomes, números, negações
  e exceções com os slides ou outra fonte fornecida; não invente lacunas nem trate
  uma fala do professor como confirmação independente de norma vigente. Se houver
  uma divergência que afete a resposta, resolva ou sinalize antes de publicar.
- Preserve a aula à qual cada material pertence. Não incorpore uma transcrição
  enviada para uma aula futura durante uma revisão das aulas existentes.
- Respeite o escopo da solicitação: na revisão restrita destes três tópicos,
  altere apenas `AL.r/d/p` e a apresentação específica dessas seções. **Não altere
  questões, feedbacks, números para decorar, mapas, tabelas ou outras áreas.**
  Se identificar divergência fora desse escopo, informe sem modificar esses dados.
- Use `**conceito**` para negrito em palavras-chave, responsáveis e números úteis.
  Evite destacar parágrafos inteiros ou dar destaque a todas as palavras.
- Cores semânticas, iguais em todas as aulas e seções, inclusive futuras:
  `{{atencao|condição/exceção}}` → lilás (`--lesson-attention`), claro no tema
  escuro e mais escuro no tema claro para preservar a legibilidade;
  `{{negacao|negação/proibição}}` → vermelho (`--hd`). Destaque comum permanece
  na cor do texto. A borda identifica a seção: resumo azul, dicas amarelo,
  pegadinhas vermelho. Não atribua uma cor diferente a um órgão ou número sem
  motivo semântico; não use cores arbitrárias nem dependa só delas para ensinar.
- A formatação passa por `lessonText`, que escapa o texto e interpreta apenas
  esses marcadores. Não use HTML bruto nos itens de `AL`. Não altere estilos de
  outras áreas para formatar os três tópicos.
- Mantenha `AL` como JSON válido. Preserve ordem das aulas, vínculos com `Q` e IDs
  existentes. Os relatórios em `docs/revisao-trilha*` são registros históricos
  da primeira reorganização; este padrão incorpora a correção posterior do
  usuário sobre concisão, remanejo e destaque visual.

Antes de publicar mudanças na trilha, execute os quatro comandos de validação
acima. O teste de navegação abre e confere as três seções das seis aulas. Faça
também revisão pedagógica manual: testes de estrutura e renderização não provam
completude, qualidade de um macete ou validade jurídica.
