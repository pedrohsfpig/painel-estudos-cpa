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
- No computador, apresente cada alternativa à esquerda e seu feedback à direita
  na mesma linha. Use o mesmo vínculo na revisão de erros e mantenha as quatro
  explicações visíveis, inclusive para alternativas eliminadas pelas ajudas.
  Evite repetir o texto da alternativa em outro bloco abaixo; em janelas pequenas,
  a explicação pode ficar imediatamente abaixo da alternativa correspondente.
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

## Painel e navegação no computador

O menu lateral usa ícones pequenos e permanece fixo nas telas de computador.
Preserve as ações existentes ao modificar a apresentação; não reinicie uma
sessão ao navegar ou trocar de tema. Os indicadores devem usar dados reais:
tentativas incluem repetições; andamento da aula mede questões únicas praticadas
(prova + Hardcore); pendências seguem a última resposta de cada questão. Não
apresente cobertura como domínio. Filtros de estatísticas afetam tentativas,
evolução e desempenho detalhado; trilha e pendências usam o histórico completo.
O acesso à última aula se baseia no histórico e abre seus materiais, sem alegar
restauração de uma sessão. Trate histórico vazio e novas aulas sem números fixos.
Confira os dois temas e os fluxos existentes antes de publicar mudanças no painel.
Mantenha as colunas independentes: trilha e evolução na principal, prioridades
e última aula empilhadas na lateral. Priorize números e títulos legíveis, com
textos secundários discretos; padronize bordas e ícones sem sugerir que cartões
estáticos sejam clicáveis. Reações ao mouse devem ser suaves e respeitar a
preferência por movimento reduzido. Ao renomear uma aula, mantenha consistência
entre `AL.t`, `AU` e o título do mapa em `MAT`, preservando IDs e conteúdos.
O sumário da aula abre e foca a seção escolhida sem renderizar novamente o app,
alterar o histórico ou reiniciar sessões. Preserve ícones e cores das seções.
A barra da sessão conta respostas concluídas: `qz.i` mais a resposta atual,
quando existente; não marque a questão apenas exibida como já respondida. O
cronômetro continua usando `qz.t0`. Destaques de feedback devem manter a ordem
e o índice original das alternativas e as quatro explicações integralmente
visíveis após responder, sem feedback imediato nos simulados.

## Alternância global de tema

O botão de lâmpada fica fixo no canto superior esquerdo, fora de `#app`, em todas
as telas, incluindo questões e resultados. Não remova esse controle ao renderizar
uma view nem reinicie questões, cronômetros ou materiais ao alternar o tema.
Reserve espaço para evitar sobreposição no celular e mantenha rótulo acessível,
foco por teclado e área clicável de pelo menos 44 × 44 pixels. A preferência fica
em `cpaTheme`, separada de `cpaH`, e deve funcionar mesmo sem armazenamento local;
sem escolha salva, acompanhe o tema do dispositivo. Aplique a escolha salva antes
da primeira renderização e respeite os destaques semânticos nos dois temas.

## Apresentação dos materiais de apoio

O usuário exige preservar os textos, quantidades e hierarquia dos mapas,
diagramas, tabelas e prazos de `MAT`. Uma mudança visual não autoriza resumir,
reescrever ou excluir informações. Confira os dados antes/depois e a presença de
cada texto renderizado. Na revisão solicitada de flashcards, reformule perguntas
vagas e esclareça respostas, preservando os conceitos, a ordem e a dificuldade.

- Mostre o nome completo da aula selecionada e mantenha abas com ícones pequenos.
- Mapas usam conceito central, conexões e ramificações; preserve os subgrupos e
  deixe todas as informações abertas para consulta. Não transforme tópicos pares
  em etapas sucessivas ou em subordinados entre si. Títulos principais são
  centralizados e destacados em maiúsculas; subtítulos abrem grupos delimitados
  que contêm os tópicos correspondentes, com recuo e conexões próprios.
  A estrutura principal de TODOS os mapas é azul (`--ac`): títulos de ramificação,
  ícones, conexões e composições não herdam a cor do órgão na tabela. Outras cores
  distinguem somente conceitos comparados dentro dos grupos, via
  `MATERIAL_MAP_COMPARISONS`; negativas reais continuam vermelhas. Priorize a
  composição/diretoria na primeira linha, após a natureza, usando `mapBranches`
  sem reordenar os dados de `MAT`. Em aulas com vários órgãos, preserve a ordem
  dos órgãos e mantenha cada composição na ramificação do próprio órgão.
