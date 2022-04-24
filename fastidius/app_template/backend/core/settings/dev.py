from .base import SettingsBase


class SettingsDev(SettingsBase):
    DATABASE_URL: str = "mongodb://localhost:27017"
