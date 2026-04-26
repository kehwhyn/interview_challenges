import sys
import shutil
from pathlib import Path


DATA_LAKE = Path("data_lake")
DATA_WAREHOUSE = Path("data_warehouse")

LAKE_LAYERS = ["bronze", "silver", "gold"]


def create():
    # data_lake + layers
    for layer in LAKE_LAYERS:
        (DATA_LAKE / layer).mkdir(parents=True, exist_ok=True)

    # data_warehouse
    DATA_WAREHOUSE.mkdir(parents=True, exist_ok=True)

    print("Created data_lake (bronze/silver/gold) and data_warehouse")


def delete():
    for path in [DATA_LAKE, DATA_WAREHOUSE]:
        if path.exists():
            shutil.rmtree(path)

    print("Deleted data_lake and data_warehouse (everything inside)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fs_manager.py [create|delete]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "create":
        create()
    elif cmd == "delete":
        delete()
    else:
        print("Invalid command")
