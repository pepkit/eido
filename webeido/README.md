# webeido

This is a web interface to eido built using FastAPI

Run with:

```

uvicorn main:app --reload
```

Then, drop all files belonging to a PEP (yaml + csvs) and upload them. webeido will validate against a list of schemas and show you what tools your PEP will work on.





You can install, but it's just so much nicer to run it with `uvicorn --reload` because then changes render in real time.


```
docker build --no-cache -t webeido .
```



To run in a container:

```
docker run --rm -p 8000:80 --name webeido \
  --volume upload:/upload \
  webeido uvicorn main:app --reload
```
```
docker run --rm -p 8000:80 --name webeido webeido
```
