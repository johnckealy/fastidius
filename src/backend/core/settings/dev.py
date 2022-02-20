from .base import SettingsBase


class SettingsDev(SettingsBase):
    DATABASE_URL: str = "postgresql+asyncpg://jokea:secrets@localhost:5432/fastidius_mould"
