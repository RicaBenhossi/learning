import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, Car, Trip

app = FastAPI(title="Car Sharing API")

db = load_db()


def __get_car_by_id(id: int) -> list[Car]:
    return [car for car in db if car.id == id]

@app.get("/")
async def welcome(name):
    return {"message": f"Hello {name}. Welcome to the Car Sharing service!"}


@app.get("/api/cars")
async def get_cars(size: str | None = None, doors: int = None) -> list:
    result = db

    if size:
        result = list(car for car in result if car.size == size)

    if doors:
        result = list(car for car in result if car.doors >= doors)

    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int) -> dict:
    result = __get_car_by_id(id)
    if result:
        return result[0].model_dump_json()
    else:
        raise HTTPException(status_code=404, detail=f"There is no cars with id {id}.")


@app.post("/api/cars")
def add_car(car: Car) -> Car:
    new_car = Car(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=db[-1].id + 1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.delete("/api/cars/{id}", status_code=204)
def remove_car(id: int) -> None:
    matches = __get_car_by_id(id)
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id {id}.")


@app.put("/api/cars/{id}", status_code=202)
def update_car(id: int, new_car: Car) -> Car:
    matches = __get_car_by_id(id)
    if matches:
        car = matches[0]
        car.size = new_car.size
        car.fuel = new_car.fuel
        car.doors = new_car.doors
        car.transmission = new_car.transmission
        save_db(db)

        return car
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id {id}.")


@app.put("/api/cars/{id}/trips", status_code=202)
def add_trip(id: int, trip: Trip) -> Car:
    car = __get_car_by_id(id)[0]
    if car:
        trip_id = 1
        if car.trips:
            trip_id = car.trips[-1].id + 1

        new_trip = Trip(id=trip_id, start=trip.start, end=trip.end, description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id {id}.")


@app.delete("/api/cars/{id}/trips/{trip_id}", status_code=204)
def remove_trip(id: int, trip_id: int) -> None:
    car = __get_car_by_id(id)[0]
    if car:
        trip = list(trip for trip in car.trips if trip.id == trip_id)[0]
        if trip:
            car.trips.remove(trip)
            save_db(db)
        else:
            raise HTTPException(status_code=404, detail=f"There is no trip with id {id} in car {car.id}.")
    else:
        raise HTTPException(status_code=404, detail=f"There is no car with id {id}.")


@app.put("/api/cars/{id}/trips/{trip_id}", status_code=202)
def update_trip(id: int, trip_id: int, trip: Trip) -> Car:
    car = __get_car_by_id(id)[0]
    if car:
        trip_bd = list(trip for trip in car.trips if trip.id == trip_id)[0]
        if trip_bd:
            trip_bd.start = trip.start
            trip_bd.end = trip.end
            trip_bd.description = trip.description
            save_db(db)
            return car
        else:
            raise HTTPException(status_code=404, detail=f"There is no trip with id {id} in car {car.id}.")


if __name__ == "__main__":
    uvicorn.run(app="car_sharing:app", reload=True)
