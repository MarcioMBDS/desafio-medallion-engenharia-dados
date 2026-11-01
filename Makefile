.PHONY: build run up down clean test

build:            ## constrói as imagens
	docker compose build

run:              ## executa só o pipeline
	docker compose run --rm pipeline

up:               ## pipeline + painel
	docker compose up --build

down:             ## derruba os serviços
	docker compose down

clean:            ## apaga o lago gerado (será recriado na próxima execução)
	rm -rf lake

test:             ## roda os testes dentro do container
	docker compose run --rm pipeline python -m pytest -q tests
