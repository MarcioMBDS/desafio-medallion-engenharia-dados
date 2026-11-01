from src.pipeline import validar_total_pessoas
from src.pipeline import validar_coordenadas
from src.pipeline import converter_inteiro

def test_total_pessoas_correto():
    assert validar_total_pessoas(
        pessoas=10,
        mortos=1,
        feridos_leves=2,
        feridos_graves=1,
        ilesos=6,
    )


def test_total_pessoas_incorreto():
    assert not validar_total_pessoas(
        pessoas=10,
        mortos=1,
        feridos_leves=2,
        feridos_graves=1,
        ilesos=5,
    )

from src.pipeline import validar_classificacao
from src.pipeline import validar_coordenadas
from src.pipeline import converter_inteiro

def test_classificacao_com_vitimas_fatais():
    assert validar_classificacao(
        classificacao="Com Vítimas Fatais",
        mortos=1,
        feridos_leves=0,
        feridos_graves=0,
    )


def test_classificacao_incorreta():
    assert not validar_classificacao(
        classificacao="Sem Vítimas",
        mortos=1,
        feridos_leves=0,
        feridos_graves=0,
    )

def test_coordenadas_validas():
    from decimal import Decimal

    assert validar_coordenadas(
        Decimal("-22.90"),
        Decimal("-43.20"),
    )


def test_coordenadas_fora_dos_limites():
    from decimal import Decimal

    assert not validar_coordenadas(
        Decimal("10.00"),
        Decimal("-43.20"),
    )


def test_converter_inteiro_valido():
    assert converter_inteiro("123") == 123


def test_converter_inteiro_invalido():
    assert converter_inteiro("abc") is None


def test_converter_inteiro_vazio():
    assert converter_inteiro("") is None
