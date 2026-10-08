# Auditoria das alternativas do painel CPA

Revisão de 8 de outubro de 2026, comparada ao commit
`4c28101e8ff7054fa0ba6732e0fdec902f18fd28`. Foram lidas as 600 questões:
480 normais (níveis 0, 1 e 2) e 120 Hardcore (nível 3). O arquivo
[auditoria-alternativas.json](auditoria-alternativas.json) registra as medidas
antes/depois e os IDs alterados.

## O alerta do Claude foi confirmado

Nas questões normais, a correta era estritamente maior em **245 de 480**
casos, ou **51,0%**, contando caracteres. Esse número não inclui empates.
Contando palavras, eram 195 de 480; trata-se de outra medida.

| Indicador nas 480 questões normais | Antes | Depois |
| --- | ---: | ---: |
| Correta estritamente maior em caracteres | 245 (51,0%) | 72 (15,0%) |
| Correta estritamente maior em palavras | 195 (40,6%) | 39 (8,1%) |
| Acerto escolhendo a maior em caracteres, sorteando entre empates | 54,4% | 19,5% |
| Acerto escolhendo a menor em caracteres, sorteando entre empates | 10,8% | 22,5% |
| Correta mais de 50% maior que cada distrator, em caracteres | 130 | 1 |

O caso remanescente no último indicador é a questão 406: o nome próprio
“Da Previdência Social” é mais longo que os nomes dos outros ministérios.
Não foi acrescentado texto de preenchimento para igualar nomes reais.

Empatar no maior tamanho não significa acertar: se quatro opções tiverem o
mesmo número de palavras, escolher por tamanho ainda dá 25% de chance.
As estratégias de escolher menor, segunda menor, segunda maior e maior ficam,
respectivamente, em 22,5%, 28,5%, 29,4% e 19,5% por caracteres; por palavras,
em 26,7%, 25,4%, 25,4% e 22,6%. A revisão não transformou a menor alternativa
em uma pista dominante.

| Aula — 80 questões normais em cada uma | Correta estritamente maior antes | Depois |
| --- | ---: | ---: |
| 1 — Estrutura do SFN | 41 | 8 |
| 2 — CMN e Comoc | 45 | 11 |
| 3 — Banco Central | 35 | 12 |
| 4 — CVM | 39 | 11 |
| 5 — Seguros e previdência | 40 | 15 |
| 6 — Operadores e operações | 45 | 15 |

Nas 120 Hardcore, a correta estritamente maior em caracteres caiu de 39 para
11. A estratégia de escolher a maior, considerando os empates, caiu de 42,8%
para 19,4%. Não é necessário que todas as alternativas tenham tamanho idêntico
ou que a correta nunca seja a maior.

## O que mudou no conteúdo

Foram alteradas **319 questões**, com **1.218 textos de alternativas**,
**174 feedbacks**, 14 enunciados e ajustes nas dicas relacionadas. Os IDs,
temas, dificuldades e flags de estudo foram preservados. Os registros do
histórico continuam vinculados aos mesmos IDs, sem apagar respostas anteriores.

A revisão tratou de quatro problemas recorrentes:

- A correta continha definição e justificativa; os distratores traziam só um
  termo. As justificativas ficam no feedback, e as alternativas usam redação
  comparável.
- Uma composição completa aparecia apenas na correta. Por exemplo, a quantidade
  de membros do BACEN vinha com presidente e diretores somente em uma opção.
  As quatro escolhas agora usam o mesmo formato, e a composição é explicada
  depois da resposta.
- Distratores destoavam do conceito. No bloco da CVM, perguntas de atribuições
  passaram a comparar blocos da própria CVM, em vez de inserir emissão de moeda
  ou meta de inflação como respostas distantes. Em cooperativas, foram usadas
  trocas entre singular, central e confederação.
- Opções de listas ou associações misturavam quantidade de itens, tipos de
  entidade ou ordem de resposta. As listas passaram a ter formatos paralelos
  e os feedbacks identificam o item ou a posição que invalida a combinação.

Correções específicas que exigiram mais que abreviar ou ampliar a redação:

| Questão | Problema e correção |
| --- | --- |
| 62 | “Fim do segundo ano” era muito próximo de “início do terceiro”. O distrator agora diz início do segundo ano. |
| 203 | A ordem dos três segmentos não estava explícita. O enunciado agora exige a ordem e as opções comparam somente operadores. |
| 263 | Três votos também constituem maioria; o enunciado agora pede o **mínimo** de votos. |
| 278 e 295 | Meta de inflação foi distinguida de meta da Selic; atribuições foram identificadas por itens e combinações. |
| 388 | A definição de contrato de investimento coletivo e seus feedbacks passaram a incluir a origem dos rendimentos no esforço do empreendedor ou de terceiros. |
| 414 e 427 | O texto explicita que pergunta a frequência ou presença mínima prevista, evitando tratar uma exigência superior como o mínimo pedido. |
| 485 | A composição do CNPC é comparada por grupos de representação, sem uma lista enorme apenas na correta. |
| 520 | O atendimento a associados foi qualificado pelas exceções legais para certos serviços a não associados. |
| 528, 574 e 597 | A afirmação de um CNPJ independente por carteira foi removida. As perguntas distinguem contabilidade separada por carteira e balanço da instituição. |
| 578–580 | A amplitude das modalidades de cooperativa segue a classificação da aula; autorização ampla não é permissão irrestrita. A restrição foi expressa como captação de depósitos. |
| 599 | O feedback distingue 51% de 50% mais uma ação: em mil ações, são 510 e 501, respectivamente. |

Seis trechos de apoio da aula 6 foram alinhados às questões, incluindo resumo,
tabela e flashcards sobre contabilidade de carteiras, atendimento aos associados
e cooperativas de capital e empréstimo.

## Outra pista identificada: posição da resposta

O embaralhamento antigo usava `sort(() => Math.random() - .5)`. Esse método
não dá a mesma chance às permutações. Em uma reprodução com 100 mil execuções
no motor V8 e semente fixa, a correta original ficou na primeira posição em
35,96% dos casos e na última em 31,26%. Isso é uma reprodução do algoritmo,
não uma medida do histórico de usuários.

Foi substituído por Fisher–Yates. Um teste percorre os 24 caminhos de sorteio
para quatro alternativas, obtém as 24 permutações e confirma seis aparições da
correta em cada posição. O mesmo método é usado na seleção de questões e na
ajuda de eliminar alternativas. O índice de origem continua acompanhando a opção
para preservar o vínculo com o feedback.

## Validação e limites

Foram aprovados 28 testes: seis de estrutura, cinco da auditoria e 17 de navegador.
A verificação de navegador responde as quatro opções de cada uma das 600 questões,
totalizando 2.400 verificações da associação entre opção, gabarito e feedback.
Também confere persistência do histórico, revisão de erros, ajudas, filtros,
prática diária, Hardcore e ausência de feedback imediato nos simulados.

Para reproduzir:

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/smoke.py
```

O GitHub Actions verifica o conteúdo e a distribuição de tamanhos. As orientações
de autoria em `AGENTS.md` exigem distratores plausíveis, redação paralela, uma única
resposta defensável e revisão dos feedbacks e do material ao mudar uma opção.
Os limites estatísticos são alertas de revisão, não quotas de tamanho.

**Limite da conferência normativa:** esta é uma revisão pedagógica e de coerência
do banco fornecido, e não uma auditoria jurídica de vigência de todas as normas.
O ambiente recusou acesso externo aos sites do Banco Central e do Planalto
(HTTP 403), impedindo consulta independente às versões atuais. As classificações,
composições e periodicidades oriundas das aulas continuam precisando de conferência
contra o material oficial da prova pretendida. Os testes não demonstram verdade
jurídica nem eliminam a possibilidade de ambiguidades restantes.

Referências oficiais para essa conferência, sem afirmar consulta realizada nesta revisão:

- [Banco Central — bancos múltiplos](https://www.bcb.gov.br/estabilidadefinanceira/bancosmultiplos)
- [Banco Central — cooperativas de crédito](https://www.bcb.gov.br/estabilidadefinanceira/coopcred)
- [Lei Complementar 179 — autonomia do Banco Central](https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp179.htm)
- [Lei 6.385 — mercado de valores mobiliários e CVM](https://www.planalto.gov.br/ccivil_03/leis/l6385.htm)
