# Quadro comparativo geral — aula 7

Entrega de 12/10/2026. Síntese adicional dos operadores já presentes na aula;
os mapas, tabelas específicas, resumos, questões e demais materiais permanecem
integralmente preservados.

## Participantes e eixos

O material contém **18 participantes**, não 20: são quatro no bloco 1, quatro
no bloco 2, quatro no bloco 3 e seis no bloco 4. CTVM e DTVM têm linhas próprias;
registro, liquidação, depositária e contraparte central aparecem como funções
da infraestrutura da B3, sem duplicá-las como novas instituições.

| Bloco | Linhas |
| --- | --- |
| Bancos especializados e fomento | Banco de investimento, banco de desenvolvimento, agência de fomento, banco de câmbio |
| Crédito especializado | SCI, companhia hipotecária, financeira/SCFI, SCMEPP |
| Consórcios e mercado de capitais | Administradora de consórcios, bolsas/B3, CTVM, DTVM |
| Seguros, capitalização e previdência | Capitalização, EAPC, EFPC, seguradora, resseguradora, corretor de seguros |

A orientação por **operador nas linhas** foi explicitamente solicitada. Há
sete colunas para manter a comparação legível no PC:

1. **Operador / forma:** nome, sigla, natureza e forma jurídica do material.
2. **Foco e público:** necessidade atendida e público-alvo.
3. **Atuação:** atividades e operações que distinguem o participante.
4. **Recursos / remuneração:** fontes de recursos ou receita de serviços.
5. **Limites e condições:** restrições e requisitos relevantes.
6. **Regulação / supervisão:** competências e órgãos, com escopo quando necessário.
7. **Observações:** particularidades e distinções úteis à revisão.

Recursos do grupo de consórcio são separados da taxa de administração da empresa;
outros encargos contratuais não são apresentados como receita integral da
administradora. Corretagem é remuneração do corretor, não o prêmio da seguradora.
Nos intermediários, taxas e comissões não foram equiparadas a depósitos bancários.

## Conferência de conteúdo

As fontes são os materiais completos já conferidos de `MAT[7]`, as três
transcrições e os 21 slides. Cada linha registra sua origem em `sources`, dentro
de `OPERATOR_OVERVIEW_ROWS`. O quadro do SFN e a aula 5 apoiam a referência de
supervisão financeira e a competência do CNSP sobre corretagem.

Foram mantidas as seguintes ressalvas:

- **SCI:** o quadro da aula prevê poupança; a prática descrita de repasse do SFH
  não é convertida em proibição legal de captar poupança.
- **CH:** inclui imóveis não residenciais, vedação de poupança e autorização
  da CVM para administrar FII, distinta da supervisão financeira.
- **Fomento:** uma por UF, vedação de recursos do público e de transformação;
  fundo de liquidez mínimo de 10% das obrigações, aplicado em títulos federais.
- **Investimento/câmbio:** as contas vinculadas têm condições diferentes; não
  são depósitos à vista. Câmbio não é atividade exclusiva de bancos de câmbio.
- **SCFI:** LC é referência tradicional, não fonte exclusiva; demais instrumentos
  obedecem a suas condições. Risco maior não significa aprovação automática.
- **SCMEPP:** crédito ao público produtivo, vedações de captação/oferta pública,
  DIM e possibilidade de correspondente sem eliminar restrições.
- **B3:** CVM/autorregulação referem-se ao mercado de valores mobiliários; a
  infraestrutura não foi apresentada como exclusivamente supervisionada pela
  CVM. Contraparte central não garante retorno ou valorização.
- **CTVM/DTVM:** supervisão por atividade, conta margem, distinção da conta de
  registro e convergência de atuação; acesso direto das DTVM desde 2009.
- **Previdência:** EAPC coletiva não se torna fechada; EFPC exige vínculo e
  segue CNPC/Previc. PGBL reduz a base, quando aplicável, não a alíquota automática.
- **Seguro/resseguro:** quem paga o prêmio não é necessariamente o beneficiário;
  resseguro não substitui automaticamente a obrigação da seguradora.
- **Corretor:** habilitação/registro e assistência não o tornam segurador.

As fontes não detalham remuneração da B3, custeio da EFPC e receita contratual
de resseguro. Essas três células mostram **Não detalhado na aula**, em cor neutra.
A forma jurídica do banco de câmbio também foi identificada como não detalhada.
Não foram acrescentadas modalidades de resseguradores estrangeiros, garantias
de depósitos, regras tributárias novas ou fontes de financiamento presumidas.

Esta é uma síntese das aulas fornecidas; não uma nova certificação normativa.

## Interface e verificação

- **Material de apoio → Aula 7 → Quadro geral**, ou **Quadro comparativo** na trilha.
- Filtros exclusivos dos quatro blocos e Todos; seleção compartilhada com
  os materiais da aula, mantendo os filtros de prática independentes.
- Azul, lilás, verde e rosa identificam os blocos. Vermelho destaca negativas
  reais e lilás no texto destaca condições; classificações e lacunas ficam neutras.
- Ícones representam funções; cabeçalhos e corpo centralizados com grade completa.
- Cabeçalho e primeira coluna fixos na área de rolagem; tabela ampliável na
  largura da página, com Reduzir/Escape e lâmpada global sempre acessível.
- Ampliação e tema mantêm a posição da tabela; troca de bloco volta ao topo.
- A sessão ativa, seu cronômetro, o histórico e os dados anteriores são preservados.
- A troca para uma aula sem quadro retorna ao mapa mental. Aulas 1, 5 e 6 também
  possuem quadro; entre essas aulas, a aba é mantida. A ampliação desse padrão
  está registrada em `quadros-gerais-comparativos.md`.

Validação funcional em Chromium, nos dois temas, em **1024, 1280, 1440 e 1920 px**.
Os testes 48–52 em `tests/smoke.py` verificam conteúdo, contagem, relações,
filtros, navegação, estado, cores e cabeçalhos fixos. Comparação direta da versão
anterior confirmou igualdade integral de `Q`, `AL` e `MAT`.

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/test_question_design.py
python3 tests/smoke.py
```
