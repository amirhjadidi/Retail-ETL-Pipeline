import pandas as pd
from logger import get_logger

logger = get_logger(__name__)


def transform_data(sales_data, stores_date, features_date):
    logger.info("Starting data transformation")
    features_date["Date"] = pd.to_datetime(
        features_date["Date"], format="mixed", dayfirst=True
    )

    features_date = features_date.fillna(
        {"MarkDown1": 0, "MarkDown2": 0, "MarkDown3": 0, "MarkDown4": 0, "MarkDown5": 0}
    )

    sales_data["Date"] = pd.to_datetime(
        sales_data["Date"], format="mixed", dayfirst=True
    )

    dim_date = sales_data[["Date", "IsHoliday"]].drop_duplicates()
    dim_date = dim_date.assign(
        Year=dim_date["Date"].dt.year,
        Month=dim_date["Date"].dt.month,
        Day=dim_date["Date"].dt.day,
    )

    dim_stores = stores_date.drop_duplicates().reset_index(drop=True)

    dim_feature = features_date.drop_duplicates().reset_index(drop=True)

    fact_sales = sales_data

    def normalize(df):
        df.columns = df.columns.str.lower()
        return df

    dim_date, dim_stores, dim_feature, fact_sales = map(
        normalize, [dim_date, dim_stores, dim_feature, fact_sales]
    )

    logger.info("Data transformation completed successfully")
    return dim_date, dim_stores, dim_feature, fact_sales
