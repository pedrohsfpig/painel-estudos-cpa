# Prática de várias aulas e consulta dos blocos

Em **Praticar**, cada botão de aula pode ser marcado ou desmarcado. A seleção
permite combinar duas, três ou mais aulas. “Todas as aulas” limpa a seleção
específica e mantém a mistura geral do banco.

## Distribuição das sessões

| Seleção | Quantidade | Participação por aula |
| --- | ---: | --- |
| Duas aulas | 20 | 10 e 10 |
| Três aulas | 30 | 10, 10 e 10 |
| Quatro aulas | 40 | 10, 10, 10 e 10 |
| Três aulas | 10 | 4, 3 e 3; a vaga extra alterna nas próximas sessões |

Em níveis **Todos**, a proporção é **25% fácil, 50% médio e 25% difícil**,
arredondada para questões inteiras. As vagas de nível são calculadas em conjunto
para aproximar essa proporção dentro de cada aula e manter os totais da sessão.
Por exemplo, 20 questões de duas aulas têm 5 fáceis, 10 médias e 5 difíceis no
total; cada aula recebe 10 questões, com uma das vagas de fácil/difícil ajustada
pelo arredondamento.
As vagas de arredondamento dos níveis também alternam entre as aulas nas
sessões seguintes, evitando que uma aula receba sempre mais questões difíceis.

Escolher somente Fácil, Médio ou Difícil restringe a sessão ao nível escolhido.
Hardcore mantém apenas questões Hardcore. Simulados excluem questões marcadas
como somente estudo e continuam sem feedback imediato.

Os filtros **Nunca respondidas** e **As que errei** continuam valendo. Se uma
aula tiver poucas questões, a quantidade total diminui para manter as aulas
equilibradas, com aviso na prévia. Se uma das aulas não tiver nenhuma questão,
o início fica indisponível até ajustar a seleção ou os filtros. Se um nível
faltar, as vagas são distribuídas pelos níveis disponíveis, preservando a
participação das aulas e mostrando um aviso. Não há repetição de IDs na sessão.

Antes de iniciar, a interface mostra a quantidade efetiva por aula e nível.
O sorteio usa exatamente essas vagas; perguntas e alternativas continuam
embaralhadas. O banco mantém as mesmas 700 questões e os mesmos IDs.

## Consulta dos quatro blocos

Resumo, dicas e pegadinhas guardam separadamente seu estado aberto/fechado por
aula. Trocar o bloco ou sair e voltar à trilha mantém as escolhas durante a
navegação, sem obrigar novos cliques. Fechar uma seção também é respeitado.

Os controles dos blocos usam os mesmos contornos discretos em todos os locais:
azul para bancos/fomento, lilás para crédito, verde para consórcios/capitais e
rosa para seguros/previdência. O estado selecionado permanece identificado por
texto, destaque e `aria-pressed`, além da cor. Isso não muda os destaques
semânticos dos textos de estudo.

Um atalho de aula ou bloco inicia a prática somente dessa aula/bloco, mesmo
que antes houvesse várias aulas selecionadas. Combinar aulas limpa o filtro de
bloco; escolher uma única aula novamente permite acessar seus blocos.

## Verificação desta atualização

Os quatro comandos exigidos em `AGENTS.md` passaram: 6 testes do banco,
5 de qualidade e 39 no navegador (**50 testes**), além da auditoria de tamanho
das alternativas. A distribuição foi exercitada em 270 combinações de modos,
aulas, quantidades e níveis. O cálculo de níveis também foi comparado com a
enumeração independente de 120 cenários de disponibilidade.

Seleção múltipla e contornos foram conferidos nos temas claro e escuro, em
larguras de 1024, 1280, 1440 e 1920 pixels, sem transbordamento horizontal.
A comparação dos dados `Q`, `AL`, `MAT` e `AU` com a versão anterior confirmou
a preservação de todo o conteúdo e dos IDs.
