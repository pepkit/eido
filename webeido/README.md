# webeido

This is a web interface to eido built using FastAPI

Run with:

```
uvicorn webeido:app --reload
```

Then, drop all files belonging to a PEP (yaml + csvs) and upload them. webeido will validate against a list of schemas and show you what tools your PEP will work on.
