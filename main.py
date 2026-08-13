from ETL.extract import extract_data
from ETL.transform import transform_data
from ETL.load import load_data
from logger import get_logger

logger = get_logger(__name__)


def run_pipeline():
    logger.info('Starting ETL pipeline')
    sales_data, stores_data, features_data = extract_data()
    dim_date, dim_stores, dim_feature, fact_sales = transform_data(sales_data, stores_data, features_data)
    load_data(fact_sales, dim_date, dim_stores, dim_feature)
    logger.info('Finished ETL pipeline')


if __name__ == "__main__":
    run_pipeline()
