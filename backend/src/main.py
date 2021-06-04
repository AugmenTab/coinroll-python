#! python3

# PSL Imports
from typing import Optional

# 3p Imports
from fastapi import FastAPI
import uvicorn

# Internal Imports
try:
    from database import establish_db
except:
    pass


app = FastAPI()


def add(a, b):
    return a + b


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == '__main__':
    establish_db()
    uvicorn.run(app, port=8000, host="0.0.0.0")
