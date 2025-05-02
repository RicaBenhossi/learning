import json

from pydantic import BaseModel


class Trip(BaseModel):
    id: int | None = None
    start: int
    end: int
    description: str


class Car(BaseModel):
    id: int | None = None
    size: str
    fuel: str | None = 'eletric'
    doors: int
    transmission: str | None = 'auto'
    trips: list[Trip] = []

    # This helps when importing an openapi.json file into postman.
    model_config = {
        "json_schema_extra": {
            "exemples": [
                {
                    "size": "m",
                    "doors": 5,
                    "transmission": "auto",
                    "fuel": "hybrid",
                }
            ]
        }
    }


def load_db() -> list[Car]:
    with open("cars.json") as f:
        return [Car.model_validate(obj) for obj in json.load(f)]


def save_db(cars: list[Car]):
    with open("cars.json", "w") as db_cars:
        json.dump([car.model_dump() for car in cars], db_cars, indent=4)
