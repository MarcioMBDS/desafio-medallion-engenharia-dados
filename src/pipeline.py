
"""Pipeline de dados de acidentes rodoviários: Bronze, Prata e Ouro."""

import csv
import hashlib
import os
from datetime import datetime, timezone, date, time
from pathlib import Path
from decimal import Decimal, InvalidOperation

LAKE_DIR = Path(os.environ.get("LAKE_DIR", "lake"))
ENTRADA = Path(os.environ.get("ENTRADA", "data/acidentes_2024_bruto.csv"))
BRONZE_DIR = LAKE_DIR / "bronze"
SILVER_DIR = LAKE_DIR / "silver"
QUARENTENA_DIR = LAKE_DIR / "quarentena"
GOLD_DIR = LAKE_DIR / "gold"


REFERENCIA_DIR = ENTRADA.parent / "referencia"
ARQUIVO_BRONZE = BRONZE_DIR / f"{ENTRADA.stem}.csv"
ARQUIVO_SILVER = SILVER_DIR / "acidentes_2024.csv"
ARQUIVO_MUNICIPIOS = REFERENCIA_DIR / "municipios.csv"
ARQUIVO_UFS = REFERENCIA_DIR / "ufs.csv"
COLUNAS_INTEIRAS = [
    "id",
    "br",
    "mortos",
    "feridos_leves",
    "feridos_graves",
    "ilesos",
    "pessoas",
    "veiculos",
]
COLUNAS_DECIMAIS = [
    "km",
    "latitude",
    "longitude",
]

DOMINIOS_TEXTO = {
    "causa_acidente": {
        "Falta de atenção à condução",
        "Velocidade incompatível",
        "Ausência de reação do condutor",
        "Desobediência às normas de trânsito",
        "Ingestão de álcool",
        "Defeito mecânico em veículo",
        "Animais na pista",
        "Condutor dormindo",
        "Falta de atenção do pedestre",
        "Defeito na via",
    },
    "tipo_acidente": {
        "Colisão traseira",
        "Colisão lateral",
        "Colisão frontal",
        "Saída de leito carroçável",
        "Capotamento",
        "Tombamento",
        "Atropelamento de pedestre",
        "Colisão com objeto fixo",
        "Atropelamento de animal",
    },
        "classificacao_acidente": {
        "Sem Vítimas",
        "Com Vítimas Feridas",
        "Com Vítimas Fatais",
    },
    "fase_dia": {
        "Amanhecer",
        "Pleno dia",
        "Anoitecer",
        "Plena Noite",
    },
    "condicao_metereologica": {
        "Céu Claro",
        "Nublado",
        "Chuva",
        "Garoa/Chuvisco",
        "Neblina/Nevoeiro",
        "Vento",
        "Sol",
    },
    "tipo_pista": {
        "Simples",
        "Dupla",
        "Múltipla",
    },
}

def carregar_referencia(caminho):
    """Lê um CSV de referência codificado em UTF-8."""
    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))

def converter_decimal(valor):
    """Converte um valor numérico para Decimal ou retorna None se inválido."""
    if valor is None:
        return None

    valor = valor.strip()

    if not valor or valor.upper() == "NULL":
        return None

    try:
        return Decimal(valor.replace(",", "."))
    except InvalidOperation:
        return None

def converter_data(valor):
    """Converte uma data no formato AAAA-MM-DD ou retorna None."""
    if valor is None:
        return None

    valor = valor.strip()

    try:
        return date.fromisoformat(valor)
    except ValueError:
        return None

def converter_hora(valor):
    """Converte um horário HH:MM:SS ou retorna None."""
    if valor is None:
        return None

    valor = valor.strip()

    try:
        return time.fromisoformat(valor)
    except ValueError:
        return None

def converter_inteiro(valor):
    """Converte um valor para inteiro ou retorna None se inválido."""
    if valor is None:
        return None

    valor = valor.strip()

    if not valor or valor.upper() == "NULL":
        return None

    try:
        return int(valor)
    except ValueError:
        return None

DIAS_SEMANA = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]


def validar_dia_semana(data_registro, dia_informado):
    """Confere se o dia informado corresponde à data."""
    if data_registro is None or not dia_informado:
        return False

    dia_correto = DIAS_SEMANA[data_registro.weekday()]
    return dia_informado.strip() == dia_correto

def validar_uf(uf_informada, ufs_validas):
    """Confere se a UF informada existe na lista de UFs válidas."""
    if not uf_informada:
        return False

    return uf_informada.strip() in ufs_validas

