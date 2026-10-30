/* Estudo por conteúdo: relações locais entre assunto + característica.
   Nunca consulta distratores, respostas erradas ou histórico para escolher IDs. */
window.ActiveStudy=(()=>{
 'use strict';
 const fold=value=>String(value??'').replace(/\{\{(?:atencao|negacao)\|([^{}]+)\}\}/g,'$1').replace(/\*\*/g,'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
 const subjects=[
  ['portfolio-weights','Médias e pesos',/medias e pesos|media aritmetica|media ponderada|pesos (?:financeiros|da carteira)|participacoes financeiras/],
  ['portfolio-maturity','Prazo médio e vencimento',/prazo medio|prazos medios|media dos vencimentos/],
  ['asset-history','Retorno histórico do ativo',/retorno historico do ativo|retorno de preco|variacao de cotacao/],
  ['portfolio-history','Retorno histórico da carteira',/retorno historico da carteira|retorno observado da carteira/],
  ['portfolio-expected','Retorno esperado e comparação',/retorno esperado|retornos esperados|projecao de retorno/],
  ['payment-calendar','Cronograma contratual',/fluxo de pagamentos|cronograma contratual|calendario contratual/],
  ['payment-cashflow','Caixa e perspectivas',/fluxo de caixa|caixa e perspectivas|entradas e saidas/],
  ['timevalue','Equivalência temporal',/equivalencia temporal|valor presente|valor futuro|\bvp\b|\bvf\b/],
  ['npv','Valor presente líquido',/valor presente liquido|\bvpl\b/],
  ['payment-net','Cupons e retorno líquido',/cupons e retorno liquido|taxa liquida|retorno liquido|liquido de impostos/],
  ['private-debt','Crédito privado',/credito privado|emissor e divida|titulos? de divida privada/],
  ['debt-yield','Juros e indexadores',/juros e indexadores|remuneracao da divida|remuneracao (?:pre|pos) fixada|remuneracao hibrida/],
  ['debt-repayment','Amortização e resgate',/amortizac|amortizacoes|\bbullet\b|resgate antecipado|resgate pela emissora/],
  ['loan-contract','Empréstimo e mútuo',/\bmutuo\b|\bmutuante\b|\bmutuario\b|emprestimos? bancarios?/],
  ['interest-capitalization','Capitalização financeira',/capitalizacao financeira|capitalizacao simples|capitalizacao composta|juros simples|juros compostos/],
  ['risk-liquidity','Risco de liquidez',/risco(?:s)? de liquidez|liquidez de financiamento|liquidez de mercado|pressao de caixa/],
  ['risk-credit','Risco de crédito',/risco(?:s)? de credito|obrigac(?:ao|oes) do emissor|inadimplencia/],
  ['risk-market','Risco de mercado',/risco(?:s)? de mercado|oscilacoes adversas|desvalorizacao a mercado/],
  ['risk-rates','Risco de juros',/risco(?:s)? (?:de taxa )?de juros|juros e marcacao|marcacao a mercado|sensibilidade a juros|taxa de desconto|fluxo unico|valores de avaliacao|exemplo prefixado/],
  ['rating','Ratings',/\bratings?\b|moodys?|moody s|standard.*poor|fitch|qualidade de credito|escala.*credito/],
  ['creditspread','Spread de crédito',/spread de credito/],
  ['bc','Banco Central',/\b(bacen|bcb|bc|banco central|banco dos bancos|banco do governo|banco emissor)\b/],
  ['cmn','CMN',/\b(cmn|conselho monetario nacional)\b/],['cvm','CVM',/\b(cvm|comissao de valores mobiliarios)\b/],
  ['comoc','Comoc',/\b(comoc|comissao tecnica da moeda e do credito)\b/],['secretaria','Secretaria-Executiva',/\bsecretaria(?: executiva)?\b/],
  ['cnsp','CNSP',/\b(cnsp|conselho nacional de seguros privados)\b/],['susep','Susep',/\b(susep|superintendencia de seguros privados)\b/],
  ['cnpc','CNPC',/\b(cnpc|conselho nacional de previdencia complementar)\b/],['previc','Previc',/\b(previc|superintendencia nacional de previdencia complementar)\b/],
  ['comef','Comef',/\bcomef\b/],
  ['commercial','Bancos comerciais',/\bbancos? comercia(?:l|is)\b/],['multiple','Bancos múltiplos',/\bbancos? multiplos?\b/],['savingsbank','Caixas econômicas',/\bcaixas? economicas?\b/],
  ['coopbank','Banco cooperativo',/\bbancos? cooperativos?\b/],['coop','Cooperativas de crédito',/\bcooperativ[ao]s?( de credito)?\b/],
  ['investment','Bancos de investimento',/\bbancos? de investimentos?\b/],['development','Bancos de desenvolvimento',/\bbancos? de desenvolvimento\b/],
  ['fomento','Agências de fomento',/\bagencias? de fomento\b|^fomento\b/],['fxbank','Bancos de câmbio',/\bbancos? de cambio\b/],
  ['sci','SCI',/\bsci\b|sociedades? de credito imobiliario/],['mortgage','Companhias hipotecárias',/\bcompanhias? hipotecarias?\b|\bch\b/],
  ['scfi','Financeiras',/\bscfi\b|sociedades? de credito financiamento|^financeiras?\b/],['scmepp','SCMEPP',/\bscmepp\b/],
  ['consortium','Consórcios',/\bconsorcios?\b/],['b3','Bolsa e B3',/\b(b3|bolsa|bolsas)\b/],['brokers','CTVM e DTVM',/\b(ctvm|dtvm|corretoras? e distribuidoras?|corretoras? de titulos|distribuidoras? de titulos)\b/],
  ['underwriting','Subscrição e distribuição',/subscri|distribuicao de titulos|distribuir|distribuicao caminho da oferta/],
  ['pledge','Cédula pignoratícia',/pignoratic/],['margin','Conta margem',/conta margem/],['fiduciary','Agente fiduciário',/agente fiduciario/],['pgbl','PGBL',/\bpgbl\b/],
  ['insurancecontract','Contrato de seguro',/\bseguro\b|\bsegurado\b|apolice|indeniza|premio do seguro/],
  ['securities','Valores mobiliários',/^valores mobiliarios\b|investimento coletivo|cedulas? de debentures/],
  ['capitalization','Capitalização',/\bcapitalizacao\b/],['eapc','Previdência aberta',/\beapc\b|previdencia (complementar )?aberta|plano aberto/],
  ['efpc','Previdência fechada',/\befpc\b|previdencia (complementar )?fechada|fundos? de pensao/],
  ['insurer','Seguradoras',/\bseguradoras?\b/],['reinsurance','Resseguro e retrocessão',/\b(ressegur\w*|retrocess\w*)\b/],['insurancebroker','Corretores de seguros',/\bcorretor(?:es)? de seguros?\b|\bcorretagem\b/],
  ['ip','Instituições de pagamento',/\bip\b|instituico?e?s? de pagamentos?|moeda eletronica|iniciador|credenciador|emissor pos pago/],
  ['scd','SCD',/\bscd\b|sociedade de credito direto/],['sep','SEP',/\bsep\b|sociedade de emprestimo entre pessoas/],['fintech','Fintechs',/\bfintechs?\b/],
  ['scr','SCR',/\bscr\b|sistema de informacoes de credito/],['str','STR',/\bstr\b|sistema de transferencia de reservas/],['spi','SPI e Pix',/\b(spi|pix|conta pi)\b|pagamentos? instantaneos?/],
  ['imf','Infraestruturas',/\b(imf|infraestruturas?|ccp|csd|sss|ps)\b|contraparte central|depositaria central|registradora/],
  ['otherpayments','Outros sistemas de pagamento',/\b(sitraf|siloc|compe)\b/],['arrangement','Arranjos e cartões',/\barranjos?\b|instituidor|instituicao domicilio|lojista|compra no debito/],
  ['spb','SPB',/\bspb\b|sistema de pagamentos brasileiro/],['selicsystem','Sistema Selic',/\bsistema selic\b|\bselic\b/],
  ['anbima','ANBIMA',/\banbima\b/],['apimec','APIMEC',/\b(apimec|cnpi)\b/],['ancord','ANCORD',/\bancord\b/],['planejar','Planejar',/^planejar$|planejadores financeiros|\bcfp\b/],
  ['fgc','FGC',/\bfgc\b|garantia ordinaria|contas? conjuntas?/],['fgcoop','FGCoop',/\b(fgcoop|fgc coop|rdc)\b/],['dpge','DPGE',/\bdpge\b|garantia especial/],
  ['freedom','Liberdade econômica',/\bliberdade economica\b|baixo risco|documentos? digitais?|13 874|livre mercado/],
  ['clearing','Clearing e liquidação',/\bclearing\b|compensacao|liquidacao|pos negociacao/],['dvp','Entrega contra pagamento',/\bdvp\b|entrega contra pagamento/],['cetip','Cetip',/\bcetip\b/],
  ['accp','ACCP Brasil',/\baccp\b/],['compulsory','Compulsórios',/\bcompulsori\w*\b/],['lfl','Linhas de liquidez',/\b(lfl|lli|llt)\b|linhas? de liquidez|cestas? de garantias?|colateral/],
  ['flow','Fluxo circular',/fluxo circular|fluxo real|fluxo monetario|mercados? de fatores|familias|bens e servicos/],
  ['fiscal','Política fiscal',/\bfiscal\b|\btribut\w*|orcamento|contas publicas|deficit|divida publica|teto de gastos|tesouro nacional/],
  ['pib','PIB',/\bpib\b|produto interno|produto nominal|produto real|per capita|valor adicionado|dupla contagem|oticas/],
  ['inflation','Inflação e índices',/inflacao|\b(?:ipca|igp m|ipa|incc|ipc)\b|deflacao|indices? de precos/],['inflationtarget','Meta de inflação',/meta de inflacao|metas para a inflacao|meta continua|tolerancia|descumprimento|\bmeta\b/],
  ['selicrate','Taxa Selic e DI',/\b(selic|copom|di)\b|taxa basica|deposito interfinanceiro/],['tr','TR',/\b(tr|tbf)\b|taxa referencial/],['tlp','TLP e TJLP',/\b(tlp|tjlp)\b|taxa de longo prazo/],
  ['spread','Spread',/\bspread\b|taxa de captacao|taxa de aplicacao/],['intermediation','Intermediação e serviços',/intermediacao|superavitario|deficitario|poupadores|tomadores|prestacao de servicos|gerenciamento de recursos/],
  ['usury','Lei da Usura',/lei da usura/],['liquidity','Liquidez',/\bliquidez\b/],['bankclass','Classificação bancária',/operadores monetarios|monetarias|nao monetarias|bancarias|nao bancarias/],
  ['operations','Operações bancárias',/^operacoes$|^as tres operacoes$|^emprestimo$|^financiamento$|\b(ativas?|passivas?|acessorias?)\b|emprestimo x financiamento|emprestimo e financiamento/],
  ['sfn','Estrutura do SFN',/\bsfn\b|sistema financeiro nacional|normativ\w*|supervisor\w*|operacional|quem e quem/],
  ['regulation','Regulação e autorregulação',/\b(heterorregulacao|autorregulacao|regulacao)\b/],
  ['markets','Mercados financeiros',/\bmercados?\b/],['money','Mercado monetário',/\bmonetario\b/],['credit','Mercado de crédito',/\bcredito\b/],['capital','Mercado de capitais',/\bcapitais\b/],['exchange','Mercado de câmbio',/\bcambio\b/],
  ['fxoperations','Operações cambiais',/cambio manual|cambio sacado|pronto|futuro|operacao cambial|operacoes cambiais|liquidacao cambial|dimensoes da operacao|classificacoes cambiais/],
  ['fxregulation','Agentes e regulação cambial',/agentes e regras|agentes e regulacao|no cambio|marco legal|14 286|pessoas fisicas|negociacao regular/],
  ['exportcredit','ACC e ACE',/\b(acc|ace)\b|credito a exportacao|financiamento a exportacao|adiantamento|embarque/],
  ['fxregimes','Regimes cambiais',/regimes? cambiais?|flutuacao|paridade|banda|currency board|defesa do fixo|\bfixo\b/],
  ['cupom','Cupom cambial',/\bcupom\b|retorno em dolares|retorno na moeda estrangeira|reconversao|retorno em reais e retorno/],
  ['swap','Swap e proteção cambial',/\bswaps?\b|protecao|hedge|exposicao|receita e obrigacao|importador|exportador/],
  ['quotation','Cotações e referências',/cotaco?e?s?|cotacao|nominal e convencoes|incerto|direta e inversa|\bspot\b|\bptax\b/],
  ['realfx','Câmbio real',/cambio real|poder de compra|precos relativos|nominal real e cupom/],
  ['fxflows','Juros, risco e divisas',/divisas|juros internos|juros externos|premio de risco|diferencial de juros|juros e capitais|comercio|cambio e atividade/]
 ];
 const orgs=new Set(['bc','cmn','cvm','comoc','secretaria','cnsp','susep','cnpc','previc','comef']);
 const facets=[
  ['members',/compoe|compoem|composicao|quantos membros|quantos diretores|quantas pessoas|presidencia|quem preside|quem coordena|coordenador|integrant|integra |membro|representante|colegiado tem|diretoria.*tem|presidente e.*diretor|presidente.*\+.*diretor|oito diretores|4 diretores|5 diretores|nove membros|cinco membros/],
  ['mandate',/mandato|reconduc|escalonamento|renovacao|inicio.*presidente|terceiro ano|3 ano/],
  ['requirements',/requisito|idoneidade|idoneos|reputacao|notoria|especializacao|capacidade economico|brasileiros/],
  ['appointment',/nomea|indicad|indicac|sabatin|aprova.*diretor|caminho.*diretor|caminho.*dirigente/],
  ['dismissal',/exonera|demissao|demit|desempenho insuficiente|perda.*cargo/],
  ['nature',/natureza|autarquia|autonom|vincula|subordin|sede|regionais|personalidade|patrimonio proprio|forma juridica|sociedade anonima|sociedade limitada|constituida|constituidas|\bs a\b|ltda/],
  ['meetings',/reuni|quorum|convoca|votos|votacao|ad referendum|ordinari|extraordinari|quinzenal|maioria simples|trimestr/],
  ['norms',/resoluco?e?s?|circulares?|instrucoes?|atos normativos|diario oficial|divulgad.*norma/],
  ['powers',/poderes?|investiga|inquerito|intima|requisita|exame de registros/],
  ['penalties',/penalidad|sancao|inabilit|suspensao|advertencia|multas?|proibicao temporaria|ampla defesa|ilicito penal|crime|medidas punitivas/],
  ['functions',/proteger|protege|assegurar|assegura|promover|promove|estimular|estimula|defender|prover|funcao|funcoes|competencia|atribuic|papel|papeis|o que faz|faz o que|finalidade|objetivo|fiscaliza|supervisiona|controla|disciplina|zelar|zela |autoriza|autorizar|executa|emiss[aã]o|impress[aã]o|banco dos bancos|depositario|redesconto|operac|atuacao|atividad|fornece|financia|empresta|concede|intermedia/],
  ['funding',/captac|capta|fontes?|recursos|depositos?|poupanca|remuneracao|rendimento|conta vinculada|lastro|cedula|pignoratic|repasses?|funding/],
  ['audience',/publico|associad|nao associados|clientes|acesso|grupos? elegiveis|empregad|populacao|\bmei\b|microempre/],
  ['limits',/limite|teto|percentual|exposicao|vedac|vedad|permit|proib|condico?e?s?|cobertura|garantia|valor maximo/],
  ['insurance',/premio|indeniza|sinistro|risco segurado|cessao|retrocessao/],
  ['structure',/singular|cooperativas? centrais|^central$|^centrais$|confederacao|piramide|carteiras|controle acionario|acionistas|minimo.*carteira/]
 ];
 const topicRules=[
  [/^Carteiras: médias/,['portfolio-weights']],[/^Carteiras: prazo/,['portfolio-maturity']],
  [/^Carteiras: retorno histórico do ativo/,['asset-history']],[/^Carteiras: retorno histórico da carteira/,['portfolio-history']],
  [/^Carteiras: retorno esperado/,['portfolio-expected']],
  [/^Fluxos: cronograma/,['payment-calendar']],[/^Fluxos: caixa/,['payment-cashflow']],
  [/^Fluxos: equivalência/,['timevalue']],[/^Fluxos: valor presente/,['npv']],[/^Fluxos: cupons/,['payment-net']],
  [/^Crédito privado: emissor/,['private-debt']],[/^Crédito privado: juros/,['debt-yield']],
  [/^Crédito privado: amortização/,['debt-repayment']],[/^Crédito privado: empréstimo/,['loan-contract']],
  [/^Crédito privado: capitalização/,['interest-capitalization']],
  [/^Riscos: liquidez/,['risk-liquidity']],[/^Riscos: crédito e ratings/,['risk-credit','rating']],
  [/^Riscos: spread/,['creditspread']],[/^Riscos: mercado/,['risk-market']],
  [/^Riscos: juros/,['risk-rates']],
  [/^IP:/,['ip']],[/^Fintechs:.*SCR/,['scd','sep','scr']],[/^Fintechs:.*SCD/,['scd']],[/^Fintechs:.*SEP/,['sep']],[/^Fintechs:/,['scd','sep','fintech']],
  [/^SPB:.*STR/,['str']],[/^SPB:.*SPI/,['spi']],[/^SPB:.*sistemas e t.tulos/,['selicsystem','otherpayments']],[/^SPB:.*infraestruturas/,['imf']],[/^SPB:.*arranjo/,['arrangement']],[/^SPB:/,['spb']],
  [/^ANBIMA:/,['anbima']],[/^Garantias:.*DPGE/,['dpge']],[/^Garantias:.*FGCoop/,['fgcoop']],[/^Garantias:/,['fgc']],[/^Liberdade:/,['freedom']],
  [/^Mercados:.*prim.rio/,['markets']],[/^Mercados:.*c.mbio/,['exchange']],[/^Mercados:.*cr.dito/,['credit','capital']],[/^Mercados:/,['markets']],
  [/^Clearing:.*Selic/,['selicsystem']],[/^Clearing:.*Cetip/,['cetip','b3']],[/^Clearing:/,['clearing','dvp','imf']],
  [/^Estabilidade:.*Comef/,['comef']],[/^Estabilidade:/,['accp']],[/^Liquidez:.*compuls.rios/,['compulsory']],[/^Liquidez:/,['lfl']],
  [/^Fluxo:/,['flow']],[/^Fiscal:/,['fiscal']],[/^Indicadores:.*PIB/,['pib']],[/^Indicadores:.*infla/,['inflation']],[/^Indicadores:.*Selic/,['selicrate']],[/^Indicadores:/,['tr','tlp']],
  [/^Mercado:.*opera/,['fxoperations']],[/^Mercado:.*agentes/,['fxregulation']],[/^Mercado:.*exporta/,['exportcredit']],[/^Mercado:.*regimes/,['fxregimes']],
  [/^Cupom:.*retorno/,['cupom']],[/^Cupom:/,['swap']],[/^Taxas:.*cota/,['quotation']],[/^Taxas:.*real/,['realfx']],[/^Taxas:/,['fxflows']]
 ];
 const microRules={
  'portfolio-weights':[['simple',/aritmetic|simples|igual|soma dos valores/],['financial',/valor|posic|participac|financeir|peso/],['normalization',/normaliz|subconjunto|soma dos pesos|total|percentua|decimal/]],
  'portfolio-maturity':[['units',/unidade|convers|equival|decimal|ano.*mes|mes.*ano/],['allocation',/peso|posic|aporte|realoc|valor|participac/],['calendar',/calendario|vencimento|contrat|receb|principal|obrigac|data/]],
  'asset-history':[['base',/preco|cotac|cotad|comprad|percentual|base|inicial|final|taxa/],['sign',/sinal|negativ|positiv|perda|ganho|recuper/],['net',/custos?|despesa|liquid|recebimento/]],
  'portfolio-history':[['weights',/peso|inicia|posic|participac/],['contribution',/contribu|compens|pont|soma|ponder/],['external',/aporte|extern|moviment|saldo|caixa/]],
  'portfolio-expected':[['projection',/previs|projec|estim|esperad|garant|observad/],['allocation',/peso|participac|aloca|intervalo|desvio/],['suitability',/escolh|risco|liquidez|horizonte|necessidade|adequac/]],
  'payment-calendar':[['dates',/emissao|vencimento|data|prazo|aquisic|compra/],['grace',/carencia|incorpora|suspende|isen/],['frequency',/periodicidade|trimestra|semestra|anua|mensal|frequencia/],['components',/cupom|cupons|principal|amortiz|tipo|evento/],['performance',/nao foi pago|atras|nao pagamento|repactu|cumprimento/]],
  'payment-cashflow':[['perspective',/perspectiva|emissora|investidor|sinais|sinal|entrad|said/],['projection',/projec|projetad|previst|realiz|disponiv|cenari/],['acquisition',/compra|comprador|aquisic|preco|despesa|antigo titular/],['diagram',/seta|desenho|altura|escala|linha do tempo/]],
  timevalue:[['present',/presente|descont|data base|avaliac/],['future',/futuro|capitaliz|posterior|frente/],['periods',/periodo|prazo|semestr|meses|ano|expoente|unidade/],['multiple',/cada|dois|varios|soma|parcelas|pagamento/],['factor',/fator|decimal|porcentagem|1 08|0 08/]],
  npv:[['initial',/inicial|investimento|desembolso|data zero|soma completa|dupl|novamente/],['interpretation',/positivo|negativo|zero|excedente|ganho|lucro/],['criterion',/taxa|criterio|comparac|exigida|hipotes/],['flows',/recebimento|despesa|saida|periodo|tribut/]],
  'payment-net':[['coupon',/cupom|cupons|periodic|reaplic|reinvest/],['taxes',/tribut|impost|aliquota|retenc|isenc|isento|brut|liquid/],['base',/principal|capital|rendimento|remunerac|saldo|preco/],['periods',/periodo|anual|semestra|prazo|taxa/],['projection',/projec|garant|cenari|realiz/]],
  'private-debt':[['issuer',/emiss|emit|governo|tesouro|public[ao]|distribu|banco/],['rights',/credor|acionista|socio|societari|capital da|participacao/],['funding',/captac|captar|financ|subscre|subscric|emissao|recursos/],['components',/juros|amortiz|principal|pagamento|extrato/]],
  'debt-yield':[['fixed',/prefixad|pre fixad|taxa fixa|taxa constante/],['indexed',/pos fixad|indexador|referencia|\bcdi\b|variavel/],['hybrid',/hibrid|\bipca\b|inflacao|parcela fixa/],['base',/saldo|amortiz|base|principal/],['comparison',/compar|relatorio|resultado|ranking|coincid|projec/]],
  'debt-repayment':[['bullet',/\bbullet\b|unica|integral.*vencimento|principal.*final/],['partial',/parcia|parcela|constante|variavel|saldo/],['coupon',/juros|cupom|cupons|remunerac/],['early',/antecip|extraordin|opcao|resgate/],['trading',/vend|mercado|outro investidor|transfer/]],
  'loan-contract':[['roles',/mutuante|mutuario|credor|tomador|entrega|fornece|recebe/],['fungible',/fungiv|cedula|equivalente/],['civil',/civil|particulares|pessoas|gratuit|juridic/],['bank',/banc|autoriz|financeir|cooperativa/],['regime',/regime|norma|clausula|disciplina|enquadramento|nome|denominac/]],
  'interest-capitalization':[['simple',/simples|linear|base inicial|capital inicial/],['compound',/compost|incorpor|acumulad|exponencial/],['period',/periodo|prazo|mensal|anual|taxa positiva|unidade/],['flows',/amortiz|fluxos?|pagamento|retirad|reaplic|saldo/],['contract',/contrat|omissao|norma|disciplina|regime juridico/]],
  'risk-liquidity':[['financing',/financiamento|saques?|caixa|honrar|pagar|patrimonio/],['trading',/liquidez de mercado|negoci|vend|convert|convers|comprador|desagio|desconto significativo|valor justo/],['interaction',/descumpr|inadimpl|credor|coexist|intera/]],
  'risk-credit':[['payment',/juros|principal|pagamento|descumpr|inadimpl|obrigac/],['analysis',/capacidade|qualidade|rating|remuneracao|compensacao|retorno|porte|patrimonio/]],
  'risk-market':[['variables',/precos|preco|juros|cambio|indices|acoes/],['valuation',/valor|desvalori|venda|realiza|perda|queda/],['exposure',/ativos|passivos|exposicao|divida|moeda/]],
  'risk-rates':[['pricing',/taxa de desconto|marcacao|valor presente|preco|precos|juros.*sobe|juros.*cai|taxa.*maior|taxa.*menor/],['coupon',/cupom|cupons|periodic/],['maturity',/prazo|vencimento|periodo|semestre/],['flows',/fluxos?|pagamento|recebimento|1 123|1 060|1 040|1 080/],['sensitivity',/sensibilidade|taxa contratada|rendimento/]],
  rating:[['scale',/aaa|aa1|baa|bbb|notac|escala|faixa|classificac/],['limits',/garant|liquidez|mercado|preco|metodologia|revist|risco zero/],['role',/avalia|qualidade|agencia|capacidade|credito/]],
  creditspread:[['definition',/diferenca|diferencial|compar|referencia|spread/],['calculation',/percentuais|calculo|calcular|ao ano|14|10|4/],['limits',/realizado|garant|liquidez|condicoes|moeda|prazo|indexador/]],
  securities:[['shares',/\bacoes\b|\bacao\b/],['debentures',/debenture/],['subscription',/bonus de subscricao/],['notes',/nota comercial|notas comerciais|commercial paper/],['funds',/cotas? de fundos?|fundos? de investimento/],['receipts',/certificados? de deposito|recibos? de deposito|cedulas? de debentures/],['derivatives',/derivativo|futuros?|opcoes|subjacente/],['collective',/investimento coletivo|oferta publica|esforco de terceiros/],['public',/divida publica|divida federal|divida municipal|divida estadual/],['bank',/titulo cambial|titulos cambiais|instituicao financeira|instituicoes financeiras/]],
  bc:[['aims',/objetivo|estabilidade de precos|pleno emprego|flutuacoes.*atividade/],['emission',/emiss|emitir|emite|moeda papel|moeda metalica|divida propria|titulos proprios/],['printing',/imprime|impressao|casa da moeda|producao fisica|produzir cedulas/],['bankofbanks',/banco dos bancos|redesconto|emprestimo.*instituic|recolhimento|compulsorio/],['governmentbank',/banco do governo|reservas internacionais|reservas oficiais|depositario|ouro/],['supervision',/supervisor|fiscaliza|vigilan|inspec/],['authorization',/autoriz|instala|transfer.*sede|fusao|fundida|incorpor|transform|controle acionario|agencia.*exterior/],['monetary',/politica monetaria|operacoes monetarias|compra.*venda.*titulos|compras.*vendas.*titulos/],['exchange',/cambio|capitais estrangeiros/],['credit',/controle do credito/],['secretariat',/secretaria|orcamento monetario|orcamentos monetarios/]],
  cmn:[['aims',/objetivo|liquidez e solvencia|desenvolvimento harmonico|coordenar.*politicas/],['credit',/credito|juros|comissoes|descontos/],['exchange',/cambio|balanco de pagamentos|emprestimo externo/],['budget',/orcamento monetario|orcamentos monetarios/],['accounting',/contabilidade|estatistica/],['capital',/bolsa|corretor|valores mobiliarios/]],
  cvm:[['aims',/objetivo|finalidade|atribuic|estimula|poupanca|mercado de acoes|expand|expansao/],['information',/informac|divulg|transparencia/],['integrity',/fraude|manipula|equitativ|regulares|regularidade|eficient/],['investigation',/investiga|intima|inquerito|examinar|requisita|exame/],['rulemaking',/normativ|regular|regula|regras de conduta/]],
  susep:[['aims',/finalidade|poupanca|direitos|desenvolvimento|concorrencia|estabilidade|liquidez|solvencia/],['supervision',/fiscaliza|supervis|controla/],['investment',/investimento/],['secretariat',/secretaria/]],
  previc:[['supervision',/fiscaliza|supervis|apur|infrac|penal|politicas/],['authorization',/autoriz|constituic|funcionamento|fusao|transferencia/],['intervention',/interven|liquidacao/],['norms',/instruc|procedimento/]],
  inflationtarget:[['change',/antecedencia|36 meses|mudanca|mudar|alterac|tolerancia.*vigor|anuncia/],['continuous',/continua|12 meses|doze meses|janela|mensal|mes a mes|dezembro|ano civil/],['breach',/descumpr|carta|comunicacao.*fazenda|fora.*intervalo|fora.*tolerancia|prazo.*retorno|seis meses|\b6 meses\b/],['roles',/quem define|quem estabelece|definida|define|conduz|persegue|copom/],['principles',/autonomia|transparencia|publica|sigilo|incentivo|prestacao de contas|responsabiliza|elemento/],['history',/1999/]],
  ip:[['nature',/natureza|instituicao financeira|instituicoes financeiras|servicos|autorizacao|autoriza/],['electronic',/moeda eletronica|pre pago|conta pre paga/],['postpaid',/pos pago|pos paga|credito/],['acquirer',/credenciador|credencia|habilita|lojista/],['initiator',/iniciador|iniciacao|sem deter|sem movimentar/],['accounts',/contas?|saldo|recursos.*cliente|patrimonio|arranjo|instituidor/]],
  fgc:[['limits',/limite|teto|250|milhao|milhoes|quatro anos|4 anos|conglomerado/],['covered',/produtos|cobert|cdb|rdb|lci|lca|letra|fundos?|debenture|financeira|tesouro|poupanca/],['joint',/conjunt|titulares|rateio|divisao|do saldo|por titular/],['nature',/natureza|associacao|privad|finalidade|estabilidade|confianca|seguro/],['funding',/contribuic|associadas|0 01|0 025/]],
  fxregimes:[['fixed',/\bfixo\b|defende.*paridade|defesa.*paridade/],['pure',/pura|livre|limpa/],['managed',/administrad|suja|intervencao eventual/],['band',/banda|faixa|rastejante|deslizante/],['board',/currency board|lastro/]],
  quotation:[['inverse',/direta|inversa|incerto|certo|reciproca|r por us|us por r|perspectiva/],['spot',/spot|negociada|negocio/],['ptax',/ptax|referencia|metodologia|boletim|cotacoes elegiveis/]],
  imf:[['ccp',/\bccp\b|contraparte central|novacao/],['csd',/\bcsd\b|depositaria central|custodia/],['tr',/\btr\b|registrador|registro/],['sss',/\bsss\b|liquidacao de titulos/],['ps',/\bps\b|sistema de pagamento|liquidacao de fundos/]],
  operations:[['active',/ativa|emprestimo|financiamento|aplicacao|credor/],['passive',/passiva|captacao|deposito|devedor|emissao/],['services',/acessoria|servico|tarifa|cobranca/]],
  pib:[['views',/otica|consumo|investimento|exportac|importac|renda|despesa/],['nominal',/nominal|real|precos correntes|quantidades|deflator/],['percapita',/per capita|populacao|distribuicao/],['added',/valor adicionado|dupla contagem|intermediari|faturamento/],['scope',/producao|territorio|periodo|estoque|fluxo|bens finais|usados|transferencia/]],
  fiscal:[['instruments',/instrumento|tribut|impost|gasto|despesa/],['orientation',/expansionista|contracionista|expansao|contracao|mistas|misto|demanda|transmissao/],['balance',/primario|nominal|deficit|superavit|divida|financiamento|estoque/],['rules',/teto|arcabouco|responsabilidade|sustentabilidade|regra|constituc|200|95/],['aims',/objetivo|alocativa|distributiva|estabiliza/]],
  inflation:[['indices',/ipca|igp m|ipa|ipc|incc|indice|cesta/],['general',/inflacao|deflacao|desaceleracao|nivel de precos|generalizada/],['compound',/acumulad|composicao|fatores|meses|multiplica/]],
  flow:[['agents',/familia|empresas|governo|fatores|mercado/],['circuits',/real|monetario|pagamento|renda|sentido|circuito/],['decisions',/decisoes|poupanca|investimento|repercussoes|consumo|demanda/]],
  lfl:[['lines',/\blli\b|\bllt\b|linha|prazo|liquidez|solvencia|elegib|acesso/],['collateral',/garantia|colateral|cesta|ativo|titulo|cdb|capital|rating/]],
  arrangement:[['roles',/instituidor|credenciador|emissor|domicilio|papel|papeis|lojista|participante|repasse/],['oversight',/supervisao|supervision|referencia|limite|volume|20 bilhoes|500/]],
  insurancecontract:[['premium',/premio/],['indemnity',/indeniza|sinistro/],['roles',/contratante|beneficiario|segurad|corretor|papel|papeis/]],
  anbima:[['mission',/missao|natureza|representa|informar|educar|fortalecer|confianca/],['hierarchy',/hierarquia|cvm|banco central|regulacao estatal|normas estatais|complementa/],['commitment',/compromisso|transparencia|etica|integridade|informacoes|dever|praticas/],['adherence',/adesao|aderente|associad|participante|aderir/],['sources',/fonte|deliberac|parecer|vinculante|normativo|codigo/],['certification',/apimec|ancord|planejar|cnpi|certifica|analista/]]
 };
 function microFacets(owners,text){const t=fold(text);return owners.flatMap(owner=>(microRules[owner]||[]).filter(([,pattern])=>pattern.test(t)).map(([key])=>owner+':'+key))}
 const focused=new Set(['members','mandate','appointment','requirements','dismissal','nature','meetings','norms']);
 // Relações editoriais: o assunto também é efetivamente cobrado na questão,
 // e não apenas citado no contexto ou nos distratores. IDs continuam estáveis.
 const privateCreditCrossTopics={1257:['debt-repayment'],1258:['loan-contract'],1259:['loan-contract'],1260:['debt-repayment'],1266:['debt-repayment'],1269:['debt-repayment'],1273:['debt-yield'],1276:['debt-yield'],1288:['interest-capitalization'],1289:['interest-capitalization'],1290:['private-debt'],1299:['debt-yield','debt-repayment'],1300:['debt-repayment']};
 const portfolioCrossTopics={1356:['portfolio-history'],1357:['portfolio-maturity'],1359:['portfolio-history'],1360:['portfolio-expected'],1379:['portfolio-expected'],1380:['payment-net'],1390:['payment-cashflow'],1395:['portfolio-history'],1400:['portfolio-history']};
 const paymentCrossTopics={1303:['payment-cashflow'],1306:['debt-repayment','payment-net'],1307:['debt-repayment'],1316:['payment-net'],1323:['interest-capitalization'],1324:['interest-capitalization'],1330:['interest-capitalization'],1332:['payment-cashflow'],1336:['payment-cashflow'],1337:['payment-cashflow'],1340:['payment-net'],1341:['timevalue'],1343:['debt-yield'],1347:['interest-capitalization'],1350:['payment-cashflow']};
 const found=text=>{const t=fold(text);let ids=subjects.filter(([, ,re])=>re.test(t)).map(([id])=>id);if(ids.includes('selicrate')&&/taxa selic|meta selic|taxa basica|copom/.test(t)&&!/sistema selic|custodia|liquidacao/.test(t))ids=ids.filter(id=>id!=='selicsystem');return ids};
 const aspects=text=>{const t=fold(text);return facets.filter(([,re])=>re.test(t)).map(([id])=>id)};
 const unique=list=>[...new Set(list)];
 function reduce(ids,lesson){
  let out=unique(ids);
  const remove=id=>out=out.filter(x=>x!==id);
  if(out.includes('npv'))remove('timevalue');
  if(out.includes('interest-capitalization'))remove('capitalization');
  if(out.includes('risk-liquidity'))remove('liquidity');
  if(out.some(id=>['risk-credit','rating','creditspread'].includes(id)))remove('credit');
  if(out.includes('creditspread'))remove('spread');
  if(out.includes('coopbank'))remove('coop');
  if(lesson===8&&out.includes('imf'))remove('tr');
  if(out.includes('insurancebroker'))remove('brokers');
  if(out.includes('selicsystem')&&out.includes('selicrate'))remove(lesson===11?'selicsystem':'selicrate');
  if(out.includes('dpge'))remove('fgc');
  if(out.some(id=>['fomento','investment','development','fxbank','scfi','sci','mortgage','scmepp','scd','sep','commercial','multiple','coop','coopbank'].includes(id)))remove('credit');
  if(out.some(id=>['fxoperations','fxregulation','fxregimes','cupom','swap','quotation','realfx','fxflows','exportcredit'].includes(id))){remove('exchange');remove('markets')}
  if(out.some(id=>['selicsystem','str','spi','imf','cetip','dvp'].includes(id)))remove('clearing');
  if(out.some(id=>!['sfn','markets','regulation','liquidity','money','credit','capital','exchange'].includes(id))){remove('sfn');remove('markets')}
  return out;
 }
 function questionProfile(q,id){
  const [lesson,topic,,stem,correct]=q,t=fold(topic),s=fold(stem),body=stem+' '+correct;
  const rule=topicRules.find(([re])=>re.test(topic));
  let owners=rule?[...rule[1]]:reduce(found(topic),lesson),parts=[];
  if(rule&&owners.length>1){const detected=reduce(found(body),lesson),specific=owners.filter(o=>detected.includes(o));if(specific.length)owners=specific;}
  if(lesson===13&&/^Crédito privado:/.test(topic))owners.push(...(privateCreditCrossTopics[id]||[]));
  if(lesson===13&&/^Carteiras:/.test(topic))owners.push(...(portfolioCrossTopics[id]||[]));
  if(lesson===13&&/^Fluxos:/.test(topic))owners.push(...(paymentCrossTopics[id]||[]));
  const base={2:'cmn',3:'bc',4:'cvm'}[lesson];
  if(base&&!rule){
   if(/comoc/.test(t))owners=['comoc'];else if(/secretaria/.test(t))owners=['secretaria'];
   else if(/meta de inflacao|politica monetaria|descumprimento/.test(t))owners=['inflationtarget'];
   else if(/compulsorios/.test(t))owners=['compulsory'];
   else if(!owners.length||owners.every(o=>['sfn','regulation','markets','capital','exchange','money'].includes(o)))owners=[base];
   if(/x |comparacao/.test(t)){const explicit=reduce(found(stem+' '+correct),lesson).filter(o=>orgs.has(o));if(explicit.length)owners=explicit;}
   if(lesson===4&&/valores mobiliarios/.test(t))owners=['securities'];
  }
  if(lesson===5&&!owners.length)owners=reduce(found(body),lesson).filter(o=>['cnsp','susep','cnpc','previc','eapc','efpc','insurer','capitalization','reinsurance','insurancebroker'].includes(o));
  if(lesson===1){
   if(/spread/.test(t))owners=['spread'];
   else if(/agentes|intermediacao|servicos|vantagens/.test(t))owners=['intermediation'];
   else if(/regulacao/.test(t))owners=['regulation'];
   else if(/lei da usura/.test(t))owners=['usury'];
   else if(/liquidez/.test(t))owners=['liquidity'];
   else if(/mercados/.test(t)){owners=reduce(found(stem+' '+correct),lesson).filter(o=>['money','credit','capital','exchange','eapc','efpc','insurer'].includes(o));if(!owners.length)owners=['markets'];}
   else if(/estrutura|quadro|mnemonico/.test(t)){owners=reduce(found(body),lesson).filter(o=>orgs.has(o)||['eapc','efpc','insurer','capitalization'].includes(o));if(!owners.length)owners=['sfn'];}
  }
  if(lesson===6&&/operacoes/.test(t))owners=['operations'];
  if(lesson===6&&/classificacao/.test(t))owners=['bankclass'];
  if(!owners.length)owners=reduce(found(body),lesson);
  // Características são determinadas pelo que é cobrado, não por distratores.
  parts=aspects(body);
  if(owners.some(o=>orgs.has(o))){
   const exact={natureza:'nature',vinculacao:'nature',sedes:'nature',composicao:'members',presidencia:'members',nomeacao:'appointment',requisitos:'requirements',exoneracao:'dismissal',mandato:'mandate',reunioes:'meetings',quorum:'meetings',decisoes:'meetings',normas:'norms'}[t];
   if(exact&&!/considere|afirmacoes|analise|verifique|avalie/.test(s))parts=[exact];
   else if(/diretoria e mandato|diretoria/.test(t)){parts=parts.filter(x=>focused.has(x));if(!parts.length)parts=['members'];}
   else if(/natureza e funcoes/.test(t)){const focus=parts.filter(x=>focused.has(x));parts=focus.length?focus:['functions'];}
   else if(/atribuicoes|competencias|objetivos|funcoes|autorizacao|poderes/.test(t))parts=['functions',...parts.filter(x=>x==='norms')];
   else if(/natureza e vinculacao/.test(t))parts=['nature',...parts.filter(x=>['appointment','mandate','dismissal'].includes(x))];
   if(!parts.length)parts=['functions'];
  }
  if(lesson===4&&/poderes/.test(t))parts=unique([...parts,'powers']);
  if(lesson===4&&/penalidades/.test(t))parts=unique([...parts,'penalties']);
  if(/regulacao/.test(t))owners.push('regulation');
  if(owners.some(o=>orgs.has(o))&&!/considere|afirmacoes|analise|verifique|avalie/.test(s)){
   if(/reuniao|reunioes|quorum|convoca|votacao|presenca minima/.test(s))parts=['meetings'];
   else if(!/compoe|compoem|composicao|quantos|quantas|quem.*preside|coordenador|presidencia|quem faz parte|integra|representante|representacao|oito diretores|membro votante/.test(s)&&!/^diretoria$/.test(t))parts=parts.filter(f=>f!=='members');
  }
  if(id===328||[287,290,321].includes(id))parts=['functions'];
  const supplemental=found(body).filter(o=>['underwriting','pledge','margin','fiduciary','pgbl','insurancecontract'].includes(o));
  owners.push(...supplemental);
  // Negociabilidade do ativo é o mesmo conceito nas aulas 1 e 13;
  // necessidade de caixa para obrigações permanece uma dimensão distinta.
  if(owners.includes('liquidity'))owners.push('risk-liquidity');
  if(owners.includes('risk-liquidity')&&/negoci|vend|convert|convers|valor justo/.test(fold(body)))owners.push('liquidity');
  if(lesson===13&&owners.includes('creditspread')&&/banco.*capta|intermediacao|spread bancario/.test(fold(body)))owners.push('spread');
  // Relações secundárias exigem o nome do risco no enunciado/correta.
  owners.push(...found(body).filter(o=>['risk-liquidity','risk-credit','risk-market','risk-rates'].includes(o)));
  if(lesson===9&&/comparacoes institucionais/.test(t))owners=reduce(found(body),lesson).filter(o=>['anbima','apimec','ancord','planejar'].includes(o));
  return {id,lesson,owners:unique(owners),facets:unique(parts),micro:microFacets(owners,body),topic,stem};
 }
 let bankCache=null;
 function bank(){if(bankCache?.length===Q.length)return bankCache.profiles;const profiles=Q.map((q,i)=>questionProfile(q,i+1));bankCache={length:Q.length,profiles};return profiles;}
 const entitySubjects=new Set(['commercial','multiple','savingsbank','coopbank','coop','investment','development','fomento','fxbank','sci','mortgage','scfi','scmepp','consortium','b3','brokers','capitalization','eapc','efpc','insurer','reinsurance','insurancebroker','ip','scd','sep']);
 const broadSubjects=new Set(['sfn','markets','money','credit','capital','exchange','regulation','clearing','bankclass']);
 function headingSubjects(label,lesson){
  let ids=reduce(found(label),lesson);
  const named=ids.filter(id=>!broadSubjects.has(id));
  if(named.length)ids=named;
  else if(!/^(?:mercado(?:s)? de |monetario$|credito$|capitais$|cambio$)/.test(fold(label)))ids=[];
  if(ids.includes('inflationtarget'))ids=ids.filter(id=>id!=='inflation');
  return ids;
 }
 function inheritedSubjects(source){
  const {lesson,label='',parents=[],whole=false}=source;
  const own=headingSubjects(label,lesson),ancestry=parents.slice(1);
  const contexts=ancestry.map(h=>headingSubjects(h,lesson));
  const entity=contexts.map(ids=>ids.filter(id=>entitySubjects.has(id))).find(ids=>ids.length);
  let context=entity||[...contexts].reverse().find(ids=>ids.length);
  const rootOrgs=reduce(found(parents[0]||''),lesson).filter(id=>orgs.has(id));
  if(!context?.length)context=rootOrgs;
  if(!context.length)return null;
  if(entity?.length)return entity;
  const refinements={imf:['selicsystem','str','spi','b3','cetip','otherpayments','dvp'],spb:['imf','selicsystem','str','spi','ip','arrangement','otherpayments'],fgc:['dpge','fgcoop']};
  const refined=own.filter(id=>context.some(parent=>refinements[parent]?.includes(id)));
  if(refined.length)return refined;
  const institution=context.filter(id=>orgs.has(id));
  const membership=ancestry.some(h=>/composicao|diretoria|colegiado|membros|participantes/.test(fold(h)));
  if(institution.length){
   if(membership)return institution;
   // A new, explicitly named group may introduce a comparison or another
   // concept. A sentence that merely cites an institution cannot do so.
   const explicit=whole&&fold(label).split(' ').length<=8?own.filter(id=>!broadSubjects.has(id)):[];
   if(explicit.length&&!explicit.every(id=>context.includes(id)))return explicit;
   const same=own.filter(id=>context.includes(id));return same.length?same:context;
  }
  // A named concept (meta de inflação, PTAX, regime cambial...) supplies
  // the meaning of roles and facts inside it, even when they cite an organ.
  if(context.includes('creditspread')&&/spread bancario/.test(fold(label)))return ['spread'];
  return context;
 }
 function profile(source){
  const {lesson,label='',text='',parents=[],whole=false,ownerHints=[],lockOwners=false}=source;
  const headings=[label,...[...parents].reverse()];
  const institutionHeadings=whole?headings:[...[...parents].reverse(),label];
  const institution=institutionHeadings.map(h=>reduce(found(h),lesson).filter(o=>orgs.has(o))).find(a=>a.length);
  let owners=[];
  for(const h of headings){const hits=reduce(found(h),lesson);if(hits.length){owners=hits;break}}
  if(owners.length===1&&['sfn','markets','regulation','spb','fintech'].includes(owners[0]))owners=unique([...owners,...reduce(found(text),lesson)]);
  if(!owners.length)owners=reduce(found(text),lesson);
  if(lesson===6){const hints=fold(label+' '+text);if(!owners.length){if(/singular|centrais|confederac|nao associad/.test(hints))owners=['coop'];else if(/carteira|multiplo|cnpj/.test(hints))owners=['multiple'];else if(/acoes com voto|50.*acao|51/.test(hints))owners=['coopbank'];else if(/deposito a vista/.test(hints))owners=['bankclass'];}}
  if(lesson===7&&!owners.length){const hints=fold(label+' '+text);if(/investimento|capital fixo|capital de giro/.test(hints))owners=['investment'];else if(/sorteio|lance|consorciad|categoria|fornecedor/.test(hints))owners=['consortium'];else if(/lim[ií]trofe/.test(hints))owners=['development'];else if(/formacao de preco/.test(hints))owners=['b3'];}
  const inherited=inheritedSubjects(source);if(inherited?.length)owners=inherited;
  // Um fragmento de diretoria herda seu órgão; citar BC como membro do CMN não
  // transforma o fragmento em composição do próprio BC.
  let fs=aspects(label+' '+text),labelFacets=aspects(label),parentFacets=[];
  for(const h of [...parents].reverse()){const f=aspects(h);if(f.length){parentFacets=f;break}}
  if(labelFacets.length)fs=labelFacets;
  if(/^(diretoria|composicao|dirigentes)|^colegiado.*(?:membro|diretor|presiden|composicao)/.test(fold(label))){fs=aspects(text).filter(f=>['members','mandate','appointment','requirements','dismissal'].includes(f));if(!fs.length)fs=['members'];}
  if(owners.some(o=>orgs.has(o))){
   const localFocus=labelFacets.filter(f=>focused.has(f));
   const parentFocus=[...parents].reverse().map(h=>/^caminho$/.test(fold(h))?['appointment']:aspects(h).filter(f=>focused.has(f))).find(fs=>fs.length)||[];
   if(localFocus.length)fs=localFocus;
   else if(/^caminho$/.test(fold(label)))fs=['appointment'];
   else if(parentFocus.length)fs=parentFocus;
   else if(whole&&fs.some(f=>focused.has(f)))fs=fs.filter(f=>focused.has(f));
   fs=fs.filter(f=>!['structure','audience','funding','insurance','limits'].includes(f));
  }
  if(!fs.length)fs=parentFacets.filter(f=>!owners.some(o=>orgs.has(o))||!['structure','audience','funding','insurance','limits'].includes(f));
  if(institution&&fs.some(f=>focused.has(f))&&owners.every(o=>orgs.has(o))){owners=institution;}
  if([2,3].includes(lesson)&&/prestacao de contas|carta.*fazenda|nota no relatorio|descumprimento|calendario da meta/.test(fold(label+' '+text))&&!/mandato|exoneracao|nomeacao/.test(fold(label)))owners=['inflationtarget'];
  const hinted=reduce(ownerHints.flatMap(found),lesson);
  if(hinted.length&&(lockOwners||!owners.some(o=>orgs.has(o))||hinted.some(o=>orgs.has(o))))owners=hinted;
  else if(whole&&!inherited?.length&&!owners.some(o=>orgs.has(o))&&!reduce(found(label),lesson).length)owners=reduce([...owners,...found(text)],lesson);
  if(lesson===13){
   const riskIds=new Set(['portfolio-weights','portfolio-maturity','asset-history','portfolio-history','portfolio-expected','risk-liquidity','risk-credit','risk-market','risk-rates','rating','creditspread','spread','private-debt','debt-yield','debt-repayment','loan-contract','interest-capitalization','payment-calendar','payment-cashflow','timevalue','npv','payment-net']);
   const convert=ids=>unique(ids.map(id=>({liquidity:'risk-liquidity',credit:'risk-credit',markets:'risk-market'}[id]||id)).filter(id=>riskIds.has(id)));
   const anchor=value=>{const t=fold(value);
    if(/^medias e pesos|^media aritmetica|^media ponderada|^pesos da carteira|^pesos em reais|^conferencia da media|^soma dos pesos de uma carteira|^subconjunto/.test(t))return ['portfolio-weights'];
    if(/^prazo medio|^media e calendario|^vencimento contratual|^parte decimal do ano|^exemplo proprio de prazo|^equivalencia de um ano|^calendario dos titulos/.test(t))return ['portfolio-maturity'];
    if(/^retorno historico do ativo|^preco.*taxa|^variacao de cotacao/.test(t))return ['asset-history'];
    if(/^retorno historico da carteira|^carteira.*contribuicao/.test(t))return ['portfolio-history'];
    if(/^retorno esperado|^historico.*esperado/.test(t))return ['portfolio-expected'];
    if(/^antes da conta$/.test(t))return ['portfolio-weights','portfolio-maturity','asset-history','portfolio-history','portfolio-expected'];
    if(/^exemplo proprio de retorno|^pontos percentuais/.test(t))return ['portfolio-history','portfolio-expected'];
    if(/^nao misture bases/.test(t))return ['portfolio-weights','portfolio-history'];
    if(/^uma perda pode coexistir/.test(t))return ['portfolio-history'];
    if(/^passado.*promessa|^taxas precisam conversar|^comparacoes$/.test(t))return ['asset-history','portfolio-history','portfolio-expected'];
    if(/^valor presente liquido|^vpl\b|^interpretacao do vpl/.test(t))return ['npv'];
    if(/^equivalencia temporal|^valor presente\b|^valor futuro\b|^varios fluxos|^para a frente|^para tras|^taxa semestral/.test(t))return ['timevalue'];
    if(/^cronograma\b|^fluxo de pagamentos|^marcos$|^carencia\b/.test(t))return ['payment-calendar'];
    if(/^caixa e perspectivas|^fluxo de caixa|^perspectiva\b|^primeiro o calendario|^quem esta olhando/.test(t))return ['payment-cashflow'];
    if(/^cupons e retorno liquido|^taxa liquida|^saldo e rendimento|^bruto\b|^reinvestimento de cupons|^desconto financeiro|^liquido\b/.test(t))return ['payment-net'];
    if(/^emissor e divida|^credito privado|^ativos de credito privado/.test(t))return ['private-debt'];
    if(/^juros e indexadores|^remuneracao\b|^referencias$|^prefixada\b|^pos fixada\b|^hibrida\b/.test(t))return ['debt-yield'];
    if(/^amortizacao|^resgate\b|^principal e juros|^pagamentos$|^sair antes|^bullet\b/.test(t))return ['debt-repayment'];
    if(/^emprestimo e mutuo|^mutuo\b|^mutuante\b|^emprestimo bancario/.test(t))return ['loan-contract'];
    if(/^capitalizacao\b|^simples$|^composta$|^tres perguntas independentes/.test(t))return ['interest-capitalization'];
    if(/^spread bancario e spread de credito/.test(t))return ['spread','creditspread'];
    if(/^spread de credito/.test(t))return ['creditspread'];
    if(/^ratings?\b|^agencias? de (?:risco|rating)/.test(t))return ['rating'];
    if(/^liquidez\b|^duas perspectivas da liquidez|^da pressao de caixa/.test(t))return ['risk-liquidity'];
    if(/^credito$|^qualidade de credito e compensacao/.test(t))return ['risk-credit'];
    if(/^mercado$|^risco de mercado/.test(t))return ['risk-market'];
    if(/^retorno exigido/.test(t))return ['risk-credit'];
    if(/^patrimonio.*caixa|^desconto grande|^financiamento.*caixa/.test(t))return ['risk-liquidity'];
    if(/^juros e principal/.test(t))return ['risk-credit','risk-market'];
    if(/^cupom\b|^vencimento$|^prazo (?:restante|original)|^taxa (?:alta|contratada)|^antes de chamar de perda|^r 1 060.*cupom|^juros compostos|^fluxo prefixado|^desconto do fluxo/.test(t))return ['risk-rates'];
    if(/^juros\b|^sensibilidade\b|^fluxo unico|^exemplo prefixado|^marcacao aos|^bases de comparacao dos exemplos/.test(t))return ['risk-rates'];
    return null;
   };
   const hintedAnchor=lockOwners?unique(ownerHints.flatMap(h=>anchor(h)||[])):[];
   const parentAnchor=parents.slice(1).map(anchor).find(Boolean);
   const primary=hintedAnchor.length?hintedAnchor:parentAnchor||anchor(label);
   owners=primary||convert(owners);
   if(!owners.length){for(const h of headings){const ids=convert(reduce(found(h),lesson));if(ids.length){owners=ids;break}}}
   if(!owners.length)owners=convert(reduce(found(text),lesson));
   if(whole&&!primary)owners=unique([...owners,...convert(reduce(found(text),lesson))]);
  }
  let micro=microFacets(owners,label+' '+text);
  if(!micro.length)micro=microFacets(owners,[...parents].reverse().find(p=>microFacets(owners,p).length)||'');
  if(whole&&lesson===13&&['medias e pesos','prazo medio e vencimento','retorno historico do ativo','retorno historico da carteira','retorno esperado e comparacao','emissor e divida','juros e indexadores','amortizacao e resgate','emprestimo e mutuo','capitalizacao financeira','cronograma contratual','caixa e perspectivas','equivalencia temporal','valor presente liquido','cupons e retorno liquido'].includes(fold(label)))micro=[];
  return {owners:unique(owners),facets:unique(fs),micro};
 }
 function directMatching(source){
  const p=profile(source);if(!p.owners.length)return [];
  return bank().filter(q=>{
   if(!q.owners.some(o=>p.owners.includes(o)))return false;
   const shared=q.owners.filter(o=>p.owners.includes(o));
   const relevantMicro=p.micro.filter(m=>shared.includes(m.split(':')[0])&&(!orgs.has(m.split(':')[0])||!p.facets.some(f=>focused.has(f))));
   if(relevantMicro.length&&!q.micro.some(m=>relevantMicro.includes(m)))return false;
   if(shared.some(o=>orgs.has(o))&&p.facets.length){if(!q.facets.some(f=>p.facets.includes(f)))return false;}
   // Características bancárias específicas também separam captação de público.
   if(shared.some(o=>['investment','development','fomento','fxbank','sci','mortgage','scfi','scmepp','commercial','multiple','coop','coopbank'].includes(o))&&p.facets.length===1&&q.facets.length&&!q.facets.includes(p.facets[0]))return false;
   return true;
  }).map(q=>q.id);
 }
 const matchCache=new WeakMap();
 function matching(source){
  const previous=matchCache.get(source);if(previous?.stamp===Q.length)return [...previous.ids];
  // A panel covers both its own concept and all concepts visibly contained
  // in it. Shared questions count once, regardless of the number of labels.
  const ids=unique([...directMatching(source),...(source.concepts||[]).flatMap(matching)]).sort((a,b)=>a-b);
  matchCache.set(source,{stamp:Q.length,ids});return [...ids];
 }
 const entries=new Map(),keys=new Map();let nextKey=0,chooser=null;
 const DENSE_SCOPE='.mind-branch,.diagram-group,.diagram-sequence,.material-time-panel,.operator-overview,.visual-map-panel';
 function register(source){
  const signature=JSON.stringify(source);let key=keys.get(signature);
  if(key===undefined){key=String(++nextKey);keys.set(signature,key);entries.set(key,{source,stamp:0,ids:[]})}
  const entry=entries.get(key);if(entry.stamp!==Q.length){entry.ids=matching(source);entry.stamp=Q.length}
  return {key,...entry};
 }
 function footer(node,source,after=false){
  if(!node||node.dataset.activeStudy)return;
  const scope=node.closest(DENSE_SCOPE);
  const container=source.whole&&after&&node.parentElement?.classList.contains('mind-group')?node.parentElement:
   source.whole&&node.matches('th')?node.closest('[data-operator]'):node;
  const choices=source.whole?unique([...container.querySelectorAll('[data-active-study]')].filter(child=>child!==node).map(child=>child.dataset.activeStudy)):[];
  const concepts=choices.map(key=>entries.get(key)?.source).filter(Boolean);
  const entry=register(concepts.length?{...source,concepts}:source),count=entry.ids.length;
  node.dataset.activeStudy=entry.key;
  // Os vínculos finos ficam disponíveis no seletor, fora do desenho do conteúdo.
  if(scope&&scope!==node)return;
  const box=document.createElement('div');
  box.className='active-study-action';box.dataset.activeStudyKey=entry.key;
  const button=document.createElement('button');button.type='button';button.className='active-study-button';button.disabled=!count;
  button.innerHTML=uiIcon('book')+'<span>Questões</span>';
  button.setAttribute('aria-label',`Fazer questões sobre ${source.label||source.parents?.at(-1)||'este conteúdo'}: ${count} ${count===1?'disponível':'disponíveis'}`);
  button.addEventListener('click',()=>start(entry.key,box));
  const total=document.createElement('span');total.className='active-study-count';total.textContent=`${count} ${count===1?'disponível':'disponíveis'}`;box.append(button,total);
  if(!count)button.title='Ainda não há questões vinculadas a este conteúdo específico.';
  if(choices.length){
   box.classList.add('active-study-scope');
   const refine=document.createElement('button');refine.type='button';refine.className='active-study-options-trigger';
   refine.innerHTML='<span>Por conceito</span>'+uiIcon('filter');refine.setAttribute('aria-haspopup','dialog');
   refine.setAttribute('aria-label',`Escolher conceito em ${source.label}`);
   refine.onclick=()=>openChooser(entry.key,choices);box.append(refine);
  }
  if(after)node.after(box);else node.append(box);
 }
 function closeChooser(restore=true){
  if(!chooser)return;
  const previous=chooser;chooser=null;previous.dialog.close();previous.dialog.remove();
  if(restore)document.querySelector(`[data-active-study-key="${previous.key}"] .active-study-options-trigger`)?.focus({preventScroll:true});
 }
 function openChooser(key,choices){
  const entry=entries.get(String(key));if(!entry)return;closeChooser(false);
  const dialog=document.createElement('dialog');dialog.className='active-study-dialog';dialog.setAttribute('aria-labelledby','active-study-dialog-title');
  dialog.innerHTML=`<header class="active-study-dialog-head"><div><span>ESTUDO POR CONTEÚDO</span><h2 id="active-study-dialog-title">Escolher conceito</h2></div><div><button type="button" class="active-study-dialog-theme" aria-label="Alternar tema na seleção de questões">${uiIcon('bulb')}</button><button type="button" class="active-study-dialog-close" aria-label="Fechar seleção de conceitos">${uiIcon('cross')}</button></div></header><div class="active-study-dialog-content"><p class="active-study-dialog-scope">${escapeText(entry.source.label)}</p><label class="active-study-dialog-search" for="active-study-concept-search">Buscar neste conteúdo<div>${uiIcon('search')}<input id="active-study-concept-search" type="search" placeholder="Nome do conceito ou característica" maxlength="160" autocomplete="off"></div></label><p class="active-study-dialog-help">Escolha o conjunto completo ou um conceito específico. Uma questão pode aparecer em vários conceitos; o total do quadro conta cada questão uma única vez. As contagens dos conceitos não devem ser somadas.</p><div id="active-study-choices"></div></div>`;
  document.body.append(dialog);chooser={dialog,key:String(key),choices:[...choices],query:''};
  dialog.querySelector('.active-study-dialog-close').onclick=()=>closeChooser();
  dialog.querySelector('.active-study-dialog-theme').onclick=()=>document.getElementById('theme-toggle')?.click();
  dialog.querySelector('input').oninput=event=>{if(!chooser)return;chooser.query=event.target.value;paintChoices()};
  dialog.addEventListener('cancel',event=>{event.preventDefault();closeChooser()});
  dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)closeChooser()});
  paintChoices();dialog.showModal();dialog.querySelector('input').focus();
 }
 function choiceRow(key,whole=false){
  const entry=entries.get(key),count=entry.ids.length,row=document.createElement('div');row.className='active-study-choice'+(whole?' is-whole':'');row.dataset.activeStudyKey=key;
  const text=document.createElement('div'),title=document.createElement('strong'),total=document.createElement('span');
  title.textContent=whole?'Todo este conteúdo':entry.source.label;total.textContent=`${count} ${count===1?'questão disponível':'questões disponíveis'}`;
  text.append(title,total);
  const action=document.createElement('button');action.type='button';action.className='active-study-choice-start';action.disabled=!count;action.innerHTML=uiIcon('book')+'<span>Questões</span>';
  action.setAttribute('aria-label',`Fazer questões: ${whole?'todo este conteúdo':entry.source.label} (${count})`);action.onclick=()=>start(key,row);row.append(text,action);return row;
 }
 function paintChoices(){
  if(!chooser)return;const root=chooser.dialog.querySelector('#active-study-choices');root.replaceChildren();
  const query=fold(chooser.query),words=query.split(' ').filter(Boolean),groups=new Map();
  if(!query)root.append(choiceRow(chooser.key,true));
  chooser.choices.forEach(key=>{
   const e=entries.get(key);if(!e)return;
   const group=e.source.parents.slice(1).join(' · ')||e.source.label;
   if(!words.every(word=>fold(group+' '+e.source.label+' '+e.source.text).includes(word)))return;
   if(!groups.has(group))groups.set(group,[]);groups.get(group).push(key);
  });
  const status=document.createElement('p');status.className='active-study-choice-status';status.setAttribute('role','status');
  const count=[...groups.values()].reduce((n,keys)=>n+keys.length,0);status.textContent=`${count} ${count===1?'conceito':'conceitos'}`;root.append(status);
  groups.forEach((keys,label)=>{
   const group=document.createElement('details');group.className='active-study-choice-group';group.open=!!query||groups.size===1;
   const heading=document.createElement('summary'),title=document.createElement('span'),total=document.createElement('small');title.textContent=label;total.textContent=`${keys.length} ${keys.length===1?'conceito':'conceitos'}`;heading.append(title,total);group.append(heading);
   keys.forEach(key=>group.append(choiceRow(key)));root.append(group);
  });
  if(!count){const empty=document.createElement('p');empty.className='active-study-choice-empty';empty.textContent='Nenhum conceito encontrado neste conteúdo. Tente outro termo.';root.append(empty)}
 }
 const textOf=node=>{if(!node)return '';const clone=node.cloneNode(true);clone.querySelectorAll('.active-study-action,svg,button,.collegiate-chart').forEach(n=>n.remove());return clone.textContent.trim()};
 function decorate(){
  if(!['t','m','x'].includes(view))return;
  const lesson=view==='t'?tr:view==='m'?mt.a:1,root=AL[lesson-1]?.t||'';
  const source=(label,text,parents=[],whole=false,ownerHints=[])=>({lesson,label,text,parents:[root,...parents],whole,ownerHints});
  if(view==='t'){
   document.querySelectorAll('.lesson-section .pt').forEach(node=>{const text=textOf(node);footer(node,source(text.split(':')[0],text))});
   document.querySelectorAll('#lesson-numbers .m').forEach(node=>footer(node,source(textOf(node.querySelector('.s')),textOf(node))));
  }
  if(view==='m'){
   document.querySelectorAll('.visual-map-panel').forEach(panel=>{
    const map=MentalMaps.current();if(!map)return;
    panel.querySelectorAll('.visual-map-transcript>section').forEach((node,index)=>{
     const [label,items]=map.branches[index],text=items.join(' · '),bindings=map.conceptBindings?.[index];
     // A síntese não vira contexto dominante: cada ramo mantém seus assuntos.
     // Estes nomes identificam assuntos completos já cadastrados. A síntese
     // não deve estreitá-los por palavras incidentais de um único exemplo.
     const concepts=(bindings||[]).map(name=>({...source(name,'',[],true,[name]),lockOwners:true}));
     footer(node,{...source(label,text,[],true),...(concepts.length?{concepts,ownerHints:bindings,lockOwners:true}:{} )},true);
    });
    footer(panel,source(map.title,MentalMaps.text(map),[],true));
   });
   document.querySelectorAll('.mind-branch').forEach(branch=>{
    const title=textOf(branch.querySelector('h3'));
    // Register descendants first so every group can include its own subgroups.
    [...branch.querySelectorAll('.mind-node')].reverse().forEach(node=>{
     const parents=[title],groups=[];let parent=node.parentElement.closest('.mind-group');
     while(parent&&branch.contains(parent)){const heading=textOf(parent.querySelector(':scope>.mind-node'));if(parent.querySelector(':scope>.mind-node')!==node)groups.unshift(heading);parent=parent.parentElement.closest('.mind-group')}
     parents.push(...groups);const label=textOf(node),group=node.parentElement.classList.contains('mind-group');
     footer(node,source(label,group?textOf(node.parentElement):label,parents,group),true);
    });
    footer(branch,source(title,textOf(branch),[],true));
   });
   document.querySelectorAll('.material-table').forEach(panel=>footer(panel,source(textOf(panel.querySelector('h3')),textOf(panel.querySelector('table')),[],true,[...panel.querySelectorAll('thead th,tbody th')].map(textOf))));
   document.querySelectorAll('.material-panel:is(.diagram-sequence,.diagram-group)').forEach(panel=>{
    const title=textOf(panel.querySelector('h3'));
    panel.querySelectorAll('.diagram-step').forEach(node=>footer(node,source(textOf(node.querySelector('strong')),textOf(node),[title])));
    footer(panel,source(title,textOf(panel),[],true));
   });
   document.querySelectorAll('.material-time-panel').forEach(panel=>{
    const title=textOf(panel.querySelector('h3'));
    panel.querySelectorAll('.time-record').forEach(node=>footer(node,source(textOf(node.querySelector('.time-description')),textOf(node),[title])));
    footer(panel,source(title,textOf(panel),[],true));
   });
   document.querySelectorAll('.operator-overview-table [data-operator]').forEach(row=>{
    const label=textOf(row.querySelector('.overview-operator-name')),short=textOf(row.querySelector('.overview-operator-short')),owner=label+' '+short;
    row.querySelectorAll('[data-feature]').forEach(cell=>{if(cell.querySelector('.overview-missing'))return;const heading=document.getElementById('overview-col-'+cell.dataset.feature)?.textContent||cell.dataset.feature;footer(cell,{...source(heading,textOf(cell),[owner],false,[owner]),lockOwners:true});});
    footer(row.querySelector('th'),{...source(owner,textOf(row),[],true,[owner]),lockOwners:true});
   });
   const overview=document.querySelector('.operator-overview');if(overview)footer(overview,{...source(textOf(overview.querySelector('h3')),textOf(overview.querySelector('table')),[],true,[...overview.querySelectorAll('.overview-operator-name,.overview-operator-short')].map(textOf)),lockOwners:true});
   const flash=document.querySelector('.flashcard-stage');if(flash){const card=currentMaterial().fc[fi];footer(flash,source(card[0],card[1]));}
  }
  if(view==='x')document.querySelectorAll('.qb,.qo').forEach(node=>footer(node,source(textOf(node),textOf(node))));
 }
 function start(key,box){
  const entry=entries.get(String(key));if(!entry)return;
  if(qz&&qz.rev.length<qz.ids.length){
   let notice=box.querySelector('.active-study-pending');if(!notice){notice=document.createElement('span');notice.className='active-study-pending';notice.setAttribute('role','status');notice.textContent='Conclua ou encerre a sessão atual para iniciar estas questões. ';const resume=document.createElement('button');resume.type='button';resume.textContent='Retomar sessão';resume.onclick=()=>{closeChooser(false);view='q';go()};notice.append(resume);box.append(notice)}return;
  }
  const ids=matching(entry.source);if(!ids.length)return;
  const origin={view,tr,mt:{...mt},fi,ff,block:selectedLessonBlocks[entry.source.lesson]||0,key:String(key)};
  const title=unique([entry.source.parents.at(-1),entry.source.label]).filter(Boolean).join(' · ');
  closeChooser(false);
  begin(shuffle([...ids]),'e',{contextStudy:{title,origin}});
 }
 function returnToContent(){
  const context=qz?.contextStudy;if(!context)return;
  const origin=context.origin;view=origin.view;tr=origin.tr;mt={...origin.mt};fi=origin.fi;ff=origin.ff;
  const entry=entries.get(origin.key);if(entry)selectedLessonBlocks[entry.source.lesson]=origin.block;
  go();const target=document.querySelector(`[data-active-study-key="${origin.key}"]`)||document.querySelector(`[data-active-study="${origin.key}"]`);target?.scrollIntoView({block:'center'});const control=target?.querySelector('button')||target;if(control){if(control===target)control.setAttribute('tabindex','-1');control.focus({preventScroll:true})}
 }
 function sessionHeader(){return qz?.contextStudy?`<div class="active-study-session"><div><span>ESTUDO POR CONTEÚDO</span><strong>${escapeText(qz.contextStudy.title)}</strong><small>${qz.ids.length} questões · Estudo e Hardcore conforme o banco</small></div><button type="button" onclick="ActiveStudy.returnToContent()">Voltar ao conteúdo</button></div>`:''}
 return {decorate,matching,profile,questionProfile,bank,start,returnToContent,sessionHeader,audit:()=>[...entries].map(([key,e])=>({key,...e,profile:profile(e.source)}))};
})();
