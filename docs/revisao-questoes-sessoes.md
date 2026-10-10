# Revisão das questões e feedback da sessão

Revisão de 10/10/2026 sobre as **700 questões existentes**, incluindo o banco
usado por Estudo, Hardcore, estudo diário, revisão de erros e Simulado.
Os simulados selecionam do mesmo `Q`; não há um segundo banco independente.

Foram lidos enunciado, resposta e distratores de cada questão. Nas reformulações,
também foram revistos justificativa geral, dica e os quatro feedbacks. O registro
[por ID](revisao-questoes-sessoes.json) distingue conteúdo reformulado, ajuste
somente de formatação e conteúdo preservado, com hashes antes/depois.

| Aula | Conteúdo reformulado | Somente formatação | Preservadas |
| --- | ---: | ---: | ---: |
| 1 — SFN | 24 | 5 | 71 |
| 2 — CMN | 27 | 2 | 71 |
| 3 — BACEN | 22 | 2 | 76 |
| 4 — CVM | 25 | 4 | 71 |
| 5 — Seguros e previdência | 29 | 1 | 70 |
| 6 — Operadores Monetários | 25 | 1 | 74 |
| 7 — Operadores Não Monetários | 15 | 1 | 84 |
| **Total** | **167** | **16** | **517** |

Das 167 reformulações, **121 são Hardcore**, 40 Difícil, 4 Médio e 2 Fácil.
A distribuição foi preservada em cada aula: **20 Fácil, 40 Médio, 20 Difícil,
20 Hardcore**. Os IDs e os indicadores de elegibilidade para simulados não
mudaram. O histórico não é apagado nem reclassificado retroativamente. Resumos,
dicas, pegadinhas, mapas, tabelas, diagramas e flashcards não foram modificados.

## O que foi identificado e corrigido

- **Regra entregue no enunciado:** o CNPC (#496) fornecia dois anos e uma
  recondução, depois pedia uma soma. Agora avalia limite já utilizado,
  autoridade designante e presidência. Não informa a regra cobrada.
- **Contagem de dados fornecidos:** Comoc (#105), renovação da CVM (#400),
  pirâmide cooperativa (#595–596) e consórcio (#671) tinham operações aritméticas
  elementares como exigência principal. Agora distinguem estrutura, permissão,
  competência e procedimento. A hierarquia de competências é necessária.
- **Percentuais sem conhecimento financeiro:** resseguro (#698) pedia apenas
  percentuais sucessivos. Agora distingue resseguro de retrocessão e a obrigação
  da seguradora perante o cliente.
- **Hardcore com identificação única ou associações elementares:** as variantes
  foram reformuladas com análise de condições, perspectivas contratuais,
  competências próximas, limites ou exceções. Trocar um nome ou adicionar
  personagens não foi usado como critério de elevar dificuldade.
- **Contas de spread como único desafio:** questões #43, #88, #211 e #214
  agora exigem distinguir margem de juros, perdas, custos e resultado, inclusive
  quando faltam dados para ordenar o lucro. Contas úteis continuam no banco.
- **Ambiguidade de controle cooperativo:** “50% mais uma ação” (#599) pode
  atingir 51% dependendo do número de ações. O caso agora usa 5.001 de 10.000
  votos e exige verificar também a carteira comercial do múltiplo cooperativo.
- **Classificação apenas pelo prazo:** #210 e variantes separam emissão de
  debêntures de financiamento bancário, que também pode ter longo prazo.
- **Conteúdo fora do objetivo da avaliação:** #195 perguntava o aproveitamento
  recomendado pelo professor; agora testa liquidez, mantendo o ID e o nível.
- **Repetição de palavras como pista:** #572 e #669 passaram a discriminar a
  operação ou o papel institucional, em vez de reproduzir o termo da pergunta.

Questões básicas que pedem reconhecimento de conceito continuam básicas. As
preservadas não foram artificialmente alongadas. O critério do Hardcore é exigir
conhecimento integrado; a dificuldade é julgamento editorial, não certificação
por contagem de palavras ou validação estatística com estudantes.

Os conceitos utilizados vieram do conteúdo já cadastrado e das fontes de aula
do projeto. Esta entrega não fez uma nova certificação das normas vigentes.

## Padrão de romanos

Os **96 enunciados com listas em romanos** apresentam introdução, uma afirmação
por linha e pergunta final separada quando existente. Referências explícitas
nas alternativas e feedbacks foram normalizadas para maiúsculas.

`questionStemHtml` é usado tanto em `ques` quanto em `qa`: Estudo, Hardcore,
Simulado, resultado e revisão de erros compartilham o padrão. Aceita marcadores
inline legados e minúsculos em conteúdo futuro, mas a autoria deve usar novas
linhas. Uma menção isolada a uma fase “II” não vira lista. Todo texto é escapado.

Na reformulação das listas, a posição das afirmações verdadeiras também variou;
as duas primeiras não são sistematicamente verdadeiras. As alternativas mantêm
ordem editorial e o embaralhamento de apresentação conserva seus feedbacks.

## Resultado de todos os modos

O resultado agora mostra:

1. Gráfico de acertos e erros, percentual e números da sessão.
2. Aulas praticadas, assuntos com erros e tempo total/médio de resposta.
3. Barras de acertos/erros por aula e por dificuldade, com denominadores próprios.
4. Até três prioridades por aula/assunto, ordenadas pelos erros reais. Os demais
   assuntos continuam disponíveis na revisão de todas as questões erradas.
5. Agrupamentos de assunto com pelo menos dois erros, com contagem visível.
   Trata-se de repetição observada no conjunto, sem inferência da causa do erro.
6. Recomendações de comparação e revisão, com atalho para o resumo da aula
   e para o bloco correspondente da aula 7 quando aplicável.
7. Botão para refazer somente os erros da sessão em Estudo ou Hardcore.
8. Revisão com a escolha e a resposta correta. Nos simulados, somente a
   explicação geral; nos outros modos, os quatro feedbacks correspondentes.

`sessionAnalysis` usa `qz.rev`, sem contaminar a análise com `H`. Consultar uma
aula mantém o resultado acessível por Praticar. Uma nova prática não apaga o
histórico. O cronômetro para ao registrar a última resposta, antes da leitura
de seu feedback. Ao chegar ao resultado pela primeira vez, a página volta ao topo.

O painel indica limite de amostra; tudo certo não gera áreas fracas fictícias.
Sem respostas, a apresentação não calcula médias inválidas. A visualização foi
conferida em 1024, 1280, 1440 e 1920 pixels e nos dois temas.

## Verificação reproduzível

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/test_question_design.py
python3 tests/smoke.py
```

São 6 testes de banco, 5 de qualidade das alternativas, 6 regressões de autoria
e 47 testes de navegador. O navegador também percorre todas as 700 questões
com cada uma das quatro escolhas, verificando o vínculo dos feedbacks.

A auditoria de tamanho verifica todas as posições, não só a maior alternativa;
permanece um alerta editorial, sem preenchimento artificial dos distratores.
Os padrões permanentes estão em [AGENTS.md](../AGENTS.md).
