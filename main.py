from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from databases import Database

app = FastAPI()

# DB接続設定（SQLite使用）
DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = MetaData()

# usersテーブル定義（SQLAlchemy）
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

# DBエンジン（テーブル作成用）
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

# Pydanticモデル（入力と出力）
class UserIn(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str

# 接続処理
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# GET: ユーザー一覧取得
@app.get("/users", response_model=list[UserOut])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)

# POST: ユーザー登録
@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name)
    user_id = await database.execute(query)
    return {**user.dict(), "id": user_id}