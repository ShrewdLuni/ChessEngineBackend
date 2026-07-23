from fastapi import FastAPI
import rest
import ws

app = FastAPI()

app.include_router(rest.router)
app.include_router(ws.router)
