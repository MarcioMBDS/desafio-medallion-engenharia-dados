# Decisões de Qualidade de Dados

## Critérios adotados

A camada Prata aplica as regras definidas em `data/dicionario_dados.csv`. Registros que falham em uma validação são encaminhados para quarentena com o motivo identificado. Cada linha recebe o primeiro motivo de rejeição encontrado; por isso, as quantidades por motivo não representam necessariamente todos os problemas existentes nos registros.

A política de duplicidade considera a primeira ocorrência de cada ID positivo como a ocorrência principal. As ocorrências seguintes são colocadas em quarentena. O ID é marcado como visto antes das demais validações; assim, uma primeira ocorrência inválida também impede que uma ocorrência posterior com o mesmo ID seja aceita.

## Decisões de qualidade

| # | Coluna(s) | Problema encontrado | Exemplo(s) | Quantidade | Ação | Justificativa |
|---|---|---|---|---:|---|---|
| 1 | id | ID duplicado | ID já encontrado em uma linha anterior | 800 | Rejeitar linha | A Prata exige IDs únicos. O pipeline mantém a primeira ocorrência do ID positivo e rejeita as seguintes. |
| 2 | data_inversa | Data inválida ou fora de 2024 | Data inexistente ou fora do ano | 641 | Rejeitar linha | A data deve ser válida e pertencer ao ano de 2024. |
| 3 | dia_semana | Dia incompatível com a data | Dia informado diferente do calendário | 591 | Rejeitar linha | O dia da semana deve corresponder à data do acidente. |
| 4 | municipio, uf | Município inexistente ou incompatível com a UF | Par município/UF não encontrado na referência | 580 | Rejeitar linha | A combinação precisa existir na referência de municípios. |
| 5 | br | BR inválida ou fora do intervalo | Valor inválido ou fora de 1 a 499 | 549 | Rejeitar linha | A rodovia deve respeitar o intervalo do dicionário. |
| 6 | horario | Horário ausente ou inválido | Horário não reconhecido | 512 | Rejeitar linha | O horário deve ser válido e estar no formato esperado. |
| 7 | mortos | Quantidade inválida ou fora do intervalo de 0 a 50 | Valor não inteiro ou fora do limite | 486 | Rejeitar linha | A contagem deve respeitar o intervalo permitido. |
| 8 | feridos_leves | Quantidade inválida ou fora do intervalo de 0 a 50 | Valor não inteiro ou fora do limite | 459 | Rejeitar linha | A contagem deve respeitar o intervalo permitido. |
| 9 | feridos_graves | Quantidade inválida ou fora do intervalo de 0 a 50 | Valor não inteiro ou fora do limite | 437 | Rejeitar linha | A contagem deve respeitar o intervalo permitido. |
| 10 | uf | UF ausente ou inexistente na referência | Sigla ausente ou não cadastrada | 417 | Rejeitar linha | A UF deve constar na tabela de referência. |
| 11 | latitude, longitude | Coordenadas inválidas ou fora dos limites | Coordenada ausente, zero ou fora do intervalo permitido | 393 | Rejeitar linha | As coordenadas devem respeitar os limites geográficos definidos. |
| 12 | ilesos | Quantidade inválida ou fora do intervalo de 0 a 50 | Valor não inteiro ou fora do limite | 384 | Rejeitar linha | A contagem deve respeitar o intervalo permitido. |
| 13 | veiculos | Quantidade inválida ou fora do intervalo de 1 a 20 | Valor não inteiro ou fora do limite | 377 | Rejeitar linha | O acidente deve ter entre 1 e 20 veículos. |
| 14 | km | KM inválido ou fora do intervalo de 0 a 999,9 | Valor não decimal ou fora do limite | 342 | Rejeitar linha | O quilômetro deve ser não negativo e respeitar o limite do dicionário. |
| 15 | causa_acidente | Causa ausente ou fora do domínio | Categoria não permitida | 327 | Rejeitar linha | A causa deve pertencer ao domínio fechado do dicionário. |
| 16 | tipo_acidente | Tipo ausente ou fora do domínio | Categoria não permitida | 284 | Rejeitar linha | O tipo de acidente deve pertencer ao domínio permitido. |
| 17 | tipo_pista | Tipo de pista ausente ou fora do domínio | Categoria não permitida | 234 | Rejeitar linha | O tipo de pista deve ser Simples, Dupla ou Múltipla. |
| 18 | condicao_metereologica | Condição meteorológica ausente ou fora do domínio | Categoria não permitida | 222 | Rejeitar linha | O valor deve pertencer ao domínio permitido. |
| 19 | pessoas | Total inválido ou fora do intervalo de 1 a 200 | Valor não inteiro ou fora do limite | 206 | Rejeitar linha | O total deve respeitar o intervalo definido. |
| 20 | fase_dia, horario | Fase do dia incompatível com o horário | Faixa horária divergente | 164 | Rejeitar linha | A fase do dia deve corresponder ao horário. |
| 21 | pessoas, mortos, feridos_leves, feridos_graves, ilesos | Total diferente da soma das categorias | Soma divergente do total informado | 161 | Rejeitar linha | O total de pessoas deve ser igual à soma das quatro categorias. |
| 22 | classificacao_acidente, contagens de vítimas | Classificação incompatível com a quantidade de vítimas | Classificação divergente das contagens | 149 | Rejeitar linha | A classificação deve seguir a regra de negócio do dicionário. |
| 23 | classificacao_acidente | Classificação ausente ou fora do domínio | Categoria não permitida | 144 | Rejeitar linha | A classificação deve pertencer ao domínio fechado. |
| 24 | fase_dia | Fase do dia ausente ou fora do domínio | Categoria não permitida | 142 | Rejeitar linha | A fase do dia deve pertencer ao domínio permitido. |
| 25 | latitude, longitude, municipio | Coordenadas incompatíveis com o município | Distância superior a 0,5 grau da referência municipal | 6 | Rejeitar linha | As coordenadas devem ser coerentes com a localização municipal. |