def validar_municipio_uf(municipio_informado, uf_informada, municipios_validos):
    """Confere se o município pertence à UF informada."""
    if not municipio_informado or not uf_informada:
        return False

    chave = (municipio_informado.strip(), uf_informada.strip())
    return chave in municipios_validos

def validar_coordenadas(latitude, longitude):
    """Confere se latitude e longitude estão nos limites definidos."""
    if latitude is None or longitude is None:
        return False

    if latitude == 0 or longitude == 0:
        return False

    latitude_valida = Decimal("-33.75") <= latitude <= Decimal("5.27")
    longitude_valida = Decimal("-73.99") <= longitude <= Decimal("-34.79")

    return latitude_valida and longitude_valida

def validar_distancia_municipio(
    latitude,
    longitude,
    latitude_referencia,
    longitude_referencia,
):
    """Confere se as coordenadas estão a até 0,5 grau da referência."""
    if any(
        valor is None
        for valor in (
            latitude,
            longitude,
            latitude_referencia,
            longitude_referencia,
        )
    ):
        return False

    diferenca_latitude = abs(latitude - latitude_referencia)
    diferenca_longitude = abs(longitude - longitude_referencia)

    return diferenca_latitude <= Decimal("0.5") and diferenca_longitude <= Decimal("0.5")

def validar_classificacao(classificacao, mortos, feridos_leves, feridos_graves):
    """Confere se a classificação corresponde às vítimas registradas."""
    if mortos is None or feridos_leves is None or feridos_graves is None:
        return False

    if mortos > 0:
        classificacao_correta = "Com Vítimas Fatais"
    elif feridos_leves + feridos_graves > 0:
        classificacao_correta = "Com Vítimas Feridas"
    else:
        classificacao_correta = "Sem Vítimas"

    return classificacao == classificacao_correta

def validar_fase_dia(fase_informada, horario):
    """Confere se a fase do dia corresponde ao horário do acidente."""
    if horario is None or not fase_informada:
        return False

    if time(5, 0) <= horario < time(7, 0):
        fase_correta = "Amanhecer"
    elif time(7, 0) <= horario < time(18, 0):
        fase_correta = "Pleno dia"
    elif time(18, 0) <= horario < time(19, 30):
        fase_correta = "Anoitecer"
    else:
        fase_correta = "Plena Noite"

    return fase_informada.strip() == fase_correta

def validar_dominio(coluna, valor):
    """Confere se um valor pertence ao domínio permitido da coluna."""
    if not valor:
        return False

    dominio = DOMINIOS_TEXTO.get(coluna)

    if dominio is None:
        return True

    return valor.strip() in dominio

def validar_intervalo(valor, minimo, maximo):
    """Confere se um valor numérico está dentro de um intervalo."""
    if valor is None:
        return False

    return minimo <= valor <= maximo

def validar_data_acidente(data_registro):
    """Confere se a data é válida e pertence ao ano de 2024."""
    return data_registro is not None and data_registro.year == 2024

def validar_total_pessoas(pessoas, mortos, feridos_leves, feridos_graves, ilesos):
    """Confere se o total de pessoas corresponde à soma das categorias."""
    valores = (pessoas, mortos, feridos_leves, feridos_graves, ilesos)

    if any(valor is None for valor in valores):
        return False

    total_calculado = mortos + feridos_leves + feridos_graves + ilesos

    return pessoas == total_calculado

def carregar_municipios_validos(caminho):
    """Carrega municípios e coordenadas em um dicionário de consulta."""
    municipios = {}

    for registro in carregar_referencia(caminho):
        chave = (registro["municipio"].strip(), registro["uf"].strip())

        municipios[chave] = {
            "latitude": converter_decimal(registro["latitude_ref"]),
            "longitude": converter_decimal(registro["longitude_ref"]),
        }

    return municipios

def carregar_ufs_validas(caminho):
    """Carrega as siglas das UFs válidas em um conjunto."""
    return {
        registro["uf"].strip()
        for registro in carregar_referencia(caminho)
        if registro.get("uf")
    }

