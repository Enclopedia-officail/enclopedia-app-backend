## 環境構築手順
開発は基本的なgit flowに沿ってdevelopからfeature/〇〇ブランチを切って作業します。  
また、基本的にはテスト駆動開発で進めています。

### 1. Projectディレクトリ配下にclone
    $ git clone enclopedia-app-frontend
    $ git clone enclopedia-app-backend
    $ git clone enclopedia-app-infra
    
### 2. 環境変数、docker-compose.ymlの準備
他メンバーから `.env` に記載する内容を共有してもらい、各プロジェクトのルートディレクトリにファイルを作成する。  
enclopedia-app-infraディレクトリからdocker-compose.ymlをプロジェクトトップに移動する。

### 3. コマンドの実行
    $ docker compose build --no-cache
    $ docker compose up -d
localhost:3000で動作確認。
