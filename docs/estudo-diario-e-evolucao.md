# Checkpoint diário e evolução completa

O cartão Estudo de hoje passa a oferecer **20 questões**, com **5 fáceis,
10 médias e 5 difíceis**, sem Hardcore. Com as oito aulas atuais, todas aparecem
em cada checkpoint, com duas ou três questões por aula. As quatro vagas extras
alternam entre as aulas conforme o dia, mantendo o equilíbrio ao longo do tempo.

## Seleção e retomada

`dailyPlan` independe dos filtros de prática, de blocos e de estatísticas. Reutiliza
o alocador de níveis, com parâmetros explícitos de Estudo/Todos e prioridade para
inéditas. A prioridade é otimizada entre as combinações que mantêm a distribuição
por aula e os totais 5/10/5. Uma única aula com inéditas não concentra todo o teste.
Depois das inéditas necessárias de cada nível, revisão prefere últimos erros e
respostas mais antigas. A seleção não repete IDs e nunca usa Hardcore para completar.

O sorteio usa a data como semente. Ao iniciar, o conjunto fica reservado no
rascunho: clicar novamente ou retomar não gera outra seleção. Abrir materiais ou
trocar tema não reinicia a sessão. Pausar ou fechar a página permite retomar
posição, alternativas, respostas, dicas, eliminação e feedback. O tempo restaurado
desconsidera o período em que a página ficou fechada ou a sessão pausada.

Se o banco não suportar vinte questões com os níveis e aulas planejados, o início
fica indisponível e a razão aparece no cartão; não se incluem níveis ou repetições
indevidos. Se futuras aulas ultrapassarem vinte, a seleção percorre grupos de
aulas em ciclos e informa essa condição. Um checkpoint reservado não é alterado
quando novos conteúdos são adicionados.

## Conclusão, data e sequência

- O resultado é gravado na **vigésima resposta**, antes de abrir a tela de análise.
- O cartão mostra percentual, acertos/20, cadeado e **Concluído hoje**. **Ver
  resultado** consulta a análise existente, sem iniciar outro checkpoint.
- O dia é calculado em **America/Sao_Paulo**, inclusive na mudança de data. Há
  atualização de calendário na página aberta, no retorno à janela e na navegação.
- A data usada é a da última resposta. Uma sessão iniciada antes da meia-noite
  e concluída depois pertence ao dia da conclusão.
- Uma sessão já concluída não é registrada outra vez na virada do dia. No dia
  seguinte o cartão permite um novo conjunto, com prioridade para novas questões.
- A sequência conta dias com vinte respostas concluídas. Hoje pendente mantém
  a sequência de ontem até o prazo de hoje terminar; pular um dia zera a sequência
  atual, preservando o recorde. Práticas comuns não aumentam a sequência.
- Refazer erros é uma prática normal, com os feedbacks habituais, e não muda a
  nota original do checkpoint ou o bloqueio diário.

## Persistência e preservação

O formato de `cpaH` permanece `[id, acerto, timestamp, modo]`. O checkpoint usa
modo Estudo e não altera nenhum ID, questão ou conteúdo de `Q`, `AL`, `MAT`.

`cpaDaily` contém uma versão do esquema, resultados por dia, um rascunho e os
detalhes do último resultado. Datas e scores podem ser mantidos por longo prazo
sem armazenar os textos de todas as sessões. A sincronização opcional da conta
grava os campos `h` e `daily` juntos, após carregar os dados existentes. A leitura
mescla datas concluídas locais e da conta; documentos antigos com apenas `h`
continuam válidos. O histórico remoto fica também no cache local.

O histórico de uma resposta é salvo antes do avanço diário, para que outra aba
receba os dois de maneira consistente. Eventos de armazenamento compartilham o
mesmo checkpoint e o bloqueio sem provocar gravações em ciclo.

Sem armazenamento disponível, a funcionalidade continua em memória durante a
página aberta. Fechar a página ou apagar seus dados pode remover esse estado
local. A funcionalidade não é um controle de acesso de servidor. O botão Zerar
histórico conserva o comportamento anterior de limpar tentativas em `cpaH`, sem
liberar um segundo checkpoint no mesmo dia nem apagar os registros de sequência.

## Evolução de todos os dias

A evolução deixa de limitar o desenho aos **14 dias registrados mais recentes**.
Considera o histórico inteiro, com todos os modos e tentativas, e continua
mostrando o percentual de cada dia. Filtros do painel aplicam-se aos indicadores
de tentativas e ao desempenho detalhado; não ocultam dias do gráfico.

Cada ponto representa `acertos / respostas` naquele dia, no horário de Brasília.
Repetições entram como tentativas, como nos indicadores anteriores. A escala
horizontal reserva espaço por dia registrado; períodos sem respostas não recebem
valores inventados. Todos os pontos ficam no desenho, com rolagem horizontal,
datas completas, percentual e contagem no título acessível. Há atalhos para
Início do histórico/Mais recente e preservação da posição de leitura.

O formato histórico não identifica sessões completas separadamente. Por isso,
o gráfico apresenta **agregados diários**, não uma reconstrução das notas de cada
simulado antigo. Registros sem data, ou com data ilegível, permanecem num resumo
de quantidade e percentual separado. Um dia que não tenha sido salvo não pode
ser recuperado a partir dessa alteração.

## Verificação

Os testes de navegador cobrem:

- 20 IDs únicos, níveis 5/10/5, todas as oito aulas e rodízio das vagas extras;
- otimização de inéditas quando um nível já está parcialmente esgotado;
- retomada após pausa/recarregamento, opções embaralhadas, ajudas e feedback;
- bloqueio persistente, consulta ao resultado e nota imutável após refazer erros;
- virada de data em Brasília, conclusão atravessando meia-noite e sequência;
- duas abas compartilhando a sessão, documentos de conta e armazenamento falho;
- **400 dias** de registros, todos os modos, percentuais e registros sem data;
- dois temas e quatro larguras de PC, com rolagem restrita ao gráfico.

```bash
python3 tests/validate_bank.py
python3 tests/audit_alternatives.py --check
python3 tests/test_alternative_quality.py
python3 tests/test_question_design.py
python3 tests/test_aula8.py
python3 tests/smoke.py
```
