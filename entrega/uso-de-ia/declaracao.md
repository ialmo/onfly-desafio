# Declaração de uso de IA

## 1. Ferramenta e modelo

- Claude Code (CLI), modelo Claude Opus 5.5 (`claude-opus-5-5`).
- Sessão exportada com `/export` em `sessao-claude-code.md`.

## 2. O que a IA fez

- Leu README, configuração, código, testes e CSVs, e resumiu contrato, regras e fluxo.
- Executou `pytest`, `ruff` e o CLI, e comparou a saída da amostra com as tabelas do README.
- Identificou os seis defeitos, com arquivo, função, regra violada e causa raiz.
- Propôs o plano de correção e os testes adicionais.
- Após aprovação, aplicou as cinco alterações de uma linha em `src/` e escreveu os quatro arquivos de teste adicionais.
- Redigiu `README-ENTREGA.md` e esta declaração, a pedido.

## 3. O que eu fiz como responsável pela solução

- Defini as regras da sessão: sem commit ou publicação, sem alterar `README.md`, `data/` e testes fornecidos, e aprovação obrigatória antes de qualquer edição.
- Conduzi cada etapa (análise, linha de base, diagnóstico, plano, correção, testes, validação e auditoria) e aprovei o diagnóstico, o plano e o escopo dos testes adicionais antes da execução.
- Limitei os testes adicionais a quatro lacunas: mais de 200 reservas, desempate em `top_hotels`, virada de ano e precisão monetária.
- Reexecutei no VS Code a instalação do ambiente, `pytest -q`, `ruff check .` e o CLI na amostra e no dataset completo.
- Revisei os documentos de entrega e fiz o commit e a publicação no GitHub.

## 4. Como o resultado foi validado

- `pytest -q`: 11 testes passando (5 fornecidos e 6 adicionais).
- `ruff check .`: sem erros.
- CLI na amostra: `summary`, `by_month` e `top_hotels` idênticos ao README, exceto `generated_at`.
- CLI no dataset completo: `total_reservations = 300` (235 `CONFIRMED`, 31 `CANCELLED`, 34 `NO_SHOW`).
- `git diff` contra a linha de base: nenhuma alteração em `README.md`, `data/` ou testes fornecidos; `git diff --check` sem problemas.
