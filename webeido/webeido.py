import eido
import jinja2
import os
import shutil
import yaml

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from peppy import Project
from peppy import __version__ as peppy_version
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import List
from yacman import load_yaml

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMPLATES_PATH = "templates"
templates = Jinja2Templates(directory=TEMPLATES_PATH)
je = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH))

# add static for images
app.mount("/" + "static", StaticFiles(directory="static"), name="static")

print("Schemas list")
print(load_yaml("schemas.yaml"))

schemas_to_test = load_yaml("schemas.yaml")


@app.get("/status")
async def status(request: Request):
    return JSONResponse({"status": "OK"})


@app.get("/schemas")
async def status(request: Request):
    return JSONResponse(schemas_to_test)


# This endpoint validates for one specific schema
# when the schema is known to the server by registry path
@app.post("/validate/{namespace}/{schemaid}")
async def validate_specific_schema(
    namespace, schemaid, request: Request, files: List[UploadFile] = File(...)
):
    # print(schemas_to_test)
    registry_path = "/".join([namespace, schemaid])
    print(schemas_to_test[registry_path])
    return await validate_pep(
        request, files, {registry_path: schemas_to_test[registry_path]}
    )
    # return validate_pep(request, files, schemas_to_test[schemaid])


# Provide an external schema
@app.post("/validate_one")
async def validate_one(
    request: Request,
    files: List[UploadFile] = File(...),
    schemas_to_test=schemas_to_test,
):
    # TODO implement this
    return False


def vwrap(p, schema):
    x = None
    try:
        eido.validate_project(project=p, schema=schema, exclude_case=True)
    except Exception as e:
        x = str(e)
        print(x)
    return x


# Provide a registry path
@app.get("/validate_fromhub/{namespace}/{project}")
async def validate_fromhub(namespace: str, pep_id: str):
    proj = peppy.Project(PEP_STORES[namespace][pep_id])
    vals = {}
    for schema_id, schema_data in schemas_to_test.items():
        vals["validations"].append(
            {
                "id": schema_id,
                "name": schema_data["name"],
                "docs": schema_data["docs"],
                "schema": schema_data["schema"],
                "result": vwrap(p, schema_data["schema"]),
            }
        )
    return JSONResponse(content=vals)


@app.post("/validate")
async def validate_pep(
    request: Request,
    files: List[UploadFile] = File(...),
    schemas_to_test=schemas_to_test,
):
    ufiles = []
    upload_folder = "uploads"
    for file in files:
        print(f"File: '{file}'")
        file_object = file.file
        full_path = os.path.join(upload_folder, file.filename)
        # if not os.path.isfile(full_path):
        #     print(f"failed isfile test: {full_path}")
        #     return JSONResponse(content={ "error": "No files provided."})
        uploaded = open(full_path, "wb+")
        shutil.copyfileobj(file_object, uploaded)
        uploaded.close()
        print(uploaded.name)
        f, ext = os.path.splitext(file.filename)
        print(ext)
        if ext == ".yaml" or ext == ".yml":
            pconf = uploaded.name
            print("Got yaml:", pconf)
    print(pconf)
    p = Project(pconf)
    print(p)

    vals = {
        "name": pconf,
        "filenames": [file.filename for file in files],
        "peppy_version": peppy_version,
        "validations": [],
    }
    for schema_id, schema_data in schemas_to_test.items():
        vals["validations"].append(
            {
                "id": schema_id,
                "name": schema_data["name"],
                "docs": schema_data["docs"],
                "schema": schema_data["schema"],
                "result": vwrap(p, schema_data["schema"]),
            }
        )
    return JSONResponse(content=vals)
    # return HTMLResponse(je.get_template("validation_results.html").render(**vals))


@app.get("/")
async def main():
    return HTMLResponse(je.get_template("index.html").render())
