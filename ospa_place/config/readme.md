For this project I'm using this folder to store services definition.
I'm also exploring ways to add separation of concerns.
This is a hobby project, exploring local development environment but still adding to my knowledge. I'll change when going cloud.

```text
root
├── docker-compose.yml      # Root compose file with include
└── configs/                # Modular service definitions
     ├── etl.yml
     ├── minio.yml
     └── postgis.yml
```

Then running this at root would be okay and create the services I need
```
docker compose up -d
```

There are other options:
- A massive `docker-compose.yml` file and then settings for each environment under `config` folder
- A folder with overrides

If I wanted I could do something like this to override specific settings
```text
root
├── docker-compose.yml          # Root compose file with include
└── configs/
    ├── services/               # Modular service definitions
    │    ├── etl.yml
    │    ├── minio.yml
    │    └── postgis.yml
    ├── dev.yml
    ├── stg.yml
    └── prd.yml
```

It would run like this?
```
docker compose -f docker-compose.yml -f configs/prd.yml up -d
```
