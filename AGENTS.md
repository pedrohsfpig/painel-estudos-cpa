# Desenvolvimento do painel CPA

Use o checkout existente: as tarefas de nuvem já são isoladas. Não crie worktrees
sem solicitação explícita do usuário. O aplicativo é uma página independente em
`index.html`; não introduza dependências de servidor para funcionalidades locais.

## Referência permanente de prioridades da prova — 27/10/2026

O usuário forneceu o quadro de relevância registrado integralmente em
`docs/guia-da-prova.md` e `EXAM_GUIDE_REFERENCE` (`exam-guide.js`). Use essa
referência até ele informar atualização; não a apresente como edital oficial
verificado. Ordem: Aula 13/F (máxima, 40%/20 questões), 11/D (alta, 20%/10),
1 (alta, base conceitual), 3 e 4 (média-alta), 8/A e 9/B (média, ~10–15%
cada), 2, 5, 6 e 7 (média), 10/C e 12/E (baixa, ~5% cada). Consulte o registro
completo para os focos temáticos e justificativas de cada linha.

- O pedido é importar/consultar a tabela, **sem alterar questões ou proporções
  de seleção**. Não aplique esses pesos ao diário, simulado ou banco sem novo
  pedido explícito. Não invente pesos/blocos ausentes nem some faixas aproximadas.
- A aba **Guia da prova** fica logo abaixo de Estatísticas. Preserve os filtros
  de importância, busca e ordem original visível. Por pedido posterior, não exiba
  filtros de bloco/cadastro nem rótulos de bloco na tabela. Ordenar somente por
  prioridade ou aula (1–13), sem opção Tema. A posição não
  muda ao filtrar; temas da tabela não renomeiam aulas já cadastradas.
- Aula 13 tem a primeira aula interna de Riscos Financeiros recebida em 28/10/2026.
  As demais aguardam fontes; o guia verifica o cadastro real ao exibir o aviso.
- Preserve Q/BP/AL/MAT, H, cfg, filtros de outras telas, sessão e relógio. Os
  blocos deste guia não substituem os blocos internos das aulas. Sem API paga.
- Ao alterar o guia, execute `tests/test_exam_guide.py`, regressões de navegação
  e `tests/smoke.py`. Mantenha dois temas, teclado, telas pequenas e o registro
  em `docs/guia-da-prova.md`.

## Regra permanente de feedback

O usuário exige feedback da alternativa correta e das três incorretas em TODAS
as questões, após a resposta, exceto nos simulados. Isso inclui Estudo, Hardcore,
estudo diário, prática por aula, revisão de erros e futuras aulas ou conteúdos.

- Toda questão de `Q` precisa de `q[11]`: quatro explicações em texto, na ordem
  original das alternativas `q[4]`, `q[5]`, `q[6]`, `q[7]`.
- A primeira justifica a resposta correta. Cada outra explica o erro específico
  daquela opção; não substitua por quatro cópias da justificativa geral.
- Confira a relação pergunta–resposta: se o enunciado pede causa, classificação,
  sequência ou efeito, as quatro opções devem responder a esse mesmo pedido.
  Não aceite dois distratores que também descrevam corretamente o caso.
- Feedback deve ensinar o motivo: indique o papel real do órgão citado, a regra,
  o mecanismo ou a diferença confundida. Negar a opção, repetir o gabarito ou
  dizer que um valor “não corresponde” não basta. Explique também a correta.
- Em números, diferencie teto de alíquota, total de membros de diretores, prazo
  inicial de recondução e mínimo de valor/data posterior também permitido.
  Em combinações, justifique cada item falso incluído e verdadeiro omitido;
  na correta, apresente a razão de todas as afirmações.
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
python3 tests/test_question_design.py
python3 tests/test_question_feedback.py
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
O usuário autorizou expressamente em 20/10/2026 publicar na `main` as alterações
solicitadas, após validação, sem pedir uma segunda confirmação. Essa autorização
inclui futuras atualizações pedidas para este sistema; mantenha o escopo solicitado
e não use force-push nem sobrescreva alterações remotas.

## Painel e navegação no computador

O menu lateral usa ícones pequenos e permanece fixo nas telas de computador.
Preserve as ações existentes ao modificar a apresentação; não reinicie uma
sessão ao navegar ou trocar de tema. Os indicadores devem usar dados reais:
tentativas incluem repetições; andamento da aula mede questões únicas praticadas
(prova + Hardcore); pendências seguem a última resposta de cada questão. Não
apresente cobertura como domínio. Filtros de estatísticas afetam tentativas e
desempenho detalhado na aba Estatísticas; painel básico, evolução, trilha e
pendências usam o histórico completo.
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
A barra da sessão conta respostas concluídas por `qz.rev.length`. `qz.i` é
somente a posição exibida; pular ou revisitar não aumenta o progresso. O
cronômetro continua usando `qz.t0`. Destaques de feedback devem manter a ordem
e o índice original das alternativas e as quatro explicações integralmente
visíveis após responder, sem feedback imediato nos simulados.

## Estudo de hoje e evolução completa

O estudo diário é um **checkpoint de 20 questões**: **5 fáceis, 10 médias e
5 difíceis**, sem Hardcore. Cada dia oferece um novo conjunto, abrangendo todas
as aulas disponíveis. Use `dailyPlan` com sorteio reproduzível pela data e os IDs
estáveis do banco. A distribuição por aula difere no máximo em uma questão;
vagas extras alternam pelos dias. Priorize o maior número possível de inéditas
sem romper participação das aulas ou dificuldade. Quando forem necessárias
repetições, prefira erros e respostas mais antigas. Os filtros da prática e das
estatísticas não alteram o plano diário. Não repita IDs para preencher vagas nem
inclua Hardcore; estoque insuficiente bloqueia a criação em vez de violar o plano.
Se houver mais de 20 aulas, elas alternam em ciclos, pois não cabem todas no mesmo
checkpoint de 20; a interface deve informar essa condição.

- `cpaDaily` guarda um livro separado de `cpaH`: rascunho da sessão, um resultado
  por data e detalhes do último resultado. Quando a API de conta estiver disponível,
  `sync` preserva tanto `h` quanto `daily`; a leitura mescla datas concluídas locais
  e da conta. Só envie após a leitura inicial da conta (`storeReady`).
- Ao começar, reserve os IDs. Clicar novamente, pausar, navegar ou recarregar
  retoma o mesmo checkpoint, com posição, alternativas, escolha, ajudas e feedback.
  Não sorteie novamente um teste parcialmente respondido. Pausa não é conclusão.
- Ao responder a vigésima questão, grave o resultado e bloqueie o início naquele
  dia, mesmo sem clicar em Ver resultado. Exiba aproveitamento e acertos no cartão,
  cadeado/Concluído hoje e consulta ao resultado. Refazer erros é prática normal
  e não altera a nota original nem cria outro checkpoint.
- Datas diárias e do gráfico usam `America/Sao_Paulo`. A conclusão pertence ao dia
  da última resposta; iniciar antes da meia-noite e terminar depois conta no dia
  de término. Não registre outra vez uma sessão concluída ao virar o calendário.
  Atualize o cartão na virada de data, mantendo sessões em andamento.
- Sequência conta somente dias consecutivos com checkpoint completo. Preservar
  a sequência de ontem enquanto hoje está pendente não significa concluir hoje.
  Mostre também o recorde. Não derive conclusões diárias de práticas antigas de
  10 questões ou de qualquer tentativa em `H`.
- Mantenha quatro feedbacks no checkpoint, como no Estudo. Salve o histórico da
  resposta antes de notificar outras abas sobre o avanço diário. Abas compartilham
  o mesmo rascunho e o bloqueio; recebê-lo não deve provocar ciclo de gravações.
- Persistência local exige armazenamento do navegador. Sem ele, mantenha a página
  utilizável e o bloqueio em memória; não alegue persistência após fechá-la. Não
  introduza servidor só para essa funcionalidade nem alegue controle inviolável.

**Evolução dos acertos:** `evolutionData` usa todas as respostas de `H`, incluindo
repetições e todos os modos, sem corte de dias e independentemente dos filtros do
painel. Cada dia salvo tem seu percentual, contagem e data completa. Use rolagem
horizontal com Início do histórico/Mais recente, preservando a leitura no PC;
não comprima meses ou anos até ocultar rótulos. Registros sem data permanecem em
um resumo separado com contagem/aproveitamento; não invente sua posição temporal.
O gráfico mostra agregados por dia, não notas individuais de sessões antigas,
cuja separação não foi gravada no formato original. Não apague nenhum registro.

Confira seleção, retomada, conclusão, repetição, meia-noite, sequência/recorde,
abas, API de conta, armazenamento indisponível, histórico longo/sem data, temas e
PC. Consulte `docs/estudo-diario-e-evolucao.md`.

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

### Estudo ativo por conceito — pedido de 28/10/2026

- Todos os conceitos de revisão oferecem Fazer questões com contagem exata:
  quadro geral (participante/característica), mapas, diagramas, tabelas, linha
  do tempo, flashcards, resumo, dicas, pegadinhas e números. Preserve o conteúdo.
- `active-study.js` associa **assunto + característica/subtema**. Não basta
  mencionar BC para ligar composição a competências. Citar BC/CVM como membros
  do CNSP não muda o colegiado estudado. No quadro geral, respeite a entidade
  da linha, inclusive na coluna Regulação/supervisão. Não use distratores.
