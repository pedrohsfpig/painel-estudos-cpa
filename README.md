# Painel de estudos CPA

Painel de estudos e simulados em português, importado do arquivo
`Painel de estudos CPA.html`. O banco contém 1.200 perguntas e 600 Bate-pronto em 12 aulas. As perguntas anteriores
mantêm seus IDs, temas, dificuldades e histórico. A versão atual contém feedback específico
para cada alternativa e uma revisão de redação para reduzir pistas de tamanho e melhorar
a plausibilidade das opções. As correções estão em
[docs/auditoria-alternativas.md](docs/auditoria-alternativas.md).

## Executar

O painel é uma página HTML independente, sem instalação de dependências,
build, servidor de aplicação ou credenciais obrigatórias.

Na pasta do repositório, execute:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Em um computador local, acesse `http://127.0.0.1:8000` no navegador.
Também é possível abrir `index.html` diretamente, mas usar sempre o mesmo
endereço e porta mantém uma origem estável para o histórico do navegador.
Para encerrar o servidor, pressione `Ctrl+C`.

## Publicar no GitHub Pages

O painel pode ser hospedado diretamente pelo GitHub Pages, sem build.
O arquivo `.nojekyll` mantém a publicação como um site estático.

No repositório `pedrohsfpig/painel-estudos-cpa`, abra **Settings → Pages**.
Em **Build and deployment**, selecione **Deploy from a branch**,
depois a branch **main** e a pasta **/(root)**, e salve.

Após o GitHub concluir a publicação, o endereço padrão será:
`https://pedrohsfpig.github.io/painel-estudos-cpa/`.
Esse endereço só fica disponível quando o Pages estiver ativado e a
publicação tiver terminado.

Com o Pages ativado, novos commits enviados à branch `main` atualizam o site.
Cada publicação pode levar alguns minutos. Para acompanhar as alterações,
aguarde a publicação e recarregue o mesmo endereço no navegador. O histórico
local permanece porque a origem do site não muda.

## Funcionalidades preservadas

- Menu lateral fixo no computador, com ícones e indicação da tela atual.
- Painel com estatísticas reais, andamento por aula, prioridades de revisão,
  evolução dos acertos e acesso à última aula praticada.
- Aba **Estatísticas**, abaixo de Quadro do SFN: gráficos de acertos por
  dificuldade, detalhamento por aula/tema e matriz comparativa expansível.
  Os filtros de análise ficam nessa aba; o painel mantém os indicadores gerais
  e a evolução do histórico completo.
- Aba **Guia da prova**, abaixo de Estatísticas: tabela de prioridades fornecida
  pelo usuário, com busca, filtros de importância/bloco/cadastro e ordenação.
  [Referência completa](docs/guia-da-prova.md), preservada sem alterar questões
  ou sorteios; a Aula 13 é identificada como prevista até ser cadastrada.
- Painel em duas colunas independentes: trilha e evolução na principal;
  revisão e última aula empilhadas na lateral, com textos e controles legíveis.
- Botão de lâmpada fixo para alternar claro/escuro em qualquer tela, com escolha
  salva neste navegador. Sem escolha salva, acompanha o tema do dispositivo.
- 1.200 questões: 100 em cada uma das 12 aulas, sendo 80 de estudo e 20 Hardcore.
- 600 Bate-pronto: 50 conceitos diretos com duas alternativas por aula.
- [Aula 10](docs/aula-10.md): mercados financeiros, clearing houses e estabilidade/liquidez,
  com três blocos, materiais visuais e quadro geral comparativo.
- [Aula 11](docs/aula-11.md): macroeconomia, atividade e política fiscal.
- [Aula 12](docs/aula-12.md): mercado de câmbio, taxas e cupom cambial, com
  as relações condicionadas de juros, risco, divisas e comércio em tabelas e dicas.
- Aula 6 identificada como **Operadores Monetários**, mantendo os conteúdos e IDs.
- Aula 7: **Operadores Não Monetários**, com 18 participantes em quatro blocos.
  A leitura, os materiais e a prática podem abranger toda a aula ou um bloco.
  Na trilha, o filtro fica acima dos números, resumo, dicas e pegadinhas; trocar
  de bloco mantém abertas as seções em consulta.
