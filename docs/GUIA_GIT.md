# Guia de Git para o Desafio

Este guia mostra uma forma simples e profissional de versionar o seu trabalho. A qualidade do seu histórico no Git também é avaliada (veja o peso em [`ENUNCIADO.md`](ENUNCIADO.md)).

## 1. Seu repositório

A equipe de seleção vai informar a URL de um **repositório privado, só seu**, com o nome no padrão:

```
desafio-medallion-<nome>-<sobrenome>
```

Somente você e os avaliadores têm acesso. Se o repositório vier vazio, comece assim:

```bash
git clone <url-do-seu-repositorio>
cd desafio-medallion-<nome>-<sobrenome>

# copie para a RAIZ do repositório: a pasta data/ do kit e, se quiser usar o esqueleto,
# o CONTEÚDO de template/ (Dockerfile, docker-compose.yml, src/, docs/... ficam na raiz,
# ao lado de data/, e não dentro de uma pasta "template")
git add .
git commit -m "chore: importa kit do desafio (dados e dicionário)"
git push origin main
```

## 2. Configure sua identidade (uma vez)

```bash
git config --global user.name  "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

Use sempre a **mesma identidade** nos commits. Ela permite ao avaliador acompanhar sua evolução.

## 3. Branches: fluxo simples e recomendado

| Branch | Para quê |
|---|---|
| `main` | Versão estável e entregável. Só recebe código que funciona. |
| `feature/<assunto>` | Uma branch por funcionalidade (`feature/ingestao-bronze`, `feature/qualidade-prata`, `feature/painel`). |

Fluxo:
```bash
git checkout -b feature/ingestao-bronze
# ... trabalha, testa, faz commits pequenos ...
git push -u origin feature/ingestao-bronze
# abra um Pull/Merge Request para a main (mesmo sendo você mesmo(a) quem aprova)
```

Abrir Pull/Merge Requests, mesmo que sozinho(a), mostra maturidade de processo. Descreva **o que mudou e por quê**.

## 4. Commits: pequenos, frequentes e com mensagem útil

Use o padrão **Conventional Commits**: `tipo: descrição curta no imperativo`.

| Tipo | Quando usar | Exemplo |
|---|---|---|
| `feat` | Nova funcionalidade | `feat: ingere CSV na bronze com hash de linha` |
| `fix` | Correção | `fix: trata decimal com vírgula em km` |
| `docs` | Documentação | `docs: adiciona diagrama de arquitetura` |
| `refactor` | Reorganização sem mudar comportamento | `refactor: separa regras de qualidade em módulo` |
| `test` | Testes | `test: cobre regra de coerência pessoas = soma` |
| `chore` | Infra, configs | `chore: adiciona Dockerfile e compose` |
| `ci` | Integração contínua | `ci: build da imagem no pipeline` |

**Evite:** um único commit gigante no último dia; mensagens como "ajustes", "final", "teste"; commits de arquivos gerados (`lake/`, `__pycache__`, `.env`).

Uma boa história de commits conta como você pensou: primeiro a ingestão, depois a qualidade, depois o enriquecimento, depois o painel.

## 5. O que NÃO versionar

Crie um `.gitignore` (há um modelo em [`../template/.gitignore`](../template/.gitignore)) que exclua:

```
lake/
__pycache__/
*.pyc
.venv/
.env
.ipynb_checkpoints/
.DS_Store
```

**Nunca** faça commit de senhas, tokens, chaves ou dados pessoais. Se fizer por engano, avise a equipe: remover do último commit **não** apaga o segredo do histórico.

Use `.env.example` para listar as variáveis necessárias, **sem valores reais**.

## 6. Dados no repositório

O arquivo de entrada do kit (~7 MB) pode ser versionado. **Não versione** a saída do pipeline (`lake/`): ela é reproduzida pelo container.

## 7. Entrega final

```bash
git checkout main
git pull
git tag -a v1.0-entrega -m "Entrega do desafio"
git push origin main --tags
```

A **data/hora da tag** é o horário oficial de entrega.

## 8. Comandos de sobrevivência

```bash
git status                  # o que mudou?
git log --oneline --graph   # histórico resumido
git diff                    # diferenças ainda não commitadas
git restore <arquivo>       # descarta alterações de um arquivo
git stash / git stash pop   # guarda e recupera alterações temporariamente
```

Dúvida sobre Git? Pergunte à equipe de seleção; **não é pecado pedir ajuda**, pecado é entregar sem testar do zero.
