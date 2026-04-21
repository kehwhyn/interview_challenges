# Desafio OSPA Place - Pipeline de Dados

## Proposta de Solução

Insights que tentei analisar com os datasets de bairros, empresas e pontos de ônibus:
- Contar empresas por bairros
- Identificar bairros sem empresas
- Segmentar empresas por MEI ou não
- Identificas empresas que possuem filias em quais bairros
- Cobertura de transporte público por bairros
- Fazer mapas de calor utilizando cálculo de densidade, por exemplo densidade comercial e pontos de ônibus

Meu foco quando fiz o brainstorm foi pensar em lugares com grandes fluxos de pessoas. Tentei imaginar como seria o processo de decidir onde abrir filiais de MC/BK/Farmácias. Procurar por áreas com quantidade razoável de comércios e acessibilidade.

Acabei me empolgando um pouco no de senvolvimento (eu me diverti na real) e criei um monorepo de serviço de dados, onde tudo está conectado e as alterações ocorrem no mesmo lugar. O objetivo é tentar reaproveitar código. Utilizei pandas para manipular os dados. MinIO para simular um S3 e PostGIS como base de dados com foco em dados geoespaciais. Fiz uso do Docker para que rode em qualquer máquina. Testei em outra máquina também e a princípio tudo rodou certo. No windows mkdir se comporta de forma diferente e eu não estava familiarizada, mas tá sinalizado mais abaixo caso dê problema.

Sei fazer visualizações mais simples, mas ainda assim me esforcei ao máximo. Não consegui fazer várias, pois não tenho tanta RAM disponível.

Próximos passos: adicionar spark, adicionar airflow para orquestrar, refatorar código e melhorar integrações.

## Pré-Requisitos

- Docker Desktop (Docker e Docker Compose)

## Iniciando os Serviços

### 1. Iniciar todos os serviços

```bash
make start_services
```

Isso inicia:
- MinIO (acesso via http://localhost:9090)
- PostgreSQL (porta 5432)
- Serviço ETL (aguarda as dependências ficarem saudáveis)

Caso dê erro nesse passo, é necessário deletar a pasta `data_warehouse` antes de rodar novamente.

### 2. Executando Pipelines ETL

```bash
make run_bronze_service
```

O que o comando roda:
```bash
docker exec dop-etl python src/main.py \
  --service bairros_bronze \
  --dataset bairro-oficial \
  --filename 20230502_bairro_oficial
```

### 3. Parar os serviços

```bash
make stop_services
```

### Comandos Úteis do Makefile

| Comando | Descrição |
|---------|-----------|
| `make start_services` | Inicia todos os serviços |
| `make stop_services` | Para todos os serviços |
| `make run_bronze_service` | Executa importação de dados brutos |
| `make run_silver_service` | Executa a transformação dos dados brutos |

## Arquitetura

### Estrutura do Projeto

```
desafio-ospa-place/
├── src/
│   ├── main.py                 # Ponto de entrada do pipeline
│   ├── settings.py             # Configurações da aplicação
│   ├── requirements.txt        # Dependências do projeto
│   ├── Dockerfile              # Container do serviço ETL
│   ├── connections/            # Conexões com BD e serviços
│   ├── services/
│   │   ├── bronze/             # Camada bronze (dados brutos)
│   │   ├── silver/             # Camada silver (dados transformados)
│   │   └── gold/               # Camada gold (dados agregados)
│   └── explore/                # Scripts exploratórios
├── data_lake/                  # Volumes do MinIO
├── data_warehouse/             # Volumes do PostgreSQL
├── docker-compose.yml          # Definição dos serviços
├── init-db.sql                 # Script de inicialização do BD
├── makefile                    # Comandos auxiliares
└── README.md                   # Este arquivo
```

### Componentes Principais

```
┌─────────────────────────────────────────────────────────┐
│                   Camadas de Dados                      │
├─────────────────────────────────────────────────────────┤
│ Bronze  │ Dados brutos do MinIO (S3-compatível)         │
│ Silver  │ Dados transformados e limpos                  │
│ Gold    │ Dados agregados prontos para análise          │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│ Data Warehouse (PostgreSQL + PostGIS)                   │
│ Armazena dados processados para consultas analíticas    │
└─────────────────────────────────────────────────────────┘
```

### Dependências Principais

- **minio** (7.2.20+): Cliente para acesso ao MinIO
- **pandas** (3.0.2+): Processamento de dados
- **sqlalchemy** (2.0.49+): ORM para banco de dados
- **psycopg2-binary** (2.9.11+): Driver PostgreSQL
- **geoalchemy2** (0.19+): Extensão SQLAlchemy para dados geográficos
- **pyarrow** (23.0.1+): Suporte para formato Parquet
- **s3fs** (2026.3.0+): Acesso a sistemas compatíveis com S3
