import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from logger import get_logger

load_dotenv()

logger = get_logger(__name__)

# Database configuration from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
POOL_SIZE = 5
MAX_OVERFLOW = 10
CHUNK_SIZE = 1000


def load_data(fact_sales, dim_date, dim_stores, dim_feature):
    try:
        admin_engine = create_engine(
            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres',
            isolation_level="AUTOCOMMIT",
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW
        )

        with admin_engine.connect() as conn:
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": DB_NAME}
            )
            db_exists = result.scalar() is not None

            if not db_exists:
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                logger.info(f"Database '{DB_NAME}' created successfully")
            else:
                logger.info(f"Database '{DB_NAME}' already exists")

        engine = create_engine(
            f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
            pool_size=POOL_SIZE,
            max_overflow=MAX_OVERFLOW
        )

        with engine.begin() as conn:
            fact_sales.to_sql(
                'fact_sales',
                conn,
                schema='public',
                if_exists='replace',
                index=False,
                chunksize=CHUNK_SIZE
            )

            dim_date.to_sql(
                'dim_date',
                conn,
                schema='public',
                if_exists='replace',
                index=False,
                chunksize=CHUNK_SIZE
            )

            dim_stores.to_sql(
                'dim_stores',
                conn,
                schema='public',
                if_exists='replace',
                index=False,
                chunksize=CHUNK_SIZE
            )

            dim_feature.to_sql(
                'dim_feature',
                conn,
                schema='public',
                if_exists='replace',
                index=False,
                chunksize=CHUNK_SIZE
            )

        logger.info('Database tables created!')
        logger.info('Data loaded successfully')

    except Exception as e:
        logger.error(f'Error during data loading: {str(e)}')
        raise
