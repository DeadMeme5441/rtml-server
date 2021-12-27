import os
import json
from os import listdir
from os.path import isfile, join
from bson import json_util
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from rtml_core import Document

app = FastAPI(debug=True)

current_obj = {}


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/file/upload")
async def upload_file(file: UploadFile = File(...)):

    global current_obj

    contents = await file.read()
    with open(f"./files/{file.filename}", "wb") as out_file:
        out_file.write(contents)  # type: ignore

    current_obj = Document.document(f"./files/{file.filename}")

    return {"Result": "File Uploaded"}


@app.post("/setfile/{file_name}")
def set_current_file(file_name):

    mypath = "./files/" + file_name + ".txt"
    global current_obj
    current_obj = Document.document(mypath)

    return {"Current File": f"{file_name}"}


@app.get("/files")
async def retrieve_files():

    mypath = "./files/"
    files = []
    for file_obj in [f for f in listdir(mypath) if isfile(join(mypath, f))]:
        files.append(json.loads(json_util.dumps(file_obj.split(".")[0])))

    return {"files": files}


@app.get("/api/{file_name}")
def get_document_object():

    global current_obj

    if current_obj != {}:
        result = current_obj.asdict  # type: ignore
        return json.loads(json_util.dumps(result))  # type: ignore

    else:
        return {"Result": "No File Loaded"}


@app.get("/api/search/{search_term}")
def get_search_results(search_term):

    search_results = current_obj.search_document(  # type: ignore
        search_type=["text", "tag", "subtag"], search_term=search_term
    )

    return search_results  # type: ignore


@app.get("/api/delete/{file_name}")
def delete_file(file_name):

    mypath = "./files/" + file_name + ".txt"

    if os.path.exists(mypath):
        os.remove(mypath)

    else:
        print(f"{file_name} does not exist.")

    return file_name


app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
