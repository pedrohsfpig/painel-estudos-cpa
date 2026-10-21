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
