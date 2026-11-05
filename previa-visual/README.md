# Prévia visual — Painel e Praticar

Proposta separada, solicitada em 05/11/2026. Não substitui `index.html` nem
carrega os scripts do aplicativo de estudos. A demonstração apresenta somente
Painel e configuração de Praticar; as demais telas estão desabilitadas.

- Alternância claro/escuro, navegação e busca por aula.
- Seleção múltipla, conteúdos internos, modos, dificuldade, histórico ilustrativo
  e quantidades 5/10/15/20/30; quantidade personalizada no Bate-pronto.
- O início abre um resumo da configuração, sem executar uma sessão de questões.
- Sem localStorage, conta, APIs, bibliotecas externas ou gravação de respostas.
- Quantidades do banco derivadas de um retrato dos dados públicos cadastrados:
  13 aulas, 1.450 questões e 725 Bate-pronto. Os indicadores e o histórico exibidos
  são fictícios e estão identificados na interface.

A proposta reduz superfícies e contornos repetidos, prioriza ações e leitura,
preserva as cores semânticas de dificuldade e mantém acertos e volume juntos.
Em janelas baixas de computador, o resumo e o início aparecem antes dos filtros
para manter a ação acessível. Suporta teclado, movimento reduzido e celular.

Abrir `index.html` por um servidor estático. Exemplos:
`?p=painel&t=dark` e `?p=praticar&t=light`.

Conferida no Chromium nos temas claro/escuro e larguras 390, 768, 1280, 1440 e
1920 px: seleção, estoque dos modos, aulas internas, busca, quantidade, teclado,
diálogo, overflow e ausência de gravações. O arquivo principal do sistema foi
conferido por SHA-256 e permaneceu idêntico. Aplicar a linguagem ao sistema
continua fora do escopo desta prévia.
