# python start.py

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from pymongo import MongoClient
import asyncio
import json
from datetime import datetime

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["riego_db"]
coleccion = db["lecturas"]

templates = Jinja2Templates(directory="templates")

class Datos(BaseModel):
    soil: int | None = None
    dist_cm: int | None = None
    riego: int | None = None
    llenado: int | None = None
    temp: float | None = None
    humedad: float | None = None
    pir: int | None = None
    mq2: int | None = None
    vent: int | None = None

@app.get("/", response_class=HTMLResponse)
def elegir_vista(request: Request):
    return templates.TemplateResponse("vistas.html", {"request": request})

@app.post("/datos")
async def recibir_datos(datos: Datos):
    registro = datos.dict()
    registro["timestamp"] = datetime.now()
    resultado = coleccion.insert_one(registro)
    registro["_id"] = str(resultado.inserted_id)
    # Enviar los datos del sensor
    asyncio.create_task(enviar_datos(registro))
    # Enviar alertas si es necesario
    if registro.get("pir") == 1:  # Ejemplo: Si PIR es 1, enviar alerta
        asyncio.create_task(enviar_alerta({"alerta": "Movimiento detectado por PIR"}))
    if registro.get("mq2", 0) > 100: # Ejemplo: Si MQ2 supera un umbral, enviar alerta
        asyncio.create_task(enviar_alerta({"alerta": "Gas detectado por MQ2"}))
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
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        if websocket in clientes_ws:
            clientes_ws.remove(websocket)
            print("WebSocket desconectado")

async def enviar_alerta(alerta: dict):
    vivos = []
    for ws in clientes_ws:
        try:
            await ws.send_json({"type": "alerta", "message": alerta.get("alerta", "Alerta Desconocida")}) # Enviar la alerta con el tipo
            vivos.append(ws)
        except Exception as e:
            print(f"Error enviando alerta: {e}")
    clientes_ws[:] = vivos

# Ejemplo de como enviar un mensaje de data
async def enviar_datos(data: dict):
    vivos = []
    # Convert datetime object to string before sending
    data_copy = data.copy()  # Create a copy to avoid modifying the original
    if "timestamp" in data_copy:
        data_copy["timestamp"] = data_copy["timestamp"].isoformat()
    for ws in clientes_ws:
        try:
            await ws.send_json({"type": "data", **data_copy}) # Enviar los datos con el tipo
            vivos.append(ws)
        except Exception as e:
            print(f"Error enviando datos: {e}")
    clientes_ws[:] = vivos



