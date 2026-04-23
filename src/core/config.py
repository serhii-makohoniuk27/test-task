from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	app_name: str = "Menu PDF Extractor API"
	app_version: str = "0.1.0"
	debug: bool = False
	api_prefix: str = "/api/v1"
	max_upload_size_bytes: int = 10 * 1024 * 1024

	model_config = SettingsConfigDict(
		env_prefix="MENU_",
		env_file=".env",
		extra="ignore",
	)


settings = Settings()