**Critério de contagem:** cada linha em quarentena é contabilizada uma única vez, conforme o primeiro motivo identificado pelo pipeline. As quantidades acima são da execução analisada e devem ser atualizadas se os dados ou as regras mudarem.

## Resumo da execução

| Métrica | Valor |
|---|---:|
| Linhas na Bronze | 40.800 |
| Registros em quarentena por ID duplicado | 800 |
| Linhas na Prata | 31.793 |
| Linhas em quarentena | 9.007 |
| Bronze = Prata + quarentena | 40.800 = 31.793 + 9.007 |
| Campos corrigidos | Não contabilizados individualmente |

A quantidade de campos corrigidos não foi contabilizada individualmente pelo pipeline. A normalização de data, horário e valores numéricos ocorre nos registros aprovados, mas isso não equivale a uma contagem de campos alterados.

## Regras de negócio implementadas

- **Identificador:** exige ID inteiro positivo e único na camada Prata.
- **Data:** exige data válida dentro do ano de 2024.
- **Dia da semana:** deve coincidir com a data e usar o nome em português com a grafia esperada.
- **Horário:** deve ser válido e é normalizado para `HH:MM:SS`.
- **UF e município:** devem existir nas referências, e o município deve pertencer à UF informada.
- **Rodovia e quilômetro:** a BR deve estar entre 1 e 499; o quilômetro, entre 0 e 999,9.
- **Classificação do acidente:** mortos acima de zero implicam `Com Vítimas Fatais`; sem mortos, mas com feridos, implica `Com Vítimas Feridas`; nos demais casos, `Sem Vítimas`.
- **Fase do dia:** é validada em relação ao horário, usando as faixas estabelecidas no dicionário.
- **Contagem de pessoas:** `pessoas` deve ser igual a mortos + feridos leves + feridos graves + ilesos.
- **Contagens e veículos:** as quantidades devem respeitar os limites do dicionário.
- **Domínios textuais:** causa, tipo e classificação do acidente, fase do dia, condição meteorológica e tipo de pista devem respeitar os domínios permitidos.
- **Coordenadas:** latitude e longitude devem estar dentro dos limites estabelecidos, ser diferentes de zero e estar a no máximo 0,5 grau das coordenadas de referência do município.
- **Quarentena:** cada registro rejeitado recebe um motivo, correspondente à primeira validação que falhou.

## O que não foi tratado e por quê

- O pipeline registra apenas o primeiro motivo de rejeição de cada linha. Portanto, não contabiliza todos os problemas presentes em cada registro.
- A política de duplicidade prioriza a primeira ocorrência do ID, mesmo quando ela apresenta outro problema de qualidade. Uma estratégia futura pode avaliar todas as ocorrências e selecionar a primeira válida, desde que essa mudança seja documentada e testada.
- O pipeline ainda não contabiliza individualmente quantos campos foram corrigidos ou normalizados.
- Os registros rejeitados são mantidos em quarentena para permitir auditoria e análise posterior, em vez de serem descartados silenciosamente.
- Os dados são tratados conforme o dicionário e as referências fornecidas. A consistência com essas referências não garante, por si só, que todos os dados representem a realidade.

## Limitações e próximos passos

As validações foram executadas na versão final analisada do pipeline. Os resultados foram conferidos com os arquivos gerados nas camadas Bronze, Prata e Quarentena, e os testes automatizados foram executados com sucesso, totalizando 9 testes aprovados.