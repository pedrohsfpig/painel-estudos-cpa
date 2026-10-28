# Fazer questões a partir do conteúdo — 28/10/2026

Cada trecho de revisão oferece **Fazer questões** e o número de questões
disponíveis para aquele conteúdo. O clique inicia uma sessão normal de Estudo
com **todos os IDs correspondentes do banco principal**, incluindo Hardcore,
sem limite de quantidade, filtro de inéditas ou proporção de sorteio.

## Onde aparece

- Trilha: cada item do resumo, dicas, pegadinhas e números para decorar.
- Mapas: cada conceito/ramificação e seus subgrupos.
- Diagramas: cada nó e o diagrama completo.
- Tabelas: abaixo de cada tabela, respeitando as entidades e os aspectos dela.
- Quadro geral: cada participante, cada característica e o quadro atualmente
  filtrado. Uma célula herda obrigatoriamente o participante da própria linha.
- Linhas do tempo: cada registro e a sequência completa.
- Flashcards: abaixo do cartão, fora da área que vira a pergunta/resposta.
- Quadro do SFN: cada órgão e grupo de operadores.

Os vínculos específicos continuam disponíveis em todos esses locais. Nos mapas,
diagramas, quadros gerais e linhas do tempo, o controle **Por conceito** abre
um seletor lateral com grupos, busca e contagem de cada conceito. Há apenas
um atalho por ramificação/quadro; os nós e células ficam livres de controles.
Tabelas mantêm o acesso discreto abaixo; os demais textos preservam seus atalhos.

A interface é inserida depois da renderização, sem reescrever AL/MAT, os
quadros, os textos, suas cores ou os dados de Q/BP. Os controles ficam fora dos
textos usados por mapas e trilha, preservando a hierarquia original. Zero
correspondências aparece como **0 disponíveis**, com ação desabilitada.

## Assunto e característica

`active-study.js` mantém um cadastro editorial local de assuntos, sinônimos,
características e subtemas. O perfil de uma questão usa aula, tema, enunciado e
alternativa correta. **Distratores, feedbacks das incorretas e o histórico não
são critérios de recuperação.** Os IDs continuam sendo a posição original de Q.

O material transmite título, texto próprio e ancestrais, além das entidades dos
cabeçalhos/linhas de uma tabela. A seleção exige assunto compatível e, quando
identificável, a característica correspondente. Não há ranking dos primeiros
resultados, limite de dez ou mistura de questões só para preencher uma sessão.

Cuidados verificados:

- Composição de uma diretoria não recupera funções ou competências por apenas
  mencionar o mesmo órgão. Mandato, nomeação, exoneração e reuniões têm vínculos
  próprios; uma ramificação que explica vários desses pontos reúne seus IDs.
- BC e CVM representados no CNSP não transformam a tabela de composição do CNSP
  em revisão da quantidade de diretores de BC ou CVM.
- Uma célula “Regulação / supervisão” de banco de investimento trata desse
  banco; a menção ao BC não autoriza recuperar todo o banco de perguntas do BC.
- Autorizações do BC separam-se de seus objetivos e demais funções. Subtemas
  como PTAX, mudança da meta de inflação, produto coberto pelo FGC e regimes
  cambiais também têm distinções próprias.
- Questões de outras aulas entram quando abordam o mesmo conceito. Uma
  comparação BC/CVM sobre mandatos pode participar da revisão de mandato.
- Não há inferência de perguntas novas nem vínculo obrigatório de todo trecho
  a algum exercício. Material sem pergunta específica pode ter zero.

As regras são determinísticas, não um modelo de IA. Os testes cobrem fronteiras
positivas e negativas; a pertinência precisa continuar sendo revisada junto ao
conteúdo. **Ao criar aulas ou assuntos, revise e amplie esse cadastro**, confira
as contagens e teste exemplos específicos e comparativos. Não use uma busca
ampla pelo nome da instituição como substituto para um vínculo ausente.

## Sessão e proteção do progresso

- O número ao lado da ação é o tamanho exato do conjunto; IDs únicos, sem
  Bate-pronto, sem limitar às aulas selecionadas em Praticar e sem alterar cfg.
- Ordem e alternativas seguem o embaralhamento normal. Perguntas mantêm suas
  dificuldades, feedbacks e navegação por números. A dificuldade Hardcore fica
  visível; Hardcore não recebe dica/eliminação e registra origem 2 no histórico.
  Demais questões registram origem Estudo (0).
