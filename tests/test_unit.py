import pytest

from app.main import preco_com_desconto


@pytest.mark.parametrize(
    "preco, pct, esperado",
    [
        (10.0, 0, 10.0),
        (10.0, 10, 9.0),
        (8.5, 50, 4.25),
    ],
)
def test_desconto_valido(preco, pct, esperado):
    assert preco_com_desconto(preco, pct) == esperado


def test_desconto_acima_do_maximo():
    with pytest.raises(ValueError):
        preco_com_desconto(10.0, 80)


def test_desconto_negativo():
    with pytest.raises(ValueError):
        preco_com_desconto(10.0, -1)


def test_maximo_configuravel_por_variavel_de_ambiente(monkeypatch):
    monkeypatch.setenv("DESCONTO_MAXIMO", "90")
    assert preco_com_desconto(10.0, 80) == 2.0