def bronze():
    """Preserva os registros originais e acrescenta metadados de ingestão."""
    if not ENTRADA.is_file():
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {ENTRADA}")

    destino = LAKE_DIR / "bronze"
    destino.mkdir(parents=True, exist_ok=True)

    nome_saida = f"{ENTRADA.stem}.csv"
    arquivo_saida = destino / nome_saida
    arquivo_metadados = destino / f"{ENTRADA.stem}_metadados.csv"

    # Lemos os bytes originais para calcular uma impressão digital do arquivo.
    conteudo_original = ENTRADA.read_bytes()
    hash_arquivo = hashlib.sha256(conteudo_original).hexdigest()

    # A mesma origem com o mesmo conteúdo não precisa ser ingerida novamente.
    if arquivo_saida.exists() and arquivo_metadados.exists():
        with arquivo_metadados.open("r", encoding="utf-8", newline="") as arquivo:
            metadados_existentes = next(csv.DictReader(arquivo), None)

        if metadados_existentes and metadados_existentes["hash_arquivo"] == hash_arquivo:
            print("Bronze: arquivo já ingerido, sem duplicar.")
            return

    # O arquivo original é copiado sem converter codificação ou valores.
    arquivo_saida.write_bytes(conteudo_original)

    instante_ingestao = datetime.now(timezone.utc).isoformat()
    linhas_metadados = []

    # Latin-1 é a codificação definida no enunciado.
    texto = conteudo_original.decode("latin-1")
    leitor = csv.reader(texto.splitlines(), delimiter=";")

    cabecalho = next(leitor, None)
    if cabecalho is None:
        raise ValueError("O arquivo de entrada está vazio.")

    for numero_linha, campos in enumerate(leitor, start=2):
        linha_original = ";".join(campos)
        hash_linha = hashlib.sha256(
            linha_original.encode("latin-1")
        ).hexdigest()

        linhas_metadados.append({
            "arquivo_origem": ENTRADA.name,
            "data_hora_ingestao": instante_ingestao,
            "numero_linha": numero_linha,
            "hash_arquivo": hash_arquivo,
            "hash_linha": hash_linha,
        })

    with arquivo_metadados.open("w", encoding="utf-8", newline="") as arquivo:
        campos_metadados = [
            "arquivo_origem",
            "data_hora_ingestao",
            "numero_linha",
            "hash_arquivo",
            "hash_linha",
        ]
        escritor = csv.DictWriter(arquivo, fieldnames=campos_metadados)
        escritor.writeheader()
        escritor.writerows(linhas_metadados)

    print(f"Bronze: arquivo preservado em {arquivo_saida}")
    print(f"Bronze: {len(linhas_metadados)} registros com metadados.")


