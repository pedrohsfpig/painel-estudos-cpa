# Consulta local aos materiais

A aba Consulta foi acrescentada entre Trilha e Praticar, com a lupa e o mesmo
padrão visual do sistema. O campo aceita uma pergunta de até 500 caracteres;
Consultar ou Enter apresenta a resposta nessa tela. Shift+Enter permite outra
linha. Não há botões de sugestões. Limpar limpa somente a consulta. Todas as
perguntas anteriores ficam sob um único controle expansível, fechado por padrão;
o rascunho e as respostas sobrevivem à navegação entre abas, não ao recarregamento.

## Dados e reconhecimento

O índice local extrai trechos de resumos, dicas, pegadinhas, números, ramos de
mapas mentais, linhas/células de tabelas, diagramas, linhas do tempo, flashcards,
quadros comparativos e explicações corretas de questões/Bate-pronto. O índice
inicial tem mais de 4 mil registros das 11 aulas. Novas aulas são incluídas pela
estrutura dos dados. Não há cópia editorial nem mudança nos conteúdos originais.

O reconhecimento usa o cadastro de siglas e nomes, títulos/operadores existentes,
normalização de acentos, formas de plural, sinônimos e características pedidas.
Inclui formas de voz como bacém/bacem/bacin e siglas no plural. Considera função,
composição, área, natureza, mandato, nomeação, recursos, limites e funcionamento.
Palavras desconhecidas só recebem correção conservadora quando há contexto ou
um termo isolado suficientemente longo, com uma única correção próxima.

A seleção prioriza fontes estruturadas, aula dedicada ao assunto, entidade e
característica solicitadas. A origem de cada coluna é preservada. Tabelas
existentes são projetadas nas colunas pertinentes quando respondem ao pedido;
comparações sem tabela conjunta selecionam trechos por característica, deixando
explícita a ausência de dado quando necessária. Substantivos compartilhados,
como “fluxos real e monetário”, e perguntas de continuidade (“e o mandato?”)
recebem tratamento de contexto. Comparações mostram até quatro assuntos, com
aviso se outros foram reconhecidos.

## Apresentação e limites

Cada resposta contém texto literal dos materiais e identificação de aula, tipo e
título da fonte, sem redirecionar a outra tela. Respostas simples usam tópicos;
comparações e tabelas existentes são mostradas no próprio resultado. Outros
trechos ficam recolhidos. Tabelas largas podem rolar dentro de sua área no celular,
sem deslocar horizontalmente a página inteira.

Conteúdo relacionado é identificado como tal. Perguntas sem correspondência não
recebem uma resposta fabricada. O motor não é um modelo de linguagem: não garante
compreender toda construção de frase, não faz pesquisa externa, não atualiza
normas nem calcula fatos ausentes das fontes. O índice não inclui alternativas
incorretas como fatos. Explicações de questões são fontes secundárias, abaixo dos
materiais estruturados, e mantêm a indicação de sua origem.

Não há assinatura adicional, API, chave ou transmissão de perguntas. Os arquivos
`consulta.js` e `consulta.css` são estáticos e devem acompanhar `index.html` no
GitHub Pages. A primeira indexação é feita ao consultar; nas conferências, ficou
abaixo de um segundo no Chromium local, sem promessa de tempo em todo aparelho.

## Verificação

Os testes específicos conferem a posição do menu, perguntas por membros/funções,
siglas e plurais, comparação CVM/Susep, projeção da tabela SCD/SEP, continuidade,
fontes literais, Selic sem contraparte central, limites ordinários/especiais,
FGCoop, ausência de resultados, texto não confiável, novas aulas e dados salvos.
As consultas são exercitadas com rede bloqueada depois do carregamento. Também
são conferidas a sessão em andamento, rascunho, histórico, seleção, tema e filtros,
sem gravar respostas novas por consultar. Temas claro/escuro e larguras 390,
1024, 1280, 1440 e 1920 px foram incluídos, com inspeção visual das respostas.

