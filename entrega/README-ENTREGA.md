# Entrega — Consolidador de reservas de hotel

## Defeitos corrigidos

| # | Arquivo / função | Regra do README violada | Causa raiz | Correção |
|-|-|-|-|-|
| D1 | `repositories/csv_reservation_repository.py` — `CsvReservationRepository.read` | `total_reservations` = número de reservas no arquivo | A leitura parava em 200 linhas (`if len(rows) == 200: break`), descartando o restante do arquivo. | Remoção do limite. |
| D2 | `services/status_policy.py` — `is_billable` | Só `CONFIRMED` é faturável | A regra excluía apenas `CANCELLED` (`status != "CANCELLED"`), tratando `NO_SHOW` como faturável. | `status == "CONFIRMED"`. |
| D3 | `services/stay_calculator.py` — `calculate_room_nights` | `(checkout - checkin).days * rooms`, inclusive na virada de mês/ano | Subtraía o dia do mês (`checkout.day - checkin.day`) em vez das datas, gerando noites erradas ou negativas na virada de mês/ano. | `(checkout - checkin).days * rooms`. |
| D4 | `services/currency_converter.py` — `convert_to_brl` | Converter com `amount * rate_to_brl` | O valor era dividido pela taxa em vez de multiplicado. | `amount * rate`. |
| D5 | `services/currency_converter.py` — `convert_to_brl` | Usar `Decimal`, nunca `float`, no dinheiro | A conversão passava por `float` antes de voltar a `Decimal`, introduzindo erro binário (ex.: `4.065` → `4.0649999999999995`). | Cálculo inteiramente em `Decimal` (mesma linha de D4). |
| D6 | `services/report_builder.py` — `ReportBuilder.build` | `top_hotels`: `total_brl` decrescente, empate por `hotel_id` ascendente | A chave de ordenação `(amount, hotel_id)` ordenava o valor em ordem crescente. | Chave `(-amount, hotel_id)`. |

Diff total em `src/`: 5 arquivos, +4/−6 linhas. CLI, schema do relatório, `README.md`, `data/` e testes fornecidos não foram alterados.

## Como investiguei

1. Leitura do README (contrato, regras, amostra), do código em `src/`, dos testes fornecidos e dos CSVs.
2. Perfil dos dados: 300 reservas (235 `CONFIRMED`, 31 `CANCELLED`, 34 `NO_SHOW`), moedas BRL/USD/EUR todas com taxa, 93 reservas que cruzam mês (incluindo dezembro → janeiro), sem duplicidades nem espaços extras.
3. Execução da linha de base: `pytest -q` com 5 falhas e CLI na amostra com 10 divergências em relação ao README (ex.: `total_room_nights = -33`, esperado `28`).
4. Mapeamento de cada divergência a uma função e a uma regra do README, e verificação em memória dos defeitos não cobertos pelos testes fornecidos (D1: o repositório devolvia 200 de 300 linhas; D5: 19 de 235 conversões inexatas via `float`).
5. Correções mínimas, uma linha por defeito, sem refatoração.
6. Testes adicionais para as lacunas dos testes fornecidos.

## Testes adicionados

| Arquivo | Cobre |
|-|-|
| `tests/test_large_input.py` | 250 reservas → `total_reservations = 250` (D1) |
| `tests/test_top_hotels_tie.py` | Empate em `total_brl` resolvido por `hotel_id` ascendente e corte de `--top` após o desempate (D6) |
| `tests/test_year_boundary.py` | Reserva 2024-12-30 → 2025-01-02 com 2 quartos = 6 noites; `by_month` pelo mês do check-in, ascendente entre anos (D3) |
| `tests/test_money_precision.py` | USD 0.75 × 5.42 = 4.065 → `"4.07"` (half-up, sem `float`); soma exata antes do arredondamento (`0.1626` → `"0.16"`) (D5) |

## Como validar

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

pytest -q
ruff check .

PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json

PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json
```

## Resultados

- `pytest -q`: **11 passed** (5 fornecidos + 6 adicionais), Python 3.11.18.
- `ruff check .`: `All checks passed!`
- Amostra (`exemplo-validacao.csv`): `Reservas: 12 | Confirmadas: 9 | Noites: 28 | Total BRL: 7566.00`; `summary`, `by_month` e `top_hotels` idênticos às tabelas do README (exceto `generated_at`, ignorado conforme o contrato).
- Dataset completo (`reservas_hoteis.csv`): `Reservas: 300 | Confirmadas: 235 | Noites: 1347 | Total BRL: 396170.00`; 31 `CANCELLED`, 34 `NO_SHOW`; somas de `by_month` consistentes com o `summary`.
