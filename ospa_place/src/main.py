import sys
import logging
import argparse

from services.silver.onibus_silver import OnibusSilver
from services.bronze.onibus_bronze import OnibusBronze
from services.bronze.bairros_bronze import BairrosBronze
from services.silver.bairros_silver import BairrosSilver
from services.bronze.empresas_bronze import EmpresasBronze
from services.silver.empresas_silver import EmpresasSilver


def setup_logging():
    """Configure root logger once for entire application"""
    root_logger = logging.getLogger()
    level = logging.INFO
    root_logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Format with module name
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    root_logger.info(f"Logging configured level={level}")


def main():
    # Setup logging FIRST
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset", help="Name of the dataset")
    parser.add_argument("--filename", help="Name of the file to download without extension")
    parser.add_argument("--service", help="Name of the service to run", required=True)

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
