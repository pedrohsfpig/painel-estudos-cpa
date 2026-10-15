# Revisão de erros e retorno à configuração de Praticar

## Resultado concluído

Ao sair da tela de resultado para qualquer outra aba, a sessão concluída deixa
de ocupar `qz`. Voltar a Praticar abre a configuração inicial, preservando filtros
anteriores. Isso também vale para o atalho de revisão de conteúdo da aula.

Re-renderizar o resultado ou alternar o tema enquanto ele está aberto não o fecha.
Uma sessão ainda em andamento conserva questão, escolha, feedback e cronômetro ao
navegar. Nenhum registro de `H` é removido. O resultado do checkpoint continua
salvo no painel diário e pode ser consultado explicitamente por Ver resultado;
isso não provoca reabertura automática ao clicar em Praticar.

## Página Erros

A entrada mostra cinco cartões com ícone, cor e número de pendências: Fácil,
Médio, Difícil, Hardcore e Bate-pronto. Não há um modo preselecionado nem uma
lista de questões aberta. As contagens usam IDs distintos cuja última resposta
foi errada; repetições não multiplicam o contador e um acerto posterior remove
apenas a pendência, mantendo o histórico completo.

Clicar em um cartão revela as questões daquele grupo. Clicar novamente recolhe
a consulta; sair da aba retorna a visão geral quando se volta. A resposta e os
feedbacks permanecem em painéis expansíveis por questão. Os cartões sem erros
mostram zero e ficam desabilitados. Há estado vazio quando nenhuma pendência existe.

As ações são separadas:

- **Refazer erros (modo estudo):** abre Praticar em Estudo com filtro As que errei.
  Se um cartão de Fácil/Médio/Difícil estiver selecionado, conserva esse nível.
- **Refazer erros bate-pronto:** abre a mesma configuração em Bate-pronto,
  exclusivamente com suas pendências e sem filtro de nível.
- **Refazer erros hardcore:** disponível quando há pendências desse nível;
  conserva o modo Hardcore e seu banco.
- **Praticar estes erros:** usa modo e nível do cartão consultado.

Os atalhos começam com todas as aulas, sem um filtro de bloco herdado, e quantidade
10, ajustável na configuração conforme o estoque disponível. Não iniciam questões
nem registram respostas; é preciso clicar em Iniciar estudo/Iniciar bate-pronto/
Iniciar hardcore. Preferências podem ser alteradas livremente antes de iniciar.
Uma prática diária em andamento é salva antes de abrir essa configuração.

Os filtros dos dois bancos tratam os resultados antigos `false/true` de modo
compatível com `0/1`, como a lista de pendências já fazia. Não há migração nem
reescrita do histórico. Questões de Bate-pronto não entram no Estudo, e vice-versa.

## Conferências

`tests/test_error_review.py` cobre cartões, filtros, acerto posterior, estoque
vazio, registros booleanos antigos, configuração antes do início, separação dos
bancos, teclado, temas e larguras de PC. `tests/test_practice_navigation.py` cobre
todos os modos e abas após finalizar, preservação da prática em andamento e
consulta explícita do resultado diário. As regressões existentes incluem os
atalhos de conteúdo e as opções/feedbacks da consulta aos erros.
