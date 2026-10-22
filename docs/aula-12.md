# Aula 12 — Mercado de Câmbio, Taxas e Cupom Cambial

Foram cruzadas as três transcrições (19, 20 e 21) com as imagens de todos os 25
slides dos dois PDFs. O conteúdo forma uma única aula, com três blocos filtráveis
na trilha, nos materiais, no comparativo e na seleção de prática.

## Distribuição e rastreabilidade

| Fonte do professor | Peso pedido | Questões | Fácil / Médio / Difícil / Hardcore | Bate-pronto |
| --- | ---: | ---: | --- | ---: |
| 19 — Mercado de Câmbio | 42,5% | 43 | 9 / 17 / 8 / 9 | 21 |
| 20 — Cupom Cambial | 15% | 15 | 3 / 6 / 3 / 3 | 8 |
| 21 — Taxas de Câmbio | 42,5% | 42 | 8 / 17 / 9 / 8 | 21 |
| Total | 100% | 100 | 20 / 40 / 20 / 20 | 50 |

O arredondamento preserva a prioridade e os totais inteiros; não representa uma
frequência oficial de prova. IDs acrescentados: **1101–1200** e **100551–100600**.
Nenhum ID, gabarito, feedback, material ou registro das onze aulas anteriores foi
reordenado ou apagado. O manifesto registra hashes e a origem de cada novo item.

## Materiais e decisões editoriais

Há três mapas de bloco e um mapa agregado, 19 tabelas, 11 diagramas, 50 flashcards
conceituais e um comparativo de 19 conceitos. As colunas do comparativo foram
adaptadas a função, mecanismo, condições, distinções e observações. Não foram
inventadas datas para preencher linhas do tempo: relações operacionais pertencem
a diagramas e tabelas.

As cadeias dos screenshots **24 e 25** aparecem tanto em **Tabelas** quanto em
**Dicas e macetes**. Identificam moeda, convenção R$/US$, fluxo de divisas e efeito
comercial condicionado. Juros internos e externos são comparados sob risco e
expectativas constantes. O uso simplificado de “prêmio de risco” como diferencial
de remuneração é separado da hipótese de aumento do risco percebido: esta pode
provocar saída de capital apesar de juros maiores. Diferença entre 10% e 3% é
**7 pontos percentuais**, e não um retorno cambial realizado de 7%.

A conferência corrigiu erros ou simplificações das fontes:

- No slide 3, IP tem referência de **US$ 100 mil**, não um milhão; o grupo de
  CTVM/DTVM e demais instituições listadas tem referência de US$ 300 mil.
  R$ 10 mil se refere a reais em espécie na operação, não a qualquer remessa.
- Sair da exceção de câmbio ocasional entre pessoas físicas não basta para
  presumir automaticamente o crime de evasão de divisas.
- ACC/ACE disponibilizam reais e se distinguem pelo embarque/documentos, não
  pela chegada física ao comprador estrangeiro. O indireto alcança a cadeia.
- Cupom do exemplo: fator 1,1365, US$ 92,78846 de ganho sobre US$ 1.000 e
  **9,28%** arredondado. 9,27% é truncamento; os números truncados da fala não
  foram usados como gabarito. Subtração simples é só aproximação.
- Swap do Banco Central: ajuste financeiro em reais, sem entrega do principal
  em dólares ou redução automática de reservas. Perspectivas do Banco Central
  e da contraparte ficam explícitas. Não se generaliza Selic a todo swap privado.
- R$ 5/US$ equivale a US$ 0,20/R$, corrigindo o exemplo invertido de convenção.
  Variações de cotações recíprocas não têm necessariamente o mesmo módulo.
- Câmbio real usa q=e×Pexterno/Pinterno; nível positivo abaixo de 1 não é negativo.
  As comparações dos exemplos são **−7,27%**, **+7,84%** e **−1,29%** contra base 1,
  sem arredondamento intermediário ou troca de nível por variação percentual.
- PTAX é referência, sem impor preço único ao cliente. O cadastro mostra sua
  descrição funcional, sem inventar uma expansão etimológica de iniciais.

As questões receberam 400 explicações específicas; os Bate-pronto, outras 100.
A segunda leitura aprofundou desafios sobre regimes, arbitragem, classificação
de fluxos e posição em swaps, substituindo casos que podiam ser resolvidos só
pelo texto. Os distratores, as dicas e os feedbacks acompanham o mesmo conceito.
Siglas seguem o renderizador comum, com adiamento pontual quando o nome informa
a resposta. O Bate-pronto continua curto, sem histórias ou contas, com algumas
lacunas de encaixe gramatical neutro e duas alternativas.

## Conferência de normas e validação

As tentativas de consulta ao Banco Central e ao Planalto foram bloqueadas pelo
proxy (403). Por isso, limites legais e detalhes metodológicos numéricos constam
em tabelas identificadas como referências dos slides, com vigência não certificada.
Não foram transformados em perguntas de número atual de norma. Os conceitos e
as contas foram reconciliados entre as fontes e revisados editorialmente.

O teste específico é `python3 tests/test_aula12.py`, acompanhado das validações
gerais de banco, alternativas, feedback, siglas e fluxos. Testes automáticos
verificam integridade e comportamento; não certificam dificuldade pedagógica ou
vigência normativa.

Validação final: **202 testes** da suíte de regressão aprovados. Após a última
leitura de cotações e concordância, passaram novamente os **11 testes da aula**,
as verificações de estrutura e tamanho e **24 testes editoriais**. A revisão
renderizada verificou as 150 questões novas, todos os materiais dos três blocos,
a preservação dos materiais anteriores, os dois temas e larguras de computador.

A bateria final de **76 fluxos de navegador** também passou, incluindo persistência,
embaralhamento, feedbacks, filtros, materiais, checkpoint diário e evolução.
