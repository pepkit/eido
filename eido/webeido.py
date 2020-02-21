from fastapi import FastAPI
from typing import List

from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse

app = FastAPI()

import eido
from peppy import Project



@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

@app.post("/validate/")
async def validate_pep(file: UploadFile = File(...)):
	p = Project("../tests/data/peps/test_cfg.yaml")
	x = eido.validate_project(project=p, schema="http://schema.databio.org/PEP/pep.yaml")
	return {"filename": file.filename, "valid": x}



@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/validate/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)