from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CARAPI_", protected_namespaces=())

    model_path: Path = BASE_DIR / "models" / "car_price_model.pkl"
    metadata_path: Path = BASE_DIR / "models" / "model_metadata.pkl"
    static_dir: Path = BASE_DIR / "app" / "static"
    log_level: str = "INFO"


settings = Settings()
