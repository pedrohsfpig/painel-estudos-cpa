# Aula 11 — Macroeconomia, Atividade e Política Fiscal

A aula reúne as transcrições das aulas 16, 18 e 22 e as 14 páginas do PDF
`Screenshot_1 (4).pdf`. Slides e fala foram conferidos em conjunto. Os trechos
visualmente encobertos foram complementados pela transcrição quando possível.

| Origem | Bloco | Questões | Fácil / Médio / Difícil / Hardcore | Bate-pronto |
| --- | --- | ---: | --- | ---: |
| Aula 16 | Fluxo circular da renda | 10 | 2 / 4 / 2 / 2 | 5 |
| Aula 18 | Política fiscal | 30 | 6 / 12 / 6 / 6 | 15 |
| Aula 22 | Indicadores econômicos | 60 | 12 / 24 / 12 / 12 | 30 |
| Total | | 100 | 20 / 40 / 20 / 20 | 50 |

A distribuição atende à prioridade solicitada pelo usuário, inclusive dentro de
cada dificuldade; não é previsão oficial da incidência na prova. O conjunto normal
mantém 80 questões e o Hardcore 20, sem aumentar a quantidade em relação às outras
aulas. Bate-pronto permanece conceitual, breve e com duas opções.

## Materiais e navegação

Os três blocos compartilham os filtros da trilha e dos materiais, preservando as
seções abertas. A prática mantém seu filtro separado. O material inclui resumo,
dicas, pegadinhas, números pertinentes, mapas, dez diagramas, oito tabelas, dois
painéis históricos e 50 flashcards. Fórmulas, circuitos e funções comparadas não
são artificialmente transformados em cronologia.

O quadro geral possui 14 linhas: dois circuitos, cinco instrumentos/orientações
fiscais e sete indicadores/referências. As colunas foram adaptadas a esse objeto:
função, âmbito/responsável, componentes, distinção e observações. Há filtro por
bloco e ampliação; os conceitos ficam nas linhas. As tabelas menores mantêm os
aspectos nas linhas e as entidades/conceitos comparados nas colunas, com células
centralizadas. Os mapas preservam a estrutura principal azul; outras cores
identificam comparações internas.

## Divergências e critérios de conteúdo

- A fala inverte estoque e fluxo. **Déficit é fluxo do período; dívida é estoque
  em uma data.** Resultado primário exclui juros; o nominal os considera.
- A fonte chama toda remuneração dos fatores de EOB e depois soma salários.
  A renda foi organizada sem repetição: remunerações de empregados, excedente
  operacional bruto, rendimento misto e impostos líquidos de subsídios nas bases
  pertinentes. Valor adicionado não é soma dos faturamentos intermediários.
- PIB é fluxo de produção, não estoque de riqueza. Per capita é média; preços,
  distribuição e outros fatores limitam inferências sobre volume ou bem-estar.
- Importações retiram produção externa já incluída no gasto; importar máquina
  pode ampliar simultaneamente investimento e importações. Transferência não
  é compra direta de produção; o consumo posterior do benefício tem registro próprio.
- A EC 95/2016 é tratada como antigo teto histórico. O regime da LC 200/2023 a
  substituiu. Não foram criados gabaritos sobre o antigo prazo de 20 anos como se
  ainda fosse a regra atual nem sobre novos limites fiscais numéricos vigentes.
- A STN tem gestão financeira e da dívida federal. Política fiscal envolve
  competências governamentais de orçamento e tributos; não foi atribuída ao
  Tesouro uma competência exclusiva sobre toda receita ou a definição da Selic.
- IGP-M usa janela de 21 do mês anterior a 20 do mês de referência e pesos
  60/30/10. IPCA usa população e metodologia distintas; mês de referência não
  significa que todos os meses tenham 30 dias. Cestas individuais podem divergir.
- Meta Selic, taxa Over e sistema de títulos são separados. **O sistema Selic não
  atua como contraparte central.** DI é referência de operações elegíveis de um
  dia útil; não determina emissor, cobertura de garantia nem todo preço de crédito.
- TR deriva da TBF com redutor, não é sinônimo de inflação. Sua relação de cálculo
  é apresentada com taxas compatíveis de período e formato. Não foram inventadas
  regras completas atuais de poupança ou FGTS a partir de menções resumidas.
- TLP combina parcela real de contratação e IPCA. A implementação desde 2018
  não foi apresentada como renomeação ou migração automática de todos os contratos
  antigos. **7,61% é ilustração, não percentual universal nem taxa atual validada.**

## Questões e siglas

Os 100 enunciados principais e 50 Bate-pronto têm feedback próprio por alternativa:
400 explicações no banco principal e 100 no conceitual. Houve revisão de contexto,
relação pergunta–opções, pistas gramaticais, tamanho e natureza dos distratores.
Desafios integram condições; os cálculos usados exigem classificação econômica
ou metodologia do indicador, sem fornecer no enunciado a regra que resolve o item.
As questões com afirmações usam romanos maiúsculos, em linhas separadas.

Foram acrescentados 15 registros de siglas. As 150 questões passaram por censo
renderizado: nenhuma definição não adiada ficou ausente. Sete itens adiam as
expansões porque elas resolveriam o fato pedido; os flashcards seguem a mesma
preferência e proteção. Bancos antigos, IDs, gabaritos e feedbacks foram preservados.
Os novos IDs são **1001–1100** e **100501–100550**.

## Limite da conferência e validação

As consultas a Planalto, IBGE e FGV foram bloqueadas pelo proxy (403 na conexão).
A entrega não declara certificação normativa atual. As decisões acima distinguem
reconciliação das fontes, conceitos estáveis e referências históricas, evitando
transformar números potencialmente desatualizados em gabaritos de norma vigente.
O manifesto `aula-11-cobertura.json` registra fontes, páginas, hashes, proporções,
normalizações e preservação dos 1.000 itens e 500 Bate-pronto anteriores.

Testes específicos: `python3 tests/test_aula11.py`. As regressões históricas foram
adaptadas para preservar os recortes originais e aceitar uma nova aula, incluindo
20 questões no checkpoint distribuídas pelas 11 aulas com 5/10/5 de dificuldade.
Os testes avaliam estrutura e comportamento; a revisão editorial não é substituída
por uma aprovação automática de autoria ou dificuldade.

Validação concluída: **125 testes** da suíte `test_*.py` e **76 testes** de fluxos
aprovados. Após a segunda leitura, oito feedbacks foram enriquecidos e a contratação
de pintura foi explicitada para distingui-la de serviço doméstico não remunerado;
os dez testes da aula e as verificações de banco, alternativas, desenho e feedback
foram novamente aprovados. A revisão visual conferiu mapas e quadro geral nos dois
temas. Nenhuma sigla em maiúsculas dos enunciados/opções novos ficou fora do glossário.
