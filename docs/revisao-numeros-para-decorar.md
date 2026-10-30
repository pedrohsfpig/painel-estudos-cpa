# Números para decorar — revisão de 30/10/2026

Revisadas todas as 13 aulas e seus blocos. Por pedido do usuário, os cartões
devem conter fatos, regras e relações gerais do conteúdo. Entradas/resultados
de exemplos, recomendações de treino e contagens editoriais não são fatos para
decorar. Os exemplos continuam nos resumos, explicações e materiais pertinentes.

Foram retiradas 13 entradas agregadas, com remoção também nos blocos internos:

- Aula 1: aproveitamento recomendado de 80% em simulados.
- Aula 10: compulsório hipotético de 10% usado num exercício.
- Aula 12: 9,28%, 7 p.p. e −1,29% dos exemplos de câmbio.
- Aula 13, Riscos Financeiros: 4 p.p., R$ 160 mil, dois semestres,
  R$ 1.123,60, um semestre, R$ 19,63 e R$ 20,38 de cenários ilustrativos.
- Aula 13, Crédito Privado: três eixos da organização editorial da revisão.

Permanecem composições institucionais, limites e prazos do conteúdo, referências
legais, relações matemáticas e classificações qualificadas pelo contexto da aula.
Na Aula 13, continuam as duas perspectivas da liquidez, a equivalência dos regimes
em um período nas condições indicadas, n, t=0 e o significado de VPL=0.
Na nova aula: pesos completos somam 1/100% e um ano tem 12 meses.

O arquivo `revisao-numeros-para-decorar.json` conserva listas anteriores,
posteriores e os vínculos por bloco. Nada de Q/BP foi removido ou alterado por
esta revisão. A inclusão da nova aula é uma mudança independente e identificada.
`tests/numbers_revision.py` reconstitui somente esses cartões quando testes de
preservação precisam comparar estados históricos; os manifests antigos mantêm
seus hashes originais. Os testes da entrega verificam também os cartões atuais,
para que a reconstrução não esconda alterações indevidas.
