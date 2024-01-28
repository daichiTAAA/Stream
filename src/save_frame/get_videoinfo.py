from googleapiclient.discovery import build
from pydantic.dataclasses import dataclass
from settings import get_env, get_config


@dataclass
class EnvInfo:
    YOUTUBE_API_KEY: str
    CONFIG_PATH: str
    CONFIG_SECTION: str


@dataclass
class ConfigInfo:
    VIDEO_ID: str


def get_videoinfo():
    env = get_env(EnvInfo, dotenv_path="./.env")
    config = get_config(
        ConfigInfo, config_path=env.CONFIG_PATH, config_section=env.CONFIG_SECTION
    )

    # YouTubeのビルドオブジェクトを作成
    youtube = build("youtube", "v3", developerKey=env.YOUTUBE_API_KEY)

    # 動画IDを指定
    video_id = config.VIDEO_ID

    # YouTube APIを呼び出して動画情報を取得
    request = youtube.videos().list(
        part="snippet,contentDetails,statistics", id=video_id
    )
    response = request.execute()

    # 動画情報を表示
    print(response)


if __name__ == "__main__":
    get_videoinfo()
