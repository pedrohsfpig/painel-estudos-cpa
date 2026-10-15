# Siglas nas questões e revisão de feedbacks numéricos

A apresentação é compartilhada por Estudo, Hardcore, Simulado, Estudo de hoje,
Bate-pronto e revisões. `questionDisplay` formata os textos para exibição:

- Primeira ocorrência de uma sigla no enunciado: sigla seguida do nome entre
  parênteses, com tamanho secundário legível.
- Alternativas: expansão quando o conceito não apareceu no enunciado. A mesma
  regra vale para cada opção, independente de seu gabarito e posição embaralhada.
- BC/BCB/BACEN e formas plurais compartilham conceitos, evitando repetições.
  Definições já existentes são reconhecidas, inclusive no formato Nome (SIGLA).
- Perguntas que cobram o significado da sigla, ou a associação inversa, mostram
  as expansões somente depois da resposta. Preferência confirmada pelo usuário.
  A primeira entrega incluía Q753 e BP100379; essas perguntas foram depois
  reformuladas em `docs/revisao-pistas-siglas.md`. No simulado, a consulta fica na revisão
  após finalizar; nenhum feedback imediato foi acrescentado.
- Pix é marca, não sigla; romanos, valores e letras de alternativas não recebem
  definições. TR tem significado conforme o contexto da aula, sem substituir
  Taxa Referencial por entidade registradora fora da aula de infraestruturas.
- A transformação preserva os textos originais de Q/BP, escolhas gravadas,
  gabaritos, vínculos dos feedbacks e IDs. Futuras questões usam o renderizador;
  novas siglas devem ser cadastradas no glossário, nunca expandidas por adivinhação.

O glossário está em `docs/siglas-questoes.json`, espelhado em
`QUESTION_ACRONYMS`. Na primeira entrega, a apresentação mudou em 856 questões dos dois bancos;
1.350 registros passaram pela verificação de renderização. Nomes por extenso
podem tornar algumas alternativas mais longas; não se alteram nomes oficiais
nem se preenchem opções artificialmente para compensar esse efeito.

## Correção solicitada a partir do DPGE

O feedback “Quarenta mil troca a unidade e reduz o valor em mil vezes” descrevia
corretamente a diferença aritmética, mas não ensinava a garantia do produto.
Foi substituído por explicação da garantia especial do FGC, com teto de R$ 40
milhões por titular e instituição/conglomerado, distinta da garantia ordinária.
O gabarito e os valores das alternativas foram mantidos.

A triagem percorreu os textos dos 900 registros Q e 450 BP para localizar
referências a números, limites, prazos e aritmética; os candidatos foram lidos no
contexto do enunciado e de cada alternativa. Não foram retirados cálculos que
aplicam regras financeiras, como limites conjuntos, janela de garantias ou fundo
de liquidez. Houve revisão editorial dos casos insuficientes, sem alegar nova
certificação normativa.

Alterações: **9 feedbacks em 5 questões Q** e **38 feedbacks em 20 Bate-pronto**:
**47 feedbacks em 25 questões**, sem alteração de enunciados, opções ou níveis.

- Prazos: antecedência da meta versus janela de apuração; vigência e mínimo.
- Composição e mandatos: total versus diretores, mandato versus recondução,
  quórum versus assentos e cargos de órgãos diferentes.
- Penalidades e compulsórios: objeto da sanção e base do teto, sem tratar o
  limite máximo como percentual obrigatório ou duração universal.
- Garantias: ordinária versus especial; teto por instituição versus janela;
  não transferir automaticamente regras do FGC ao FGCoop.
- BP100249: removido parágrafo sobre representação no CNPC que não explicava
  autorização de fusão pela Previc. As duas opções agora distinguem norma geral
  de autorização individual da autarquia supervisora.

Os IDs e campos antes/depois ficam em `docs/revisao-feedbacks-numericos.json`.
A cadeia de testes reconstrói as revisões anteriores sem alterar seus relatórios.

## Validação

`tests/test_acronyms_and_numeric_feedback.py` verifica casos concretos,
exceções antes/depois da resposta, plurais/aliases, definições existentes,
escape de HTML, contexto de TR, histórico com textos originais, embaralhamento,
temas e larguras de computador. Os testes gerais continuam conferindo todos os
feedbacks por índice de origem, simulados sem explicação imediata, distribuição,
retomada e armazenamento. Esses testes verificam comportamento e regressões;
a avaliação didática depende também da leitura editorial.
