# Desempenho detalhado — aba Estatísticas

Desde 27/10/2026, o bloco fica na aba **Estatísticas**, abaixo de Quadro do SFN,
e começa aberto. A matriz de aulas × dificuldades fica recolhida. A apresentação
e a separação do painel estão em [estatisticas.md](estatisticas.md).

A consulta anterior mostrava níveis,
aulas e todos os temas ao mesmo tempo, com barras extensas e cores que ora
indicavam dificuldade, ora aproveitamento. Agora Aulas, Temas e Dificuldades
ocupam abas de uma única área, com até seis cartões por página.

Cada cartão mostra título, percentual neutro, contagem de acertos em verde,
erros em âmbar e total de tentativas. Aulas têm nome completo e número; temas
identificam suas aulas. O contorno verde marca grupos sem erros, sem pintar o
cartão inteiro. Mini gráficos circulares usam verde nos acertos e âmbar nos erros. Não há
barras extensas nem cores de dificuldade misturadas ao aproveitamento.

Aulas aparecem em ordem numérica, incluindo 10 e 11 depois de 9. Temas abrem
pelo menor aproveitamento, e níveis seguem sua ordem. A consulta permite trocar
ordenação, buscar por nome de aula/tema e paginar, mantendo todos os resultados
acessíveis. A busca ignora acentos e usa as equivalências já existentes. Temas
com o mesmo nome mantêm o agrupamento anterior e indicam as aulas envolvidas.

O foco sugerido considera o menor aproveitamento nos filtros atuais, mostra sua
amostra e só aparece quando há erros. Totais continuam contando tentativas,
inclusive repetições, registros antigos booleanos e Bate-pronto. Uma nota explica
que poucas respostas ainda não indicam domínio. Os filtros de nível e origem
ficam na aba Estatísticas; painel, evolução e prioridades usam o histórico completo.

Controles internos atualizam só a seção: não renderizam novamente a sessão,
não registram respostas, não alteram a seleção da prática nem os filtros globais.
A busca conserva foco e posição de digitação. Abas funcionam por setas, Home/End
e Enter; paginação conserva foco em botão disponível. O layout usa três colunas
no computador, duas em larguras intermediárias e uma no celular.

## Verificação

`tests/test_dashboard_details.py` confere os totais de todos os grupos e páginas
contra as tentativas originais, ordem numérica, filtros, busca, estados vazios,
amostra pequena, ausência de falsa fraqueza, teclado, foco e preservação de uma
sessão em andamento. Foram conferidos temas claro/escuro nas larguras 390, 1024,
1280, 1440 e 1920 px e inspecionadas visualmente as três abas e a tela pequena.

Q, BP, AL, MAT, quadros comparativos, histórico, filtros globais e distribuição
de questões foram comparados com a versão anterior e permanecem inalterados.

Validação da apresentação anterior: **126 testes aprovados** — 5 do desempenho detalhado,
4 de hierarquia do painel, 11 de busca contextual, 6 de refinamentos, 4 dos menus,
4 de layout da prática, 3 de navegação/retorno, 9 de navegação entre questões,
4 de cartões do resultado e 76 de fluxos completos. Contextos de navegador
isolados; nenhum histórico real do usuário foi manipulado.
