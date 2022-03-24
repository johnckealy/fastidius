from .base import SettingsBase


class SettingsProd(SettingsBase):
    DATABASE_URL: str = "postgresql+asyncpg://ubuntu:secrets@${app_name}-db:5432/${app_name}_db"
