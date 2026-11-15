"""Testes adicionais: precisão monetária com Decimal e arredondamento half-up."""

from helpers import run_cli


def test_conversion_rounds_half_up_without_float_error(tmp_path):
    """USD 0.75 * 5.42 = 4.065 exato; float daria 4.0649... e half-even daria 4.06."""
    report = run_cli(tmp_path, [{"reservation_id": "R-1", "currency": "USD", "amount": "0.75"}])
    assert report["summary"]["total_amount_brl"] == "4.07"


def test_amounts_are_summed_exactly_and_rounded_only_on_output(tmp_path):
    """3 * (USD 0.01 * 5.42) = 0.1626 exato; arredondar cada linha antes daria 0.15."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": f"R-{index}", "currency": "USD", "amount": "0.01"} for index in range(1, 4)],
    )
    assert report["summary"]["total_amount_brl"] == "0.16"
    assert report["summary"]["average_nightly_rate_brl"] == "0.05"
