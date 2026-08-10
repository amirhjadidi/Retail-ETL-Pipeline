from ETL.extract import extract_data
from ETL.transform import transform_data

if __name__ == "__main__":
    sales_data, stores_data, features_data = extract_data()
    dim_date, dim_stores, dim_feature, fact_sales = transform_data(sales_data, stores_data, features_data)
