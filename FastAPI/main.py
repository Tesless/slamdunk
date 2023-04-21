# from fastapi import FastAPI
# from pymongo import MongoClient
# from fastapi.responses import HTMLResponse
# from bson.json_util import dumps

# app = FastAPI()

# # MongoDB에 접속
# client = MongoClient("mongodb+srv://.mongodb.net/test")

# # 데이터베이스 선택
# db = client["test"]

# # 컬렉션 선택
# collection = db["customers"]

# @app.get("/")
# async def get_collection_data():
#     # MongoDB 컬렉션에서 데이터 조회
#     data = list(collection.find().limit(1).sort("_id", -1))  # 컬렉션의 모든 데이터를 리스트로 조회

#     # 데이터가 없는 경우
#     if not data:
#         return {"message": "데이터가 없습니다."}
#      # 데이터를 JSON 형태로 변환하여 반환
#     data_json = dumps(data)

#     # 데이터를 HTML 형식에 적용하여 반환
#     html = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <style>
#             body {{
#                 background-color: black;
#                 color: white;  /* 글자색을 흰색으로 설정 */
#             }}
#         </style>
#     </head>
#     <body>
#         <h1>Hello, World!</h1>
#         <p>{data_json}</p>  <!-- 데이터를 동적으로 표시 -->
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html, media_type="text/html")
    


# # FastAPI 애플리케이션 실행
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request
from pymongo import MongoClient
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bson.json_util import dumps
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()
# MongoDB에 접속
client = MongoClient("mongodb+srv://.mongodb.net/test")

# 데이터베이스 선택
db = client["test"]

# 컬렉션 선택
collection = db["customers"]


# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

app = FastAPI()
origins = ["*"]  # 수정해야 할 가능성이 있습니다.

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 모델 정의
class CarStatus(BaseModel):
    name: str
# '/update' 엔드포인트 정의
@app.post("/update")
def update_car_status(car_status: CarStatus):
    # 처리할 로직 작성
    # ...
    #name="khj"
    name = car_status.name
    #data = list(collection.find().limit(1).sort("_id", -1))  # 컬렉션의 모든 데이터를 리스트로 조회
    #data_json = dumps(data)

    # 응답 데이터 반환
    #return car_status.dict()
    return {"name": name}

@app.get("/")
async def get_collection_data(request: Request):
    # MongoDB 컬렉션에서 데이터 조회
    data = list(collection.find().limit(1).sort("_id", -1))  # 컬렉션의 모든 데이터를 리스트로 조회

    # 데이터가 없는 경우
    if not data:
        return {"message": "데이터가 없습니다."}
     
    # 데이터를 JSON 형태로 변환하여 반환
    data_json = dumps(data)

    # Jinja2 템플릿에 데이터를 전달하여 HTML 형식으로 렌더링
    return templates.TemplateResponse("db.html", {"request": request, "data_json": data_json})

# @app.post("/update")
# async def poat_collection_data(request: Request):
#     # MongoDB 컬렉션에서 데이터 조회
#     data = list(collection.find().limit(1).sort("_id", -1))  # 컬렉션의 모든 데이터를 리스트로 조회

#     # 데이터가 없는 경우
#     if not data:
#         return {"message": "데이터가 없습니다."}
     
#     # 데이터를 JSON 형태로 변환하여 반환
#     data_json = dumps(data)

#     # Jinja2 템플릿에 데이터를 전달하여 HTML 형식으로 렌더링
#     return templates.TemplateResponse("db.html", {"request": request, "data_json": data_json})