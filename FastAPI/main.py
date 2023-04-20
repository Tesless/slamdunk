from fastapi import FastAPI
from pymongo import MongoClient
from bson.json_util import dumps

app = FastAPI()

# MongoDB에 접속
client = MongoClient("mongodb+srv://tesless:123@cluster0.xyeyaz7.mongodb.net/test")

# 데이터베이스 선택
db = client["test"]

# 컬렉션 선택
collection = db["customers"]

@app.get("/")
async def get_collection_data():
    # MongoDB 컬렉션에서 데이터 조회
    data = list(collection.find().limit(1).sort("_id", -1))  # 컬렉션의 모든 데이터를 리스트로 조회

    # 데이터가 없는 경우
    if not data:
        return {"message": "데이터가 없습니다."}

    # 데이터를 JSON 형태로 변환하여 반환
    return dumps(data)

# FastAPI 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

