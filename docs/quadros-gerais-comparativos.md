# Quadros gerais das aulas 1, 5 e 6

O quadro da aula 7 passa a ser um componente compartilhado. A apresentação se
mantém, mas os eixos são definidos pelo conteúdo de cada aula, conforme pedido
do usuário. Os quadros são sínteses adicionais; questões, trilha e materiais
detalhados anteriores permanecem integralmente preservados.

| Aula | Linhas | Grupos de consulta | Colunas além do participante |
| --- | --- | --- | --- |
| 1 — SFN | CMN, BCB, CVM, CNSP, Susep, CNPC, Previc | Financeiro; seguros; previdência fechada | Segmento; papel; relação na estrutura; operadores do segmento; observações |
| 5 — Seguros e Previdência | CNSP, Susep, CNPC, Previc | Seguros/previdência aberta; previdência fechada | Segmento; competências; composição/liderança; vinculação/sede; reuniões/decisão; observações |
| 6 — Operadores Monetários | Comercial, múltiplo, caixas econômicas, cooperativa de crédito, banco cooperativo | Bancos; caixas econômicas; cooperativismo | Foco/público; atuação; captação; estrutura/regra central; depósitos à vista/condição; observações |

Na aula 1, são comparados órgãos da estrutura, sem misturar mercados ou agentes
econômicos nas mesmas linhas. Os operadores listados pertencem ao segmento;
não se atribui a BCB ou CVM supervisão indistinta de todo o conjunto. A diferença
entre nível normativo e poder de editar normas aparece na observação da CVM.

Na aula 5, conselho normativo e autarquia supervisora ficam claramente distintos.
Composição não é quórum; indicação/nomeação não se confunde com a designação de
representantes do CNPC. O CNSP é presidido pelo representante da Fazenda descrito
na fonte. Lideranças incluem o órgão e não nomes pessoais presumidos. Sedes de
conselhos, mandatos de diretores e periodicidades não presentes na aula não foram
inventados. A falta de periodicidade do CNPC/Previc é indicada em texto neutro.

Na aula 6, banco múltiplo é monetário quando tem carteira comercial; cooperativa
é monetária se habilitada a captar à vista. Capital e empréstimo não capta
depósitos. Banco cooperativo é distinto da sociedade cooperativa; 51% incide sobre
ações com voto. Fontes de captação não foram preenchidas por analogia com outros
tipos de instituição. Recursos de associados e serviços a não associados são
separados. A forma jurídica do banco cooperativo segue a descrição dessa aula.

## Fontes e extensibilidade

Cada linha de `LESSON_OVERVIEWS` registra `sources` apontando para os resumos e
mapas/tabelas correspondentes de `AL`/`MAT`. O quadro é uma síntese dessas fontes,
sem alegar uma nova validação independente das normas.

Novas aulas com múltiplos participantes recebem uma configuração com título,
colunas, larguras, grupos e linhas após análise das fontes. Cada coluna precisa
ajudar a distinguir os participantes. Observações fica no final. Não há geração
automática de fatos, nem uma obrigação de preencher os sete eixos da aula 7.
Aulas de foco único, como Banco Central, não recebem quadro apenas por conterem
mais de um material de apoio.

## Navegação e validação

Em **Material de apoio → Aula 1, 5 ou 6 → Quadro geral**, ou pelo atalho
**Quadro comparativo** na trilha. Entre aulas com quadro, a aba é mantida; ao
escolher uma aula sem quadro, retorna ao mapa mental. A aula 7 mantém seus dados,
seus quatro filtros e o vínculo com o bloco selecionado na leitura.

As novas aulas têm filtros exclusivos da consulta, preservados individualmente.
Trocar aula/grupo começa a tabela no topo; ampliar/reduzir e trocar tema preservam
a posição atual. Sessão de questões, IDs, histórico e filtros de prática continuam
independentes. Células centralizadas, grade, ícones, cores por grupo, negativas
vermelhas e condições lilás seguem o padrão aprovado.

Os testes de navegador verificam associações entre participantes e células,
condições de depósitos, composições/quóruns, filtros por aula, atalhos, navegação
com sessão ativa, ampliação, teclado, temas e quatro larguras de PC. A comparação
integral antes/depois confere que `Q`, `AL`, `MAT` e o quadro da aula 7 não mudaram.

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/test_question_design.py
python3 tests/smoke.py
```
