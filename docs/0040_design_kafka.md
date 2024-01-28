# 詳細設計書 Kafka

### Kafka クラスターの構築

- https://docs.confluent.io/platform/current/installation/docker/image-reference.html

* Docker Compose を使用して Kafka クラスターを構築する。
* コンテナの立ち上げ前に下記のコマンドを実行する。
  ```bash
  docker network create kafka_network
  docker volume create frame_volume
  ```
