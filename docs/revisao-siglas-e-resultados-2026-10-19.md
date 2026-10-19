# Siglas e resultados — 19/10/2026

A conferência percorreu os 1.000 itens regulares e os 500 de Bate-pronto. Há
siglas em 940 itens. O caso LFL já tinha a expansão correta no glossário, mas a
questão 967 estava indevidamente marcada para adiá-la até a resposta.

A revisão do fato pedido em cada exceção identificou 32 adiamentos desnecessários:
17 questões regulares e 15 de Bate-pronto, da aula 10. LFL por extenso não revela
as garantias exigidas; nomes de LLI e LLT não fornecem limites em dias, cestas
aceitas ou público elegível. As 72 exceções que revelariam o fato pedido continuam
adiadas. A preferência pelo enunciado e a prevenção de duplicações permanecem.
Os 1.468 outros itens tiveram exibição idêntica na comparação completa.

Os bancos, IDs, gabaritos, dicas, feedbacks e históricos não foram reescritos.
O manifesto JSON desta data registra motivos por item e hashes de integridade;
os manifestos históricos continuam preservados.

## Resultado da sessão

- Nota, acertos, aulas, assuntos com erro e tempo ficam juntos no início.
- Ações aparecem logo abaixo da nota, antes dos gráficos.
- Aulas ocupam uma grade de cartões com título completo, percentual e contagens.
- Dificuldades usam pequenos gráficos circulares, com acertos/erros por grupo.
- A lateral dos gráficos reúne os padrões de erro da sessão.
- Recomendações continuam completas, com os atalhos de revisão de conteúdo.
- Questões erradas ficam em duas colunas; abrir uma usa a largura completa,
  preservando a alternativa e sua explicação lado a lado.
- Conceitos de sessões extensas de Bate-pronto têm uma região de rolagem acessível
  por teclado, sem corte de assuntos. Telas menores reorganizam as colunas.

No cenário comparativo de 30 questões das 10 aulas, a altura total diminuiu de
2.888 para 1.678 pixels em janela de 1.440 pixels de largura, aproximadamente 42%.
Os gráficos diminuíram de 867 para 525 pixels; as ações passaram da posição
vertical 1.990 para 345 pixels. As medidas variam conforme a sessão; o arquivo
`resultados-compactos-2026-10-19.json` registra os quatro tamanhos conferidos.

A mudança é de apresentação. A análise continua usando somente respostas da
sessão, com o mesmo cálculo de notas, duração, recomendações e refazimento de erros.

## Validação

- Suíte `test_*.py`: 110 testes aprovados; o caso adicional de prioridade única
  passou junto aos seis testes finais de `test_compact_results.py`.
- `tests/smoke.py`: 76 testes aprovados, cobrindo os modos, o diário, temas,
  persistência, feedbacks, materiais e navegação existentes.
- `tests/validate_bank.py`: seis testes aprovados.
- `tests/audit_alternatives.py --check`: aprovado, sem mudanças nas alternativas.
- Censo renderizado: 1.500 itens, exatamente 32 diferenças, nenhuma definição
  não adiada ausente. Os hashes de Q e BP permaneceram iguais aos anteriores.
- Conferência visual nos temas claro/escuro e larguras de computador de 1.024 a
  1.920 pixels; sem transbordamento horizontal. Regressão adicional em tela pequena
  e região de conceitos operável por teclado.
