# 詳細設計書 - 保存したフレーム情報を Kafka に Publish する

### Kafka にパブリッシュする

- frames フォルダ内の画像ファイルの変更を監視し、新しい画像が追加されるたびに Kafka にパブリッシュする。
- Python の watchdog ライブラリを使用してフォルダを監視し、kafka-python ライブラリを使用して Kafka にメッセージをパブリッシュする。
