import time

from pydantic.dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaProducer

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
    KAFKA_TOPIC: str
    KAFKA_SERVER: str
    LOCAL_KAFKA_SERVER: str


class ImageFileHandler(FileSystemEventHandler):
    def __init__(self, producer, topic):
        self.producer = producer
        self.topic = topic

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".jpg"):
            print(f"New image file detected: {event.src_path}")
            self.producer.send(self.topic, event.src_path.encode("utf-8"))


def main():
    env = get_env(EnvInfo, dotenv_path="./.env")
    config = get_config(
        ConfigInfo, config_path=env.CONFIG_PATH, config_section=env.CONFIG_SECTION
    )
    # Kafka設定
    kafka_topic = config.KAFKA_TOPIC  # Kafkaトピック名を指定
    kafka_server = config.KAFKA_SERVER  # Kafkaサーバーのアドレスを指定

    # Kafkaプロデューサーの初期化
    try:
        producer = KafkaProducer(bootstrap_servers=kafka_server)
    except Exception as e:
        print(f"Failed to initialize Kafka producer: {e}")
        print("Trying to connect to the local Kafka server instead...")
        producer = KafkaProducer(bootstrap_servers=config.LOCAL_KAFKA_SERVER)

    # 監視するディレクトリ
    watch_directory = config.FRAMES_DIR

    # イベントハンドラの設定
    event_handler = ImageFileHandler(producer, kafka_topic)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=True)

    # 監視の開始
    observer.start()
    print(f"Watching directory: {watch_directory}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