- 240 fáceis, 480 médias, 240 difíceis e 240 Hardcore.
- Estudo com dicas, eliminação de alternativas e correção imediata.
- Feedback da resposta correta e das três alternativas incorretas após responder,
  tanto em Estudo quanto em Hardcore, incluindo prática diária e por aula.
- [Quadro numerado de questões](docs/navegacao-questoes.md) no Estudo e Hardcore,
  incluindo o checkpoint diário: navegação livre, amarelo para pendentes deixadas,
  verde para acertos e vermelho para erros, preservando escolhas e ajudas.
- Simulados com resultado e revisão dos erros ao final.
- Filtros de aula, dificuldade, questões inéditas e erros pendentes.
  É possível selecionar várias aulas, com participação igual e distribuição
  proporcional de níveis; a prévia mostra os números de cada aula.
- Estudo de hoje, cronômetro, indicadores e evolução diária.
- Trilha de aulas, quadro do SFN, mapas mentais, diagramas, tabelas,
  linhas do tempo e flashcards.
- Materiais com nome completo da aula e abas com ícones. Mapas mostram o conceito
  central e ramificações abertas, títulos centralizados e subtópicos agrupados.
  Diagramas distinguem fluxos de grupos. Tabelas usam grade completa, cabeçalhos
  padronizados e cores por coluna nas comparações, sem listras por linha.
- Datas e sequências usam conexões; durações comparáveis usam uma escala de tempo,
  e periodicidades mostram recorrência. Todos os textos desses materiais são
  mantidos; negativas recebem destaque vermelho, assim como na trilha, sem
  aplicar a formatação às questões, alternativas ou feedbacks.
- Flashcards com pergunta e resposta identificadas, posição no conjunto e
  controles agrupados; o cartão também vira com Enter ou espaço quando em foco.
  A face da resposta tem fundo lilás. Os 240 cartões foram revisados; 90 perguntas
  ganharam contexto explícito, e oito respostas foram esclarecidas, mantendo
  quantidades, conceitos, ordem e dificuldades.
- Sumário lateral nas aulas, com atalhos que abrem e focam números, resumo,
  dicas e pegadinhas; ícones pequenos identificam as seções.
- Cabeçalho das questões com cronômetro e barra de respostas concluídas nos
  três modos. Nos simulados, o avanço automático continua sem feedback imediato.
- Feedback com destaque para a resposta correta e a alternativa escolhida,
  à direita de cada alternativa no computador, mantendo as quatro explicações
  completas e a ordem das opções apresentada, inclusive na revisão de erros.

## Organização da trilha

As três seções das aulas foram revistas individualmente e confrontadas com
as questões e o material de apoio existente. **Resumo da aula** explica conceitos
e regras; **Dicas e macetes** oferece métodos para memorizar ou resolver;
**Pegadinhas** mostra uma afirmação enganosa, sua correção e o motivo do erro.
Um tema pode voltar em outra seção com uma função diferente, sem copiar o texto.

O padrão vale para todas as futuras aulas, usando as transcrições e os slides
fornecidos como fontes e conferindo também a consistência das questões e dos
materiais. A revisão e os conteúdos recuperados estão em
[docs/revisao-trilha.md](docs/revisao-trilha.md); a rastreabilidade dos 128 itens
anteriores está em [docs/revisao-trilha-itens.json](docs/revisao-trilha-itens.json).

A aula 7 reúne três aulas do professor, sem aumentar o padrão de 100 questões.
O bloco de mercado de capitais recebe mais exercícios, conforme a prioridade
solicitada. Fontes, cobertura e correções estão em
[docs/aula-7-operadores-nao-monetarios.md](docs/aula-7-operadores-nao-monetarios.md).

## Histórico

Fora do Claude, o progresso é salvo no `localStorage` do navegador, na chave
`cpaH`. Recarregar a página mantém as respostas. Trocar de navegador, endereço
ou porta cria outro histórico; limpar os dados do site apaga os registros.
Importar o HTML não transfere automaticamente o progresso do ambiente anterior.

O HTML original também tenta sincronizar o histórico pela API `claude.use`.
Essa integração foi preservada, mas não está disponível neste ambiente.
Não há login nem sincronização entre dispositivos na versão independente.

## Indicadores do painel

Respondidas, acertos e erros contam **tentativas**, inclusive respostas repetidas.
O aproveitamento é a proporção de acertos nessas tentativas. Os filtros de nível
e origem valem para esses indicadores, o gráfico e o desempenho detalhado.

