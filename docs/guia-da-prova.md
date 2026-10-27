# Guia da prova — referência de prioridades

Referência recebida do usuário em **27/10/2026**, por imagem de sua tabela no
Google Sheets. A ordem e os textos abaixo são o padrão de planejamento até o
usuário informar uma atualização. Não foram confrontados com um edital externo
e não devem ser apresentados como distribuição oficial verificada da CPA.

| Posição | Aula | Bloco | Foco temático | Importância | Detalhe informado |
| --- | --- | --- | --- | --- | --- |
| 1º | 13 | F | Métricas Matemáticas, Gestão de Riscos e Clientes | Máxima | 40% da prova / 20 questões |
| 2º | 11 | D | Macroeconomia, Atividade e Política Fiscal | Alta | 20% da prova / 10 questões |
| 3º | 01 | Não informado | Sistema Financeiro Nacional | Alta | Base conceitual obrigatória |
| 4º | 03 | Não informado | Banco Central do Brasil | Média-alta | Autarquia mais cobrada |
| 5º | 04 | Não informado | Comissão de Valores Mobiliários | Média-alta | Mercado de Capitais |
| 6º | 08 | A | Inovação, Pagamentos e Crédito Digital | Média | ~10% a 15% da prova |
| 7º | 09 | B | Autorregulação, Proteção e Livre Mercado | Média | ~10% a 15% da prova |
| 8º | 02 | Não informado | Conselho Monetário Nacional | Média | Fixação de metas |
| 9º | 05 | Não informado | Seguros e Previdência (SUSEP/PREVIC) | Média | Estrutura técnica |
| 10º | 06 | Não informado | Operadores Monetários | Média | Bancos Múltiplos e Comerciais |
| 11º | 07 | Não informado | Operadores Não Monetários | Média | Corretoras e Financeiras |
| 12º | 10 | C | Infraestrutura, Negociação e Risco Sistêmico | Baixa | ~5% da prova |
| 13º | 12 | E | Mercado de Câmbio e Relações Internacionais | Baixa | ~5% da prova |

## Escopo e memória permanente

- Esta entrega importa a referência e cria uma consulta interativa. **Não
  altera questões, dificuldades, proporções de sorteio, estudo diário,
  simulados, Bate-pronto ou histórico.** Uma alteração desses mecanismos exige
  solicitação específica posterior; os pesos não são aplicados automaticamente.
- Blocos A–F pertencem a este quadro de prioridades; não são os filtros internos
  das várias partes de uma aula. Preserve a associação explícita fornecida.
- Não preencha pesos ou blocos ausentes, não some percentuais aproximados nem
  derive novas quantidades de questões. 40%/20 e 20%/10 permanecem literais.
- Os focos temáticos da tabela são os da imagem, mesmo quando diferem do título
  cadastrado da aula; não renomeie aulas para fazer os dois textos coincidirem.
- A Aula 13 está prevista, ainda sem conteúdo no sistema. Sua linha não cria
  aula nem questões. A presença é verificada por AL, e o aviso desaparece quando
  o conteúdo for cadastrado no seu ID habitual.

## Interface

**Guia da prova**, com ícone de prova, fica imediatamente abaixo de
**Estatísticas** no menu lateral. Todos os 13 registros aparecem inicialmente,
na ordem original. A posição permanece a mesma após filtros e reordenação.

Busca sem distinção de acento/caixa por aula, bloco, tema e descrição, incluindo
aliases Bacen, BC, CVM, CMN e SFN. Filtros combináveis de importância, bloco e
cadastro (todas/cadastradas/previstas), com botões no padrão do sistema; não há
menus nativos antigos. Ordenação por prioridade, aula ou tema e limpeza única.

Sinais de cor discretos acompanham os nomes de importância; informação não
depende só de cor. No computador, tabela sem cortes de dados. Em telas pequenas,
as mesmas linhas tornam-se cartões legíveis. Contagem, vazio, busca escapada,
foco/teclado e ambos os temas. Fonte e limites ficam sob um único controle
expansível, fechado inicialmente.

Dados imutáveis em `EXAM_GUIDE_REFERENCE`, no arquivo local `exam-guide.js`;
apresentação em `exam-guide.css`. Sem API, IA, serviço externo ou nova chave no
armazenamento. Filtros sobrevivem à navegação durante a visita e não interferem
na consulta de outras abas.

## Validação

Testes em navegador: fidelidade das 13 linhas à imagem, pesos, blocos, ordem,
filtros combinados, busca por sigla/acentos, vazio, limpeza, teclado, temas,
larguras 390–1920, cadastro futuro e preservação da prática/checkpoint ativos.
Resultado: **17 testes** do guia/Estatísticas/painel, **6 validações** do banco e
**76 testes** de fluxos gerais aprovados. Conferência visual em claro/escuro;
nenhuma alteração nos dados de Q/BP/AL/MAT ou nas regras de seleção.

```bash
PYTHONPATH=tests python3 -m unittest -v test_exam_guide test_statistics test_dashboard_hierarchy
python3 tests/validate_bank.py
python3 tests/smoke.py
```
