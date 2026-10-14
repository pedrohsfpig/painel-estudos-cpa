# Bate-pronto

Validação da entrega: **125 testes aprovados** — 41 verificações do banco e
revisões, 76 testes existentes no navegador e 8 testes específicos do Bate-pronto.
`git diff --check` passou; `Q`, `AL` e `MAT` foram comparados à versão inicial e
permanecem com o mesmo conteúdo.

Em **Praticar → Bate-pronto**, selecione as aulas, o filtro de questões e a
quantidade. Há botões para 5, 10, 20, 30, 40 ou 50 e um campo para outro valor.
O limite da sessão depende do estoque dos filtros e da participação equilibrada
das aulas. Em seleção explícita, nenhuma aula é excluída silenciosamente.

São **450 questões novas, 50 por aula**, com duas opções. Os enunciados têm até
10 palavras e as alternativas até 8 palavras nesta entrega. Há **61 lacunas**,
intercaladas com definições, funções, composições, prazos e classificações diretas.
O modo não tem níveis de dificuldade, casos contextualizados ou cálculos.

Exemplos:

- Banco Central é: Autarquia de natureza especial / Sociedade de economia mista.
- _____ define a meta de inflação: CMN / Copom.
- Conta PI admite saldo negativo para liquidar? Não / Sim.

Depois da escolha, aparecem o resultado e as duas justificativas ao lado das
alternativas. Próxima permite seguir depois da leitura; a seleção não avança
automaticamente. As opções são embaralhadas, preservando o vínculo das explicações.
As lacunas são renderizadas com destaque azul e nome acessível.

O resultado apresenta acertos, erros, tempo, desempenho por aula e por conceito,
prioridades de revisão e atalho para refazer erros no próprio Bate-pronto.
O histórico salva origem própria, permite inéditas/erros e participa da evolução
diária e dos indicadores de tentativas. Andamento da trilha conserva o banco
principal; novos itens curtos não entram nos simulados ou no checkpoint.

A regressão também corrigiu o cache da data exibida no cartão diário: ele
acompanha a data efetivamente renderizada, permitindo que a virada de dia
atualize um painel aberto corretamente.

## Conteúdo e preservação

Cada registro de `BP` tem duas explicações próprias e uma referência de conteúdo
em `Q`, complementada pelos materiais da respectiva aula. A referência não indica
que o enunciado original foi simplesmente reduzido: as perguntas e explicações
foram redigidas para relações conceituais diretas. `bate-pronto-banco.json` registra
ID, aula, assunto, referência e formato.

As aulas 8 e 9 mantêm, no novo banco, os pesos temáticos: 25 IP/fintechs e 25 SPB;
25 ANBIMA/comparações, 20 garantias e 5 liberdade econômica. Aula 7 cobre bancos,
fomento, crédito especializado, consórcios, bolsa/intermediários, seguros e
previdência. Nenhum valor cuja vigência foi marcada como incerta nas revisões
anteriores foi convertido em gabarito numérico novo.

Os 900 registros de `Q` e os materiais de `AL`/`MAT` permanecem intactos. IDs
100001–100450 pertencem ao Bate-pronto, sem deslocar registros históricos.
Adicionar aulas futuras exige itens conceituais novos e revisão das duas opções,
com as mesmas regras de clareza, exclusividade de resposta e feedback específico.

Os testes verificam quantidade, formatos, fontes, respostas e riscos de
generalização; no navegador, seleção múltipla, quantidades personalizadas,
escassez, rotação, feedback após embaralhamento, teclado, histórico, revisão,
recarregamento, temas e PC. Testes de estrutura não certificam legislação nem
garantem ausência absoluta de falhas pedagógicas.
