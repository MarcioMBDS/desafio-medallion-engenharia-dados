# Desafio Medallion: <seu nome>

> Substitua este texto pelo resumo do seu projeto em 3 a 5 linhas: o que ele faz, a stack escolhida e o que você considera o diferencial da sua solução.

## Pré-requisitos
- Docker <versão> e Docker Compose <versão>
- Testado em: <Windows 11 / Ubuntu 24.04 / macOS ...>

## Como executar (passo a passo)

```bash
git clone <url-do-repositorio>
cd <pasta>
docker compose up --build
```

1. Aguarde o término do serviço `pipeline` (mensagem esperada: `<descreva>`).
2. Acesse o painel em: <http://localhost:8501> (ajuste a porta).
3. As camadas ficam em `./lake/bronze`, `./lake/silver`, `./lake/quarentena` e `./lake/gold`.

### Usando outro arquivo de entrada
```bash
ENTRADA=/app/data/outro_arquivo.csv docker compose up --build
```
<ajuste conforme sua solução>

### Rodando os testes
```bash
make test
```

## Arquitetura
Veja [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md). <inclua aqui o diagrama>

## Qualidade de dados
Veja [`docs/DECISOES_QUALIDADE.md`](docs/DECISOES_QUALIDADE.md).

## Indicadores e enriquecimento
Veja [`docs/INDICADORES.md`](docs/INDICADORES.md).

## Limitações conhecidas e próximos passos
- <o que ficou de fora e por quê>
- <o que você faria com mais tempo>

## Uso de ferramentas de IA (declaração)
- <ferramenta, para quê usou, e o que você validou manualmente> (ou "não utilizei")
