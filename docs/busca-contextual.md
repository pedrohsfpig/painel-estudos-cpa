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
