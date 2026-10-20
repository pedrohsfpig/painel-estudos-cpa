# Busca contextual — 20/10/2026

Substitui a apresentação da busca de `docs/busca-e-hierarquia-painel.md` após o
usuário rejeitar a mistura de áreas nas telas locais e a lista extensa com
rolagem interna. A hierarquia do restante do painel é preservada.

| Tela | Conteúdo pesquisado |
| --- | --- |
| Painel | Todas as áreas, com filtros Trilha, Questões e Materiais; seletor de tipo de material |
| Trilha | Aulas/blocos, resumo, dicas, pegadinhas e números |
| Praticar | Enunciados dos modos Estudo, Simulado, Hardcore ou Bate-pronto, conforme modo/nível/histórico atuais |
| Tabelas | Somente tabelas, entre todas as aulas |
| Outros materiais | Somente o tipo aberto: mapas, diagramas, prazos, flashcards ou quadro comparativo |

A busca geral fica imediatamente depois do estudo diário. Cada contexto tem sua
própria consulta e página; os tipos de material também têm consultas independentes.
Resultados são cartões com aula, origem/nível, título, contexto curto e ação.
São quatro por página, com contador, anterior/próxima e seletor para qualquer
página. Não há lista de resultados com rolagem interna nem filtros universais nas
telas locais. Campos e cartões usam a mesma paleta e bordas dos outros componentes.

O índice deriva dos dados atuais, inclui o quadro do SFN e enunciados dos bancos
Q/BP, e mantém a equivalência de siglas e a normalização de acentos. Alternativas,
gabaritos e feedbacks não entram nos resultados de questões. A busca não modifica
conteúdo, IDs, histórico, seleção de aulas ou proporções da prática.

“Praticar esta questão” inicia explicitamente o ID encontrado, em Estudo por
padrão no painel, Hardcore ou Bate-pronto para seus bancos; na prática de Simulado,
respeita esse modo. Se já há uma sessão em andamento, o cartão oferece retomá-la,
sem substituir IDs, respostas ou relógio. A sessão normal configurada continua
seguindo a seleção de aulas e seus filtros, sem aplicar o termo silenciosamente.

Abrir material ou trilha expande e foca a origem, sem resumir/excluir textos.
Flashcards abrem na pergunta. Recolher resultados mantém a consulta disponível.

## Conferências

- Testes de busca contextual, filtros globais, separação das consultas, paginação
  completa, equivalências, entrada não confiável, destinos e futuras aulas.
- Questões por modo/nível/histórico; sem gabaritos antes de responder; início
  somente por ação explícita e preservação de sessão existente.
- Temas claro/escuro e larguras 390, 1024, 1280, 1440 e 1920.
- Regressões de painel, seleção/distribuição, retorno da prática, navegação entre
  questões, materiais, checkpoint diário e armazenamento.

Validação concluída: **107 testes aprovados** — 11 de busca contextual, 4 de
hierarquia do painel, 4 de layout da prática, 3 de navegação/retorno da prática,
9 de navegação entre questões e 76 de fluxos completos. Inspeção visual dos temas
claro/escuro em painel, prática e tabelas, além da tela estreita. A comparação com
a versão anterior confirmou Q, BP, AL, MAT, quadros e `pool` idênticos. Os testes
usam armazenamento isolado; nenhum histórico real do usuário foi manipulado.

## Refinamento por aula, questões e tipo de material

A Trilha passa a mostrar primeiro cartões de aulas em ordem numérica, com a
quantidade de informações encontradas. Escolher a aula abre só seus resultados;
Trocar aula retorna ao conjunto. Essa etapa existe no filtro Trilha do painel e
na busca local da Trilha. Os filtros internos de resumo/dicas/pegadinhas não mudam.

Os cartões da pesquisa têm identidade consistente: selo numérico, título da aula,
ícone e cor. O mesmo número/cor acompanha a aula em seleção, conteúdo, questões
e materiais, sem atribuir logos oficiais inventados nem alterar cores dos mapas.

Questões no painel oferece dificuldade, modo, histórico e aula. Contagens são
reais e os filtros se combinam; pendências seguem a última resposta. O modo
Simulado exclui itens somenteEstudo e inicia o resultado no modo correspondente.
Os controles da busca não alteram a sessão configurada nem registram respostas.

Materiais usa cartões visuais por tipo, com ícones, contagens, seleção indicada e
cores consistentes com a paleta existente. Há também seleção de aula. Tipos sem
resultados mostram zero. Corrigida a indexação do quadro SFN: rótulos e nomes
são separados, permitindo encontrar BCB/BACEN também nesse quadro.

Testes específicos em `tests/test_search_refinements.py` cobrem contagens, ordem
numérica, dificuldade/modo/histórico, seleção de aula, materiais, cores estáveis,
teclado, zero resultados e larguras de PC/celular nos dois temas.

Validação dos refinamentos: **113 testes aprovados** — 6 específicos dos novos
filtros/identidades, 11 de busca contextual, 4 de painel, 4 de layout da prática,
3 de navegação/retorno, 9 de navegação entre questões e 76 de fluxos completos.
Conferidos os temas claro/escuro e larguras de 390 a 1920 px. Q, BP, AL, MAT,
quadros comparativos e a seleção de questões permanecem idênticos. A inspeção
visual incluiu a grade de aulas, a aula selecionada e os filtros de questões e
materiais. Trechos de contexto respeitam limites de palavras ao abreviar.

## Apresentação dos menus de filtro

Modo, Meu histórico e Aula mantêm todas as opções e combinações, com um menu
visual compartilhado: paleta dos dois temas, ícones discretos, cantos e espaços
consistentes, marca de seleção e foco visível. A lista de aulas mostra número,
nome e contagem, em ordem. O mesmo seletor de aula é usado em Materiais.

Os menus abrem sobre o conteúdo e ajustam posição/altura ao espaço disponível,
sem serem cortados pelos cartões. Fecham com novo clique, Escape, Tab ou clique
fora. Setas, Home/End, digitação e Enter/Espaço permitem selecionar pelo teclado;
foco volta ao filtro após a escolha. A seleção só é aplicada ao confirmar.

`tests/test_search_filter_menus.py` cobre mouse, teclado, foco, fechamento,
seleção de aula e limites de tela em 390, 1280 e 1920 px nos dois temas. Os testes
de refinamento passam a usar os menus visíveis, sem chamar setters diretamente.
Conferidos visualmente os menus abertos no computador e celular. Q, BP, AL, MAT,
quadros comparativos e distribuição de questões foram comparados com a versão
anterior e permanecem idênticos.

Validação desta atualização: **117 testes aprovados** — 4 dos menus visuais,
6 dos refinamentos, 11 de busca contextual, 4 de painel, 4 de layout da prática,
3 de navegação/retorno, 9 de navegação entre questões e 76 de fluxos completos.
Os testes usam contextos isolados, sem modificar o histórico real do usuário.
