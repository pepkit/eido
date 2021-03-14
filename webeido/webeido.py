from typing import List

from fastapi import FastAPI, File, UploadFile
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

import os
import shutil

import jinja2
import yaml
from peppy import Project

import eido

TEMPLATES_PATH = "templates"
templates = Jinja2Templates(directory=TEMPLATES_PATH)
je = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH))


# add static for images
app.mount("/" + "static", StaticFiles(directory="static"), name="static")


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


# Removed links from template because url_for gave errors:


schemas_to_test = {
    "Generic PEP": "http://schema.databio.org/pep/2.0.0.yaml",
    "PEPPRO": "http://schema.databio.org/pipelines/ProseqPEP.yaml",
    "PEPATAC": "http://schema.databio.org/pipelines/pepatac.yaml",
    "bedmaker": "http://schema.databio.org/pipelines/bedmaker.yaml",
    "refgenie": "http://schema.databio.org/refgenie/refgenie_build.yaml",
    "bulker": "http://schema.databio.org/bulker/manifest.yaml",
}


@app.post("/validate/")
async def validate_pep(request: Request, files: List[UploadFile] = File(...)):
    ufiles = []
    upload_folder = "uploads"
    for file in files:
        print(file)
        file_object = file.file
        uploaded = open(os.path.join(upload_folder, file.filename), "wb+")
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

    def vwrap(p, schema):
        x = None
        try:
            eido.validate_project(project=p, schema=schema, exclude_case=True)
        except Exception as e:
            x = e
            print(x)
        return str(x)

    vals = {
        "name": pconf,
        "filenames": [file.filename for file in files],
        "request": request,
        "validations": [],
    }
    for name, schema in schemas_to_test.items():
        vals["validations"].append(
            {"name": name, "schema": schema, "result": vwrap(p, schema)}
        )
    return HTMLResponse(je.get_template("validation_results.html").render(**vals))


@app.get("/")
async def main():
    content = """
<body>
<form action="/validate/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
