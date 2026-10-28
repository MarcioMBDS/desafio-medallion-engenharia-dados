# Desafio Prático: Lago de Dados com Arquitetura Medallion

Bem-vindo(a) à terceira etapa do processo seletivo de estágio em **Engenharia de Dados, Big Data, Ciência de Dados**.

Neste desafio você vai construir, do zero, um pequeno pipeline de dados completo: **ler dados "sujos", organizá-los em camadas (bronze, prata e ouro), gerar indicadores e apresentá-los em um painel**, tudo empacotado em um **container Docker** e versionado no **Git**.

Não existe uma única resposta certa. Queremos ver **como você pensa**, o que você **já sabe fazer na prática** e o quanto você consegue **criar e inovar** com autonomia.

## O que está neste kit

| Caminho | Conteúdo |
|---|---|
| [`docs/ENUNCIADO.md`](docs/ENUNCIADO.md) | O desafio em detalhes: requisitos, prazos e regras |
| [`docs/ARQUITETURA_MEDALLION.md`](docs/ARQUITETURA_MEDALLION.md) | Orientação sobre as camadas e o que esperamos em cada uma |
| [`docs/ENTREGA.md`](docs/ENTREGA.md) | Checklist de entrega e contrato mínimo da estrutura de pastas |
| [`docs/GUIA_GIT.md`](docs/GUIA_GIT.md) | Como organizar repositório, branches e commits |
| [`docs/FAQ.md`](docs/FAQ.md) | Perguntas frequentes e uso de ferramentas de IA |
| [`data/acidentes_2024_bruto.csv`](data/) | **O dataset** (mistura de registros íntegros e "fora do padrão") |
| [`data/dicionario_dados.csv`](data/dicionario_dados.csv) | **O dicionário de dados** com as regras que a camada prata deve respeitar |
| [`data/referencia/`](data/referencia/) | Tabelas de apoio: UFs e municípios (domínios válidos) |
| [`template/`](template/) | Esqueleto opcional de projeto (Dockerfile, compose, Makefile, CI, modelos de documentação) |

## Em uma frase

> Pegue `acidentes_2024_bruto.csv`, grave-o **como veio** na **bronze**, aplique as regras do dicionário para gerar a **prata**, enriqueça e agregue na **ouro**, mostre os indicadores que **você** escolher em um **painel**, e entregue tudo rodando com `docker compose up`.

## Por onde começar

1. Leia o [`ENUNCIADO`](docs/ENUNCIADO.md) até o fim.
2. Abra o dicionário e o CSV e **explore antes de programar** (veja a seção "Sobre o dataset" do enunciado).
3. Crie seu repositório seguindo o [`GUIA_GIT`](docs/GUIA_GIT.md).
4. Comece pelo pipeline mais simples que funcione de ponta a ponta e evolua a partir dele.

Boa sorte, e divirta-se com os dados!

