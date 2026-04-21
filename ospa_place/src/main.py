import argparse

from services.silver.onibus_silver import OnibusSilver
from services.bronze.onibus_bronze import OnibusBronze
from services.bronze.bairros_bronze import BairrosBronze
from services.silver.bairros_silver import BairrosSilver
from services.bronze.empresas_bronze import EmpresasBronze
from services.silver.empresas_silver import EmpresasSilver


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset", help="Name of the dataset")
    parser.add_argument("--filename", help="Name of the file to download without extension")
    parser.add_argument("--service", help="Name of the service to run", required=True)

    args = parser.parse_args()
    print(f"Running service: {args.service} for dataset: {args.dataset} and filename: {args.filename}")

    services: dict[str, object] = {
        "bairros_bronze": BairrosBronze(),
        "bairros_silver": BairrosSilver(),
        "empresas_bronze": EmpresasBronze(),
        "empresas_silver": EmpresasSilver(),
        "onibus_bronze": OnibusBronze(),
        "onibus_silver": OnibusSilver(),
    }

    service = services.get(args.service)

    if service is None:
        print(f"Service {args.service} not found. Available services: {list(services.keys())}")
        return

    service.run(args)

if __name__ == "__main__":
    main()