- Puxe todos os IDs pertinentes de Q, de todas as aulas, incluindo Hardcore,
  sem Bate-pronto, limite, cota ou filtro de histórico. Zero é válido; não
  preencha com outro assunto. O número exibido deve ser o total da sessão.
- Preserve cfg, H, materiais e sessões existentes. Se já há prática pendente,
  mostre a indicação e Retomar sessão; não substitua o diário ou outra prática.
  Na sessão por conteúdo, Hardcore mantém badge, ausência de ajudas e origem 2;
  Estudo mantém ajudas e origem 0. Resultado/refazer erros conservam o contexto.
- Ao criar conteúdo, confira/amplie o cadastro editorial de assuntos e subtemas
  e audite os botões. Não aceite correspondências amplas como solução automática
  para tema novo. Veja `docs/estudo-por-conteudo.md`.
- Execute `tests/test_active_study.py`, regressões de navegação/resultados e
  `tests/smoke.py`; confira temas, teclado, telas pequenas e os textos originais.
- Refinamento visual solicitado no mesmo dia: mapas, diagramas, linhas do tempo
  e quadro geral usam **um controle por quadro/ramificação**, com acesso aos
  conceitos em um seletor lateral. Não inserir botões/contagens em cada nó ou
  célula. Preserve TODOS os vínculos, contagens e ações no seletor; pesquisa,
  grupos expansíveis, teclado, foco e fechamento precisam funcionar. Tabelas
  mantêm o atalho discreto abaixo. Não aumentar linhas/colunas para acomodar
  ações. Verifique também `tests/test_active_study_design.py`.

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
  cargo com a instituição escrito por completo, via `collegiateOrgan` e
  `collegiateChart`: “Presidente do BACEN”, “Diretor do BACEN”, “Presidente da
  CVM”, “Diretor da CVM”. Não use “Presidente”/“Diretor” isolados, nem dependa
  de uma sigla entre parênteses. Isso vale para TODOS os nós de pessoas, em mapas,
  diagramas e calendários. Nos conselhos, explicite a função e a origem:
  “Ministro da Fazenda — presidente do CMN”; nos representantes, indique a
  instituição representada. Não troque um cargo institucional por “CEO”.
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

## Aula 13 — bloco final com aulas internas (28/10/2026)

A primeira aula interna foi recebida em 28/10/2026: transcrição da aula 23,
seis imagens, assunto **Riscos Financeiros**. Está cadastrada como Aula 1 dentro
de **Aula 13: Bloco Final**. As outras cinco aulas aguardam fontes; não criar
placeholders ou conteúdo presumido.

Pedido FINAL explícito: metade do padrão **por aula interna**: **50 questões
(10 fáceis, 20 médias, 10 difíceis, 10 Hardcore), 25 Bate-pronto e 25 flashcards**.
Estudo e simulado compartilham as 40 normais. Flashcards: arredondar a proporção
usual; primeira interna 9/8/8. Esta exceção substitui o volume indefinido e a
quota normal de 100. Não impor 100 ao bloco inteiro nem novos pesos temáticos.

Leitura/material por aula interna ou bloco completo; praticar/simular o conjunto
e selecionar uma ou mais aulas internas. Preservar as doze aulas, IDs e histórico.
Cruzar fontes e conferir feedbacks, siglas, pistas gramaticais e cálculos.
Detalhes: `docs/aula-13-planejamento.md`, `docs/aula-13.md` e cobertura JSON.
Rodar também `tests/test_aula13.py` ao alterar este bloco.

## Novas aulas com vários blocos

A aula 7 reúne as três transcrições e os 21 slides em quatro blocos internos,
mantendo uma única entrada na trilha. `AL[n].b` contém os blocos com `id`, `t`,
`operators`, `topics`, `r`, `d`, `p` e `n`; `MAT[n].b` contém seus materiais.
As listas agregadas de `AL` e `MAT` continuam completas para “Toda a aula”.
Blocos são opcionais; não os imponha às aulas antigas ou a conteúdos pequenos.

**Quantidade de questões:** mantenha o padrão de **100 por aula**, com **80
normais (20 fáceis, 40 médias, 20 difíceis) e 20 Hardcore**. O usuário exigiu
explicitamente que a aula 7 tenha o mesmo número das anteriores. Reunir várias
transcrições não autoriza aumentar esse número. Só mude mediante pedido explícito.
Distribua a seleção entre todos os participantes, preservando as prioridades
pedagógicas solicitadas e evitando perguntas repetidas.

- Os tópicos de questões pertencem a um único bloco. Use temas úteis à revisão,
  compartilhados por questões relacionadas, evitando um tema novo por pergunta
  ou o prefixo Hardcore no nome do tema. A dificuldade já é um campo separado.
- A seleção de leitura usa `selectedLessonBlocks`; a prática usa `cfg.b`.
  Na trilha, o filtro deve estar junto do conteúdo, acima de números, resumo,
  dicas e pegadinhas. Ao trocar de bloco, mantenha abertas as seções que o usuário
  já abriu, para permitir comparar os conteúdos sem novos cliques.
  `lessonSectionState` registra separadamente abertas e fechadas por aula;
  `rememberLessonSections` captura o estado antes de qualquer renderização.
  Os quatro blocos têm contornos discretos e constantes: azul, lilás, verde e
  rosa, nos controles da trilha, dos materiais e da prática. As cores dos
  controles não alteram a semântica dos destaques no conteúdo.
  `currentMaterial` fornece os cartões e materiais do bloco selecionado.
  Preserve a face do flashcard ao trocar tema e reinicie sua posição ao trocar
  aula/bloco. Consultar materiais não reinicia a sessão de questões em andamento.
- Na trilha, estatísticas do bloco usam seus tópicos; no painel, os indicadores
  de aula e o histórico continuam completos. “Todas as aulas” não herda um
  filtro de bloco de uma aula específica. Não altere os IDs de `Q` existentes.
- O usuário pediu maior atenção a CTVM/DTVM, B3, bancos múltiplos e aos demais
  participantes priorizados, quando presentes nas fontes da aula. Aplique isso
  na variedade e profundidade das questões. Não crie capítulos sem material nem
  apresente esse critério como frequência oficial ou previsão garantida da prova.
- Ausência de números, prazos ou cronologia é válida: não invente informações
  para preencher “Números” ou “Linha do tempo”. Relações operacionais pertencem
  aos diagramas; conceitos comparáveis pertencem às tabelas.
- Cruze transcrições e slides; resolva erros de reconhecimento e inconsistências
  antes de criar gabaritos. Registre cobertura e correções em relatório de aula,
  diferenciando verificação das fontes fornecidas de consulta normativa oficial.

O relatório `docs/aula-7-cobertura.json` registra os 18 participantes, as fontes,
o alcance da revisão e os exercícios desta entrega; seus volumes não são quotas
obrigatórias para futuros materiais. O número de questões segue a regra acima.

### Aula 8 — Inovação, Pagamentos e Crédito Digital

A aula 8 reúne as transcrições das aulas 10, 11 e 14 do professor e os 19 slides
do PDF `Screenshot_1 (1).pdf`. Tem três blocos: IP, fintechs de crédito e SPB/
arranjos. O pedido final do usuário foi **50% IP + fintechs / 50% SPB**:
25 questões de IP, 25 de fintechs e 50 de SPB. Em cada dificuldade, preserve
essa proporção: IP 5/10/5/5, fintechs 5/10/5/5 e SPB 10/20/10/10, na ordem
Fácil/Médio/Difícil/Hardcore. Isso não é uma previsão oficial de frequência na prova.
Os IDs novos são 701–800; a divisão não reordena as primeiras 700 questões.

- Os três filtros de leitura e materiais compartilham `selectedLessonBlocks[8]`;
  os filtros de prática continuam separados. Preservam-se seções abertas.
- O quadro geral compara modalidades de IP, instituições financeiras de crédito
  e infraestruturas, identificando suas naturezas. As colunas são função, objeto
  movimentado, conta/registro, condições, aplicação e observações. Não trate
  SCD/SEP como IP nem um sistema como se fosse uma pessoa jurídica de crédito.
- Distinga Pix/arranjo de SPI/infraestrutura, contas PI de contas dos usuários,
  SCR/informação de STR/SPI/liquidação e depósito de títulos de registro.
  Não generalize LBTR a todo o SPB, nem diga que STR liquida literalmente toda
  obrigação financeira do país. CCP não garante rentabilidade.
- Crédito próprio da SCD, recursos vinculados de credores na SEP e saldos dos
  usuários de IP não são intercambiáveis. A marca do grupo não muda a entidade.
  Autorização de iniciação não permite gerir contas ou deter fundos nessa função.
- O fluxo simplificado dos cartões não pode impor débito imediato ao comprador
  de qualquer instrumento pós-pago; fatura e recebimento do lojista são distintos.
- Os slides/transcrições contêm referências e simplificações cuja vigência não
  foi confirmada, porque a consulta ao BCB foi bloqueada. R$15 mil da SEP e
  R$20 bilhões/100 milhões de transações dos arranjos ficam identificados como
  referências da fonte em tabelas específicas; não foram usados como gabaritos
  numéricos de norma vigente. Não transformar a fala “por operação” em licença
  para fracionar exposição, nem a fala com “ou” em dispensa por um só indicador.
  Ao obter fontes oficiais, reveja a referência antes de acrescentar questões
  que dependam de unidade, valor ou vigência. Não apresente a revisão de slides
  como certificação normativa independente.

