# Área de estatísticas — 27/10/2026

O menu ganhou **Estatísticas**, abaixo de **Quadro do SFN**. O painel mantém
checkpoint diário, busca geral, próximo passo, quatro indicadores básicos,
evolução completa, andamento das aulas e acessos de revisão. O detalhamento e
seus filtros saíram do painel, que passa a mostrar sempre o histórico completo.
Há também um atalho “Ver estatísticas detalhadas” junto aos indicadores.

A área dedicada aproveita a largura disponível e concentra:

- Filtros por nível e origem, com seleção visível, teclado e limpeza.
- Tentativas, acertos, erros, aproveitamento, itens diferentes e aulas praticadas.
- Gráficos circulares para o aproveitamento total e por dificuldade. Acertos
  usam verde, erros usam vermelho exclusivamente nesta aba e os percentuais ficam neutros. Sem respostas,
  o gráfico fica vazio e mostra um traço, não um percentual estimado.
  O texto é arredondado; os arcos mantêm a fração exata, inclusive um erro
  residual quando o valor exibido arredonda para 100%.
- Detalhamento por aulas, temas ou dificuldades, com seis cartões por página,
  mini gráficos, amostra, busca e ordenação. Aulas seguem ordem numérica;
  temas começam pelo menor aproveitamento. As três dimensões permanecem
  acessíveis, com o agrupamento histórico de temas iguais entre aulas.
- Matriz expansível de todas as aulas × dificuldades. Células mostram percentual
  e acertos/tentativas; sem respostas é diferente de 0% de acerto. Uma única
  escala verde permite comparar resultados sem misturar cores de dificuldade.

O detalhamento começa aberto e a matriz recolhida. A escolha de abrir ou fechar
é mantida ao filtrar, navegar e alternar tema durante o uso. No celular, cartões
se reorganizam e a matriz tem rolagem própria por teclado, preservando a página.
O foco de revisão não aparece se tudo foi correto; amostras inferiores a cinco
respostas são apresentadas como revisão pontual, com seu tamanho explícito.

## Métricas e preservação

Todos os gráficos e cartões usam as mesmas respostas de `HF`, sem corte de datas.
Repetições continuam sendo tentativas; itens únicos são contados separadamente.
Registros booleanos antigos são aceitos e IDs inexistentes são ignorados, sem
apagar nada. Erros nas tentativas não equivalem aos erros pendentes, que continuam
seguindo a última resposta de cada ID na aba Erros.

Os filtros de estatísticas não alteram os indicadores básicos do painel, a
série de evolução, o plano diário, a distribuição da prática ou os erros pendentes.
A busca, a ordenação e a paginação do detalhamento atualizam só a consulta.
Nenhum filtro registra respostas, reinicia sessões ou altera o relógio. No
checkpoint, a persistência normal continua atualizando tempo decorrido e data do
rascunho, preservando ID, respostas, posição, alternativas, ajudas e resultado.

Não há serviço, modelo de IA, biblioteca externa ou novo armazenamento. Q, BP,
AL, MAT, quadros e manifestos das aulas permanecem intactos. A mudança é de
organização e apresentação das métricas existentes.

## Validação

`tests/test_statistics.py` verifica navegação, métricas com repetições, filtros,
matriz, diferença entre ausência e zero, dados antigos, histórico inválido,
seções expansíveis, sessão normal e diária, temas e larguras 390–1920 px.
`tests/test_dashboard_details.py` confere todos os grupos, ordenação, paginação,
percentuais, foco e semântica visual. As regressões de painel e fluxos foram
atualizadas para acessar os filtros na nova área.

A revisão geral aprovou **209 testes de regressão** e **76 fluxos de navegador**.
A verificação específica da área reúne **16 casos**, incluindo matriz célula a
célula, filtros, teclado, preservação de sessões e amostras vazias. Foram
inspecionados os temas claro/escuro em 1440 px e a matriz no celular em 390 px;
os testes também cobrem 768, 1024, 1280 e 1920 px. Os dados completos de
Q (1.200), BP (600), AL (12) e MAT foram comparados à versão anterior e
permanecem iguais. Não foi manipulado histórico real do usuário.

## Refinamento de cores — 27/10/2026

A escala da matriz passou a ocupar uma faixa ampla de verdes: clara a escura no
tema claro, escura a clara no escuro. Uma legenda com 0%, 25%, 50%, 75% e 100%
facilita distinguir as intensidades. O texto troca entre preto e branco para
manter contraste mínimo de 4,5:1, inclusive nas contagens das células. Sem
respostas continua sendo um traço, separado do verde de 0% observado.

Erros aparecem em vermelho no resumo, anéis, legendas e detalhamento de
Estatísticas. As telas de resultado continuam usando âmbar, como antes.
Filtros de nível seguem as cores já usadas em Fácil, Médio, Difícil e Hardcore;
as opções de origem usam ícones de conjunto, livro, questionário e associação
rápida, mantendo seus rótulos e o comportamento de seleção.

`tests/test_statistics_colors.py` confere os 101 percentuais em ambos os temas,
a separação visual dos intervalos, contraste, cores semânticas, ícones distintos,
teclado, larguras de 390–1920 px e preservação do histórico e bancos.

Validação deste refinamento: **23 testes específicos e 76 fluxos de navegador
aprovados**. Inspeção visual das escalas e filtros nos temas claro/escuro;
index.html e os bancos de conteúdo permaneceram integralmente iguais.
