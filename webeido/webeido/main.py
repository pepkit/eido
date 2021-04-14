import eido
import jinja2
import logmuse
import logging
import os
import shutil
import yaml
import uvicorn

from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from platform import python_version
from starlette.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from typing import List
from peppy import Project

from _version import __version__ as webeido_version
from __init__ import build_parser
from eido._version import __version__ as eido_version

ALL_VERSIONS = {"webeido_version": webeido_version,
    "eido_version": eido_version,
    "python_version": python_version()}

TEMPLATES_PATH = "templates"
templates = Jinja2Templates(directory=TEMPLATES_PATH)
je = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES_PATH))

_LOGGER = logging.getLogger(__name__)
_LOGGER.info("Welcome to the webeido app")
app = FastAPI()

# add static for images
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("input.html", dict({"request": request}, **ALL_VERSIONS))

@app.get("/index")
async def index(request: Request):
    """
    Returns a landing page HTML with the server resources ready do download. No inputs required.
    """
    templ_vars = {"request": request, 
                  "openapi_version": app.openapi()["openapi"]}
    _LOGGER.debug("merged vars: {}".format(dict(templ_vars, **ALL_VERSIONS)))
    return templates.TemplateResponse("index.html", dict(templ_vars, **ALL_VERSIONS))


# Removed links from template because url_for gave errors:

schemas_to_test = {
    "Generic PEP": "http://schema.databio.org/pep/2.0.0.yaml",
    "PEPPRO": "http://schema.databio.org/pipelines/ProseqPEP.yaml",
    "PEPATAC": "http://schema.databio.org/pipelines/pepatac.yaml",
    "bedmaker": "http://schema.databio.org/pipelines/bedmaker.yaml",
    "refgenie": "http://schema.databio.org/refgenie/refgenie_build.yaml",
    "bulker": "http://schema.databio.org/bulker/manifest.yaml"
}

@app.post("/upload/")
async def upload(request: Request, file: UploadFile = File(...)):
    upload_folder = "uploads"
    print(file)
    file_object = file.file
    uploaded = open(os.path.join(upload_folder, file.filename), 'wb+')
    shutil.copyfileobj(file_object, uploaded)
    uploaded.close()
    print(uploaded.name)
    f, ext = os.path.splitext(file.filename)
    print(ext)
    if ext == ".yaml" or ext == ".yml":
        pconf = uploaded.name
        print("Got yaml:", pconf)


@app.post("/validate/")
async def validate_pep(request: Request, files: List[UploadFile] = File(...)):
    ufiles = []
    upload_folder = "uploads"
    for file in files:
        print(file)
        file_object = file.file
        uploaded = open(os.path.join(upload_folder, file.filename), 'wb+')
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

    vals = {"name": pconf,
            "filenames": [file.filename for file in files],
            "request": request,
            'validations': []
            }
    for name, schema in schemas_to_test.items():
        vals['validations'].append({
            "name": name,
            "schema": schema,
            "result": vwrap(p, schema)
            })
    return HTMLResponse(je.get_template("validation_results.html").render(**vals))

def main():
    global _LOGGER
    parser = build_parser()
    parser = logmuse.add_logging_options(parser)
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        print("No subcommand given")
        sys.exit(1)

    _LOGGER = logmuse.logger_via_cli(args, make_root=True)
    _LOGGER.info("Welcome to the webeido app")
    args.port
    _LOGGER.info("Running on port {}".format(args.port))
    uvicorn.run(app, host="0.0.0.0", port=args.port)
