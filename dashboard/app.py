import streamlit as st
import pandas as pd
from pathlib import Path


# Configuração da página — deve vir primeiro
st.set_page_config(
    page_title="Painel de Acidentes Rodoviários",
    page_icon="🚗",
    layout="wide"
)


# Localização da pasta principal do projeto
PASTA_PROJETO = Path(__file__).resolve().parent.parent

# Localização dos arquivos da camada Ouro
PASTA_OURO = PASTA_PROJETO / "lake" / "gold"


# Carregamento das tabelas
@st.cache_data
def carregar_dados():
    acidentes_mes = pd.read_csv(
        PASTA_OURO / "acidentes_por_mes.csv",
        sep=";",
        encoding="utf-8"
    )

    acidentes_uf = pd.read_csv(
        PASTA_OURO / "acidentes_por_uf.csv",
        sep=";",
        encoding="utf-8"
    )

    acidentes_classificacao = pd.read_csv(
        PASTA_OURO / "acidentes_por_classificacao.csv",
        sep=";",
        encoding="utf-8"
    )

    return acidentes_mes, acidentes_uf, acidentes_classificacao


# Recebendo os dados
df_mes, df_uf, df_classificacao = carregar_dados()


# Título principal
st.title("🚗 Painel de Acidentes Rodoviários - Brasil")

# Descrição
st.write(
    "Análise dos acidentes rodoviários registrados em 2024, "
    "com dados processados pela arquitetura Medallion."
)

st.divider()

# Indicadores principais
total_acidentes = int(df_mes["quantidade_acidentes"].sum())

total_ufs = int(df_uf["uf"].nunique())

acidentes_fatais = int(
    df_classificacao.loc[
        df_classificacao["classificacao_acidente"] == "Com Vítimas Fatais",
        "quantidade_acidentes"
    ].sum()
)

# Exibição dos indicadores
col1, col2, col3 = st.columns(3)

col1.metric("Total de acidentes", f"{total_acidentes:,}".replace(",", "."))

col2.metric("UFs com registros", total_ufs)

col3.metric("Acidentes com vítimas fatais", f"{acidentes_fatais:,}".replace(",", "."))


# Gráfico de acidentes por mês
st.divider()

st.subheader("📅 Acidentes por mês em 2024")

st.bar_chart(
    df_mes,
    x="ano_mes",
    y="quantidade_acidentes",
    x_label="Mês",
    y_label="Quantidade de acidentes"
)


# Gráfico de acidentes por UF
st.divider()

st.subheader("📍 Acidentes por Unidade Federativa")

# Ordena as UFs da maior para a menor quantidade de acidentes
df_uf_ordenado = df_uf.sort_values(
    by="quantidade_acidentes",
    ascending=False
)

st.bar_chart(
    df_uf_ordenado,
    x="uf",
    y="quantidade_acidentes",
    x_label="Unidade Federativa",
    y_label="Quantidade de acidentes"
)


# Gráfico de acidentes por classificação
st.divider()

st.subheader("⚠️ Acidentes por classificação")

st.bar_chart(
    df_classificacao,
    x="classificacao_acidente",
    y="quantidade_acidentes",
    x_label="Classificação do acidente",
    y_label="Quantidade de acidentes"
)



# Informações sobre os dados
st.divider()

st.caption(
    "Fonte: conjunto de dados disponibilizado no desafio. "
    "Os registros são sintéticos e não representam necessariamente "
    "ocorrências reais. "
    "Indicadores calculados a partir dos 31.793 registros aprovados "
    "na camada Prata."
)




st.info("Painel em construção. Em breve, indicadores e gráficos estarão disponíveis.")