import tomllib
from dataclasses import dataclass

@dataclass(frozen=True, unsafe_hash=True)
class Config:
    client_secret: str
    api_key: str
    # TODO: Maybe this variable should be extracted into another dataclass?
    # (it's not great that Kadinsky class has access to this thing)
    telegram_api_key: str

def load() -> Config:
    with open("config.toml", "rb") as fp:
        # TODO: Extract all of the repeating if statements into a function somehow
        raw_config = {k.casefold(): v for k, v in tomllib.load(fp).items()}
        if (api_key := raw_config.get("api_key")) is None:
            print("ERROR: No API key was provided!")
            exit(1)
        if (client_secret := raw_config.get("client_secret")) is None:
            print("ERROR: No client secret was provided!")
            exit(1)
        if (telegram_api_key := raw_config.get("telegram_api_key")) is None:
            print("ERROR: No API key for Telegram was provided!")
            exit(1)

        return Config(api_key=api_key, client_secret=client_secret,
                      telegram_api_key=telegram_api_key)

            

