import os

import ffmpeg
from pydantic.dataclasses import dataclass
from pytube import YouTube

from settings import get_env, get_config


@dataclass
class EnvInfo:
    YOUTUBE_API_KEY: str
    CONFIG_PATH: str
    CONFIG_SECTION: str


@dataclass
class ConfigInfo:
    VIDEO_ID: str
    FRAMES_DIR: str


def main():
    env = get_env(EnvInfo, dotenv_path="./.env")
    config = get_config(
        ConfigInfo, config_path=env.CONFIG_PATH, config_section=env.CONFIG_SECTION
    )

    # 動画のURLを指定
    video_url = f"https://www.youtube.com/watch?v={config.VIDEO_ID}"

    # pytubeを使用して動画をダウンロード
    yt = YouTube(video_url)
    stream = (
        yt.streams.filter(file_extension="mp4").order_by("resolution").desc().first()
    )
    if not stream:
        raise Exception("No suitable stream found")

    # ダウンロード先のパスを指定
    download_path = stream.download()

    # 画像を保存するディレクトリを作成
    frames_dir = config.FRAMES_DIR
    os.makedirs(frames_dir, exist_ok=True)

    # FFmpegを使用して動画を1fpsで画像フレームに変換し、保存
    (
        ffmpeg.input(download_path)
        .output(os.path.join(frames_dir, "frame_%04d.jpg"), vf="fps=1")
        .run()
    )


if __name__ == "__main__":
    main()
