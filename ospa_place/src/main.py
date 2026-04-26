import sys
import argparse
import logging as lg

from utils.logger import Logger

from services.extract.onibus_bronze import OnibusBronze
from services.transform.onibus_silver import OnibusSilver
from services.extract.bairros_bronze import BairrosBronze
from services.transform.bairros_silver import BairrosSilver
from services.extract.empresas_bronze import EmpresasBronze
from services.transform.empresas_silver import EmpresasSilver


def main():
    app_logger: Logger = Logger()
    logger: lg.Logging = app_logger.get_logger(__name__)

    parser = argparse.ArgumentParser()

    parser.add_argument("--service", help="Name of the service to run", required=True)
    parser.add_argument("--dataset", help="Name of the dataset")
    parser.add_argument("--filename", help="Name of the file to download without extension")

    args = parser.parse_args()
    logger.info(f"Running service: {args.service} for dataset: {args.dataset} and filename: {args.filename}")

    services: dict[str, object] = {
        "bairros_bronze": BairrosBronze,
        "bairros_silver": BairrosSilver,
        "empresas_bronze": EmpresasBronze,
        "empresas_silver": EmpresasSilver,
        "onibus_bronze": OnibusBronze,
        "onibus_silver": OnibusSilver,
    }

    service_class = services.get(args.service)

    if service_class is None:
        logger.error(f"Service {args.service} not found. Available services: {list(services.keys())}")
        return

    try:
        service = service_class()
        service.run(args)

    except Exception as e:
        logger.exception(f"Service {args.service} failed => {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
