from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from typing import List
import time
from datetime import datetime

app = FastAPI()


# Modelul pentru datele de senzor
class SensorData(BaseModel):
    timestamp: int
    sensor_type: str
    value: float


# Listă pentru stocarea datelor senzorilor
sensor_data_list = []


# Endpoint pentru primirea datelor senzorilor
@app.post("/sensor")
async def receive_sensor_data(data: SensorData):
    sensor_data_list.append(data)
    return {"status": "Data received"}


# Endpoint pentru a afișa datele într-o pagină HTML
@app.get("/", response_class=HTMLResponse)
async def display_data():
    html_content = """
     <!DOCTYPE html>
     <html lang="en">
     <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>Sensor Data</title>
     <!-- Bootstrap CSS -->
     <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
     </head>
     <body>
     <div class="container mt-5">
     <h1 class="mb-4">Sensor Data</h1>
     <button onclick="location.reload()" class="btn btn-primary mb-3">Refresh Data</button>
     <table class="table table-striped">
     <thead>
     <tr>
     <th>Timestamp</th>
     <th>Sensor Type</th>
     <th>Value</th>
     </tr>
     </thead>
     <tbody>
     """
    # Generăm toate rândurile pentru tabel
    # for data in sensor_data_list:
    # Generăm rândurile pentru ultimele 5 valori din tabel
    for data in sensor_data_list[-5:]:
        dt_object = datetime.fromtimestamp(data.timestamp)
        time_formatted = dt_object.strftime("%H:%M:%S")
        html_content += f"""
         <tr>
         <td>{time_formatted}</td>
         <td>{data.sensor_type}</td>
         <td>{data.value}</td>
         </tr>
         """
    html_content += """
     </tbody>
     </table>
     </div>
     </body>
     </html>
     """
    return HTMLResponse(content=html_content)
