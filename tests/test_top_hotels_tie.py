"""Testes adicionais: desempate do ranking de hotéis."""

from helpers import run_cli

ROWS = [
    {"reservation_id": "R-1", "hotel_id": "H03", "hotel_name": "Hotel C", "amount": "900.00"},
    {"reservation_id": "R-2", "hotel_id": "H02", "hotel_name": "Hotel B", "amount": "500.00"},
    {"reservation_id": "R-3", "hotel_id": "H01", "hotel_name": "Hotel A", "amount": "500.00"},
]


def test_top_hotels_tie_breaks_by_hotel_id(tmp_path):
    """Empate em total_brl é resolvido por hotel_id ascendente, não pela ordem do arquivo."""
    report = run_cli(tmp_path, ROWS, top=3)
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H03", "H01", "H02"]
    assert [hotel["total_brl"] for hotel in report["top_hotels"]] == ["900.00", "500.00", "500.00"]


def test_top_hotels_cut_applies_after_tie_break(tmp_path):
    """O corte em --top acontece depois do desempate."""
    report = run_cli(tmp_path, ROWS, top=2)
    assert [hotel["hotel_id"] for hotel in report["top_hotels"]] == ["H03", "H01"]
