import json

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

db = [
    {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "auto"},
    {"id": 2, "size": "s", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 3, "size": "s", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 4, "size": "m", "fuel": "electric", "doors": 3, "transmission": "auto"},
    {"id": 5, "size": "m", "fuel": "hybrid", "doors": 5, "transmission": "auto"},
    {"id": 6, "size": "m", "fuel": "gasoline", "doors": 5, "transmission": "manual"},
    {"id": 7, "size": "l", "fuel": "diesel", "doors": 5, "transmission": "manual"},
    {"id": 8, "size": "l", "fuel": "electric", "doors": 5, "transmission": "auto"},
    {"id": 9, "size": "l", "fuel": "hybrid", "doors": 5, "transmission": "auto"}
]


# URL Parameter "name"
# http request: GET http://localhost:8000/?name=test
@app.get("/")
async def welcome(name):
    return {"message": f"Welcome, {name} to the Car Sharing service!"}


# requests
#   GET http://localhost:8000/api/cars?size=m&doors=3
#   GET http://localhost:8000/api/cars?size=m
#   GET http://localhost:8000/api/cars

@app.get("/api/cars")
async def get_cars(size: str | None = None, doors: int = None) -> list:
    result = db

    if size:
        result = list(car for car in result if car['size'] == size)

    if doors:
        result = list(car for car in result if car['doors'] >= doors)

    return json.loads(json.dumps(result))


# Requests
#   Success     -> GET http://localhost:8000/api/cars/2
#   Not Found   -> GET http://localhost:8000/api/cars/100
@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    result = [car for car in db if car['id'] == id]
    if result:
        return json.loads(json.dumps(result[0]))
    else:
        raise HTTPException(status_code=404, detail=f"There is no cars with id {id}.")


if __name__ == "__main__":
    uvicorn.run(app="car_sharing:app", reload=True)