O andamento da trilha conta **questões diferentes praticadas** em cada aula,
incluindo Hardcore, usando todo o histórico. Responder novamente à mesma questão
não aumenta esse andamento; a barra não representa domínio do conteúdo.

As prioridades agrupam **erros pendentes** por aula e tema: uma questão fica
pendente quando sua última resposta foi errada e sai da lista ao ser acertada.
Mostramos os três grupos com mais pendências, com acesso à revisão completa.
O botão de retomar abre o material da última aula praticada; não restaura uma
sessão de questões após fechar o navegador. Com histórico vazio, o painel orienta
o início dos estudos sem inventar dados.

## Testes de navegador

Os testes usam Python 3 e Playwright; essas dependências são necessárias
somente para os testes, não para utilizar o painel.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/smoke.py
```

Quando Python, Playwright e Chromium já estiverem disponíveis no ambiente:

```bash
python3 tests/smoke.py
```

Para conferir o banco de questões, sem instalar pacotes externos:

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
```

O teste inicia e encerra seu próprio servidor local e usa um histórico isolado
por caso. Ele detecta Chromium no sistema; para informar outro executável,
use a variável `CHROMIUM_PATH`.

Os casos verificam o banco de questões, os materiais das dez aulas, os três
modos de prática, ajudas, revisão de erros, filtros, estudo diário, persistência,
limpeza do histórico e um fluxo em tela móvel. Também exercitam as quatro escolhas
de todas as questões para conferir a associação entre alternativa embaralhada e
feedback, a ausência de feedback em simulados e o contrato de conteúdo futuro.
Os blocos da aula 7 também são conferidos na leitura, na prática e nos simulados,
incluindo os 18 participantes, o limite de 100 questões e a preservação dos IDs.
A integração com a conta do Claude não faz parte desses testes.

A seleção múltipla também é testada em todos os modos e dificuldades, incluindo
arredondamento, pouca disponibilidade, ausência de questões em uma aula e
transição para atalhos de uma aula/bloco. Veja as regras e exemplos em
[docs/pratica-varias-aulas.md](docs/pratica-varias-aulas.md).

Também verificamos a diferença entre tentativas, cobertura única e erros
pendentes, a aplicação dos filtros e o menu fixo nos dois temas, em larguras
de 1024, 1280, 1440 e 1920 pixels.
Os atalhos da aula também são exercitados por teclado, sem alterar uma sessão
de questões em andamento. A barra de progresso é conferida nos três modos.

## Feedback e novas questões

O banco atual inclui 2.800 feedbacks: quatro por questão. A justificativa geral
original fundamenta a resposta certa. As explicações das demais opções apontam
conceitos confundidos, papéis trocados, exclusões, erros de cálculo ou afirmações
indevidamente incluídas/omitidas. Nas perguntas que pedem INCORRETA ou NÃO,
distinguem afirmação verdadeira de resposta correta ao enunciado.

As explicações são exibidas somente depois da resposta, seja acerto ou erro,
inclusive para opções eliminadas pela ajuda. A revisão de erros também contém
os quatro feedbacks. Simulados mantêm o avanço sem feedback imediato e a revisão
geral já existente no resultado, sem o novo bloco de quatro explicações.

Cada linha de `Q` usa esta estrutura:

```text
[aula, tema, nível, enunciado,
 correta, incorreta1, incorreta2, incorreta3,
 justificativaGeral, somenteEstudo, dica,
 [feedbackCorreta, feedbackIncorreta1, feedbackIncorreta2, feedbackIncorreta3]]
```

Os feedbacks ficam em `q[11]` na ordem ORIGINAL, não na ordem A/B/C/D da tela.
As opções embaralhadas carregam o índice de origem para manter esse vínculo.
Todas as novas questões precisam de quatro explicações próprias e preenchidas.
O aplicativo valida isso antes de iniciar, e o GitHub Actions executa a checagem
de conteúdo em pushes e pull requests. Essa checagem não substitui a revisão
pedagógica: confira cada explicação com o material usado na aula.

## Qualidade das alternativas

A auditoria mede caracteres e palavras nas questões normais e Hardcore, incluindo
os empates. Compara as estratégias de escolher a menor, a segunda menor, a
segunda maior e a maior. Os testes alertam quando uma posição de tamanho fica
demasiado associada ao gabarito ou quando uma alternativa longa destoa das outras.
As opções de uma mesma pergunta também precisam ter textos distintos.

