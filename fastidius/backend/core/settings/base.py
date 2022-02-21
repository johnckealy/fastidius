from pydantic import BaseSettings


class SettingsBase(BaseSettings):
    SECRET: str = "SECRET"
 