A cobertura e as decisões estão em `docs/aula-8-cobertura.json` e
`docs/aula-8-inovacao-pagamentos-credito-digital.md`.
Além das verificações gerais, execute `python3 tests/test_aula8.py` ao alterar
esta aula; confira a proporção, a associação entre fontes/questões e a separação
entre referência de slide e gabarito numérico de norma vigente.

### Aula 9 — Autorregulação, Garantias e Liberdade Econômica

A aula 9 cruza **todos os 15 slides** de `Screenshot_1 (2).pdf` com as três
transcrições. O usuário reforçou a regra permanente: **sempre comparar slides e
transcrição**, incluindo nomes, números, negações e condições. Registre qualquer
divergência e o critério adotado; trechos encobertos podem ser completados pela fala.

O pedido específico é **50% ANBIMA / 40% FGC e FGCoop / 10% Liberdade Econômica**.
Preserve em cada nível: ANBIMA 10/20/10/10; garantias 8/16/8/8; liberdade 2/4/2/2,
na ordem Fácil/Médio/Difícil/Hardcore. Os IDs são 801–900. APIMEC, Planejar e
ANCORD ficam nos materiais e comparações centradas em ANBIMA; não reduza a quota
ANBIMA para criar questões isoladas das outras entidades.

- Três blocos opcionais: Autorreguladores, FGC/FGCoop e Liberdade Econômica.
  Preserve conteúdo agregado, seções abertas e separação dos filtros de prática.
- DPGE: `R$ 40k` no slide 10 conflita com slide 9 e transcrição: **R$ 40 milhões**.
  A inconsistência foi corrigida e registrada. Conta conjunta limita o total antes
  de dividir, conferindo a janela/limites de cada titular.
- Produto, titular e emissor/conglomerado são filtros distintos. CDB de fundo e
  cota de fundo não herdam cobertura por canal bancário. Compromissadas exigem
  condições do lastro; não generalize a partir de uma lista resumida.
- Não transporte automaticamente teto global ou garantia especial do FGC para
  FGCoop: esses pontos não foram detalhados para o segundo fundo nas fontes.
- Parecer sem força própria não elimina dever do código; deliberação vincula no
  âmbito aplicável; conselho interno não está acima do regulador estatal.
- A consulta oficial foi bloqueada. Taxas de contribuição e certas siglas de
  certificações ficam como referências da fonte, sem gabarito de vigência atual.
- Liberdade econômica mantém condições de baixo risco, limites legais e requisitos
  de documentos digitais; intervenção mínima não é ausência de regulação.

Consulte `docs/aula-9-cobertura.json` e
`docs/aula-9-autorregulacao-garantias-liberdade.md`. Além dos testes gerais, execute
`python3 tests/test_aula9.py` ao alterar esta aula. Atualize os testes de rotação
do checkpoint para a quantidade real de aulas, preservando 20 questões e 5/10/5.

## Prática com várias aulas

### Bate-pronto — banco conceitual próprio

O usuário pediu **conteúdo bruto e direto**, sem contextualização, cenários,
interpretação ou contas para resolver. Cada aula recebe **50 itens** adicionais:
enunciado breve, exatamente duas alternativas (uma correta) e dois feedbacks
específicos após acertar ou errar. Misture perguntas diretas e algumas lacunas;
a lacuna deve ser preenchida pela alternativa, com frase gramaticalmente coerente.
Não transforme todas em lacunas ou tudo em Sim/Não. Figuras devem ajudar a
associação sem revelar a resposta ou acrescentar informação irrelevante.

- `BP` é o banco próprio, com aula, tema, enunciado, correta, incorreta, duas
  explicações e referência ao conteúdo existente. `BP_Q` adapta o esquema para
  sessão/revisão. O nível `-1` é conceito, sem inventar dificuldade de prova.
- Os IDs começam em `100001`. Use `questionById` nos fluxos compartilhados;
  preserve a posição dos IDs existentes e acrescente novos itens ao fim de `BP`.
  Não coloque esses itens em `Q`, Simulado, Hardcore ou checkpoint diário.
- O modo `b` grava origem `3` no histórico existente. Todos os registros antigos
  ficam intactos. Tentativas, evolução por dia, prioridades e revisão de erros
  incluem Bate-pronto; andamento da trilha continua medindo os itens do banco
  principal. Não confunda reconhecer um conceito em duas opções com domínio de
  questão contextualizada de prova.
- Escolha aulas e quantidade como na prática, incluindo valor personalizado.
  `bateProntoPlan` distribui igualmente as aulas explicitamente selecionadas,
  com diferença máxima de uma e alternância dos restos. Nunca omita uma aula
  explicitamente escolhida por estoque insuficiente. No filtro Todas, sessões
  menores que a quantidade de aulas alternam grupos, informando a prévia.
- Filtros Todas/Nunca respondidas/As que errei usam a última resposta daquele
  ID. Refazer erros do Bate-pronto conserva duas opções e o modo `b`.
- Embaralhe as duas opções com índice original e mostre cada feedback ao lado
  de sua opção. O próximo item só aparece após Próxima, permitindo ler o feedback.
  Resultado usa a sessão, com acertos, erros, aulas e conceitos; sem referência
  de aprovação ou ritmo de prova oficial.

Consulte `docs/bate-pronto.md` e `docs/bate-pronto-banco.json`. Ao alterar esse
modo, execute `python3 tests/test_bate_pronto.py`, além das verificações gerais.

O usuário pode marcar e desmarcar aulas individualmente em Praticar. `cfg.as`
guarda a seleção múltipla; `cfg.a` continua identificando uma aula única, para
preservar os atalhos existentes. Use `selectedPracticeLessons` em vez de testar
somente `cfg.a`. “Todas as aulas” limpa a seleção específica e usa o banco geral.
Ao iniciar por um atalho de aula/bloco, limpe `cfg.as`; ao combinar aulas, limpe
`cfg.b`. O bloco aparece na configuração apenas quando uma única aula está marcada.

- `sessionPlan` define vagas por aula e por nível antes de sortear os IDs; a
  prévia da sessão e `mix` precisam usar a mesma distribuição.
- Aulas selecionadas recebem quantidades iguais. Quando a divisão não for exata,
  a diferença é de no máximo uma questão; `practiceRound` alterna as vagas extras
  entre sessões consecutivas. Não fixe o excedente sempre na primeira aula.
- Nos níveis Todos, mantenha a proporção 25% fácil, 50% médio e 25% difícil,
  com arredondamento e distribuição proporcional dentro de cada aula. Calcule
  os níveis conjuntamente para não concentrar todas as vagas de arredondamento
  no mesmo nível. Se o usuário escolher um nível, use somente esse nível;
  Hardcore usa somente Hardcore. Simulado continua excluindo `somenteEstudo`.
- Nunca repita questões para preencher vagas nem inclua aulas fora da seleção.
  Se uma aula tiver pouca disponibilidade com os filtros, reduza a quantidade
  e avise. Se uma aula não tiver questões, mostre qual é e peça ajuste dos
  filtros/seleção na interface; não a exclua silenciosamente.
- Escassez de um nível pode exigir outra proporção entre os níveis disponíveis;
  preserve as vagas por aula e explique a exceção na prévia. Não invente questões
  nem altere sua dificuldade para forçar a proporção.
- Teste seleção/desmarcação, 2/3/4 aulas, restos de divisão, limites de estoque,
  inéditas/erros, nível fixo, Hardcore, Simulado e transição para atalhos únicos.
  Preserve feedbacks, histórico, IDs e o estudo diário.

O comportamento e exemplos estão em `docs/pratica-varias-aulas.md`.

## Exigência cognitiva das questões e enunciados

O usuário exige questões que testem conhecimento do conteúdo, em todos os modos.
Fácil pode reconhecer um conceito; Médio deve discriminar ou aplicar um conceito;
Difícil deve combinar condições ou distinguir regras próximas; Hardcore deve
exigir aplicação integrada, análise de limites, exceções ou procedimentos.
O nível não se torna alto apenas por conter números, texto longo ou romanos.

- Não forneça no enunciado a regra, a definição completa ou todos os fatores
  cuja repetição, soma ou multiplicação já resolva a resposta sem conhecimento.
  Exemplo proibido como Hardcore: informar “2 anos, uma recondução” e perguntar
  o total. Prefira avaliar admissibilidade de outra recondução, procedimento e
  competência sem fornecer a regra que está sendo avaliada.
- Contas financeiras são válidas quando exigem conceito: base correta, natureza
  da operação, limites e interpretação. Conta genérica isolada não é Hardcore.
- Use distratores plausíveis, da mesma categoria, sem exclusões absurdas que
  permitam acertar por bom senso. Nenhuma opção deve ser correta por repetição
  exclusiva de palavras do enunciado. Uma questão deve ter resposta única.
- Ao alterar uma questão, atualize alternativas, justificativa geral, dica e
  os quatro feedbacks. Preserve ID, ordem e distribuição por aula/nível; revise
  também variantes da mesma falha em todas as aulas e no conjunto de simulados.
