# Quadro de questões

Estudo e Hardcore, incluindo seus atalhos e o Estudo de hoje, mostram todas as
posições da sessão em uma grade à esquerda. A grade não aparece em Simulado ou
Bate-pronto. No quadro visível, cada botão contém somente seu número.

| Aparência | Significado |
| --- | --- |
| Neutra | Questão ainda não deixada sem resposta |
| Amarela | Saiu dessa questão sem responder |
| Verde | Resposta correta |
| Vermelha | Resposta incorreta |
| Contorno azul | Questão atualmente exibida |

Cada célula tem rótulo acessível e tooltip. As cores usam as variáveis semânticas
do tema; foco e estado atual se distinguem do acerto ou erro.

É possível pular diretamente da primeira para a quarta questão e voltar depois.
As alternativas conservam o embaralhamento, as dicas e as eliminações usadas.
Questões respondidas mostram a escolha e seus feedbacks, sem permitir nova
resposta na mesma sessão ou duplicar a tentativa no histórico.

Próxima leva à próxima questão sem resposta, dando a volta no conjunto quando
necessário. Ver resultado fica disponível após responder todas. A posição no
quadro não aumenta o progresso nem faz as pendentes virarem erros. O cronômetro
para na última resposta, independentemente da posição.

## Estado e compatibilidade

`qz.items` registra o estado de cada posição; `qz.i` aponta a posição exibida.
Os campos correntes `a`, `o`, `h` e `x` continuam disponíveis às rotinas de sessão.
`qz.rev` conserva somente respostas efetivas e os IDs originais; `H` mantém seu
formato e é atualizado apenas ao confirmar uma alternativa.

O rascunho diário inclui os estados individuais. A leitura normaliza opções pelos
índices originais, aceita respostas fora de ordem e reconstrói estados de versões
anteriores que registravam somente a sequência linear. As regras de nota,
conclusão por dia, pausa, retomada, mudança de data e comunicação entre abas
permanecem em vigor. A rolagem do quadro é preservada e a célula atual fica visível.

Os bancos e conteúdos das dez aulas permanecem intactos. Esta entrega não muda a
classificação de dificuldade ou o funcionamento de Simulado e Bate-pronto.

## Verificação

`python3 tests/test_question_navigation.py` verifica:

- Quantidades de 10/20/40, estados iniciais e modos incluídos/excluídos.
- Navegação sem responder, volta com ajudas e embaralhamento preservados.
- Acertos, erros e consulta sem repetição de tentativas.
- Avanço circular, conclusão fora de ordem, nota e relógio.
- Pausa, recarga, conclusão e bloqueio diário com respostas fora de ordem.
- Compatibilidade com rascunho diário anterior e comunicação entre duas abas.
- Preservação ao trocar tema e tela.
- Layout de computador em 1024, 1280, 1440 e 1920 pixels, temas claro/escuro,
  acesso por teclado e rolagem em uma sessão de 120 questões.

As regressões gerais verificam os fluxos anteriores, incluindo resultado, revisão,
feedbacks, diário, simulados, Bate-pronto e materiais.

Validação desta entrega: nove testes específicos aprovados, incluídos na bateria
completa de 101 regressões aprovadas; os 76 fluxos gerais de navegador também
passaram. Os temas claro/escuro foram inspecionados visualmente. Comparação direta
com a versão anterior confirmou Q, BP, AL, MAT, glossário e registro de proteção
de siglas intactos.
