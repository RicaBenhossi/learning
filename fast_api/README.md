#FAST API LEARNING

Course: Fast API Foundations by Reindert-Jan Ekker on Pluralsight

## Instalation

- pip
  - Run in ternimal: `python -m pip install "fastapi[all]`
- uv
  - Run in terminal: `uv tool install "fastapi[all]"`
- pyproject
  - Add a pyproject file to your project with "fastapi[all]" to the dependencies section
  ```python
    [project]
    name = "fast-api"
    version = "0.1.0"
    description = "Add your description here"
    readme = "README.md"
    requires-python = ">=3.13"
    dependencies = [
        "fastapi[all]",
    ]
    ```
  - Run in ternimal: `uv sync`

## Base Structure

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello world!"}

```

## Running FastAPI

- Run in terminal: 'fastapi dev <file_name>.py'
  - Running with **dev** flag make it auto-reload when change something.
- Run in pycharm: 
  ![img.png](img.png)

## Documentation (auto-generated)

### Swagger

Access [127.0.0.1:8000/docs](127.0.0.1:8000/docs) to access your API Swagger style documentation.

### Redocly

Access [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) to access your API Redocly style documentation.

**OBS**: both documentation allows you to see an openapi.json specification.
