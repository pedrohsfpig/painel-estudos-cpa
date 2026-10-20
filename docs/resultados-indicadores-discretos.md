# Indicadores de resultado — refinamento de 19/10/2026

O usuário considerou as barras extensas, a divisão verde/vermelho e os percentuais
azuis pouco agradáveis e difíceis de analisar rapidamente.

A apresentação passa a usar percentuais maiores na cor neutra do texto. As aulas
mantêm título completo, acertos, total e erros. Pontos preenchidos indicam acertos;
pontos em contorno indicam erros, com legenda. São respostas reais do grupo,
na ordem em que foram respondidas, não segmentos arredondados de uma escala.
Há no máximo 12 pontos por grupo: o sinal + informa as demais respostas, a legenda
explica o limite e as contagens/percentuais sempre incluem todas as respostas.

As dificuldades usam a mesma linguagem visual em linhas compactas, sem os anéis
verdes/vermelhos. O indicador circular geral usa um único destaque sobre trilha
neutra. Erros recebem destaque pontual em âmbar quando existem; zero erros fica
neutro. As cores das respostas e feedbacks durante a prática não foram alteradas.

Os controles Por aula/Mais erros reorganizam somente os cartões de aula. Mais
erros usa contagem de erros decrescente, depois aproveitamento crescente e número
da aula como desempate. Não inventa uma medida de domínio ou a causa dos erros.
A operação preserva foco, revisões abertas, cronômetro, sessão e histórico.

Cálculos, recomendações, questões, gabaritos, feedbacks e fluxos de refazimento
permanecem os mesmos. A apresentação é compartilhada por Estudo, diário,
Hardcore, Simulado e Bate-pronto, incluindo resultados consultados pelos atalhos.

## Conferências

- `tests/test_result_scorecards.py`: pontos por resposta, legenda, limite de 12,
  totais completos, ordenação por teclado e cores neutras nos dois temas.
- `tests/test_compact_results.py`: mesmas informações e ações em todos os modos,
  revisão na largura completa, temas, acesso por teclado e larguras de tela.
- `tests/smoke.py`: fluxos existentes. A verificação dos estados 0% e 100% passou
  a conferir pontos e totais reais, substituindo o teste de larguras das barras.
- Inspeção visual nos dois temas; larguras 390, 1024, 1280, 1440 e 1920 sem
  transbordamento horizontal. Comparações no computador continuam compactas.

Validação concluída: quatro testes de indicadores/ordenação, seis de resultados
compactos e 76 de fluxos aprovados (86 no total). A comparação com o HTML anterior
confirmou os 1.000 itens de Q, os 500 de BP e `sessionAnalysis` sem alterações.

## Ajuste de cores — 20/10/2026

Por solicitação do usuário, os acertos passam a verde: pontos preenchidos de
9 px, contagem destacada e arco do resultado geral. Cartões por aula ou conceito
com 100% recebem borda verde e um pequeno reforço interno à esquerda, preservando
o fundo. Cartões com erros mantêm borda neutra. Os erros continuam em âmbar,
inclusive nos pontos vazados. Os percentuais permanecem neutros.
A mudança é compartilhada por todos os modos e não altera dados ou cálculos.

Validação do ajuste: 90 testes aprovados (4 de indicadores, 6 de resultados
compactos, 4 de exibição de siglas e 76 de fluxos), além da inspeção visual
nos temas claro e escuro. Banco de questões, Bate-pronto e trilha idênticos
à versão anterior; o diff do aplicativo se restringe à apresentação dos resultados.
