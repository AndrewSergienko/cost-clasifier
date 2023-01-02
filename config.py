class Config:
    DB_USER = "postgres"
    DB_PASSWORD = "123456"
    DB_NAME = "finances"
    DB_HOST = "localhost"
    DB_CONFIG = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"