- Afirmações em romanos usam I, II, III, IV etc. em maiúsculas, uma por linha,
  com introdução e pergunta final separadas. Grave texto simples em `Q`, usando
  novas linhas e marcadores; não grave HTML. `questionStemHtml` é o renderizador
  compartilhado por sessão e revisões. Não formate somente um modo nem transforme
  menções soltas a uma fase “II” em listas. Escape todos os textos exibidos.
- Faça leitura editorial de todo o conjunto solicitado. Registre por ID as
  alterações e o alcance da revisão. Heurísticas, contagens de palavras e testes
  não certificam grau de dificuldade nem validade normativa.

### Questões autossuficientes em todos os modos

O usuário exige que **cada questão traga seu próprio contexto**, inclusive em
Estudo, Hardcore, Simulado, estudo diário e conteúdos futuros. As perguntas
avaliam conhecimentos financeiros, não lembrança do que um professor disse.

- Não remeta enunciado, alternativa, dica ou feedback a “na aula”, “segundo o
  professor”, “no slide”, “no material enviado” ou à classificação vista em uma
  tabela externa. A questão deve ser compreensível fora da tela da respectiva aula.
- Nomeie órgão, instrumento, relação financeira e perspectiva quando necessários:
  “meta de inflação”, “diretores do BACEN”, “participação no STR”, “código ANBIMA”.
  Não use só “qual associação” ou “qual bloco” se o objeto depender do título.
- Uma pergunta direta de conceito pode continuar curta. Casos de aplicação devem
  conter os fatos relevantes e pedir uma decisão específica. Não alongue todos
  os enunciados nem entregue a definição/regra solicitada para fornecer contexto.
- Expanda siglas quando isso ajuda a compreensão, exceto se a expansão entregar
  a própria resposta pedida. Não dê no Hardcore a regra que basta somar/aplicar
  mecanicamente. Dicas opcionais orientam a análise, sem remeter ao professor.
- Fonte, data de conferência e limitações normativas pertencem ao relatório da
  aula. Eliminar a referência ao professor não é autorização para inventar uma
  regra vigente. Preserve condições, qualificação de hipóteses e limites de escopo.
- Ao corrigir, preserve IDs, nível, aula, assunto e flags do Simulado. Alinhe
  alternativas, explicação geral, dica e quatro feedbacks somente quando preciso;
  mantenha o vínculo pelo índice original. Não modifique materiais ou histórico
  numa revisão restrita às questões.
- Registre quais IDs mudaram, os campos, motivos e contagens sem dupla contagem.
  O usuário dispensou Excel nesta revisão: apresente quantidades e achados no chat.

A revisão de 13/10/2026 cobriu os 900 IDs. O registro está em
`docs/revisao-enunciados-autossuficientes.json` e o resumo em
`docs/revisao-enunciados-autossuficientes.md`. São 182 enunciados e 113 outras
questões com ajustes só em apoio; 605 ficaram intactas. As contagens são desta
entrega, não metas editoriais para futuras revisões.

Execute também `python3 tests/test_question_context.py`. O helper
`tests/question_revision.py` encadeia a autoria das aulas 8/9 aos campos revisados:
valida a versão atual e reconstrói a anterior, sem atualizar hashes históricos
para esconder divergências. Futuras alterações autorizadas precisam manter essa
rastreabilidade e a ausência de dependência externa.

## Feedback visual depois da sessão

Estudo, Hardcore, Simulado e seus atalhos usam o mesmo resultado em `fin`.
`sessionAnalysis` usa exclusivamente `qz.rev`, sem misturar o histórico completo
nem avaliar como erros as questões que não foram respondidas.

- Mostre acertos/erros com números, proporções e gráficos por aula e nível.
  Cada proporção usa como denominador as respostas daquele grupo, não as do banco.
- Prioridades são assuntos com erros reais, separados por aula. Recomendações
  orientam revisão e comparação de regras; não afirmam a causa do erro.
- Repetição de erros é agrupamento explícito por assunto (`sessionTheme`), com
  pelo menos dois erros e contagem visível. Não apresente esse agrupamento como
  correlação estatística comprovada, diagnóstico ou medida de domínio.
- Mostre limite de amostra e trate sem respostas, tudo certo e tudo errado.
  Não invente áreas fracas quando não houve erros. Não compare velocidades sem
  base nem declare aprovação na prova oficial com base numa prática local.
- Pare o cronômetro ao registrar a última resposta. O tempo de leitura do
  resultado ou do último feedback não entra no tempo de resposta.
- A revisão mostra escolha e resposta correta; Estudo/Hardcore conservam os
  quatro feedbacks. Simulado mantém só a explicação geral após finalizar, sem
  feedback imediato nem bloco de quatro alternativas no resultado.
- Refazer erros considera somente esta sessão e começa em Estudo ou Hardcore,
  com feedback após responder. Ao sair da tela de resultado para qualquer outra
  aba, descarte somente a sessão concluída de `qz`; voltar a Praticar deve abrir
  a configuração inicial. Isso inclui o atalho de revisão de conteúdo. Preserve
  histórico, resultado diário salvo, tema, filtros e sessões ainda em andamento.
- Preserve o resultado compacto: nota e indicadores juntos, cartões por aula e
  indicadores discretos por dificuldade. Use percentuais neutros e pontos por
  resposta (preenchido para acerto, contorno para erro), com legenda. Não retome
  barras extensas, percentuais azuis ou gráficos divididos em verde/vermelho.
  Acertos usam verde (`--ok`): pontos preenchidos maiores e contagem destacada.
  Cartões com 100% têm contorno verde, sem preenchimento integral; cartões com
  erros mantêm contorno neutro. Erros usam âmbar (`--md`), inclusive os pontos
  vazados. O anel geral também usa verde para acertos. Preserve percentuais
  neutros e aplique esse padrão em todos os resultados e nos dois temas.
  Se limitar pontos, informe o limite e as demais respostas; totais sempre
  incluem o grupo inteiro. Ordenar por Mais erros só reorganiza os cartões;
  não modifica sessão, histórico, revisão aberta nem cálculos.
  Em telas largas, use a lateral dos
  gráficos para padrões de erro e mantenha as ações logo abaixo da nota.
  Não corte aulas, assuntos, explicações ou valores para encurtar a página.
  A revisão em duas colunas deve abrir a questão na largura completa; listas
  extensas de conceitos do Bate-pronto devem continuar acessíveis por teclado.
- Verifique todos os modos, valores percentuais, histórico anterior distinto,
  recomendações/atalhos, romanos, estados extremos e os dois temas no PC.
  Execute também `python3 tests/test_compact_results.py` e
  `python3 tests/test_acronym_visibility_review.py`. Para indicadores e ordenação,
  execute `python3 tests/test_result_scorecards.py`.

O registro desta revisão está em `docs/revisao-questoes-sessoes.json`, e o
relatório pedagógico e funcional em `docs/revisao-questoes-sessoes.md`.

## Quadros gerais comparativos — padrão permanente

Quando uma aula reunir vários órgãos, operadores ou conceitos comparáveis,
acrescente a aba **Quadro geral** e o atalho **Quadro comparativo** na trilha.
Escolha o objetivo da comparação antes de definir suas linhas, grupos e colunas.
Não imponha o quadro a aulas de um único foco, como a aula do Banco Central.
Isso vale também para futuras aulas, quando seus conteúdos forem fornecidos.

- `LESSON_OVERVIEWS` registra as configurações por aula. Use o mesmo renderizador,
  aparência, filtros, ícones, ampliação, cabeçalhos fixos e controles da aula 7.
  Cadastrar outra aula nesse registro deve habilitar a aba e o atalho sem
  acrescentar condições numéricas espalhadas pela navegação.
- **As colunas podem e devem variar conforme a aula**: composição, competências,
  vinculação e reuniões são adequadas a órgãos; captação e carteiras a operadores.
  Não force recursos/remuneração ou público-alvo quando não ajudam a comparação.
  Preserve Observações como última coluna e o participante nas linhas neste
  quadro de consulta amplo; não mude os eixos das tabelas detalhadas existentes.
- Escreva sínteses adicionais com fontes por linha; preserve `Q`, `AL` e `MAT`.
  Não misture agentes, mercados e órgãos como se fossem participantes equivalentes.
  Distinga o papel do órgão dos operadores do seu segmento; listar operadores
  de um segmento não atribui a todos os supervisores competência indistinta.
- Aulas 1, 5 e 6 têm quadros próprios: estrutura do SFN (7 órgãos), seguros e
  previdência (4 órgãos), operadores monetários (5 tipos). Na aula 6, explicite
  carteira comercial no múltiplo e autorização de depósitos na cooperativa;
  cooperativas de capital e empréstimo não captam depósitos.
- `selectedOverviewGroups` guarda filtros próprios dos quadros sem blocos de aula.
  A aula 7 continua compartilhando `selectedLessonBlocks[7]` com seus materiais.
  Não crie blocos pedagógicos artificiais em `AL` só para filtrar uma tabela.
  Filtros e rolagem não devem vazar entre aulas, nem alterar a prática/histórico.

Consulte `docs/quadros-gerais-comparativos.md` para os eixos e a validação.

### Conteúdo específico da aula 7

O usuário solicitou uma tabela grande de consulta no PC, com cada operador nas
**linhas**, características nas colunas e **Observações na última coluna**.
Essa orientação é uma exceção explícita às comparações curtas de `MAT` que põem
entidades em colunas. Não transponha o quadro geral nem altere as tabelas antigas.

