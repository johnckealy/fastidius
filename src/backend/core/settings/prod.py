from .base import SettingsBase


class SettingsProd(SettingsBase):
    DATABASE_URL: str = "postgresql+asyncpg://ubuntu:secrets@db:5432/fasty_test"
