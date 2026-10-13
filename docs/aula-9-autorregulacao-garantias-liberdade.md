# Aula 9 — Autorregulação, Garantias e Liberdade Econômica

A aula reúne os 15 slides de `Screenshot_1 (2).pdf` e as três partes da
transcrição: Autorreguladores, FGC e FGCoop, Lei da Liberdade Econômica.
Cada página foi lida e cruzada com a fala. A transcrição complementa trechos
encobertos pela imagem do professor. A cobertura por slide e a origem de cada
questão estão em [aula-9-cobertura.json](aula-9-cobertura.json).

## Distribuição solicitada

Mantêm-se 100 questões por aula, com 80 normais e 20 Hardcore.

| Foco | Fácil | Médio | Difícil | Hardcore | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| ANBIMA | 10 | 20 | 10 | 10 | 50 |
| FGC e FGCoop | 8 | 16 | 8 | 8 | 40 |
| Liberdade Econômica | 2 | 4 | 2 | 2 | 10 |
| Total | 20 | 40 | 20 | 20 | 100 |

A prioridade é a escolha de estudo do usuário, sem afirmar frequência oficial
na prova. APIMEC, Planejar e ANCORD permanecem integralmente nos materiais; nas
questões, aparecem em comparações que distinguem seus requisitos e papéis dos
vínculos ANBIMA. Não recebem questões isoladas que consumam a quota de ANBIMA.

Os novos IDs são **801–900**. Os 800 anteriores permanecem com todos os campos
inalterados. As questões normais integram Estudo/Simulado e as questões Hardcore
permanecem no nível próprio. O estudo diário continua com 20 perguntas e níveis
5/10/5, agora abrangendo as nove aulas; a sessão existente não é reiniciada.

Toda alternativa tem explicação própria, vinculada à posição de origem, mesmo
com embaralhamento e ajudas. Simulados conservam a ausência de feedback imediato.
As afirmações em romanos têm linhas separadas e maiúsculas no renderizador comum.
Hardcore combina vínculos, fontes, competências, bases elegíveis ou limites;
enunciados não fornecem a regra numérica necessária para uma simples soma.

## Leitura e materiais

Há três filtros compartilhados pela trilha e pelos materiais:

1. Autorreguladores: ANBIMA, APIMEC, Planejar e ANCORD.
2. FGC e FGCoop: natureza, proteção, limites, produtos, titulares e casos.
3. Liberdade Econômica: fundamentos, baixo risco, autonomia e condições.

Resumo concentra conceitos; dicas são associações e métodos de leitura;
pegadinhas distinguem ambiguidades e condições. Seções abertas permanecem abertas
na troca de bloco. Os controles conservam os contornos azul/lilás/verde.

O quadro geral tem sete itens em linhas, identificando quatro associações,
dois garantidores e uma lei, sem confundir suas naturezas. As colunas comparam
função, âmbito, vínculo, instrumentos, limites e observações. As tabelas menores
comparam entidades em colunas e aspectos em linhas, com texto centralizado e
cores constantes. A estrutura principal dos mapas permanece azul.

Os três mapas, oito diagramas, onze tabelas e **54 flashcards** cobrem os slides.
Diagramas representam relações reais ou passos de análise; não são cronologias
artificiais. Prazos e referências têm seus contextos: quatro anos é janela da
garantia, não vencimento de um CDB. O bloco de autorregulação não ganha datas
inventadas. Flashcards são perguntas explícitas, com a face de resposta distinta.
Negativas reais usam vermelho somente nos materiais de contexto; condições usam
lilás. Questões e flashcards não recebem a marcação automática de negativas.

## Divergências e limites da conferência

- **DPGE:** o slide 10 apresenta `R$ 40k`; o slide detalhado 9 e a fala indicam
  **R$ 40 milhões**. A unidade foi corrigida, e a inconsistência permanece
  registrada na tabela de modalidades e no relatório.
- **Conta conjunta:** `R50.000` na fala transcrita foi conferido com os exemplos
  e o slide: teto de R$ 250 mil da conta, dividido pelos titulares, respeitado o
  saldo e os demais limites do titular.
- Nomes/siglas e palavras de reconhecimento foram normalizados: ANBIMA,
  valores mobiliários, FGCoop e saldo existente. CNPI/T/P foram conferidos no
  slide. Quantidades de participantes e voluntários são referências da fonte,
  sem serem tratadas como contagens atuais ou perguntas de memorização.
- Compromissadas não são apresentadas como cobertura universal. O recorte FGCoop
  mantém o lastro de empresa ligada e emissão após 8/3/2012 do slide; a data não
  vira gabarito numérico de regra vigente.
- O material não detalha para o FGCoop o teto global de quatro anos nem a
  garantia especial do FGC. Não se transferem automaticamente essas regras.
- Taxas FGC de 0,01%/0,03% e a menção incompleta de 0,02% ficam identificadas como
  **referências da aula**, sem gabaritos numéricos de contribuição vigente.
- AAI é identificado como nome usado pela fonte, com assessor de investimento
  na leitura. Referências específicas RPPS, AGRO 100 e CCA foram preservadas,
  sem certificar vigência nem criar questões isoladas dessas certificações.
- Digitalização pressupõe requisitos de validade/autenticidade/integridade;
  baixo risco não dispensa normas ambientais, trabalhistas ou de segurança.

A consulta a ANBIMA, FGC, FGCoop e Planalto retornou bloqueio do proxy
(`Tunnel connection failed: 403 Forbidden`). A entrega confere as fontes
fornecidas, **sem certificação normativa independente**. Os testes verificam
estrutura, proporções, regressões e funcionamento, não certificam dificuldade
pedagógica ou vigência jurídica.

## Verificações

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/test_question_design.py
python3 tests/test_aula8.py
python3 tests/test_aula9.py
python3 tests/smoke.py
```

O contrato da aula 9 verifica divisão 50/40/10 em cada nível, quatro explicações,
proveniência e cobertura dos 15 slides, IDs antigos, blocos agregados e referências
não certificadas. O navegador confere texto integral dos materiais, filtros e
seções abertas, feedback em Estudo/Hardcore, ausência em Simulado, prática e
histórico, nove aulas no checkpoint e dois temas em quatro larguras de computador.