- Diagramas `f` mantêm os fluxos e a ordem das setas; diagramas `g` ligam os
  elementos do mesmo grupo ao título, sem criar relações sequenciais. Preserve
  as cores de papéis já existentes em cada nó. Conexões decorativas usam a cor
  de destaque do tema.
- Tabelas mantêm todas as células, com grade horizontal e vertical, cabeçalhos de
  coluna padronizados e cabeçalhos de linha distintos. Não use listras alternadas.
  Comparações têm colunas de conteúdo com larguras iguais, cores por entidade
  consistentes via `MATERIAL_COLUMN_COLORS` e destaque nas diferenças, inclusive
  negativas. Use negrito nos números e condições, sem mudar textos das células.
  Centralize cabeçalhos e corpo de todas as células. Entidades e conceitos de
  comparação são colunas; os aspectos são linhas. O eixo depende do objetivo:
  em “Os três tipos de entidade”, Normativa/Supervisora/Operacional são colunas,
  com Papel e Exemplos nas linhas. Já no “Quadro do SFN”, os segmentos são
  colunas e Normativo/Supervisor/Operadores são linhas. Não escolha o eixo só
  pela palavra “tipo” ou “classificação”; examine o que se deseja comparar.
  Registre inversões em `MATERIAL_TRANSPOSE_TABLES`,
  preservando o conteúdo original de `MAT` e os vínculos de cada célula.
- Use `collegiateChart` para composições: presidência/coordenação acima dos demais
  membros, com o mesmo desenho para todos os órgãos. Mostre somente papéis e
  quantidades disponíveis no material. Dentro do quadro de liderança, mostre o
  cargo e o órgão entre parênteses, via `collegiateOrgan` e `collegiateChart`.
  Preserve a distinção entre presidente, coordenador e superintendente; a Comoc
  é coordenada pelo presidente do BC. Use nomes pessoais apenas se fornecidos
  nas fontes e pertinentes à aula, sem inventar titulares atuais. No CNSP, a
  fonte identifica o representante da Fazenda; não o substitua automaticamente
  pelo ministro. Imagens precisam expressar relações reais, sem sugerir
  subordinação entre diretores pares. Identifique o que se renova antes da taxa
  (por exemplo, renovação do colegiado: 1/5 por ano); mantenha datas em calendário
  e durações em escala. Não invente mandatos ou datas para preencher campos.
- Linhas conectadas com setas representam apenas sequências e cronologias que
  existem no material. Durações comparáveis usam trilhas em escala comum;
  periodicidades mostram recorrência; regras e quóruns usam linhas de referência.
  Não use hashtags nem invente cronologia entre penalidades. O calendário pode
  ordenar visualmente janeiro antes de julho, mantendo todos os fatos e os dados
  originais. Ao acrescentar uma sequência, registre o título em
  `MATERIAL_SEQUENCES`, sem reescrever seu conteúdo para caber no desenho.
- Flashcards mantêm pergunta/resposta, dificuldade e navegação circular, com
  controles por mouse e teclado. A barra mostra a posição do cartão, sem sugerir
  domínio ou memorização. Trocar aula/tipo reinicia apenas o cartão, não a sessão
  de questões nem o histórico. Alternar tema preserva o cartão e sua face.
  A resposta tem fundo lilás, borda e rótulo próprios. Cada pergunta deve indicar
  explicitamente o conceito, órgão ou aspecto que a pessoa precisa recordar;
  evite fragmentos como “Empréstimo x financiamento?”. Comparações devem dizer
  o que comparar; cálculos devem indicar a grandeza e a unidade pedidas. Uma
  possibilidade de recondução não pode virar permanência automática.
- Nos materiais de contexto, aplique vermelho (`--hd`) à frase negativa e ao
  objeto negado: “não recebem depósitos à vista”, “sem recondução”. Rótulos de
  classificação (“não monetárias”, “não bancárias”, “não associados”) não são
  afirmações negativas e não recebem vermelho. Nas comparações, use cores
  distintas e constantes por conceito/órgão; `contextHeading` distingue as
  classificações monetária (azul) e não monetária (lilás). Use `contextText` nos
  mapas, diagramas, tabelas e prazos;
  `lessonText` mantém os marcadores e também destaca negativas na trilha.
  Preserve exceções e condições afirmativas fora do trecho negativo. Não pinte
  negativas em questões, alternativas, seus feedbacks, controles do sistema ou
  flashcards. Confira a marcação no contexto; cores não autorizam mudar fatos.
- Confira os dois temas e larguras de PC. Restrinja os estilos aos materiais e
  preserve o painel, a trilha, as questões, os simulados e o armazenamento.

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