Validação concluída: **134 testes aprovados** — 12 da Consulta, 11 de busca
contextual, 6 de refinamentos, 4 dos menus, 4 de hierarquia do painel, 5 do
desempenho detalhado, 4 de layout da prática, 3 de navegação/retorno, 9 de
navegação entre questões e 76 de fluxos completos. Os testes usam contextos
isolados. Q, BP, AL, MAT, quadros comparativos e funções de histórico/filtro
foram comparados com a versão anterior e permanecem idênticos.

## Ajustes visuais da consulta

Retirados os botões de sugestões. Perguntas anteriores ficam em um único
controle fechado, com contagem; a lista é montada somente ao expandir e retirada
do DOM ao recolher. Cada pergunta conserva a própria resposta e os destaques
correspondentes, sem acrescentar resumos de perguntas antigas à página fechada.

Os termos da consulta aparecem em negrito e na cor de atenção (`--md`), sem
pintar o cartão inteiro. O destaque cobre tópicos, títulos, nomes de assuntos e
tabelas, incluindo nomes/siglas equivalentes e variantes de plural e gênero,
como pignoratício/pignoratícias e TLP/Taxa de Longo Prazo. Palavras genéricas de
comando, como função e comparação, não recebem o mesmo destaque dos assuntos.
Fontes e avisos mantêm apresentação discreta.

A marcação é aplicada a nós de texto depois do escape HTML, com limites de
palavra e junção de intervalos sobrepostos. Preserva grafia, acentos, pontuação,
atributos e textos integrais. Não altera o índice, a busca, a seleção dos trechos,
os dados de aula ou qualquer resposta registrada.

Validação dos ajustes visuais: **115 testes aprovados** — 16 da Consulta, 11 de
busca contextual, 3 de retorno/navegação da prática, 9 de navegação entre questões
e 76 de fluxos completos. Inspecionados os exemplos pignoratício, Bacen e TLP nos
dois temas. O motor de consulta anterior ao renderizador permanece idêntico,
assim como index.html, os bancos, materiais, histórico e seleção das respostas.


## Relações e perguntas abertas

A recuperação agora identifica pedidos de histórico/substituição, cálculo,
causa/efeito e sequência, além das características e comparações existentes.
Termos de comando da intenção deixam de competir com o assunto. Sinônimos de
redução, obrigação e empréstimo aproximam perguntas abertas do vocabulário das
fontes. Trechos com evidência da relação recebem prioridade sobre cartões que
apenas descrevem a entidade.

Itens de uma mesma linha do tempo compartilham contexto para a recuperação,
sem alterar seu texto ou misturar linhas do tempo distintas. Por exemplo,
“Qual era a taxa antes da TLP?” encontra o item TJLP anterior a 2018, o item TLP
desde janeiro de 2018 e a ressalva do resumo: novas operações cabíveis, sem mera
renomeação ou migração automática dos contratos antigos. A pergunta inversa
prioriza a etapa posterior. TJLP também recebe destaque, por ser o outro assunto
expresso nas fontes dessa relação. Nenhuma resposta TLP/TJLP foi cadastrada à
parte: o teste de nova fonte verifica que outra relação entra pelo mesmo índice.

A evidência precisa pertencer ao assunto e à fonte. Menção incidental ao IPCA
numa mudança de regime fiscal não comprova uma taxa predecessora do IPCA;
“não substitui” não comprova substituição. Datas e marcos desconexos não
comprovam sucessão de entidades. Perguntar por que houve uma mudança exige
evidência causal, não apenas seu histórico. Quando ela falta, o resultado
continua identificado como relacionado, sem inventar o motivo.

Perguntas de continuidade, como “e o que era usado antes?” ou “como é
calculada?”, retomam o assunto anterior. Uma entidade explicitamente citada
prevalece sobre esse contexto. O mecanismo continua local e extrativo, sem
treinamento de modelo, IA, serviço pago ou acesso externo. Reconhecer padrões
e relações documentadas amplia a consulta; não garante interpretação irrestrita
de qualquer formulação.

A revisão acrescenta sete testes de contexto, com paráfrases, direção temporal,
ressalvas contratuais, cálculo, causa, sequência, fontes literais, nova aula,
continuidade, destaques e perguntas negativas. `index.html`, conteúdos e bancos
permanecem inalterados.

