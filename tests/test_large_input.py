"""Testes adicionais: leitura completa de arquivos com mais de 200 reservas."""

from helpers import run_cli


def test_reads_more_than_200_reservations(tmp_path):
    """Todas as reservas do arquivo entram no relatório, sem limite de linhas."""
    report = run_cli(
        tmp_path,
        [{"reservation_id": f"R-{index}", "amount": "100.00"} for index in range(1, 251)],
    )
    assert report["summary"]["total_reservations"] == 250
    assert report["summary"]["confirmed_reservations"] == 250
    assert report["summary"]["total_room_nights"] == 250
    assert report["summary"]["total_amount_brl"] == "25000.00"
