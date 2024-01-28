import configparser
import os
from typing import Type, TypeVar

from dotenv import load_dotenv
from pydantic.dataclasses import dataclass

# 新しい型変数を定義
T = TypeVar("T", bound=dataclass)


def get_env(EnvInfo: Type[T], dotenv_path: str) -> T:
    try:
        # .envファイルを読み込む
        load_dotenv(dotenv_path=dotenv_path, verbose=True)
    except FileNotFoundError:
        print(f"{dotenv_path} is not found")

    # 環境変数の値を取得し、EnvInfoのインスタンスを生成する
    env_vars = {}
    for field in EnvInfo.__annotations__.keys():
        value = os.getenv(field)
        if value is None:
            raise ValueError(
                f"{field} is not defined in .env or as an environment variable"
            )
        env_vars[field] = value

    env = EnvInfo(**env_vars)
    return env


def get_config(ConfigInfo: Type[T], config_path: str, config_section: str) -> T:
    # configparserを使ってINIファイルから設定を読み込む
    config = configparser.ConfigParser()
    config.read(config_path)

    # コンフィグファイルの値を取得し、ConfigInfoのインスタンスを生成する
    config_vars = {}
    if config_section not in config:
        raise ValueError(f"Section '{config_section}' not found in the config file")

    for field in ConfigInfo.__annotations__.keys():
        if field not in config[config_section]:
            raise ValueError(
                f"{field} is not defined in the config file under section '{config_section}'"
            )
        config_vars[field] = config[config_section][field]

    return ConfigInfo(**config_vars)