Para comparar outra versão do HTML:

```bash
python3 tests/audit_alternatives.py --html /caminho/versao-anterior.html --json
```

Essas métricas são alertas editoriais: não imponha tamanho exato nem acrescente
texto de preenchimento. Distratores precisam testar confusões plausíveis no mesmo
tema, com formato paralelo, e ter feedback coerente com a redação atual.
A checagem automática não prova plausibilidade, resposta única ou atualização
das normas; esses pontos precisam de revisão humana.

Para preservar históricos, acrescente questões ao final do banco, sem reordenar
as antigas. Leia `AGENTS.md` antes de implementar novas aulas ou conteúdos.

O visual prioriza o computador. Em janelas pequenas, o menu passa para o topo
para manter os controles acessíveis.

## Busca contextual e busca geral

O painel oferece a busca geral logo abaixo de **Estudo de hoje**, com filtros de
**Trilha**, **Questões** e **Materiais**. A busca encontra nomes e conteúdos entre
as aulas, reconhece equivalências como Bacen/BCB/Banco Central e ignora acentos.

Nas outras telas, cada campo pesquisa apenas seu contexto: aulas e resumos na
Trilha, questões em Praticar e o tipo aberto em Material de apoio. Por exemplo,
em **Tabelas** só aparecem tabelas. As consultas ficam separadas por tela/tipo.

Resultados usam cartões curtos, quatro por página, com acesso direto ao conteúdo.
A busca de questões mostra enunciados sem alternativas ou gabarito; praticar um
resultado exige clique explícito. Uma sessão em andamento é preservada e pode ser
retomada. A busca não altera a seleção de aulas nem a distribuição da sessão.

Detalhes em [docs/busca-contextual.md](docs/busca-contextual.md).

Na busca da Trilha, escolha primeiro uma aula nos cartões numerados, em ordem,
com a quantidade de informações encontradas. Nos resultados, número, ícone e cor
identificam sempre a mesma aula. O filtro Questões do painel oferece dificuldade,
modo, histórico e aula; Materiais oferece cartões por tipo com contagens e filtro
de aula. Esses refinamentos não mudam a configuração da sessão nem o histórico.

Os seletores de modo, histórico e aula usam menus no padrão visual do painel,
com seleção marcada, navegação por teclado e adaptação ao espaço da tela.

O desempenho detalhado do painel fica recolhido até o clique. A consulta tem
abas por aulas, temas e dificuldades, busca local, ordenação e seis cartões por
página, mantendo o histórico completo e os filtros de estatísticas.

## Consulta aos materiais

A aba **Consulta**, entre Trilha e Praticar, recebe perguntas e mostra os trechos
na própria tela, com suas fontes. Reconhece siglas, nomes, plurais e sinônimos;
organiza características lado a lado em comparações. Por exemplo: “funções do
Bacen”, “quantos membros compõem o Bacen?”, “comparação entre CVM e Susep” e
“limites do FGC”. Perguntas curtas de continuidade retomam o assunto anterior.

A consulta é local, sem IA paga, chave ou serviço externo. É uma seleção de
conteúdo cadastrado, com indicação quando só há trechos relacionados ou nenhuma
correspondência. Rascunho e perguntas ficam na memória desta visita; Limpar não
apaga o histórico de estudos. Publique também `consulta.js` e `consulta.css`.
Veja [docs/consulta-local.md](docs/consulta-local.md).

Na Consulta, os termos encontrados ficam em negrito e na cor de atenção, inclusive
siglas/nomes equivalentes e variantes de plural. Perguntas anteriores aparecem
somente ao abrir seu controle expansível. Os botões de sugestões foram retirados.

A seleção também considera histórico e substituições, cálculo, causa e sequência.
“Qual era a taxa antes da TLP?” recupera os trechos sobre TJLP e a mudança de
2018, com as condições dos contratos. Relações são extraídas da mesma fonte;
quando não há evidência para responder ao pedido, o resultado é identificado
como relacionado.


**Refinar pesquisa** permite combinar aulas e tipos de material em um controle
recolhido. Siglas ambíguas recebem escolhas de significado quando o contexto não
basta. Os trechos relevantes têm destaque e **Ver contexto** preserva a íntegra;
comparações permitem escolher características ou restaurar todas. As respostas
anteriores guardam seus próprios filtros e escolhas, sem alterar o estudo.
