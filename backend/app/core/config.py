from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(populate_by_name=True)

    appName: str = Field(default="Companion Platform API", validation_alias="APP_NAME")
    databaseUrl: str = Field(default="sqlite:///./companion.db", validation_alias="DATABASE_URL")
    kafkaBootstrapServers: str = Field(default="kafka:9092", validation_alias="KAFKA_BOOTSTRAP_SERVERS")
    enableKafka: bool = Field(default=False, validation_alias="ENABLE_KAFKA")


settings = Settings()
