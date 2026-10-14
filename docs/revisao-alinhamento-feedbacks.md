# Revisão de alinhamento e justificativas

O banco de 900 questões foi verificado quanto ao objeto pedido pelo enunciado,
ao tipo de resposta das quatro opções e à utilidade da explicação de cada uma.
As explicações pertinentes foram preservadas; uma definição direta não precisa
ser longa para justificar uma resposta direta.

## Resultado

- 138 questões alteradas; 762 preservadas.
- 15 enunciados ajustados e 5 conjuntos de alternativas ajustados.
- 131 questões com alteração no bloco de feedbacks: 273 explicações individuais.
- 100 explicações gerais e 3 dicas ajustadas.

As contagens por campo se sobrepõem: uma mesma questão pode ter enunciado,
alternativas, dica e explicações alterados. Não são questões adicionais.

## Problemas e correções

- **Pedido e resposta diferentes:** perguntas de classificação com opções de
  funcionamento ou atributos não perguntados. Identificado o objeto e a ordem
  das etapas; exemplos: abertura de crédito, repasses, SCI e Letra de Câmbio.
- **Distrator também defensável:** a questão de SEP descrevia a confusão com
  crédito próprio tanto na correta quanto numa incorreta. A incorreta agora
  afirma uma permissão indevida, em vez de também diagnosticar o mesmo erro.
- **Justificativa numérica genérica:** todos os 16 casos com o texto “O valor
  indicado nesta opção ... não corresponde” foram substituídos por explicações
  de regras, bases, contagens e unidades. Na mudança da meta em junho de 2026,
  junho de 2030 é reconhecido como prazo permitido, porém posterior à primeira
  data possível, junho de 2029; não é tratado como data proibida.
- **Combinações de afirmações:** 14 questões com justificativa incompleta do
  conjunto passaram a explicar cada afirmação na correta e cada item falso
  incluído ou verdadeiro omitido nos distratores.
- **Motivo e função real:** revisadas explicações que trocavam o assunto por
  outra competência do órgão ou só negavam a opção. CNPI/APIMEC, atuação da
  equipe na adesão ANBIMA e confiança/investimento receberam contexto e
  explicações específicas. Informação confiável pode estimular investimentos;
  não assegura retorno nem transforma certificação em garantia de depósitos.
- **Generalizações:** controles de intermediação contribuem para gerir riscos,
  sem provar que qualquer empréstimo intermediado é sempre mais seguro. A
  modalidade cooperativa sem captação de depósitos foi distinguida das plenas
  e clássicas em um distrator sobre instituições monetárias.

A referência “descrita na aula” do print da questão de confiança já havia sido
retirada na revisão anterior. A redação atual foi novamente aprimorada; o print
isolado não comprova qual versão estava publicada ou carregada no navegador.

## Preservação e evidência

IDs, aulas, temas, níveis, elegibilidade para simulado e ordem original do gabarito
foram mantidos. Continuam 100 questões por aula, com 20 fáceis, 40 médias, 20
difíceis e 20 hardcore. A distribuição dos assuntos das aulas 8 e 9 foi preservada.
Nenhum código da aplicação fora de `Q` foi alterado: materiais, histórico,
layout e fluxo dos modos continuam iguais.

O manifesto `revisao-alinhamento-feedbacks.json` registra o resultado por ID,
campos modificados e hashes anteriores/posteriores. Os testes reconstroem cada
revisão na ordem inversa para conservar os registros históricos de autoria.
Esse registro interno não é uma planilha de Excel.

As regressões verificam os três exemplos, a distinção entre data posterior e
mínimo, a ambiguidade da SEP, o vínculo dos feedbacks após embaralhamento, a
preservação do histórico e o simulado sem feedback imediato. A auditoria de
tamanho continua sem estratégia dominante de maior/menor opção.

Validação concluída: 41 testes de banco/revisões e 76 testes no Chromium,
totalizando 117 aprovados. A auditoria de tamanho e `git diff --check` também
passaram. O HTML fora do bloco `Q` foi comparado com a versão inicial e permanece
idêntico.

Revisão editorial e testes de execução não certificam a vigência de toda a
legislação nem garantem ausência absoluta de falhas pedagógicas. Não houve
certificação normativa independente nesta revisão.
