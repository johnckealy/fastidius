from .base import SettingsBase


class SettingsProd(SettingsBase):
    DATABASE_URL: str = "mongodb://${app_name}-db:27018"
