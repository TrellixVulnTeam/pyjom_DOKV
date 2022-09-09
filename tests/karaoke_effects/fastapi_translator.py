from typing import Union

from fastapi import FastAPI

app = FastAPI()

import paddlehub as hub
language_translation_model = hub.Module(name='baidu_translate')
language_recognition_model = hub.Module(name='baidu_language_recognition')

@app.get("/")
def read_root():
    return {"message": "unified translator hooked on some clash server"}

@app.get("/items/{item_id}")
def read_item(item_id: int, backend: str, text: str):
    code = 200
    if not backend in ['deepl','baidu']:
        code = 400
        result = 'INVALID BACKEND'
    return {"item_id": item_id, "q": q}