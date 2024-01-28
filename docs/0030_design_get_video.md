# 詳細設計書

### Youtube の動画を取得する

- 動画の取得
  - pytube で動画をダウンロードしてから ffmpeg で画像フレームに変換する。
- メタデータの取得
  - 初期設定を行う
    https://github.com/googleapis/google-api-python-client/blob/main/docs/start.md
    1. Google アカウントのサインアップをする
    2. プロジェクトを作成する
    3. ライブラリをインストールする
  - YouTube Data API v3 を有効化する
    https://qiita.com/koki_develop/items/4cd7de3898dae2c33f20
