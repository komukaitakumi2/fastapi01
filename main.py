from fastapi import FastAPI ##FastAPIの本体をインポート


app = FastAPI()##アプリケーションを作成

@app.get("/")##/にアクセスした時の処理(GETリクエスト)を定義

def read_root():##エンドポイントに対応する関数(処理の中身)
    return {"message": "Hello, FastAPI!"}##クライアントに返すJSONレスポンス
