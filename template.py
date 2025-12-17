import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

project_name = "mlproject"

list_of_files = [
    f"source/{project_name}/__init__.py",
    f"source/{project_name}/components/__init__.py",
    f"source/{project_name}/components/data_ingestion.py",
    f"source/{project_name}/components/data_transformation.py",
    f"source/{project_name}/components/data_training.py",
    f"source/{project_name}/components/data_monitoring.py",
    f"source/{project_name}/pipeline/__init__.py",
    f"source/{project_name}/pipeline/training_pipeline.py",
    f"source/{project_name}/pipeline/prediction_pipeline.py",
    f"source/{project_name}/logger.py",
    f"source/{project_name}/expection.py",
    f"source/{project_name}/utils.py"
]

for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Director created {filedir} for the file {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
        logging.info("File {filename} created under the director {filedir}")
    else:
        logging.info("File already exists")
