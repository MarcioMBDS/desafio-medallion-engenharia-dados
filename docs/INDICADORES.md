# Indicadores e Enriquecimento

## Perguntas de negócio e indicadores

| # | Pergunta de negócio | Indicador (KPI) | Tabela da Ouro | Visualização no painel |
|---|---|---|---|---|
| 1 | Em quais meses ocorre a maior quantidade de acidentes? | Quantidade de acidentes por mês | `acidentes_por_mes` | Gráfico de barras |
| 2 | Quais UFs apresentam a maior quantidade de acidentes? | Quantidade de acidentes por UF | `acidentes_por_uf` | Gráfico de barras |
| 3 | Qual é a distribuição dos acidentes por gravidade? | Quantidade de acidentes por classificação | `acidentes_por_classificacao` | Gráfico de barras |

## Enriquecimentos aplicados

| Enriquecimento | Fonte | Licença | Como foi obtido | Funciona sem internet? |
|---|---|---|---|---|
| Nenhum enriquecimento externo nesta versão | Não se aplica | Não se aplica | Indicadores calculados a partir dos dados da camada Silver | Sim |

## Modelagem da camada Ouro

A camada Ouro é composta por três tabelas agregadas:

- `acidentes_por_mes`: quantidade de acidentes agrupada por ano e mês.
- `acidentes_por_uf`: quantidade de acidentes agrupada por unidade federativa.
- `acidentes_por_classificacao`: quantidade de acidentes agrupada por classificação.

Cada registro da camada Silver representa um acidente válido e possui um identificador único. As tabelas da Ouro possuem uma linha por grupo de agregação, sem duplicar os registros de origem.

## Principais achados

A análise dos 31.793 registros aprovados na camada Prata apresentou os seguintes resultados:

- **Distribuição mensal:** julho foi o mês com maior quantidade de registros, totalizando 2.802 acidentes. Fevereiro apresentou a menor quantidade, com 2.504.
- **Distribuição por UF:** São Paulo (SP) apresentou a maior quantidade, com 5.145 acidentes. Rondônia (RO) apresentou a menor, com 200.
- **Classificação:** foram identificados 16.630 acidentes com vítimas feridas, 14.227 sem vítimas e 936 com vítimas fatais.

Os indicadores são apresentados no dashboard desenvolvido com Streamlit.

Os dados utilizados são sintéticos e não representam necessariamente ocorrências reais.

## Ideias futuras

- Enriquecer os dados com informações geográficas externas.
- Criar análises por município e tipo de acidente.
- Comparar períodos e identificar variações nos indicadores.
- Ampliar os testes automatizados e as validações de qualidade.