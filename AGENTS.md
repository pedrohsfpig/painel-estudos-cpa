# Desenvolvimento do painel CPA

Use o checkout existente: as tarefas de nuvem já são isoladas. Não crie worktrees
sem solicitação explícita do usuário. O aplicativo é uma página independente em
`index.html`; não introduza dependências de servidor para funcionalidades locais.

## Regra permanente de feedback

O usuário exige feedback da alternativa correta e das três incorretas em TODAS
as questões, após a resposta, exceto nos simulados. Isso inclui Estudo, Hardcore,
estudo diário, prática por aula, revisão de erros e futuras aulas ou conteúdos.

- Toda questão de `Q` precisa de `q[11]`: quatro explicações em texto, na ordem
  original das alternativas `q[4]`, `q[5]`, `q[6]`, `q[7]`.
- A primeira justifica a resposta correta. Cada outra explica o erro específico
  daquela opção; não substitua por quatro cópias da justificativa geral.
- Em perguntas que pedem INCORRETA, NÃO, exceções ou combinações de afirmações,
  explique por que a opção atende ou não ao enunciado. Não chame uma afirmação
  verdadeira de falsa só porque ela não é a resposta pedida.
- Em contas, indique a operação ou o abatimento omitido. Em associações, indique
  os papéis ou posições trocados. Evite apenas repetir que a resposta está errada.
- O feedback acompanha o índice original da opção, inclusive após embaralhar.
  Nunca derive seu vínculo de A/B/C/D nem do lugar da opção na tela.
- Não exiba os feedbacks antes da resposta. Mostre os quatro depois de acertar
  OU errar, inclusive das alternativas eliminadas pelas ajudas.
- Nos simulados, preserve o avanço sem feedback imediato e a revisão geral já
  existente no resultado; não acrescente o bloco de quatro feedbacks ao simulado.
- Adicione questões ao final de `Q`; não reordene os IDs já usados em `cpaH`.
  Preserve o histórico existente e as ajudas/opções originais ao evoluir o esquema.

Antes de publicar alterações em questões ou feedbacks, execute:

```bash
python3 tests/validate_bank.py
python3 tests/smoke.py
```

A validação de conteúdo é feita também na inicialização. Nenhuma questão nova
deve ser publicada com explicação faltando, vazia ou repetida para todas as opções.
Os testes automáticos verificam estrutura e comportamento; confira também o
conteúdo pedagógico de cada nova explicação com as aulas e referências fornecidas.

O site publicado usa `main` no GitHub Pages. Quando o usuário pedir atualizações
para vê-las no site, valide, envie os commits e informe o resultado real do envio.
Não confunda envio ao GitHub com confirmação de que o Pages já publicou.
