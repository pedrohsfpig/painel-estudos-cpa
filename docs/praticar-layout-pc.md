# Praticar — organização para computador

A configuração passa a ocupar a largura útil da página. Os quatro modos ficam
em uma faixa superior; a seleção de aulas ocupa a coluna principal e os controles
de nível, filtro e quantidade ficam na coluna ao lado. A grade de aulas usa duas
ou três colunas conforme a largura disponível, mantendo os nomes completos.

Uma barra com resumo, quantidade efetiva e ação **Iniciar** permanece acessível
durante a rolagem. Avisos de estoque/filtros e indisponibilidade continuam junto
dessa ação. O botão é desabilitado quando o plano não pode ser iniciado.

A distribuição detalhada por aula pode ser expandida sem ocupar permanentemente
a configuração. Sua abertura é mantida ao alterar as escolhas. A seleção múltipla
usa indicação visual de marcação, além de `aria-pressed`; títulos dos grupos e
foco de teclado ajudam a localizar os controles. Os modos conservam seus estados
selecionados, e Bate-pronto mantém o campo de quantidade personalizada.

Não houve alteração em Q, BP, AL ou MAT, nem nas funções de filtros, planejamento,
sorteio e início. A classe de largura expandida se aplica somente à configuração,
sem modificar telas de questões, feedbacks ou resultados.

## Conferência

- Temas claro e escuro, nos quatro modos, em 1024×768, 1280×720, 1366×768,
  1440×900 e 1920×1080: botão acessível sem rolar e sem transbordamento horizontal.
- Em 1440×900, configuração padrão reduzida de cerca de 1778 para 903 pixels de
  altura total; o botão, antes abaixo de 1650 pixels, passa a estar visível.
- Seleção de várias aulas, prévia e início com o mesmo plano; preservação da
  abertura do detalhamento ao trocar a quantidade.
- Blocos da aula 7, clique na última aula em tela baixa, início por teclado,
  filtro sem estoque e lista maior de futuras aulas com rolagem.
- Testes existentes do aplicativo e do Bate-pronto, além de
  `python3 tests/test_practice_layout.py` para os pontos de acesso acima.

Resultado: **88 testes aprovados** (76 fluxos gerais, 8 do Bate-pronto e 4 da
organização de Praticar), além da conferência visual nas 40 combinações de
resolução, tema e modo. Comparação com a versão anterior confirmou que os bancos
e as regras de planejamento/sorteio permaneceram intactos.