def prata():
    """Lê os dados da Bronze e prepara a validação da camada Prata."""

    SILVER_DIR.mkdir(parents=True, exist_ok=True)
    QUARENTENA_DIR.mkdir(parents=True, exist_ok=True)

    if not ARQUIVO_BRONZE.exists():
        raise FileNotFoundError(
            f"Arquivo Bronze não encontrado: {ARQUIVO_BRONZE}. "
            "Execute a etapa Bronze primeiro."
        )

    with ARQUIVO_BRONZE.open(
        "r",
        encoding="latin-1",
        newline="",
    ) as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        colunas = leitor.fieldnames
        registros = list(leitor)

    print(f"Prata: {len(registros)} registros lidos da Bronze.")
    print(f"Prata: {len(colunas)} colunas identificadas.")

    ufs_validas = carregar_ufs_validas(ARQUIVO_UFS)
    municipios_validos = carregar_municipios_validos(ARQUIVO_MUNICIPIOS)

    print(f"Prata: {len(ufs_validas)} UFs carregadas para validação.")
    print(f"Prata: {len(municipios_validos)} municípios carregados para validação.")

    ids_vistos = set()
    registros_prata = []
    registros_quarentena = []

    for registro in registros:
        id_registro = converter_inteiro(registro.get("id"))

        if id_registro is None or id_registro <= 0:
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "ID ausente, inválido ou menor que 1",
            })
            continue

        if id_registro in ids_vistos:
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "ID duplicado",
            })
            continue

        ids_vistos.add(id_registro)

        data_registro = converter_data(registro.get("data_inversa"))

        if not validar_data_acidente(data_registro):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Data inválida ou fora do ano de 2024",
            })
            continue

        registro["data_inversa"] = data_registro.isoformat()

        dia_semana = registro.get("dia_semana", "").strip()


        if not validar_dia_semana(data_registro, dia_semana):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Dia da semana incompatível com a data",
            })
            continue

        horario = converter_hora(registro.get("horario"))

        if horario is None:
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Horário ausente ou inválido",
            })
            continue

        registro["horario"] = horario.strftime("%H:%M:%S")

        uf = registro.get("uf", "").strip()

        if not validar_uf(uf, ufs_validas):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "UF ausente ou inexistente na referência",
            })
            continue

        municipio = registro.get("municipio", "").strip()

        if not validar_municipio_uf(
            municipio,
            uf,
            municipios_validos,
        ):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Município inexistente ou incompatível com a UF",
            })
            continue

        br = converter_inteiro(registro.get("br"))

        if not validar_intervalo(br, 1, 499):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "BR inválida ou fora do intervalo de 1 a 499",
            })
            continue

        km = converter_decimal(registro.get("km"))

        if not validar_intervalo(km, Decimal("0"), Decimal("999.9")):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "KM inválido ou fora do intervalo de 0 a 999,9",
            })
            continue

        mortos = converter_inteiro(registro.get("mortos"))

        if not validar_intervalo(mortos, 0, 50):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Quantidade de mortos inválida ou fora do intervalo de 0 a 50",
            })
            continue

        feridos_leves = converter_inteiro(registro.get("feridos_leves"))

        if not validar_intervalo(feridos_leves, 0, 50):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Quantidade de feridos leves inválida ou fora do intervalo de 0 a 50",
            })
            continue

        feridos_graves = converter_inteiro(registro.get("feridos_graves"))

        if not validar_intervalo(feridos_graves, 0, 50):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Quantidade de feridos graves inválida ou fora do intervalo de 0 a 50",
            })
            continue

        ilesos = converter_inteiro(registro.get("ilesos"))

        if not validar_intervalo(ilesos, 0, 50):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Quantidade de ilesos inválida ou fora do intervalo de 0 a 50",
            })
            continue

        pessoas = converter_inteiro(registro.get("pessoas"))

        if not validar_intervalo(pessoas, 1, 200):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Total de pessoas inválido ou fora do intervalo de 1 a 200",
            })
            continue

        if not validar_total_pessoas(
            pessoas,
            mortos,
            feridos_leves,
            feridos_graves,
            ilesos,
        ):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Total de pessoas diferente da soma das categorias",
            })
            continue


        veiculos = converter_inteiro(registro.get("veiculos"))

        if not validar_intervalo(veiculos, 1, 20):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Quantidade de veículos inválida ou fora do intervalo de 1 a 20",
            })
            continue


        causa_acidente = registro.get("causa_acidente", "")

        if not validar_dominio("causa_acidente", causa_acidente):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Causa do acidente ausente ou fora do domínio permitido",
            })
            continue


        tipo_acidente = registro.get("tipo_acidente", "")

        if not validar_dominio("tipo_acidente", tipo_acidente):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Tipo de acidente ausente ou fora do domínio permitido",
            })
            continue


        classificacao = registro.get("classificacao_acidente", "")

        if not validar_dominio("classificacao_acidente", classificacao):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Classificação do acidente ausente ou fora do domínio permitido",
            })
            continue

        if not validar_classificacao(
            classificacao,
            mortos,
            feridos_leves,
            feridos_graves,
        ):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Classificação incompatível com a quantidade de vítimas",
            })
            continue

        fase_dia = registro.get("fase_dia", "")

        if not validar_dominio("fase_dia", fase_dia):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Fase do dia ausente ou fora do domínio permitido",
            })
            continue

        if not validar_fase_dia(fase_dia, horario):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Fase do dia incompatível com o horário do acidente",
            })
            continue

        condicao_metereologica = registro.get("condicao_metereologica", "")

        if not validar_dominio("condicao_metereologica", condicao_metereologica):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Condição meteorológica ausente ou fora do domínio permitido",
            })
            continue

        tipo_pista = registro.get("tipo_pista", "")

        if not validar_dominio("tipo_pista", tipo_pista):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Tipo de pista ausente ou fora do domínio permitido",
            })
            continue

        latitude = converter_decimal(registro.get("latitude"))
        longitude = converter_decimal(registro.get("longitude"))

        if not validar_coordenadas(latitude, longitude):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Latitude ou longitude inválida ou fora dos limites definidos",
            })
            continue

        coordenadas_municipio = municipios_validos[(municipio, uf)]

        latitude_referencia = coordenadas_municipio["latitude"]
        longitude_referencia = coordenadas_municipio["longitude"]

        if not validar_distancia_municipio(
            latitude,
            longitude,
            latitude_referencia,
            longitude_referencia,
        ):
            registros_quarentena.append({
                **registro,
                "motivo_quarentena": "Coordenadas incompatíveis com o município informado",
            })
            continue

        for coluna in registro:
            if isinstance(registro[coluna], str):
                registro[coluna] = registro[coluna].strip()

        registro["id"] = str(id_registro)
        registro["br"] = str(br)
        registro["km"] = str(km)
        registro["mortos"] = str(mortos)
        registro["feridos_leves"] = str(feridos_leves)
        registro["feridos_graves"] = str(feridos_graves)
        registro["ilesos"] = str(ilesos)
        registro["pessoas"] = str(pessoas)
        registro["veiculos"] = str(veiculos)
        registro["latitude"] = str(latitude)
        registro["longitude"] = str(longitude)

        registros_prata.append(registro)

    print(f"Prata: {len(registros_prata)} registros aprovados.")
    print(f"Prata: {len(registros_quarentena)} registros em quarentena.")
    assert len(registros_prata) + len(registros_quarentena) == len(registros)


    arquivo_silver = SILVER_DIR / "acidentes_2024.csv"

    with arquivo_silver.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas,
            delimiter=";",
            extrasaction="ignore",
        )
        escritor.writeheader()
        escritor.writerows(registros_prata)

    print(f"Prata: arquivo salvo em {arquivo_silver}.")


    arquivo_quarentena = QUARENTENA_DIR / "acidentes_2024.csv"
    colunas_quarentena = colunas + ["motivo_quarentena"]

    with arquivo_quarentena.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=colunas_quarentena,
            delimiter=";",
            extrasaction="ignore",
        )
        escritor.writeheader()
        escritor.writerows(registros_quarentena)

    print(f"Prata: arquivo salvo em {arquivo_quarentena}.")



