# Aula 4 do bloco final — Prazos e Retornos de Carteiras

Recebida em 30/10/2026. Reúne as aulas 26 (Prazo Médio e Vencimento) e 27
(Retorno Histórico e Esperado). O PDF `Screenshot_1 (6).pdf` tem quatro páginas:
1–2 para prazos; 3–4 para retornos. Transcrição e imagens foram cruzadas.

São 50 questões: 10 fáceis, 20 médias, 10 difíceis e 10 Hardcore, IDs 1351–1400.
Estudo e Simulado compartilham as 40 normais; 25 Bate-pronto próprios
(100676–100700) e 25 flashcards (8/8/9). O bloco recebido passa a somar
200 questões, 100 Bate-pronto e 100 flashcards, com seleção conjunta ou por aula
interna. A reunião de duas fontes não duplica a quota da aula interna.

O material apresenta média aritmética, ponderação, pesos financeiros, prazo
médio, vencimento, retorno de preço, retorno histórico da carteira e retorno
esperado. Há ramificações, cinco diagramas, oito tabelas, uma linha do tempo,
quadro comparativo e um mapa mental em imagem adicional, conferido visualmente.
Os exemplos resolvidos usam valores próprios. Os cartões de números guardam
somente soma dos pesos e conversão de anos para meses; resultados ilustrativos
ficam nas explicações.

As questões variam a tarefa: conta direta, identificação da base, conversão,
subconjunto, hierarquia de pesos, variável desconhecida, contribuição, conferência
de relatório, separação de aporte e ganho, calendário e comparação de previsões.
Dificuldade não depende apenas do tamanho dos números. As questões fáceis têm
operações curtas; difíceis e Hardcore combinam condições e interpretação.
Bate-pronto e flashcards cobram conceitos, sem contas a executar.

O manifesto `aula-13-carteiras-cobertura.json` registra um ângulo por questão,
quatro feedbacks individualizados, hashes e 64 verificações numéricas exatas,
além das fontes. Os IDs anteriores e o histórico foram preservados. Não foram
alteradas questões antigas nesta entrega. A revisão de números é documentada
separadamente, com reconstrução dos estados anteriores para validar hashes
históricos sem reescrever evidências antigas.

Cuidados pedagógicos:

- Prazo médio ponderado não é nova data de pagamento integral. O calendário
  de cupons e amortizações precisa ser examinado separadamente.
- Valores usados nos pesos têm a mesma data-base; prazos têm a mesma unidade.
  Pesos de referência mantidos para observar passagem do tempo são explícitos.
- No modelo de posições mantidas, sem fluxos externos, retorno histórico da
  carteira usa os pesos iniciais. Pesos finais já incorporam desempenho.
- A fórmula de variação de preço não inclui custos ou outros recebimentos por
  si. Quando a questão trata de retorno líquido, informa fluxos e seus momentos.
- Retorno esperado é estimativa e não demonstra sozinho adequação ao investidor.
  Não se misturam horizontes ou colunas de observado e projetado.
- O slide 4 identifica indevidamente como RHC a fórmula sob retorno esperado;
  o material usa o nome correto. O lapso de transcrição 0,8 para 8% foi resolvido
  pelo slide (0,08). O total do exemplo de prazos é R$ 10.000.
- Não se antecipam fórmulas de duration, TIR ou conteúdos não fornecidos.

Assuntos e subtemas novos foram registrados no estudo por conteúdo. Relações
secundárias explicitamente cobradas têm vínculos editoriais; mencionar uma
palavra isolada não amplia o escopo para assuntos alheios. Na Consulta, aliases
específicos dos conceitos substituem rótulos genéricos como “Carteira”. Fontes
que explicam média ponderada também contam como evidência de cálculo, preservando
as palavras originais e os filtros locais.

Validação: `test_aula13_carteiras.py`, regressões das três internas, aulas
10–12, estudo ativo/escopo/desenho, mapas visuais, Bate-pronto, siglas,
busca/Consulta, feedbacks, banco, qualidade de alternativas e smoke.
Testes verificam estrutura, contas e funcionamento; a revisão editorial foi
feita contra as fontes fornecidas, sem alegação de certificação normativa.
