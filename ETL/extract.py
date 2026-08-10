import pandas as pd
import logging

from config import DATA_DIR

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _read_csv(file_path, data_name):
    try:
        data = pd.read_csv(file_path, encoding="utf-8")
        logger.info(f'Extracted {data_name} data')
        return data
    except FileNotFoundError:
        logger.error(f'{data_name} dataset not found')
        raise
    except Exception as e:
        logger.error(f"Error reading {data_name} data: {e}")
        raise


def extract_data():
    base_path = DATA_DIR

    sales_data = _read_csv(base_path / "sales_dataset.csv", "sales")
    stores_data = _read_csv(base_path / "stores_dataset.csv", "stores")
    features_data = _read_csv(base_path / "features_dataset.csv", "features")

    return sales_data, stores_data, features_data