- `OPERATOR_OVERVIEW_ROWS` guarda a síntese adicional e suas fontes; `MAT`, `AL`
  e `Q` permanecem intactos. Há 18 participantes da aula, incluindo CTVM e DTVM
  separadas. Funções da B3 não viram operadores novos; não acrescente operadores
  de outras aulas para completar uma quantidade presumida.
- Os sete eixos são operador/forma, foco/público, atuação, recursos/remuneração,
  limites/condições, regulação/supervisão e observações. A forma jurídica fica
  junto do nome para evitar mais uma coluna larga. Compare funções reais:
  captação bancária, recursos do grupo/plano e remuneração de serviços diferem.
  Não classifique todos os participantes como instituições financeiras.
- Observações registram distinções úteis e particularidades do participante.
  Preserve SCI/poupança versus prática de repasse, conta vinculada versus à vista,
  DTVM/acesso à bolsa, limites de fomento, aberta versus fechada, seguro versus
  resseguro e responsabilidade de corretor e seguradora.
- Use os quatro blocos existentes como filtro exclusivo, mais Todos. Compartilhe
  `selectedLessonBlocks[7]` com a leitura e os materiais; não altere `cfg.b`,
  seleção de aulas da prática, sessão ativa ou histórico ao consultar o quadro.
- Bordas e ícones identificam os blocos com azul, lilás, verde e rosa, nas mesmas
  cores dos filtros. Cabeçalhos estruturais são azuis, células centralizadas e
  grade completa. Vermelho marca negativas reais; lilás no texto marca condições.
  Natureza, classificação e ausência de detalhe nas fontes ficam neutras.
- Ausência de informação é identificada como “Não detalhado na aula”, nunca
  completada com restrições, fontes de recursos ou regras inventadas. Não use
  vermelho para sugerir proibição quando apenas falta informação na aula.
- A aba Quadro geral aparece nas aulas registradas; a trilha tem atalho correspondente.
  O cabeçalho e a primeira coluna ficam fixos dentro da área de rolagem.
  Ampliação usa a largura da página, com botão Reduzir e Escape; a lâmpada global
  continua clicável. Preserve posição da tabela ao ampliar/reduzir e trocar tema;
  mudar bloco inicia a consulta desse grupo no topo.
- Confira todos os participantes e as associações entre células, as duas
  aparências, larguras de PC, filtros, atalhos, transição para outra aula e uma
  sessão de questões em andamento. Não substitua os materiais detalhados pelo
  quadro de síntese. Consulte `docs/aula-7-quadro-comparativo.md`.

### Justificativa didática e contexto — regra reforçada em 14/10/2026

- Feedback precisa ensinar a relação ou o mecanismo: afirmar “também pode” ou
  repetir uma data/número correto não explica por que a opção atende ao pedido.
  Nas permissões, explique a natureza da atividade e o alcance da exceção;
  não invente a intenção da norma. Ex.: distribuição de fundos é serviço de
  investimento em patrimônio separado, distinto de depósito/crédito cooperativo.
- Nomeie a instituição e a perspectiva em classificações de operações. Para o
  banco, conceder crédito gera direito; receber depósito gera obrigação. Não
  deixe “da instituição” depender de cabeçalho da aula ou de inferência das opções.
- Revise cada alternativa, incluindo a correta; preserve explicações que já
  ensinam e acrescente só contexto relevante. Extensão não certifica qualidade.
  Bate-pronto mantém conteúdo direto no enunciado, com ensino no feedback.
- Preserve IDs, alternativas, dificuldades e histórico em revisões editoriais.
  O manifesto `docs/revisao-justificativas-contexto.json` estende a cadeia das
  revisões anteriores sem reescrever suas evidências. Execute também
  `python3 tests/test_teaching_revision.py` e `python3 tests/test_bate_pronto.py`.

## Configuração de Praticar no computador

A tela usa a largura disponível com modos no topo, aulas em grade à esquerda e
nível/filtro/quantidade à direita. Preserve a barra de resumo e início acessível
sem rolar até o final, inclusive em 1280×720 e com blocos, avisos ou várias aulas.
Detalhamento de distribuição pode ser expandido e mantém a abertura entre
seleções. Não aplique a largura de configuração às questões ou aos resultados.

Mantenha seleção múltipla, proporções, quantidades personalizadas do Bate-pronto,
estado desabilitado quando não há estoque e foco de teclado. A reorganização é
visual; não muda planejamento, filtros ou sorteio. Confira os dois temas e
execute `python3 tests/test_practice_layout.py` e os testes dos fluxos afetados.
Consulte `docs/praticar-layout-pc.md` para a comparação e as resoluções verificadas.

## Concordância sem pistas de resposta

Antes de publicar enunciados, confira o encaixe com CADA alternativa, incluindo
as incorretas. Artigos, contrações, particípios e verbos não devem permitir
eliminar opções apenas por gênero ou número. Isso vale para todos os modos e,
principalmente, para frases curtas e lacunas do Bate-pronto.

- Prefira “Quem colhe as assinaturas?” a “São colhidas pela:” quando as opções
  incluem Secretaria-Executiva e Senado. Use perguntas neutras ou preposições
  sem artigo quando necessário; não deturpe nomes oficiais para igualar gêneros.
- Leia a frase completa com cada preenchimento: “precisam ser abatidos” pode
  favorecer um sujeito masculino plural e excluir outro feminino plural.
- Não confunda concordância do sujeito já nomeado com pista da alternativa:
  “O BC é classificado como autarquia” tem concordância legítima com BC.
- Gênero de siglas depende do nome: Comoc é comissão, Copom é comitê; não infira
  gênero só pela última letra. A varredura lexical é apoio à leitura editorial.
- O manifesto `docs/revisao-pistas-gramaticais.json` preserva a revisão atual e
  a cadeia histórica. Execute `python3 tests/test_grammar_and_quick_visual.py`.

## Identidade visual das questões Bate-pronto

A apresentação fica sob `.quick-round`, sem mudar os outros modos. Preserve
cartão de enunciado maior, duas escolhas igualmente destacadas antes da resposta,
mesma altura/largura e gráficos genéricos que não revelem o conceito correto.
Após responder, conserve o vínculo alternativa/feedback à direita, destaque da
escolha e correção e avanço apenas por Próxima. Respeite movimento reduzido e
os temas, mantendo Tab/Enter e o cronômetro existentes. Não acrescente leitura
contextual ao banco conceitual para preencher o espaço visual.

## Siglas em enunciados e alternativas

Use `questionDisplay`, `questionTextHtml` e `questionAnswerHtml` em todos os modos
para mostrar a sigla e seu nome entre parênteses, preferencialmente na primeira
ocorrência do enunciado. Se o conceito não apareceu no enunciado, expanda-o nas
alternativas, com tratamento igual para cada opção. Não duplique definições já
presentes; BC/BCB/BACEN e plurais compartilham o conceito. Preserve textos brutos
no banco e no histórico, o índice original e o gabarito.

O usuário confirmou: quando a pergunta cobra o significado da sigla ou a sigla
correspondente a um nome, mostre a expansão **somente após responder**. Não entregue
o gabarito para cumprir a regra visual. Cadastre novas siglas em
`QUESTION_ACRONYMS` e `docs/siglas-questoes.json`; não invente a expansão. Considere
o contexto de siglas ambíguas. Pix, romanos e letras de opções não são siglas.
Confira Estudo, Simulado, Hardcore, diário, Bate-pronto e revisões, nos dois temas.

Feedback de número/prazo deve explicar a regra e a distinção relevante, além da
conta quando houver aplicação financeira. Conversões como “mil vezes menor” ou
repetir um valor por extenso não substituem explicar a garantia, o objeto, a base,
o teto ou o regime. Não acrescente parágrafo de outro assunto para dar tamanho.
O manifesto `docs/revisao-feedbacks-numericos.json` estende a cadeia editorial;
execute também `python3 tests/test_acronyms_and_numeric_feedback.py`.

## Não testar apenas o encaixe das iniciais

Não crie perguntas cujo acerto dependa apenas de escolher o nome por extenso cujas
iniciais combinam com a sigla do enunciado. Exemplo proibido: “RDC é:” com opções
“Recibo de Depósito Cooperativo” e “Cota de fundo de previdência”. Reescreva para
avaliar característica, limite, funcionamento ou distinção do conteúdo, preservando
a objetividade do Bate-pronto. Adiar a expansão não conserta uma autoria assim.

Confira a pergunta renderizada COM as expansões: o nome oficial pode conter a
função, o segmento ou o regime solicitado. Nesses casos, registre o ID em
`QUESTION_ACRONYM_CLUES` e no relatório editorial e mostre os nomes somente após
responder. Trate todas as siglas daquela questão igualmente. Preserve nomes antes
da resposta quando eles não resolvem o que se pergunta. Não use similaridade de
palavras isoladas como certificação de qualidade ou para reescrever itens bons.
Julgue a exceção pelo fato específico pedido: LFL por extenso não revela as
garantias exigidas; LLI/LLT por extenso não revelam os tetos de dias, as cestas
elegíveis ou a necessidade de aprovação. Nesses casos, expanda antes da resposta.
A revisão de exibição de 2026-10-19 está em
`docs/revisao-exibicao-siglas-2026-10-19.json`; preserve os manifestos anteriores.

