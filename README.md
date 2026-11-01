# Pipeline de Dados — Arquitetura Medallion

Projeto desenvolvido como desafio técnico para a etapa de seleção de estágio em Engenharia de Dados.

O objetivo é construir um pipeline de dados utilizando a arquitetura Medallion (Bronze, Prata e Ouro), aplicando regras de qualidade, organizando os dados em camadas e disponibilizando indicadores em um dashboard interativo.

## Tecnologias utilizadas

- Python 3.12
- Pandas
- Streamlit
- Docker e Docker Compose
- Pytest
- Git e GitHub

## Arquitetura do projeto

O pipeline está organizado em três camadas:

**Bronze — Dados brutos**

- Ingestão do arquivo CSV original.
- Preservação dos dados de origem.
- Controle para evitar duplicação da ingestão.

**Prata — Dados tratados**

- Conversão e padronização de tipos e formatos.
- Validação de datas, horários, coordenadas e domínios.
- Verificação de regras de negócio.
- Identificação de registros duplicados.
- Separação dos registros rejeitados em quarentena, com seus respectivos motivos.

**Ouro — Indicadores**

Geração de tabelas agregadas para análise:

- Acidentes por mês.
- Acidentes por unidade federativa.
- Acidentes por classificação.

## Resultados do processamento

Na execução do conjunto de dados disponibilizado no desafio:

| Camada | Registros |
|---|---:|
| Bronze | 40.800 |
| Prata | 31.793 |
| Quarentena | 9.007 |

Os 40.800 registros da Bronze foram distribuídos entre 31.793 registros aprovados na Prata e 9.007 registros rejeitados.

### Indicadores gerados

- **31.793** acidentes aprovados na camada Prata.
- **25** UFs com registros.
- **936** acidentes classificados como com vítimas fatais.
- **2.802** acidentes em julho, mês com maior quantidade de registros.
- **5.145** acidentes registrados em SP, UF com maior quantidade.

O dashboard apresenta esses indicadores e gráficos para facilitar a análise dos dados.

> Os dados disponibilizados no desafio são sintéticos e não representam necessariamente ocorrências reais.

## Estrutura do projeto

```text
desafio-medallion-marcio-moraes/
├── dashboard/
│   └── app.py
├── data/
│   ├── acidentes_2024_bruto.csv
│   ├── dicionario_dados.csv
│   └── referencia/
├── docs/
│   ├── ARQUITETURA.md
│   ├── DECISOES_QUALIDADE.md
│   └── INDICADORES.md
├── src/
│   └── pipeline.py
├── tests/
│   └── test_validacoes_prata.py
├── lake/
│   ├── bronze/
│   ├── silver/
│   ├── quarentena/
│   └── gold/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pytest.ini
└── requirements.txt
```

A pasta `lake/` é gerada durante a execução e não precisa ser versionada no Git.

## Como executar o projeto

### Pré-requisitos

- Docker Desktop instalado e em execução.
- Git instalado.

### 1. Clonar o repositório

```bash
git clone https://github.com/estagio-anasa-serpro/desafio-medallion-marcio-moraes.git
cd desafio-medallion-marcio-moraes
```

### 2. Executar o projeto

```bash
docker compose up --build
```

O Docker Compose executa primeiro o pipeline de dados. Após a conclusão bem-sucedida do processamento, inicia o dashboard.

### 3. Acessar o dashboard

Abra o navegador no endereço:

```text
http://localhost:8501
```

### 4. Encerrar os containers

```bash
docker compose down
```

Os arquivos gerados na pasta `lake/` permanecem disponíveis no ambiente local.

## Testes automatizados

Para executar os testes localmente, tenha Python 3.12 instalado.

Instale as dependências:

```bash
py -3.12 -m pip install -r requirements.txt
```

Execute:

```bash
py -3.12 -m pytest -v
```

Os testes verificam funções de validação e conversão utilizadas no processamento da camada Prata.

**Resultado da execução:** 9 testes aprovados.

## Documentação complementar

- [Arquitetura do projeto](docs/ARQUITETURA.md)
- [Decisões de qualidade dos dados](docs/DECISOES_QUALIDADE.md)
- [Indicadores e enriquecimentos](docs/INDICADORES.md)
- [Enunciado do desafio](docs/ENUNCIADO.md)
- [Requisitos de entrega](docs/ENTREGA.md)

## Possíveis evoluções

- Ampliar a cobertura de testes automatizados.
- Criar indicadores por município e tipo de acidente.
- Implementar monitoramento de qualidade e histórico de processamento.
- Adicionar novos enriquecimentos geográficos.
- Evoluir o pipeline para processamento incremental.

## Uso de inteligência artificial

Ferramentas de inteligência artificial foram utilizadas como apoio durante o desenvolvimento, principalmente para esclarecimento de conceitos, orientação na implementação, revisão de código, identificação de problemas e organização da documentação.

As decisões de implementação, adaptações, execuções e validações do projeto foram realizadas e revisadas durante o desenvolvimento.

---

**Projeto desenvolvido para o desafio técnico de Engenharia de Dados — 2026.**