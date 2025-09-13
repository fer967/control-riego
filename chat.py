from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from pymongo import MongoClient
import asyncio

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["riego_db"]
coleccion = db["lecturas"]

templates = Jinja2Templates(directory="templates")

class Datos(BaseModel):
    soil: int
    dist_cm: int
    riego: int
    llenado: int
    temp: float = None
    humedad: float = None
    pir: int = None
    mq2: int = None
    vent: int = None

@app.get("/", response_class=HTMLResponse)
def elegir_vista(request: Request):
    return templates.TemplateResponse("vistas.html", {"request": request})

@app.post("/datos")
async def recibir_datos(datos: Datos):
    registro = datos.dict()
    registro["timestamp"] = datetime.now()
    resultado = coleccion.insert_one(registro)
    registro["_id"] = str(resultado.inserted_id)
    asyncio.create_task(enviar_alerta(registro))
    return {"status": "ok", "recibido": registro}

@app.get("/datos/ultimos")
async def ultimos_datos(limit: int = 10):
    cursor = coleccion.find().sort("timestamp", -1).limit(limit)
    datos = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        datos.append(doc)
    return datos

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    cursor = coleccion.find().sort("timestamp", -1).limit(20)
    datos = list(cursor)
    labels = [d["timestamp"].strftime("%H:%M:%S") for d in datos][::-1]
    soil = [float(d["soil"]) for d in datos][::-1]
    dist = [float(d["dist_cm"]) for d in datos][::-1]
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "labels": labels,
        "soil": soil,
        "dist": dist
    })

clientes_ws = []

@app.websocket("/ws/alertas")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clientes_ws.append(websocket)
    try:
        while True:
            await websocket.receive_text()  
    except WebSocketDisconnect:
        if websocket in clientes_ws:
            clientes_ws.remove(websocket)
            print("WebSocket desconectado")     

async def enviar_alerta(alerta: dict):
    vivos = []
    for ws in clientes_ws:
        try:
            await ws.send_json(alerta)
            vivos.append(ws)
        except:
            pass
    clientes_ws[:] = vivos