A regra se aplica a todos os modos e futuras aulas. Execute
`python3 tests/test_acronym_clues.py` e as regressões gerais. O manifesto
`docs/revisao-pistas-siglas.json` estende a cadeia anterior, sem alterar seus hashes.

## Página Erros: consulta e prática separadas

A entrada deve mostrar cartões de Fácil, Médio, Difícil, Hardcore e Bate-pronto,
com ícones, cores de nível e contagens por ID cuja última resposta foi errada.
Não abra lista ou modo automaticamente. Selecionar um cartão revela só seu grupo;
selecionar novamente recolhe. Ao sair da aba, limpe somente `reviewGroup`.

Botões de refazer abrem `configureErrorPractice` na configuração normal de
Praticar, com `cfg.m="err"`, modo correto, todas as aulas e sem bloco herdado.
Um cartão regular selecionado conserva seu nível; Bate-pronto e Hardcore usam
seus próprios bancos. Iniciar questões é uma ação posterior explícita. Não misture
Bate-pronto, Hardcore e Estudo para preencher estoque; não apague `H` para limpar
pendências. A última resposta vale também em registros antigos booleanos.

Mantenha consulta expansível de respostas/feedbacks e cartões vazios sem ação.
Execute `python3 tests/test_error_review.py`,
`python3 tests/test_practice_navigation.py` e as
regressões de prática/histórico. Consulte `docs/revisao-erros-e-retorno-pratica.md`.

### Aula 10 — Mercados Financeiros, Clearing e Estabilidade

- Três transcrições e 13 slides, em três blocos: mercados; clearing;
  estabilidade/liquidez. Mantém 100 questões (20/40/20/20) e 50 Bate-pronto.
- **O sistema Selic não atua como contraparte central.** O usuário reiterou
  expressamente essa distinção. DVP não equivale a CCP; registro não assume
  obrigações do emissor. Não confunda Câmara B3 com todo serviço Cetip/B3.
- Crédito/capitais não se classificam só por prazo; primário de capitais
  corresponde a nova emissão, mesmo em companhia já listada. Câmbio tem critério
  próprio de primário/secundário (cliente/instituição versus interbancário).
- ACCP é capital contracíclico, não dinheiro de compulsório. O exemplo de 10%
  é hipotético; não sustenta crédito ilimitado na prática. LLI/LLT exigem classe,
  prazo, cesta e limite; automação não dispensa essas condições.
- IDs 901–1000 e 100451–100500 são append-only. Relatório e escopo de conferência
  em `docs/aula-10-cobertura.json` e `docs/aula-10.md`. Não altere hashes de
  revisões históricas ao adicionar aulas; testes históricos devem manter seu
  escopo original, com validação separada de cada nova autoria.
- Cada bloco de `MAT[n].b` precisa de `id` correspondente ao bloco de `AL`.
  Teste que `currentMaterial()` retorna o bloco escolhido, além de conferir
  seu texto renderizado. Comparar somente a tela com o mesmo helper pode deixar
  passar um filtro que continua retornando toda a aula.
- Execute `python3 tests/test_aula10.py`, além das regressões gerais, ao alterar
  esse conteúdo. Os testes não substituem a releitura pedagógica das alternativas
  e feedbacks. A conferência desta autoria não certificou vigência normativa.


## Navegação entre questões — Estudo e Hardcore

O usuário pediu um quadro à esquerda, com apenas os números das questões da
sessão. Aplica-se a Estudo, estudo diário, prática por aula/bloco, revisão de erros
em Estudo e Hardcore. Simulado e Bate-pronto continuam sem o quadro.

- `qz.items` guarda alternativas embaralhadas, escolha, dica, eliminações e estado
  de saída sem resposta, separados por posição. Voltar restaura essa informação.
- Células neutras indicam questões ainda não deixadas; sair sem responder marca
  amarelo. Resposta certa fica verde e errada fica vermelha. A posição atual tem
  contorno azul; rótulos acessíveis e tooltips explicam os estados sem depender só
  da cor. No quadro visível ficam somente os números.
- `jumpQuestion` permite ir e voltar sem registrar tentativas. Uma resposta já
  confirmada é somente leitura, com os mesmos feedbacks e sem alterar o histórico.
- `nextQuestion` procura a próxima pendente em ordem circular. Não finalize pela
  posição da questão: resultado exige todas as respostas, mesmo fora de ordem.
- `qz.rev` permanece lista compacta das respostas, na ordem em que foram dadas.
  `H` recebe uma única tentativa por posição respondida. Progresso e nota usam
  respostas reais, não o maior número de questão visitado. O relógio para na
  última resposta, mesmo que ela esteja na primeira posição.
- O diário persiste também os estados individuais e a rolagem do quadro. A
  validação aceita respostas fora de ordem, rejeita IDs repetidos/externos à
  sessão e mantém compatibilidade com rascunhos lineares anteriores. Preserve
  bloqueio diário, retomada, comunicação entre abas e escolha das 20 questões.
- Preserve a leitura dos feedbacks ao lado das alternativas no PC, foco por
  teclado e acesso ao botão de tema. Sessões longas usam rolagem interna no quadro
  e mantêm a célula atual visível.
- Não altere questões, dificuldades, bancos, materiais ou IDs para acrescentar
  navegação. Execute `python3 tests/test_question_navigation.py`, as regressões de
  prática/diário/Bate-pronto e `python3 tests/smoke.py` antes de publicar.

- Preferência visual corrigida pelo usuário: quadro compacto no canto esquerdo,
  apenas um pouco maior que a primeira versão (coluna de 184 px, números de 15 px;
  coluna menor nas janelas estreitas). Não volte às células grandes da versão de
  400 px. Em telas largas, centralize a área da questão com espaço simétrico à
  direita, sem deixar o quadro empurrar a leitura para o centro-direita.

### Aula 11 — Macroeconomia, Atividade e Política Fiscal

As transcrições 16/18/22 e os 14 slides foram cruzados. O usuário pediu 10% fluxo
circular, 30% fiscal e 60% indicadores: preserve 10/30/60 nas 100 questões e
5/15/30 nos 50 Bate-pronto. Dentro dos níveis Fácil/Médio/Difícil/Hardcore, os
blocos recebem 2/4/2/2, 6/12/6/6 e 12/24/12/12, respectivamente.
IDs 1001–1100 e 100501–100550; três blocos com filtros e um quadro de 14 conceitos.

Déficit é fluxo; dívida é estoque. Salários não são contados novamente dentro do
excedente operacional bruto. PIB não é estoque de riqueza, inflação nem garantia
de bem-estar individual. Importações retiram produção externa já contida no gasto;
transferências não são compras diretas de produção. IPCA e IGP-M têm cestas e pesos
distintos. TLP combina IPCA e parcela real: 7,61% é exemplo, não constante universal.
O antigo teto da EC 95/2016 é histórico; não o publique como regra vigente.
Não trate a TLP como migração automática de todos os contratos TJLP.
Sistema Selic não é CCP.
Consultas oficiais foram bloqueadas; não declare certificação normativa a partir
da comparação das fontes. Veja `docs/aula-11.md` e `docs/aula-11-cobertura.json`.
Execute `python3 tests/test_aula11.py` e as regressões gerais. Preserve relatórios
históricos usando seus recortes de IDs; novas siglas/exceções podem ser acrescentadas
com motivos por item sem reescrever decisões e hashes anteriores.

## Busca contextual e hierarquia — correção aprovada em 20/10/2026

O usuário rejeitou a busca universal dentro das telas locais e a lista extensa
com rolagem interna. A implementação contextual substitui o padrão anterior.

- Estudo de hoje continua principal. A busca geral fica imediatamente abaixo,
  antes de `nextStudyAction`, indicadores e evolução. Mantenha todas as aulas,
  datas, filtros, histórico e regras do checkpoint.
- Apenas no painel a busca reúne todo o conteúdo e oferece filtros Tudo/Trilha/
  Questões/Materiais. Em Materiais há cartões visuais por tipo, incluindo
  tabelas, quadros comparativos e flashcards. O índice inclui aulas, AL/MAT, quadros, enunciados de Q/BP e o quadro SFN.
  Nunca inclua alternativas, gabaritos ou feedbacks nos resultados de questões.
- Trilha retorna somente aulas e conteúdo da trilha. Materiais retorna somente
  o tipo atualmente aberto (tabelas, mapas, diagramas, prazos, flashcards ou
  quadro comparativo), em todas as aulas; a busca fica após as abas de material.
  Praticar retorna somente questões do modo, nível e filtro de histórico atuais.
  Hardcore e Bate-pronto ignoram o nível normal herdado da configuração.
- Guarde consultas e paginação separadas por contexto, incluindo cada tipo de
  material. Uma busca geral não deve filtrar as telas locais ao navegar.
- Use cartões com aula, tipo/nível, título, trecho curto e ação explícita. Mostre
  quatro por página, com contador, Anterior/Próxima e seletor de página. Todos os
  resultados permanecem acessíveis; não crie lista de resultados com rolagem
  interna, accordion aninhado nem grupos de filtros universais nas telas locais.
- `contentSearchIndex` deriva os dados atuais, com equivalências de siglas pelo
  cadastro existente, ignorando acentos/maiúsculas. Novas aulas entram no índice.
