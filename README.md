# HOLLA FastAPI Backend

このリポジトリは、FastAPI によって構築された HOLLA アプリケーションのバックエンドです。  
JWT認証、SQLiteによるユーザー管理、Dockerによる環境構築などをサポートしています。

---

## ✅ 機能一覧

- ユーザー登録（パスワードはハッシュ化）
- JWTによるログイン認証
- 認証付きエンドポイント（ユーザー自身の取得）
- ユーザーのCRUD（作成・取得・更新・削除）
- Swagger UIでAPIの操作が可能
- `.env` によるシークレット管理
- Docker / Docker Compose 対応

---

## 🏗️ 環境構築手順

### ① Poetry のインストール

```bash
pip install poetry

### ２ pythonのバージョン切り替え
pyenv install 3.12.7
pyenv local 3.12.7

### 3 仮想環境の作成と依存関係のインストール
poetry install

### 4 Gitにあげるな！！秘密鍵のファイルを生成。.gitignoreに.envを追加
SECRET_KEY=your_super_secret_key_here

### 5 サーバーの起動
poetry run uvicorn main:app --reload

