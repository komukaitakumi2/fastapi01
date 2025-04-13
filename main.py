from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from databases import Database
from fastapi import HTTPException
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
@app.get("/users", response_model=list[UserOut])#(ユーザ全員の情報)
async def get_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=UserOut)#(ユーザ個別情報)
async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/")
def root():
    return {"message": "Welcome to HOLLA backend!"}


# POST: ユーザー登録
@app.post("/users", response_model=UserOut)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name)
    user_id = await database.execute(query)
    return {**user.dict(), "id": user_id}


@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserIn):
    # 対象のユーザーが存在するか確認
    query = users.select().where(users.c.id == user_id)
    existing_user = await database.fetch_one(query)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 更新クエリを発行
    update_query = users.update().where(users.c.id == user_id).values(name=user.name)
    await database.execute(update_query)

    # 更新後の情報を取得して返す
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}", response_model=UserOut)
async def delete_user(user_id: int):
    # 対象のユーザーが存在するか確認
    query = users.select().where(users.c.id == user_id)
    existing_user = await database.fetch_one(query)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 削除クエリを実行
    delete_query = users.delete().where(users.c.id == user_id)
    await database.execute(delete_query)

    # 削除前のデータを返す（確認用）
    return existing_user
