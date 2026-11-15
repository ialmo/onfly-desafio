"""Testes adicionais: noites e agrupamento mensal na virada de ano."""

from helpers import run_cli


def test_nights_and_months_across_year_boundary(tmp_path):
    """Noites usam a diferença de datas e by_month usa o mês do check-in, em ordem ascendente."""
    report = run_cli(
        tmp_path,
        [
            {
                "reservation_id": "R-1",
                "checkin_date": "2025-01-05",
                "checkout_date": "2025-01-06",
                "rooms": "1",
                "amount": "100.00",
            },
            {
                "reservation_id": "R-2",
                "checkin_date": "2024-12-30",
                "checkout_date": "2025-01-02",
                "rooms": "2",
                "amount": "600.00",
            },
        ],
    )
    assert report["summary"]["total_room_nights"] == 7
    assert report["by_month"] == [
        {"month": "2024-12", "reservations": 1, "room_nights": 6, "total_brl": "600.00"},
        {"month": "2025-01", "reservations": 1, "room_nights": 1, "total_brl": "100.00"},
    ]
