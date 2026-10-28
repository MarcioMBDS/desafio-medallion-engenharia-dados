# Enunciado do Desafio

## 1. Contexto

Você integra o time de dados de uma organização que recebe, de várias fontes, arquivos de **ocorrências de acidentes em rodovias federais**. Os arquivos chegam com problemas: formatos misturados, valores fora do domínio, duplicidades e incoerências.

Sua missão é transformar esse arquivo bruto em **informação confiável e útil** usando a **arquitetura medallion**, e comunicar o resultado em um **painel**.

## 2. Sobre o dataset

- Arquivo: `data/acidentes_2024_bruto.csv`
- Formato: **CSV, separador `;`, codificação ISO-8859-1 (Latin-1)**, decimais com vírgula. Isto é intencional e comum em dados abertos governamentais.
- Cerca de 40 mil linhas e 22 colunas.
- **Origem e natureza:** os dados são **sintéticos** (fictícios). A estrutura de colunas é inspirada nos [Dados Abertos da PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf), mas os registros **não representam ocorrências reais**. Não tire conclusões sobre trânsito real a partir deles.
- O arquivo mistura registros **íntegros** e registros **"fora do padrão"**. Não vamos dizer quais nem quantos. Descobrir isso faz parte do desafio.
- O [dicionário de dados](../data/dicionario_dados.csv) define, para cada coluna, o tipo, o domínio e as regras de qualidade. **O dicionário é a fonte da verdade**: o que o contradiz está errado.
- As tabelas em [`data/referencia/`](../data/referencia/) trazem os domínios válidos de UFs e municípios (com coordenadas aproximadas de referência).

## 3. O que você deve entregar

### 3.1 Camada Bronze
- Ingerir o arquivo bruto **sem alterar seu conteúdo**, preservando a fidelidade ao original.
- Registrar **metadados de ingestão** (por exemplo: arquivo de origem, data/hora da carga, número da linha, hash da linha).
- Uma segunda execução **não deve duplicar** dados (a ingestão deve ser idempotente).

### 3.2 Camada Prata
- Aplicar **todas** as regras do dicionário de dados: tipos, formatos, domínios, faixas e **regras de negócio** (coerências entre colunas).
- Decidir, e **documentar**, o que fazer com cada tipo de problema: **corrigir** (quando o valor correto é deduzível com segurança), **anular** ou **rejeitar** a linha.
- Registros rejeitados devem ir para uma **área de quarentena** com o **motivo** da rejeição (isso conta pontos).
- A tabela prata deve manter o campo `id` e os **mesmos nomes de coluna do dicionário**.
- Não vale "arrumar" valores sem critério: queremos corrigir o que é corrigível e **não inventar** o que não é.

### 3.3 Camada Ouro
- Enriquecer os dados **com criatividade**: fontes externas públicas, colunas derivadas, calendário (feriados), geografia, faixas horárias, índices, o que você imaginar.
- Definir **você mesmo(a)** os indicadores (KPIs) e modelar tabelas prontas para consumo que os sustentem.
- Cada indicador deve ter uma **pergunta de negócio** associada (ex.: "Em que horários os acidentes são mais graves?").

### 3.4 Painel
- Apresentar seus indicadores em um painel. **A ferramenta é livre** (Streamlit, Grafana, Superset, Metabase, Power BI em container, Dash, HTML estático, notebook, o que preferir).
- O painel deve subir **junto com o container** ou ser gerado por ele, e ser acessível seguindo o passo a passo da sua documentação.
- Valorizamos clareza: um painel simples que responde bem às perguntas vale mais que um painel enfeitado.

### 3.5 Docker e reprodutibilidade
- Todo o trabalho deve rodar em **container Docker** (de preferência com `docker compose`).
- Um avaliador, em uma máquina limpa, deve conseguir executar seguindo apenas o seu passo a passo.
- O pipeline precisa funcionar também se trocarmos o arquivo de entrada por **outro lote com a mesma estrutura** (faremos esse teste na apresentação).

### 3.6 Documentação e Git
- Todo o projeto versionado no repositório indicado pela equipe (veja o [`GUIA_GIT`](GUIA_GIT.md)).
- Documentação mínima: visão geral, **desenho de arquitetura**, **decisões de qualidade de dados**, indicadores e perguntas de negócio, **passo a passo para executar e visualizar o painel** (veja o [`ENTREGA`](ENTREGA.md)).

## 4. Liberdade e restrições

**Livre:** linguagem (Python e Java são as mais usadas por aqui, mas não é obrigatório), bibliotecas e frameworks (pandas, Spark/PySpark, DuckDB, Polars, SQL, dbt...), formato de armazenamento (Parquet, Delta, CSV, SQLite...), ferramenta de painel, enriquecimentos.

**Obrigatório:** as três camadas, container Docker, repositório Git, documentação, e o contrato de pastas descrito em [`ENTREGA.md`](ENTREGA.md).

**Proibido:** editar manualmente o CSV de origem; dados reais de pessoas; credenciais ou segredos no repositório.

## 5. Prazo e esforço

- **Prazo para entrega:** definido pela equipe de seleção no convite (sugestão: 5 dias corridos). A referência é a **data/hora da tag de entrega** no Git.
- **Esforço estimado:** 8 a 12 horas. Não precisa fazer tudo. **Entregue algo que funcione de ponta a ponta e documente o que ficaria para uma próxima versão.**

## 6. Como será avaliado

| Dimensão | Peso |
|---|---|
| Engenharia: camadas, ingestão, idempotência, estrutura do código | 20 |
| Qualidade de dados: aderência ao dicionário, critério nas correções, quarentena | 25 |
| Enriquecimento e indicadores: criatividade, relevância, valor de negócio | 15 |
| Painel: clareza e utilidade | 10 |
| Docker e reprodutibilidade | 10 |
| Git e boas práticas (commits, branches, CI opcional) | 10 |
| Documentação e arquitetura | 10 |

Parte da avaliação da camada prata é **automática**: comparamos sua prata com um gabarito que nós conhecemos. Por isso o contrato de pastas e os nomes de colunas importam.

## 7. Apresentação

O(s) candidato(s) selecionado(s) fará(ão) uma apresentação de **15 minutos** + 10 minutos de perguntas: arquitetura, decisões de qualidade, indicadores, demonstração do painel e **execução do pipeline sobre um lote novo**. Esteja preparado(a) para explicar **qualquer linha do seu código**.

## 8. Conduta

Veja o [`FAQ`](FAQ.md) sobre uso de ferramentas de IA e consulta a materiais externos. Resumo: é permitido, **desde que declarado** e que você domine o que entregou.
