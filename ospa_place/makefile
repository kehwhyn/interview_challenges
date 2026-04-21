start_services:
	mkdir -p data_lake data_warehouse
	docker compose up -d

stop_services:
	docker compose down
	rm -rf data_lake data_warehouse

run_bairros_bronze:
	docker exec dop-etl python main.py --service bairros_bronze --dataset bairro-oficial --filename 20230502_bairro_oficial

run_bairros_silver:
	docker exec dop-etl python main.py --service bairros_silver --filename 20230502_bairro_oficial

run_onibus_bronze:
	docker exec dop-etl python main.py --service onibus_bronze --dataset ponto-de-onibus --filename 20260401_ponto_onibus

run_onibus_silver:
	docker exec dop-etl python main.py --service onibus_silver --filename 20260401_ponto_onibus

run_empresas_bronze:
	docker exec dop-etl python main.py --service empresas_bronze --dataset atividade-economica --filename 20260401_atividade_economica

run_empresas_silver:
	docker exec dop-etl python main.py --service empresas_silver --filename 20260401_atividade_economica
