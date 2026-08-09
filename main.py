from ETL.Extract import extract_data


if __name__ == "__main__":
    sales_data, stores_data, features_data = extract_data()
    print(sales_data.head())

