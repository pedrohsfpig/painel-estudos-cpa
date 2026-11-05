# Revisão visual global — 05/11/2026

A linguagem aprovada na prévia foi aplicada ao aplicativo completo. A mudança
fica em `interface.css`, carregada por último, e em um contêiner de apresentação
na configuração de Praticar. Os arquivos JavaScript dos módulos permanecem
idênticos; no script embutido, apenas a estrutura HTML de `setup()` mudou.

## Apresentação

- Fundo branco quente ou grafite, seleção azul, contornos discretos e raios de
  5–8 px. Hierarquia e espaçamento comuns às nove áreas do menu.
- Corpo de leitura em 15–17 px; rótulos normalmente em 14 px. Contagens e atalhos
  compactos com mínimo de 13 px. Enunciados normais em 20 px; Bate-pronto maior.
- Painel com indicadores planos e gráfico de aproveitamento/volume preservado.
- Prática com modos, lista de aulas e painel lateral de configuração/sessão.
  No computador, o início fica acessível na rolagem. No celular, o resumo entra
  no fluxo entre aulas e filtros, sem cobrir os controles.
- Trilha, Consulta, erros, estatísticas, guia, Quadro do SFN e todos os tipos de
  material recebem os mesmos padrões de leitura e acabamento. Mapas em imagem
  conservam seus arquivos, conteúdo, download e ampliação.
- Cores de dificuldades, destaques do conteúdo, feedbacks, resultados e matriz
  estatística mantêm seus significados anteriores.

## Preservação e verificação

Q, BP, AL e MAT não foram editados. Histórico, regras de seleção, ajudas,
feedback por alternativa, progressão, relógio, estudo diário e persistência
continuam nos módulos originais. Nenhum dado ilustrativo da prévia foi importado.

Verificações no Chromium, em claro/escuro, com larguras de 390 a 1920 px:

- `tests/test_interface.py`: legibilidade nas nove áreas, materiais, filtros
  expandidos, seleção de conceitos, resultados, celular e preservação da sessão.
- `tests/smoke.py`: regressão dos 76 cenários. Os pontos de tema e estatísticas
  foram conferidos novamente após os respectivos ajustes responsivos.
- Regressões de prática, hierarquia do painel, estudo ativo, navegação entre
  questões, Bate-pronto, mapas, resultados, Consulta, menus de busca, Guia da prova
  e cores/contraste das estatísticas.
- `tests/validate_bank.py`: banco válido e preservado.

Os testes antigos de resultados usavam limites absolutos de 460 px de posição
para ações e 600 px de altura para gráficos. Com a tipografia maior autorizada,
passam a verificar ações visíveis antes dos gráficos e indicadores integralmente
contidos nos painéis, mantendo os testes de valores, ordem e estado intactos.