- O cabeçalho identifica o conteúdo e oferece **Voltar ao conteúdo**. Retorno
  preserva aula, tipo de material, bloco, posição/face do flashcard e a sessão.
  A ação de retorno depois do resultado segue a regra normal de sair do resumo.
- Refazer os erros do resultado mantém o contexto e usa só os IDs errados.
- Se já existe uma sessão incompleta, o clique **não a substitui**: explica que
  é necessário concluí-la ou encerrá-la e oferece Retomar sessão. Isso também
  protege o checkpoint diário, suas escolhas, relógio e regra de uma vez ao dia.
- Nenhum início/consulta adiciona tentativas a H. A gravação acontece somente
  na resposta, pelo fluxo existente. Estatísticas continuam usando dados reais.

## Recursos e validação

Recursos locais `active-study.js`/`active-study.css`, carregados com index.html.
Sem API, credencial, IA, serviço externo ou nova chave de armazenamento.

```bash
python3 tests/test_active_study.py
python3 tests/test_question_navigation.py
python3 tests/test_practice_navigation.py
python3 tests/test_bate_pronto.py
python3 tests/test_result_scorecards.py
python3 tests/smoke.py
```

O teste de estudo ativo percorre os materiais das 12 aulas, confere igualdade
entre contagem e sessão, IDs únicos, classes de dificuldade, fronteiras de
assunto, leitura por teclado, dois temas e larguras 390–1920. Confere também
retorno ao material, flashcards, sessões em andamento e o diário. A auditoria
gera `/tmp/cpa-active-study/final-links.json` para inspeção local dos vínculos.

### Resultado da validação

- 11 testes específicos de estudo ativo aprovados, incluindo todas as aulas,
  a distinção de TR registradora/Taxa Referencial e a composição do Comef.
- 24 regressões de navegação, Bate-pronto e resultados aprovadas.
- Os 76 fluxos gerais foram executados: 75 passaram inicialmente. O caso de
  células sem conteúdo identificou um atalho indevido; ele foi retirado e o caso
  passou na reexecução junto aos 11 testes específicos (12 aprovações finais).
- Conferência visual em claro/escuro, teclado e larguras 390–1920.
- 3421 descritores de conteúdo percorridos na auditoria de materiais;
  contagens e conjuntos sem IDs duplicados. Zero não é preenchido artificialmente.
- Bancos Q/BP, textos AL/MAT e quadros preservados; o diff de index.html contém
  somente os recursos, integração visual, retorno e regras da nova sessão.

### Refinamento visual posterior — 28/10/2026

O usuário considerou os botões repetidos visualmente prejudiciais. Foram
retirados dos nós de mapas/diagramas, células do quadro geral e registros de
linha do tempo. Os mesmos vínculos ficam em **Por conceito**, ao lado da ação
compacta do quadro/ramificação. O seletor lateral é fechado por padrão e não
ocupa espaço no material, com conjunto completo e todos os conceitos específicos.

Busca local, contagens, grupos expansíveis, vazio, zero desabilitado, navegação
por teclado, Escape, clique fora, devolução de foco e tema preservados. Iniciar
fecha o seletor; Retomar sessão também o fecha, sem substituir uma prática.
Voltar ao conteúdo pode focar o conceito original, mesmo sem botão em seu nó.

O seletor não modifica o catálogo de assuntos, os conjuntos de IDs ou a lógica
da sessão. Os controles não alargam colunas nem aumentam os nós dos diagramas.
Conferir `tests/test_active_study_design.py` além das regressões existentes.

Validação do refinamento: 11 testes de estudo ativo, 6 testes de apresentação e
76 fluxos gerais aprovados. Comparação dos 3.421 descritores com a versão
anterior: **nenhum conjunto de IDs alterado**. Os testes de geometria confirmam
que a tabela do quadro geral e os nós dos diagramas conservam suas dimensões;
o mapa recebe apenas o controle compacto por ramificação. Conferência visual
em dois temas e no computador/celular concluída.

## Aula 13: riscos financeiros

Em 28/10/2026, o cadastro ganhou assuntos de risco de liquidez, crédito,
mercado, juros, ratings e spread de crédito. A correspondência considera
financiamento/negociação, pagamento, avaliação, sensibilidade, cupom e prazo.
Os grupos do mapa herdam o assunto do quadro: Mercado dentro de Liquidez é
liquidez de mercado; Cupom dentro de Sensibilidade pertence aos juros.
Mercado de crédito não equivale automaticamente a risco de crédito. Exemplos
numéricos identificam o conceito no próprio texto, sem relações por ID fixo.
Os controles compactos e o seletor Por conceito permanecem iguais.
