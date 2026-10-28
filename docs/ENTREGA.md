# Entrega: Checklist e Contrato Mínimo

## 1. Contrato de pastas (obrigatório)

Seu container deve produzir, em um diretório `lake/` na raiz do projeto (montado como volume), a seguinte estrutura. Os nomes de pasta são fixos; o conteúdo interno é livre.

```
lake/
├── bronze/        # dados como vieram + metadados de ingestão
├── silver/        # tabela prata em CSV ou Parquet (pode ter vários arquivos)
├── quarentena/    # linhas rejeitadas, com coluna de motivo (nome contendo "motivo")
└── gold/          # tabelas de indicadores / enriquecidas
```

**Regras do contrato da prata** (usadas pela avaliação automática):
- Formato **CSV** (UTF-8, separador `,` ou `;`) ou **Parquet**.
- Deve conter **todas as 22 colunas** do dicionário, com os **mesmos nomes**, incluindo `id`.
- Datas em `AAAA-MM-DD`, horas em `HH:MM:SS`, decimais com **ponto**.
- Uma linha por `id` (sem duplicatas).
- Colunas técnicas extras (ex.: `_ingestao_ts`) são permitidas.

## 2. Estrutura sugerida do repositório

```
.
├── README.md                  # visão geral + COMO EXECUTAR (obrigatório)
├── docker-compose.yml         # sobe pipeline e painel
├── Dockerfile
├── Makefile                   # atalhos (opcional, recomendado)
├── .env.example               # variáveis de ambiente (sem segredos reais)
├── .gitignore
├── data/                      # arquivo de entrada (como no kit)
├── src/                       # código do pipeline (bronze, prata, ouro, painel)
├── tests/                     # testes automatizados (bônus)
├── docs/
│   ├── ARQUITETURA.md         # desenho + explicação dos componentes
│   ├── DECISOES_QUALIDADE.md  # regra por regra: corrigir, anular ou rejeitar, e por quê
│   ├── INDICADORES.md         # perguntas de negócio, KPIs, fontes de enriquecimento
│   └── img/                   # diagramas
└── lake/                      # gerado em execução; NÃO versionar (.gitignore)
```

O diretório [`../template/`](../template/) traz um esqueleto equivalente, que você pode usar ou ignorar.

## 3. O que o `README.md` deve conter

1. **O que é** o projeto (3 a 5 linhas).
2. **Pré-requisitos** (Docker e versão; sistema operacional testado).
3. **Passo a passo para executar**, com comandos copiáveis, do clone ao painel no navegador. Exemplo:
   ```bash
   git clone <url-do-seu-repositorio>
   cd <pasta>
   docker compose up --build
   # painel em http://localhost:8501
   ```
4. **Como trocar o arquivo de entrada** por outro lote com a mesma estrutura.
5. **Como rodar os testes** (se houver).
6. **Onde estão as camadas** (`lake/...`) e o que cada tabela da ouro contém.
7. **Limitações conhecidas** e **próximos passos**.
8. **Declaração de uso de ferramentas de IA** (veja o [`FAQ`](FAQ.md)).

## 4. Checklist final (marque antes de entregar)

**Funcionalidade**
- [ ] `docker compose up --build` funciona a partir de um clone limpo, sem passos manuais
- [ ] Bronze preserva o dado original e registra metadados de ingestão
- [ ] Segunda execução não duplica a bronze
- [ ] Prata respeita todas as regras do dicionário
- [ ] Rejeitados vão para `lake/quarentena/` com motivo
- [ ] Ouro tem enriquecimento e tabelas de indicadores
- [ ] Painel acessível e com indicadores ligados às perguntas de negócio
- [ ] Pipeline funciona com outro arquivo de mesma estrutura

**Documentação e Git**
- [ ] README com passo a passo testado por você em um clone limpo
- [ ] Diagrama de arquitetura em `docs/`
- [ ] Decisões de qualidade documentadas
- [ ] Commits pequenos, com mensagens claras
- [ ] Nenhum segredo, senha ou dado pessoal no repositório
- [ ] `lake/` fora do versionamento
- [ ] Tag `v1.0-entrega` criada na versão final

## 5. Como entregar

1. Garanta que tudo está na branch `main` do repositório indicado pela equipe.
2. Crie a tag de entrega e envie:
   ```bash
   git tag -a v1.0-entrega -m "Entrega do desafio"
   git push origin main --tags
   ```
3. Avise a equipe de seleção por e-mail (ou pelo canal combinado) informando a URL do repositório.

A **data/hora da tag** vale como horário oficial de entrega. Commits posteriores à tag **não serão considerados** na avaliação.
