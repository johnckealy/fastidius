from .base import SettingsBase


class SettingsDev(SettingsBase):
    DATABASE_URL: str = "postgresql+asyncpg://ubuntu:secrets@${app_name}-test-db:5432/${app_name}_test_db"
