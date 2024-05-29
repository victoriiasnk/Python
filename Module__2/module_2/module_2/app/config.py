from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

API_PREFIX = "/api"
SECRET_KEY = config("SECRET_KEY", cast=str, default="VERY_HARD_TO_GUESS")
POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str)
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)
DATABASE_URL = config(
  "DATABASE_URL",
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)
ALGORITHM = config("ALGORITHM", cast=str)
JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=str)
JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", cast=str)
