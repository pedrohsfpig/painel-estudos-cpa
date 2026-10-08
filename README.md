# Painel de estudos CPA

Painel de estudos e simulados em português, importado do arquivo
`Painel de estudos CPA.html`. O conteúdo original foi preservado integralmente
em `index.html`, incluindo o visual, as questões e a lógica de funcionamento.

## Executar

O painel é uma página HTML independente, sem instalação de dependências,
build, servidor de aplicação ou credenciais obrigatórias.

Na pasta do repositório, execute:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Em um computador local, acesse `http://127.0.0.1:8000` no navegador.
Também é possível abrir `index.html` diretamente, mas usar sempre o mesmo
endereço e porta mantém uma origem estável para o histórico do navegador.
Para encerrar o servidor, pressione `Ctrl+C`.

## Publicar no GitHub Pages

O painel pode ser hospedado diretamente pelo GitHub Pages, sem build.
O arquivo `.nojekyll` mantém a publicação como um site estático.

No repositório `pedrohsfpig/painel-estudos-cpa`, abra **Settings → Pages**.
Em **Build and deployment**, selecione **Deploy from a branch**,
depois a branch **main** e a pasta **/(root)**, e salve.

Após o GitHub concluir a publicação, o endereço padrão será:
`https://pedrohsfpig.github.io/painel-estudos-cpa/`.
Esse endereço só fica disponível quando o Pages estiver ativado e a
publicação tiver terminado.

Com o Pages ativado, novos commits enviados à branch `main` atualizam o site.
Cada publicação pode levar alguns minutos. Para acompanhar as alterações,
aguarde a publicação e recarregue o mesmo endereço no navegador. O histórico
local permanece porque a origem do site não muda.

## Funcionalidades preservadas

- 600 questões: 100 em cada uma das 6 aulas.
- 120 fáceis, 240 médias, 120 difíceis e 120 Hardcore.
- Estudo com dicas, eliminação de alternativas e correção imediata.
- Simulados com resultado e revisão dos erros ao final.
- Filtros de aula, dificuldade, questões inéditas e erros pendentes.
- Estudo de hoje, cronômetro, indicadores e evolução diária.
- Trilha de aulas, quadro do SFN, mapas mentais, diagramas, tabelas,
  linhas do tempo e flashcards.

## Histórico

Fora do Claude, o progresso é salvo no `localStorage` do navegador, na chave
`cpaH`. Recarregar a página mantém as respostas. Trocar de navegador, endereço
ou porta cria outro histórico; limpar os dados do site apaga os registros.
Importar o HTML não transfere automaticamente o progresso do ambiente anterior.

O HTML original também tenta sincronizar o histórico pela API `claude.use`.
Essa integração foi preservada, mas não está disponível neste ambiente.
Não há login nem sincronização entre dispositivos na versão independente.

## Testes de navegador

Os testes usam Python 3 e Playwright; essas dependências são necessárias
somente para os testes, não para utilizar o painel.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m playwright install chromium
.venv/bin/python tests/smoke.py
```

Quando Python, Playwright e Chromium já estiverem disponíveis no ambiente:

```bash
python3 tests/smoke.py
```

O teste inicia e encerra seu próprio servidor local e usa um histórico isolado
por caso. Ele detecta Chromium no sistema; para informar outro executável,
use a variável `CHROMIUM_PATH`.

Os casos verificam o banco de questões, os materiais das seis aulas, os três
modos de prática, ajudas, revisão de erros, filtros, estudo diário, persistência,
limpeza do histórico e um fluxo em tela móvel. A revisão pedagógica das perguntas
e a integração com a conta do Claude não fazem parte desses testes.

## Validação da importação

Os 10 testes passaram no Chromium deste ambiente. O HTML foi servido via HTTP
e conferido byte a byte com o arquivo enviado: nenhuma alteração de conteúdo,
visual ou lógica foi feita em `index.html`.

Uma limitação do visual original foi confirmada: em uma tela de 390 pixels,
o menu superior amplia a página para 540 pixels e exige rolagem horizontal.
O fluxo de responder questões funciona nessa largura, mas a adaptação do menu
para celular fica como melhoria futura.