- Digitar/filtrar não altera H, cfg, Q/BP, proporções ou a sessão em andamento.
  Na prática, mantenha selecionadas as aulas ocultas pela consulta e seus controles
  de remoção. Iniciar a sessão normal continua seguindo a seleção configurada,
  sem aplicar silenciosamente o termo às questões sorteadas.
- A ação Praticar esta questão inicia só aquele ID, após clique explícito, no
  modo correspondente (Simulado se escolhido na prática; Estudo por padrão na
  busca geral). Com sessão em andamento, a ação deve apenas retomá-la, preservando
  IDs, respostas e relógio. Não inicie questões ao digitar ou selecionar filtro.
- Abrir conteúdo expande/foca a origem, preservando textos integrais. Não use
  índices agregados para destacar outro bloco ou cartão após mudar a seleção.
  Flashcards abrem na pergunta; consultas nunca reiniciam uma sessão existente.
- Atualize apenas os resultados ao digitar, mantendo foco. Escape consultas e
  conteúdos, ofereça limpeza/Escape, estado vazio, teclado, dois temas e layout
  de PC/celular. Use a paleta existente e preserve a legibilidade.
- Execute `tests/test_content_search.py`, `tests/test_dashboard_hierarchy.py`,
  `tests/test_practice_layout.py`, `tests/test_practice_navigation.py`,
  `tests/test_question_navigation.py` e `tests/smoke.py` antes de publicar.
  Registre a entrega em `docs/busca-contextual.md`.

### Refinamentos e identidade das aulas na busca

- Em Trilha (filtro do painel e tela local), mostre primeiro as aulas encontradas,
  em ordem numérica, com quantidade real de informações. Só abra os resultados
  após escolher uma aula; Trocar aula retorna à seleção. Preserve todos os itens.
- Todos os cartões da busca usam a mesma identidade de aula: número em selo,
  título completo, ícone e cor constantes. Restrinja essas cores à pesquisa; não
  altere a estrutura azul dos mapas ou as cores semânticas de acerto/erro.
- No filtro Questões do painel, ofereça dificuldade, modo (Estudo, Simulado,
  Hardcore, Bate-pronto), histórico (todas, inéditas, respondidas, erros pendentes)
  e aula. Interseccione os filtros sem alterar cfg ou H. Erros pendentes seguem a
  última resposta; Simulado exclui somenteEstudo e inicia resultados nesse modo
  quando selecionado na busca geral. Trocar modo reinicia apenas o
  filtro de dificuldade da busca, evitando herdar uma combinação incompatível.
- Em Materiais, use cartões com ícone, cor, tipo e contagem, além do filtro de
  aula. Zeros continuam identificados; não invente resultados para completar tipos.
- O usuário retirou explicitamente o pedido de mudar filtros internos de resumo,
  dicas e macetes: mantenha os controles e conteúdos dessa parte como estão.
- Execute também `python3 tests/test_search_refinements.py` e atualize o relatório
  `docs/busca-contextual.md` ao alterar esses refinamentos.

### Apresentação dos seletores da busca

- Modo, Meu histórico e Aula usam o mesmo componente de menu visual, inclusive
  no estado aberto: paleta do sistema, ícones discretos, espaçamento, seleção
  marcada e opções legíveis. Não reintroduza o popup nativo nesses filtros.
- Preserve as opções e os setters de busca. Menus devem funcionar por clique,
  setas, Home/End, digitação, Enter/Espaço, Escape e Tab; fechar ao clicar fora,
  manter foco após selecionar e caber no espaço visível nos dois temas.
- Ao alterar esse componente, execute também `tests/test_search_filter_menus.py`.

## Estatísticas — área dedicada em 27/10/2026

- A aba **Estatísticas** fica abaixo de Quadro do SFN. O painel mantém
  checkpoint, evolução completa, acompanhamento básico e acessos. Os filtros
  de nível/origem e o detalhamento ficam na área dedicada; o painel usa H
  completo com IDs válidos, independentemente de fl/fm.
- O detalhamento começa aberto, com uma dimensão por vez
  (Aulas, Temas, Dificuldades), em cartões compactos, no máximo seis por página.
  Todos os grupos continuam acessíveis por paginação e busca local; não retome
  barras longas, listas gigantes ou cores de nível misturadas ao aproveitamento.
- Gráficos circulares usam verde nos acertos, vermelho nos erros e percentuais
  neutros. Matriz aulas × dificuldades começa recolhida; cada célula mostra
  percentual e amostra. Ausência de respostas é um traço, não 0%. Preserve
  abertura das seções ao filtrar e navegar. Grupos com poucas respostas
  recebem indicação de revisão pontual, sem diagnóstico de domínio.
- Percentuais ficam neutros; acertos em verde e erros em vermelho, com números e
  rótulos. Os cartões são informativos, sem aparência de ação. Aulas seguem ordem
  numérica e temas começam por menor aproveitamento. Permita reordenar e buscar.
- Use HF para respeitar nível/origem. Conte todas as tentativas, inclusive
  repetições e Bate-pronto; ignore IDs inexistentes. Temas iguais conservam o
  agrupamento histórico e mostram as aulas envolvidas. Não chame amostra pequena
  de domínio nem sugira fraqueza se todas as respostas foram corretas.
- Trocar aba, buscar, ordenar e paginar atualizam somente a consulta. Preserve H,
  cfg, fl/fm, sessão, alternativas e relógio. Mantenha teclado, foco e dois temas.
- Execute `tests/test_statistics.py`, `tests/test_dashboard_details.py`,
  `tests/test_dashboard_hierarchy.py` e `tests/smoke.py`. Registre a entrega em
  `docs/estatisticas.md`; mantenha dois temas, teclado e telas pequenas.
- Os filtros usam as mesmas tentativas de HF em todos os gráficos; preserve
  Q/BP/AL/MAT, H, cfg, sessão e cronômetro. A gravação normal de um rascunho
  diário pode atualizar elapsed/updatedAt, sem reiniciar ou concluir a sessão.

- Ajuste visual solicitado em 27/10/2026: vermelho nos erros **somente em
  Estatísticas**; preservar âmbar nos resultados das sessões e nas demais telas.
  A matriz mantém uma escala sequencial verde mais ampla, com referências
  0/25/50/75/100 e tinta contrastante nos dois temas. A orientação foi
  ajustada pelo usuário: **0% verde claro, pouco mais claro que 25%, e 100% verde escuro em ambos os temas**. Não misturar cores de
  dificuldade nessa escala. Filtros de dificuldade seguem verde/âmbar/vermelho/
  Hardcore do sistema; origem recebe ícones, sem cores aleatórias por modo.
  Todos os anéis de Estatísticas usam contorno espesso, com percentual legível
  no centro; preservar as proporções reais de acerto/erro. As cores dos anéis
  são um pouco mais escuras e saturadas; manter espessura e dimensões aprovadas.
  Conferir também `tests/test_statistics_colors.py` e `tests/test_result_scorecards.py`.

## Consulta local aos materiais — 21/10/2026

- A aba Consulta fica entre Trilha e Praticar, com lupa. `consulta.js` e
  `consulta.css` são recursos locais da página estática; publique-os junto com
  index.html. Não integre IA, API paga, chave ou consulta externa sem solicitação.
- Responda na própria aba com trechos literais, tópicos e tabelas, identificando
  aula, tipo e título da fonte. Não transforme o resultado em um conjunto de
  links que obrigue a sair da consulta. Não invente respostas ou complete lacunas.
- O índice deriva AL, MAT, quadros, flashcards e explicações corretas. Distratores
  não são fatos: nunca os indexe como respostas. Preserve os textos originais.
- Reconheça siglas, nomes, plurais, sinônimos, perguntas por característica e
  comparações. Erros de digitação só têm tolerância conservadora, com contexto;
  palavras de fora do domínio não devem virar termos financeiros por semelhança.
- Composição total não é contagem de mandatos iniciados num ano. Limite ordinário
  não é garantia especial. Em comparações, alinhe características e preserve
  a entidade de cada coluna; use tabelas existentes quando forem pertinentes.
- Diferencie conteúdo encontrado, relacionado e ausente. Uma resposta parcial
  deve ser identificada; ausência de informação não autoriza inferência nova.
- Perguntas anteriores e rascunho ficam somente na memória da visita. Consultar,
  limpar e navegar não alteram H, cfg, qz, cronômetro, filtros ou materiais.
- Novas aulas entram automaticamente pelo índice. Confira relevância e fontes,
  não apenas a presença de um resultado; teste perguntas dos exemplos e de aulas
  variadas. Execute `tests/test_consulta.py`, regressões de navegação/busca e
  `tests/smoke.py`. Registre escopo e limites em `docs/consulta-local.md`.

### Apresentação da Consulta

- Não mostre botões de sugestões de perguntas. Perguntas anteriores ficam sob
  um único controle expansível, fechado por padrão, com contagem. Monte a lista
  somente ao abrir; uma pergunta nova não deve expandir o histórico sozinha.
- Destaque termos pesquisados em negrito e na cor de atenção do tema, incluindo
  siglas/nomes equivalentes, plurais e gênero (pignoratício/pignoratícias).
  Preserve o texto literal e os limites de palavra; não pinte cartões inteiros
  nem destaque palavras de comando como se fossem o assunto principal.
- Faça a marcação apenas no texto escapado das respostas, nunca em atributos,
  HTML ou no banco. Cada pergunta anterior usa os próprios termos de destaque.


### Relações na Consulta