Validação desta revisão: **122 testes aprovados** — 23 da Consulta (16 existentes
+ 7 de contexto), 11 de busca contextual, 3 de retorno/navegação, 9 de navegação
entre questões e 76 de fluxos completos. A resposta TLP/TJLP foi inspecionada nos
dois temas. `index.html` e `consulta.css` permanecem idênticos à versão anterior.


## Esclarecimento, leitura e refinamento das fontes

A Consulta ganhou quatro controles locais, com a paleta e a navegação existentes:

1. **Esclarecer ambiguidades.** Significados de uma mesma sigla permanecem
   separados. Além do cadastro, o índice reconhece definições explícitas dos
   resumos quando as iniciais correspondem ao nome, e rótulos como
   “Registradora (TR)”. Assim, TR pode ser Taxa Referencial (aula 11) ou entidade
   registradora (aula 8). Nome completo, contexto distintivo ou uma aula com
   definição única podem resolver o sentido. Quando faltam esses sinais,
   aparecem escolhas na própria Consulta, sem selecionar um significado por
   frequência ou posição. Uma legenda como “CMN — composição” não vira expansão.
2. **Trecho relevante e contexto.** Cartões e células de comparações extraídas
   enfatizam uma frase literal e podem mostrar um recorte compacto. Os demais
   dados ficam em “Ver contexto”, fechado por padrão, com a íntegra do registro
   e a fonte sempre identificada. Sentenças com qualificadores explícitos são
   preservadas junto da frase principal; listas de composição ficam completas.
   Esse destaque é distinto da marcação amarela dos termos pesquisados. Tabelas
   originais conservam os textos das células e os filtros de linhas.
3. **Refinar pesquisa.** Um controle recolhido abre seleção múltipla de aulas e
   tipos de material. Sem seleção específica, todas as fontes participam.
   Selecionar aulas e tipos intersecciona os dois filtros em cartões, tabelas e
   comparações. Uma pergunta aberta se atualiza sem criar outra entrada no
   histórico; um rascunho diferente aguarda Consultar. Não há retorno silencioso
   a fontes de fora do filtro se faltar informação. A resposta identifica seu
   escopo. Limpar restaura também todos os filtros.
4. **Características da comparação.** Um controle expansível permite escolher
   características e restaurar Todas. Em comparações montadas, as opções seguem
   as características com evidência disponível; nas tabelas existentes, seguem
   as linhas originais, inclusive rótulos próprios como Modelo e Fonte principal.
   Campos sem evidência são indicados. Contagem de membros não comprova duração
   de mandato. Nenhuma seleção recebe preenchimento inventado. Desmarcar tudo
   apresenta uma orientação; selecionar uma característica recupera a tabela.

Filtros e escolhas ficam apenas na memória da visita e sobrevivem à navegação.
Respostas anteriores conservam seus próprios recortes, filtros e linhas de
comparação; seus controles não alteram a resposta atual. Escolher significado,
filtrar ou personalizar não duplica entradas. O histórico continua recolhido,
sem botões de sugestões. Abrir o histórico durante um esclarecimento não altera
sua ordem. Todos os controles funcionam por teclado e mantêm o foco ao atualizar.

O mecanismo continua extrativo e baseado em regras: não reescreve os materiais,
não infere fatos ausentes, não usa IA generativa e não envia perguntas à rede.
Nenhuma alteração foi feita em `index.html`, nos bancos, materiais ou histórico
de estudo. O teste antigo do histórico passou a selecionar somente o summary
da pergunta, pois agora há também summaries internos de “Ver contexto”.


Validação dos quatro refinamentos: **135 testes aprovados** — 36 da Consulta
(16 de base, 7 de contexto e 13 de refinamentos), 11 de busca contextual, 3 de
retorno/navegação, 9 de navegação entre questões e 76 de fluxos completos.
Incluídos significados separados de TR, fontes por aula/tipo, seleção e restauração
de linhas, falta de evidência, recorte literal com ressalvas, contexto integral,
rascunho, histórico durante esclarecimento, sessão em andamento e rede bloqueada.
Inspecionados os quatro recursos nos temas claro e escuro, além do celular;
os testes de largura incluem 390, 1024 e 1440 px para os novos controles.
