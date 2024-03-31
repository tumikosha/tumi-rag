import dataset as dataset
import uvicorn
from fastapi import FastAPI
import requests

from app import models, db_util, util
from app.settings import Settings

settings = Settings()
print(settings)

app = FastAPI()


def check_url(url):
    try:
        requests.get(url)
        return True
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        return False


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


@app.post("/add")
async def add(query: models.PutQuery):
    print("add")
    # app.table.upsert(dict(url_uuid=url_uuid, url=query.url, article=query.article), ["url_uuid"], ensure=True)
    db_util.insert_row(app.db, query.url, query.article, table_name=settings.table_name)
    return {"status": True, "message": "Ok"}


@app.get("/search/{limit}/{text}")
async def limit(text: str, limit=10):
    res = db_util.search(app.db, text, table_name=settings.table_name, limit=limit)
    return list(res)


@app.get("/get")
async def get(url: str):
    url_uuid = str(util.string_to_uuid4(str(url)))
    res = app.table.find_one(url_uuid=url_uuid)
    for row in app.table.all():
        print(row)
    return res


# app.db = dataset.connect('sqlite:///:memory:')
app.db = dataset.connect(settings.db_uri)
db_util.make_table(app.db, table_name=settings.table_name)
# db_util.insert_row(app.db, "http://example.com", "This is example")
# print(db_util.search(app.db, "examples"))

print(f"⬤ Waiting for requests on http://{settings.addr}:{settings.port}")

if __name__ == "__main__":
    # app.main_api_route = settings.addr + ":" + str(settings.port)  # проблема порта при
    uvicorn.run("__main__:app", host=settings.addr, port=settings.port)
    # uvicorn.run("__main__:app", host=settings.addr, port=settings.port, reload=True, log_level="info")
    # port=9777 python -m gunicorn main:app --workers 10 --worker-class uvicorn.workers.Uv    # port=9876 python -m gunicorn main:app --workers 10 --worker-class uvicorn.workers.Uv# --access-logfile FILE1Help   2Save   3