- Priorize o pedido (histórico/substituição, cálculo, causa ou sequência), além
  dos termos literais. Use evidências da mesma fonte; não cadastre respostas
  manuais para contornar uma pergunta específica.
- Preserve o contexto entre itens da mesma linha do tempo. Não una marcos ou
  fontes independentes para inferir sucessão. “Antes da TLP” deve recuperar TJLP,
  a transição de 2018 e as condições sobre novas operações/contratos antigos.
- Menção incidental, negação de substituição ou origem financeira de recursos
  não comprovam relação histórica. Um histórico não explica sozinho o motivo
  da mudança. Se faltar evidência da relação pedida, identifique como relacionado.
- Perguntas de continuidade podem herdar o assunto; uma entidade explícita
  substitui esse contexto. Preserve textos literais, fontes, destaques e estados
  de estudo. Execute também `tests/test_consulta_context.py` nas revisões.


### Refinamentos da Consulta

- Separe significados de siglas coincidentes no índice local. Use nomes completos,
  definições explícitas com iniciais compatíveis e rótulos do material; não
  transforme legendas genéricas em significados. Se o contexto não distinguir,
  ofereça escolhas na própria aba. TR registradora é da aula 8; Taxa Referencial,
  da aula 11. Não altere o cadastro global ou os materiais para resolver a busca.
- Refinar pesquisa fica recolhido. Interseccione aulas e tipos em TODAS as fontes,
  comparações e tabelas. Zero resultados não autoriza buscar fora do escopo.
  Preserve rascunhos diferentes; atualize a pergunta aberta sem duplicar histórico.
- Destaque uma frase literal e preserve qualificadores e listas completas de
  composição. Ver contexto abre o registro integral; não substitua o texto da
  fonte por uma paráfrase. Preserve fontes visíveis e destaque amarelo dos termos.
- Características da comparação ficam sob controle expansível, com seleção
  múltipla e Todas. Use rótulos reais das tabelas quando existentes. Campo sem
  evidência recebe indicação de ausência; composição não comprova mandato.
- Guarde escopo e características em cada resposta anterior, sem controles que
  alterem a consulta atual. Abrir histórico não pode reordenar o array salvo.
  Preserve H, cfg, qz, cronômetro, materiais, navegação, teclado e dois temas.
- Execute também `tests/test_consulta_refinements.py` e mantenha a documentação
  em `docs/consulta-local.md`. Não acrescente chamadas externas ou modelos pagos.

## Próxima aula de câmbio — orientação registrada em 22/10/2026

O usuário ainda enviará os slides e as transcrições. Ao criar a próxima aula,
cruze as fontes e aplique a divisão FINAL solicitada:

- Aula-fonte 19 — Mercados de Câmbio: **42,5%** das questões.
- Aula-fonte 21 — Taxas de Câmbio: **42,5%** das questões.
- Aula-fonte 20 — Cupom Cambial: **15%** das questões.

Essa orientação substitui o pedido inicial de 40%/40%/20%. Os números 19, 21 e
20 identificam as aulas-fonte do professor, não três novas aulas da plataforma.
O usuário escolheu os pesos conforme sua avaliação de incidência no CPA;
não os apresente como estatística oficial da prova.

Mantenha a quantidade por aula e a distribuição de dificuldades já estabelecidas:
100 questões, com 20 fáceis, 40 médias, 20 difíceis e 20 Hardcore, além do banco
próprio de 50 Bate-pronto. Aplique os pesos temáticos também dentro dos níveis e
no Bate-pronto, com arredondamento proporcional para números inteiros, preservando
os totais e equilibrando as fontes 19 e 21. Em 100 questões, os pesos resultam
em 43/42/15 (ou 42/43/15); em 50 Bate-pronto, a aproximação é 21/21/8. Não
aumente o banco apenas para eliminar frações. Confira e informe o arredondamento
na entrega da aula, sem prometer percentuais exatos impossíveis nesses totais.

Este registro não autoriza antecipar conteúdo: aguarde os materiais que o
usuário enviará para produzir a aula e suas questões.

### Associações de causa e efeito — padrão registrado em 22/10/2026

O usuário aprende por associações entre conceitos. Sempre que os slides ou a
explicação do professor apresentarem encadeamentos, registre-os em AMBOS:

- **Material de apoio → Tabelas:** quadro que permita acompanhar as etapas.
- **Trilha → Dicas e macetes:** a mesma relação em sequência curta e legível,
  explicando o mecanismo, sem depender exclusivamente de setas ou cores.

Na próxima aula de câmbio, confira especialmente os DOIS ÚLTIMOS slides citados
pelo usuário: relações com juros internos, juros externos e prêmio de risco.
Esses pontos devem ganhar tabelas, além de aparecer nas dicas. O exemplo dado
foi a cadeia juros internos maiores → entrada de divisas → valorização da moeda
doméstica → importações favorecidas. Confirme a formulação, as condições e os
sentidos das setas nos slides E na transcrição antes de incorporá-la ao conteúdo.

Quando couber, organize colunas como mudança inicial, fluxo de divisas, efeito
sobre a moeda/cotação, comércio exterior e condições/observações. Adapte as
colunas à relação efetivamente ensinada; não invente etapas para preencher o
quadro. Explique a direção de cada elo e suas premissas. Diferencie tendência
econômica de consequência automática e correlação de causalidade. Nas relações
cambiais, identifique a moeda e a convenção de cotação: valorização da moeda
doméstica não equivale necessariamente a alta do número usado para cotar câmbio.

A orientação vale também para futuras aulas e pode ser aplicada às anteriores
quando suas fontes forem revisadas, conforme autorização do usuário. Preserve
coerência entre tabelas e dicas, conteúdos existentes e o padrão visual do
sistema. Não crie as tabelas da nova aula antes de receber os materiais.

### Slides recebidos para a próxima aula de câmbio

- `Screenshot_1 (5).pdf`, Sediment `file_000000007fa0820e8a3b761d3c374229`:
  20 páginas, correspondentes aos screenshots 1–20.
- `Screenshot_21.pdf`, Sediment `file_000000005fa4820ea24c791f84d903f7`:
  5 páginas, correspondentes aos screenshots 21–25, nessa ordem.
- Os dois PDFs foram abertos e suas 25 páginas renderizadas. São prints sem
  camada de texto; confira as imagens em resolução adequada ao extrair conteúdo.
- O usuário confirmou os screenshots **24 e 25**: são, respectivamente, as
  páginas **4 e 5 do segundo PDF**. O 24 trata das relações com juros internos e
  externos; o 25, de prêmio de risco. Ambos foram inspecionados individualmente.
- No 25, o exemplo de prêmio é o diferencial de juros 10% − 3% = 7%. Ao cruzar
  com a transcrição, preserve o contexto desse diferencial; não confunda uma
  remuneração relativa maior com a afirmação universal de que aumento do risco
  percebido atrai capitais. Registre as premissas nas tabelas e dicas.
- A transcrição foi recebida em 22/10/2026 e cruzada com as 25 imagens na aula 12. A regra de aguardar as fontes foi satisfeita.

### Aula 12 — Mercado de Câmbio, Taxas e Cupom Cambial

- Três blocos: mercado (transcrição 19, slides 1–11), cupom e swaps (20, slides
  12–15), taxas e relações econômicas (21, slides 16–25). Manter as três partes
  acessíveis na única entrada Aula 12, com filtros compartilhados e agregados.
- Pedido final: 42,5% / 15% / 42,5%. Arredondamento em 100 questões: 43/15/42;
  níveis Fácil/Médio/Difícil/Hardcore por fonte: 9/17/8/9, 3/6/3/3 e 8/17/9/8.
  Bate-pronto: 21/8/21. IDs 1101–1200 e 100551–100600, sem alterar os anteriores.
- Screenshots 24 e 25: cadeias explícitas nas tabelas E nas dicas; cotação em
  R$/US$, divisas, moeda doméstica, comércio e hipóteses. Maior diferencial com
  risco constante não é piora de risco. 10% − 3% = 7 pontos percentuais.
- Cupom usa fatores compatíveis no tempo; 13,65% com cotação 5→5,20 resulta em
  9,28% arredondado. Swap do BC liquida em reais, sem entrega do principal em
  dólares e sem retirada automática de reservas. Explicitar a perspectiva das
  pernas e condições de valor, prazo e indexador do hedge.
- Câmbio real: q=e×Pexterno/Pinterno; separar nível de variação. Os exemplos
  conferidos são 255/275, 275/255 e 306/310, com variações contra base 1 de
  −7,27%, +7,84% e −1,29%. Preço positivo abaixo de 1 não é número negativo.
- A expansão ACE foi cadastrada; PTAX recebe descrição funcional fiel, não uma
  etimologia inventada. Adiar nomes só quando revelam o fato cobrado.
- Limites do slide 3: IP US$100 mil, grupo CTVM/DTVM etc. US$300 mil, reais em
  espécie R$10 mil. Referências, sem certificação de vigência: consultas oficiais
  bloqueadas pelo proxy. Não usar como gabaritos numéricos atuais nem inferir
  crime de evasão de divisas automaticamente de descumprimento da exceção PF.
- Relatórios: docs/aula-12.md e docs/aula-12-cobertura.json. Rodar também
  tests/test_aula12.py ao alterar esta aula. Preservar o conteúdo e os hashes
  históricos das onze aulas, seus manifestos e registros de respostas.