def ouro():
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_SILVER, "r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        registros = list(leitor)

    print(f"Ouro: {len(registros)} registros carregados da Silver.")

    acidentes_por_mes = {}

    acidentes_por_uf = {}

    for registro in registros:
        uf = registro["uf"]
        acidentes_por_uf[uf] = acidentes_por_uf.get(uf, 0) + 1

    print("\nOuro: acidentes por UF:")
    for uf, quantidade in sorted(
        acidentes_por_uf.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"{uf}: {quantidade} acidentes")

    arquivo_gold_uf = GOLD_DIR / "acidentes_por_uf.csv"

    with open(arquivo_gold_uf, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["uf", "quantidade_acidentes"])

        for uf, quantidade in sorted(
            acidentes_por_uf.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            escritor.writerow([uf, quantidade])

    print(f"\nOuro: tabela por UF salva em {arquivo_gold_uf}.")

    acidentes_por_classificacao = {}

    for registro in registros:
        classificacao = registro["classificacao_acidente"]
        acidentes_por_classificacao[classificacao] = (
            acidentes_por_classificacao.get(classificacao, 0) + 1
        )

    print("\nOuro: acidentes por classificação:")
    for classificacao, quantidade in sorted(
        acidentes_por_classificacao.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(f"{classificacao}: {quantidade} acidentes")

    arquivo_gold_classificacao = GOLD_DIR / "acidentes_por_classificacao.csv"

    with open(arquivo_gold_classificacao, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["classificacao_acidente", "quantidade_acidentes"])

        for classificacao, quantidade in sorted(
            acidentes_por_classificacao.items(),
            key=lambda item: item[1],
            reverse=True,
        ):
            escritor.writerow([classificacao, quantidade])

    print(
        f"\nOuro: tabela por classificação salva em "
        f"{arquivo_gold_classificacao}."
    )




    for registro in registros:
        data_acidente = registro["data_inversa"]
        ano_mes = data_acidente[:7]

        acidentes_por_mes[ano_mes] = acidentes_por_mes.get(ano_mes, 0) + 1

    print("\nOuro: acidentes por mês:")
    for mes, quantidade in sorted(acidentes_por_mes.items()):
        print(f"{mes}: {quantidade} acidentes")

    arquivo_gold_mes = GOLD_DIR / "acidentes_por_mes.csv"

    with open(arquivo_gold_mes, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["ano_mes", "quantidade_acidentes"])

        for mes, quantidade in sorted(acidentes_por_mes.items()):
            escritor.writerow([mes, quantidade])

    print(f"\nOuro: tabela mensal salva em {arquivo_gold_mes}.")


if __name__ == "__main__":
    bronze()
    prata()
    ouro()