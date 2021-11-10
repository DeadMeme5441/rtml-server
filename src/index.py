import os
import json
from bson import json_util
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from rtml_core import Document
from pymongo import MongoClient

app = FastAPI()

origins = ["*"]

path = os.system("pwd")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(
    "mongodb+srv://deadmeme:Reeve123@cluster0.mr6hw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)

main_db = client["rtml_db"]


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}


@app.post("/file/upload")
async def upload_file(file: UploadFile = File(...)):

    contents = await file.read()
    with open(f"./files/{file.filename}", "wb") as out_file:
        out_file.write(contents)  # type: ignore

    os.system("pwd")
    print(file.filename)

    document_obj = Document.document(f"./files/{file.filename}")

    print(document_obj.asdict)

    if main_db["files"].find_one({"file_name": file.filename}) is None:
        main_db["files"].insert_one(document_obj.asdict)

    else:
        main_db["files"].delete_one({"file_name": file.filename})
        main_db["files"].insert_one(document_obj.asdict)

    return {"Result": "File Uploaded"}


@app.get("/files")
async def retrieve_files():

    files = []
    for file_obj in main_db["files"].find():
        files.append(json.loads(json_util.dumps(file_obj["file_name"])))

    return {"files": files}


@app.get("/api/{file_name}")
def get_document_object(file_name):

    result = main_db["files"].find_one({"file_name": file_name})
    return json.loads(json_util.dumps(result))  # type: ignore


@app.get("/api/search/{file_name}/{search_term}")
def get_search_results(file_name, search_term):

    mypath = "./files/" + file_name + ".txt"
    document_obj = Document.document(mypath)

    search_results = document_obj.search_document(
        search_type=["text", "tag", "subtag"], search_term=search_term
    )

    return search_results  # type: ignore
