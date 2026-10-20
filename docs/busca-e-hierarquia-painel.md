# Busca de conteúdo e hierarquia do painel — 20/10/2026

## Escopo

Implementados somente os três pontos aprovados: hierarquia do painel inicial,
busca por nome/assunto e hierarquia visual sem ampliar a paleta. Bancos Q/BP,
conteúdo de AL/MAT, critérios de seleção e histórico são preservados.

## Painel

1. Estudo de hoje continua sendo a atividade principal, com as mesmas regras.
2. Próximo passo sugerido indica sessão ainda em andamento; na ausência dela,
   o assunto com mais erros pendentes; depois, a última aula praticada; sem
   histórico, a primeira aula. Recomendações não afirmam domínio ou causa do erro.
3. Indicadores e filtros ficam sob “Seu acompanhamento”, com números e títulos
   legíveis e ícones secundários menores.
4. Evolução aparece antes da trilha na coluna principal, mantendo todas as datas,
   percentuais e a navegação temporal. Prioridades e última aula ficam na lateral.
5. A lista de todas as aulas tem área de rolagem própria, com acesso por teclado,
   para que mais aulas não empurrem o restante do painel indefinidamente.

## Busca

- Mesma consulta e apresentação em Trilha, Material de apoio e seleção de aulas
  em Praticar. A busca da prática fica junto das aulas.
- Consulta local, sem serviço externo ou dependência nova; índice criado sob
  demanda a partir dos conteúdos atuais, incluindo futuras aulas.
- Fontes: títulos, objetivos, blocos e assuntos; resumo, dicas, pegadinhas e
  números; ramificações dos mapas; diagramas; tabelas; prazos; flashcards;
  linhas dos quadros comparativos. Não indexa alternativas do banco de questões.
- Usa o cadastro existente de siglas para equivalências (BC, BCB, BACEN e Banco
  Central, por exemplo), desconsidera acentos/maiúsculas e permite prefixos de
  palavras. Vários termos precisam estar presentes no mesmo resultado, incluindo
  o contexto da aula. Não promete entender sinônimos fora desse cadastro.
- Resultados agrupados por aula e identificados por material, com trecho de
  contexto e filtros por tipo. Ordenação prioriza termos no título e no conteúdo.
  A primeira página distribui vagas entre as aulas encontradas. “Mostrar mais”
  permite acessar todos os resultados sem um limite permanente.
- Abrir resultado expande a seção apropriada e foca o item, a ramificação,
  o diagrama, a tabela, o prazo, o flashcard ou a linha do quadro comparativo.
  Flashcards abrem na pergunta. Blocos podem ser abertos por seu próprio resultado.
- A lista da busca recolhe ao abrir um trecho, mantendo consulta e resultados
  disponíveis. A navegação não reinicia uma sessão de questões em andamento.
- Em Praticar, a busca filtra somente as aulas visíveis. A seleção permanece,
  inclusive se uma aula deixar de aparecer; as selecionadas são mostradas
  separadamente e podem ser removidas. Questões continuam seguindo as aulas,
  proporções, níveis e filtros da sessão. Buscar não seleciona/inicia uma prática.
- Limpar/Escape restaura a lista completa. Consulta e materiais são escapados
  antes da inserção no HTML. Controles e destinos têm navegação por teclado.

## Verificações

- `tests/test_content_search.py`: equivalências, acentos, combinação de termos,
  todas as fontes, relevância/navegação, paginação integral, seleção múltipla,
  sessão em andamento, termos sem resultados, entrada não confiável, novas aulas,
  os dois temas e larguras 390/1024/1280/1440/1920.
- `tests/test_dashboard_hierarchy.py`: hierarquia, sugestões com dados reais,
  preservação de todas as aulas/datas/filtros, foco e layout nos dois temas.
- Regressões de prática, navegação, materiais, diário, histórico e resultados.
- Inspeção visual de painel, busca e prática nos dois temas; dados de teste
  isolados, sem acesso ou alteração do histórico do usuário.

Validação concluída: **109 testes aprovados** — 7 de busca, 4 de hierarquia,
4 de layout da prática, 3 de retorno/navegação da prática, 9 de navegação entre
questões, 76 de fluxos completos e 6 de estrutura do banco. Inspeção visual nos
dois temas. Comparação com a versão publicada confirmou Q, BP, AL, MAT e os dados
dos quadros comparativos idênticos; as mudanças se limitam à navegação e apresentação.
