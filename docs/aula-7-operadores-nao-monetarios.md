# Aula 7: Operadores Não Monetários

A aula reúne as três transcrições e os 21 slides enviados pelo usuário em uma
entrada da trilha. Quatro blocos permitem consultar e praticar partes menores
sem dividir a aula em novas aulas ou aumentar a quantidade de questões.

## Quantidade e prioridade

O padrão permanece **100 questões por aula**: 20 fáceis, 40 médias, 20 difíceis
e 20 Hardcore. A aula 7 usa IDs de 601 a 700; as 600 questões anteriores mantêm
seu conteúdo e sua posição, preservando os vínculos do histórico.

| Bloco | Participantes | Estudo | Hardcore | Total |
| --- | --- | ---: | ---: | ---: |
| Bancos especializados e fomento | Investimento, desenvolvimento, câmbio e agências de fomento | 20 | 5 | 25 |
| Crédito especializado | SCI, companhias hipotecárias, financeiras e SCMEPP | 14 | 3 | 17 |
| Consórcios e mercado de capitais | Administradoras de consórcios, bolsas/B3, CTVM e DTVM | 28 | 8 | 36 |
| Seguros, capitalização e previdência | Capitalização, EAPC, EFPC, seguradoras, resseguradoras e corretores de seguros | 18 | 4 | 22 |
| **Total** | **18 participantes** | **80** | **20** | **100** |

CTVM/DTVM e B3 recebem maior variedade de exercícios e casos dentro do material
fornecido. Bancos de investimento e financeiras também recebem atenção. Esse
critério atende à preferência pedagógica do usuário; não representa frequência
oficial de cobrança. Participantes de outras aulas ou sem fontes nesta entrega
não foram acrescentados apenas para seguir um ranking externo.

## Materiais e funcionamento

- Resumos trazem definições e regras; dicas oferecem associações de memória;
  pegadinhas distinguem conceitos que podem ser confundidos.
- Mapas preservam os conceitos e usam títulos principais azuis. Comparações
  mantêm cores por participante, e negativas reais recebem destaque vermelho.
- Tabelas comparam participantes em colunas e aspectos em linhas, com grade e
  texto centralizado. Diagramas distinguem relações e sequências.
- Prazos aparecem somente quando constam das fontes. Blocos sem cronologia não
  ganham uma linha do tempo artificial.
- Os 94 flashcards têm perguntas explícitas e respostas separadas. O conteúdo
  dos materiais permanece completo apesar da seleção de 100 questões.
- “Toda a aula” reúne os quatro blocos. A seleção por bloco filtra leitura,
  materiais, estatísticas locais e prática; o painel mantém o andamento da aula
  inteira. As aulas anteriores continuam funcionando sem blocos.
- Cada questão nova tem quatro feedbacks específicos, vinculados às alternativas
  mesmo depois de embaralhá-las. Simulados mantêm o avanço sem feedback imediato.

## Correções das fontes

As transcrições foram confrontadas com os slides. O registro detalhado de
conceitos, fontes e divergências está em [aula-7-cobertura.json](aula-7-cobertura.json).
Entre as correções:

- Preparar documentos não equivale a subscrever títulos; captação de recursos
  por empresa não é atividade exclusiva de um tipo de banco.
- Contas descritas para investimento e câmbio não foram tratadas como depósitos
  à vista. A finalidade federal do BNDES foi distinguida da categoria estadual
  de bancos de desenvolvimento.
- Fontes de fomento não foram reduzidas a capital próprio e repasses. A atuação
  prática descrita para SCI não foi transformada em proibição legal da poupança;
  a financeira não foi apresentada como captadora exclusivamente por LC.
- “17/09” da decisão conjunta sobre DTVM significa número 17/2009, não uma data
  de setembro. Conta margem e financiamento por corretoras foram preservados.
- Garantias da B3 não foram tratadas como garantia de retorno do investimento.
- Dedução da base no PGBL não foi confundida com redução automática da alíquota;
  planos coletivos de previdência aberta não foram confundidos com EFPC.
- O pagamento do prêmio não foi atribuído obrigatoriamente ao beneficiário.
  Resseguro não foi apresentado como substituição da responsabilidade da seguradora.
  Capitalização não garante sorteio nem devolução integral de todos os pagamentos.

A revisão confirma coerência com as fontes fornecidas. O acesso independente
a sites oficiais permaneceu bloqueado neste ambiente; esta entrega não certifica
a atualização de cada norma vigente.

## Verificação

Os comandos de verificação são os quatro exigidos em `AGENTS.md`:

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/smoke.py
```

O navegador confere leitura, materiais, filtros, feedbacks, flashcards, temas,
persistência, erros pendentes e simulado por aula. A conferência dos dados
anteriores compara as 600 questões, `AL` e `MAT` das aulas 1 a 6 com a versão
anterior; não apenas seus totais.

Nesta entrega, os **43 testes passaram** (6 do banco, 5 de qualidade e 32 no
navegador), assim como a auditoria de tamanho das alternativas. Os quatro blocos
e seus cinco tipos de material também foram conferidos nos temas claro e escuro
em larguras de 1024, 1280, 1440 e 1920 pixels, sem transbordamento horizontal.
