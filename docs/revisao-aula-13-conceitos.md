# Revisão conceitual de riscos e progresso por questão — 28/10/2026

Pedido: corrigir questões que repetiam os números dos slides ou cobravam apenas
operações aritméticas, explicitar o cenário de juros quando necessário e manter
coerência entre enunciado, alternativas, dicas e feedbacks.

As 50 questões da primeira aula interna foram revisadas. Dezesseis foram
reformuladas (1206, 1207, 1222–1224, 1227, 1231–1232, 1239–1243, 1245, 1247 e
1250), preservando IDs, temas, níveis, elegibilidade e os quatro feedbacks.
Quatro flashcards numéricos foram convertidos em revisão de conceitos. Os
exemplos dos slides permanecem nos mapas, tabelas, diagramas, resumos e dicas.
As doze aulas anteriores e o Bate-pronto foram preservados.

- Spread: distinguir intermediação de remuneração relativa, investigar crédito
  e liquidez e separar variação da referência de deterioração do emissor.
- Mercado: reconhecer desvalorização antes da venda. Preço de ação, sozinho,
  não identifica movimento dos juros; o cenário de lucro foi descrito.
- Prefixados: alta/queda da taxa de desconto é explícita; manter crédito, prazo
  e fluxos permite avaliar o efeito sobre preço. Marcação não altera o contrato.
- Comparação de valores: interpretar exposição de mercado mesmo com preço
  acima do custo, sem pedir uma simples diferença entre dois números.
- Fluxo e caixa: preço de avaliação não é cupom, resgate ou entrada de caixa.
- Caso integrado Hardcore: classificar necessidade de caixa, reprecificação por
  juros e desconto adicional por pouca demanda, em vez de decompor uma soma.

Valores novos conferidos com aritmética decimal: 12.600/1,05 = 12.000 e
12.600/1,12 = 11.250; 9.450/1,08 = 8.750 e 9.450/1,05 = 9.000. Os enunciados
usam esses valores para interpretar os mecanismos, sem exigir essas contas.
O manifesto JSON registra os estados anterior/final e seus hashes; os relatórios
de autoria originais permanecem intactos. Os testes reconstroem a autoria antes
de comparar seus hashes, mantendo a cadeia de revisão verificável.

A questão 1250 agora aborda explicitamente as três dimensões. Por isso, também
é pertinente ao conjunto Liquidez, que passa de 13 para 14 questões únicas. Seus
subconceitos continuam dentro do conjunto principal; não se conserva a contagem
antiga excluindo uma questão agora relevante.

## Progresso e seleção de quantidade

A barra da sessão mantém altura de 6 px e a cor azul do tema, com um segmento
por questão em Estudo, Hardcore, Simulado, Bate-pronto e checkpoint diário.
O preenchimento segue o ID respondido, incluindo navegação fora de ordem:
pular/revisitar não preenche outro segmento nem grava uma tentativa adicional.
Cor de acerto/erro continua no feedback e no navegador de questões, como antes.
O espaçamento adapta-se a sessões longas e telas pequenas sem alargar a página.

Os botões de quantidade passam a 5, 10, 15, 20 e 30 em todos os modos da seleção.
A quantidade personalizada do Bate-pronto permanece disponível. Checkpoint diário
continua com 20 e o estudo por conteúdo continua usando todas as questões
pertinentes: os novos botões não limitam esses conjuntos ou a revisão de erros.

Validação específica em `tests/test_risk_concepts_and_progress.py`, regressões da
aula 13, vínculos por conceito, navegação, Bate-pronto, layout e os checks gerais
de conteúdo. A validação financeira confere os dados dos novos cenários; os testes
automáticos não substituem a revisão editorial das alternativas.
