# Bate-pronto: rodada visual e pistas gramaticais

Atualização de 14/10/2026, com duas solicitações do usuário.

## Concordância e encaixe

A varredura considerou os 900 enunciados principais e os 450 Bate-pronto.
Foram ajustados **31 enunciados principais e 18 Bate-pronto**. Incluem pistas de
artigos/contrações e ajustes de encaixe gramatical, sem mudanças de alternativas,
gabaritos, feedbacks, níveis, proporções ou IDs. As 61 lacunas foram preservadas.

Exemplos:

- “Assinaturas [...] colhidas pela: Secretaria-Executiva / Senado” passou a
  “Quem colhe as assinaturas nas atas aprovadas do CMN?”.
- “A meta da Selic é definida pelo: Copom / Comoc” passou a
  “Quem define a meta da Selic?”. Comoc é comissão; Copom é comitê.
- A lacuna com “precisam ser abatidos” foi reformulada para “descontar _____”,
  aceitando gramaticalmente tanto Custos e perdas quanto Taxas já líquidas.
- Operações interfinanceiras são perguntadas na perspectiva da instituição,
  com concordância de “operação” e sem confundir o gênero de “depósito”.

O manifesto `revisao-pistas-gramaticais.json` guarda todos os IDs, hashes e os
campos alterados. A cadeia histórica desfaz esta revisão antes de validar as
anteriores; relatórios antigos não foram sobrescritos. O detector lexical dos
testes reconhece padrões de gênero conhecidos, não certifica toda a língua
portuguesa nem substitui a leitura editorial das alternativas.

## Apresentação exclusiva das questões Bate-pronto

- Enunciado centralizado e maior, em cartão com ícone genérico e lacuna visual.
- Duas alternativas lado a lado, com cartões de mesma largura e altura, letras
  A/B e o mesmo tratamento visual antes de responder. O destaque de mouse/foco
  não depende da correção da opção.
- Barra de andamento e cronômetro existentes preservados, sem avanço automático.
- Depois da escolha, enunciado mais compacto e explicação à direita de cada
  alternativa. Escolha e correção seguem o índice original após embaralhamento.
- Botão Próxima destacado; navegação por Tab/Enter e preferência por movimento
  reduzido preservadas. Não há novos atalhos de teclado implícitos nas letras.
- Estudo, Hardcore, Simulado, revisão e resultado mantêm sua apresentação.

As regras de seleção, sorteio, tempo, resposta, resultado e histórico não mudam.
Os enunciados do Bate-pronto continuam curtos; a mudança visual não acrescenta
contextos ou cenários às perguntas.

## Verificação

Conferência visual de pergunta e feedback nos temas claro e escuro. Testes em
1024, 1280, 1440 e 1920 pixels, além da verificação existente da configuração de
prática, sem rolagem horizontal. Regressões conferem a igualdade de apresentação
das opções antes da resposta, vínculo dos feedbacks, movimento reduzido,
continuidade da sessão ao trocar tema e isolamento dos outros modos.

Resultado: **141 testes aprovados**, contando validação do banco (6), qualidade
(5), contexto/design/feedback (19), aulas 8/9 (11), revisão didática (6),
Bate-pronto (8), gramática/isolamento visual (6), configuração de prática (4)
e regressões gerais no navegador (76), além da auditoria das alternativas.

O usuário reforçou que “enunciado maior” significa cartão, fonte e espaçamento
maiores, sem acrescentar palavras para preencher a apresentação. A alteração
visual segue esse critério; a revisão gramatical é a solicitação separada acima.
