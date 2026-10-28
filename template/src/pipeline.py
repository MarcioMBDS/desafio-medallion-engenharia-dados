"""Ponto de entrada do pipeline (esqueleto). Implemente bronze -> prata -> ouro."""
import os

LAKE_DIR = os.environ.get("LAKE_DIR", "lake")
ENTRADA = os.environ.get("ENTRADA", "data/acidentes_2024_bruto.csv")


def bronze():
    raise NotImplementedError("TODO: ingerir ENTRADA em LAKE_DIR/bronze, com metadados")


def prata():
    raise NotImplementedError("TODO: aplicar regras do dicionário; rejeitados em LAKE_DIR/quarentena")


def ouro():
    raise NotImplementedError("TODO: enriquecer e gerar indicadores em LAKE_DIR/gold")


if __name__ == "__main__":
    for etapa in (bronze, prata, ouro):
        etapa()
