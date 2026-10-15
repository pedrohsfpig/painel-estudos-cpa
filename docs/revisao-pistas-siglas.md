# Questões sem pistas por iniciais ou expansão de siglas

O exemplo BP100445 (`RDC é:`) permitia acertar pelo encaixe das iniciais de
“Recibo de Depósito Cooperativo”, eliminando “Cota de fundo de previdência”.
Ocultar o nome por extenso antes da resposta não resolveria esse defeito de
autoria. A inclusão recente de expansões também tornava necessário verificar
se a própria explicação entre parênteses antecipava o que se perguntava.

## Reformulação de quatro questões

- **BP100445 — RDC:** aplicação do limite do FGCoop ao conjunto de RDC e poupança
  elegíveis do beneficiário na mesma cooperativa, versus limites independentes
  por produto. Os feedbacks explicam por que os créditos se somam.
- **BP100379 — STR:** disponibilidade de fundos no momento da liquidação versus
  regularização posterior. Não pede mais o nome do sistema.
- **BP100394 — CCP:** distinção entre gestão do risco das obrigações de liquidação
  e garantia de valorização dos ativos. Não pede mais a tradução do nome.
- **Q753 — STR:** condição de saldo para liquidar a transferência. Quatro opções
  comparáveis sobre disponibilidade de recursos, sem listas de nomes por extenso.

São **4 enunciados e 10 feedbacks** alterados (4 no banco principal e 6 no
Bate-pronto), com alternativas, dica e explicação geral alinhadas quando cabível.
IDs, ordem, temas, referências de origem, aulas, níveis e número de perguntas
permanecem preservados: 900 Q e 450 BP, 100 e 50 por aula, respectivamente.

## Expansões que dão a resposta

A triagem dos dois bancos confrontou nomes oficiais, perguntas e alternativas.
A seleção editorial protege **56 itens — 28 Q e 28 BP**. Exemplos: expandir Compe
como Centralizadora da Compensação de Cheques antes de perguntar seu instrumento;
expandir SILOC antes de perguntar se a liquidação é diferida; expandir DPGE antes
de pedir qual produto recebe garantia especial.

Nesses itens, **todas as siglas** ficam sem a expansão até a resposta, para tratar
as opções igualmente. Depois, os nomes aparecem no enunciado ou nas alternativas,
seguindo a preferência pelo enunciado e evitando duplicações. Em Simulado,
continuam disponíveis somente na revisão após finalizar. Não há feedback imediato.

A regra normal de nomes entre parênteses permanece nas demais questões, inclusive
nas quatro reformuladas quando o nome já não resolve a pergunta. A lista editorial
`QUESTION_ACRONYM_CLUES` é rastreável por ID no manifesto JSON. O reconhecedor de
perguntas sobre significado também aceita formatos curtos como `RDC é:` em casos
futuros, mas isso não autoriza criar novamente perguntas resolvíveis por iniciais.

Coincidência de uma palavra comum, como “banco” ou “sociedade”, não basta para
classificar uma pergunta como defeituosa. A conferência considera a relação entre
pedido, informação acrescentada pelo nome e distratores. Essa seleção não é uma
garantia automática de ausência de toda pista semântica possível.

## Rastreabilidade e verificações

`docs/revisao-pistas-siglas.json` registra antes/depois e hashes sem modificar os
manifestos anteriores. `tests/question_revision.py` reconstrói primeiro a versão
anterior a esta alteração, depois as revisões numérica, gramatical e anteriores.

`tests/test_acronym_clues.py` verifica as quatro reformulações, manutenção dos
bancos, ausência do modelo direto defeituoso e exibição de nomes somente após
responder nos 56 itens. Também confere feedbacks embaralhados e escolhas brutas
no histórico. As validações gerais conferem seleção, níveis, simulados, diário,
resultados, temas, materiais e persistência.
