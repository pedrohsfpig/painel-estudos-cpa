# Revisão de contexto das questões

A solicitação foi revisar todo o banco para eliminar perguntas que dependam de
uma aula, do professor ou dos slides e esclarecer enunciados vagos. Questões
claras foram preservadas. O usuário dispensou a planilha Excel; o resultado é
informado no chat. O registro técnico por ID fica em
[revisao-enunciados-autossuficientes.json](revisao-enunciados-autossuficientes.json).

## Resultado

- **900 questões revisadas** nas nove aulas, incluindo as disponíveis nos simulados.
- **295 questões alteradas**, sem contar uma mesma questão novamente por cada campo.
- **182 enunciados ajustados** para remover referências externas ou definir o contexto.
- **113 outras questões** com ajustes somente em dicas/explicações/feedbacks.
- **605 questões preservadas integralmente**.

| Aula | Enunciados alterados | Só campos de apoio | Total alterado | Preservadas |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2 | 17 | 19 | 81 |
| 2 | 13 | 12 | 25 | 75 |
| 3 | 18 | 19 | 37 | 63 |
| 4 | 21 | 22 | 43 | 57 |
| 5 | 9 | 16 | 25 | 75 |
| 6 | 15 | 10 | 25 | 75 |
| 7 | 30 | 10 | 40 | 60 |
| 8 | 31 | 2 | 33 | 67 |
| 9 | 43 | 5 | 48 | 52 |
| Total | 182 | 113 | 295 | 605 |

Por dificuldade, as questões com alguma alteração são: **52 fáceis, 126 médias,
57 difíceis e 60 Hardcore**. Das 295, **135 também estão disponíveis em Simulado**;
100 são normais de Estudo que já não integravam o Simulado; 60 são Hardcore.
Estudo continua compartilhando seu banco com o Simulado, respeitadas as exclusões
já existentes. Nenhuma flag foi mudada para esconder um problema de redação.

As contagens por campo são sobrepostas: 182 enunciados, 71 explicações gerais,
40 dicas e 152 conjuntos de feedbacks. Somente duas questões receberam alterações
no texto das alternativas: 732 (avaliação do funding SCD, sem remeter ao material)
e 788 (exigência de conta no STR, sem remeter à tabela). A alternativa correta
continua no índice original zero e tem o mesmo conteúdo conceitual.

## O que foi encontrado e corrigido

1. **Referências didáticas externas:** “segundo a aula”, “no slide”, “no conteúdo
   enviado”, “conforme o material” e “pelo mnemônico da aula”. Foram substituídas
   pelo objeto financeiro ou pelo requisito que a questão realmente avalia.
2. **Dependência do título da aula:** perguntas que pediam só “qual associação”,
   “os diretores” ou “a meta” sem identificar o órgão ou a política. A instituição,
   o objeto e a perspectiva da operação agora constam do próprio enunciado.
3. **Classificações de apoio tratadas como conteúdo pressuposto:** perguntas sobre
   “blocos” da CVM agora pedem o objetivo ou a função da medida descrita.
4. **Conceitos vagos sem contexto suficiente:** vínculos ANBIMA, contas de liquidação
   e modalidades de garantia recebem o âmbito necessário. Na questão 808,
   “vinculante” é explicado como cumprimento obrigatório, sem citar a resposta.
5. **Explicações que mandavam lembrar o professor:** dicas e feedbacks passaram a
   justificar conceitos, condições e competências, inclusive nas revisões finais
   do Simulado. A origem e as limitações normativas continuam nos relatórios das
   fontes, sem serem perguntas sobre o que um professor disse.

A correção não consiste em apagar a expressão “na aula” e deixar uma lacuna.
Foram preservadas as condições necessárias à resposta, sem expandir uma sigla
quando sua expansão entregaria a função perguntada. SILOC e DIM, por exemplo,
são contextualizados por atividade e instituição; sua definição continua sendo
conhecimento a recordar. Nos cálculos, os dados do caso permanecem e a regra
avaliada não é fornecida como mera instrução de soma.

## Exemplo do usuário — questão 808

Antes:

> Qual fonte da ANBIMA tem caráter vinculante no âmbito descrito pela aula?

Depois:

> Entre as opções abaixo, qual instrumento de autorregulação da ANBIMA tem caráter
> vinculante, isto é, estabelece determinações de cumprimento obrigatório para os
> participantes aos quais se aplica?

A resposta permanece **Deliberação**. O feedback de **Programa educacional**
esclarece que capacitar e exigir conduta ética não torna o programa a fonte
que formaliza a determinação de autorregulação pedida.

Na questão 880, as afirmações avaliam instituição, produto e limite por
beneficiário, em vez de perguntar quais frases “têm apoio no material”. O
conjunto correto continua no mesmo índice e as quatro explicações foram alinhadas.

## Preservação e alcance

Os 900 IDs, ordem, tema, aula, dificuldade e inclusão/exclusão de Simulado
permanecem iguais. AL, MAT, quadros, lógica de seleção, renderização, ajudas,
cronômetros, armazenamento e indicadores não foram alterados. Esta revisão
não recalcula acertos antigos nem apaga sessões de `cpaH` ou `cpaDaily`.

Os relatórios originais das aulas 8 e 9 são registros históricos da autoria.
`tests/question_revision.py` valida o hash atual, reconstrói os campos anteriores
pelo manifesto e os compara à autoria, mantendo a cadeia verificável sem
sobrescrever as fontes originais.

A revisão trata de redação e contexto. Não representa nova certificação normativa
independente nem medição científica de dificuldade; continuam válidas as
limitações de acesso registradas nos relatórios originais.

## Verificações

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/test_question_design.py
python3 tests/test_aula8.py
python3 tests/test_aula9.py
python3 tests/test_question_context.py
python3 tests/smoke.py
```

Os testes novos verificam referências externas em todos os campos das questões,
contagens reais, preservação de metadados, proveniência e exemplos de contexto.
O navegador confere as perguntas corrigidas, a resposta incorreta mostrada pelo
usuário, quatro feedbacks vinculados após embaralhamento, ausência de feedback
imediato em Simulado, romanos, histórico anterior e os dois temas no computador.
