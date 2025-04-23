import requests
import csv
import datetime
from pathlib import Path
import os

# Configuración
CSV_FILE = "data/precios_verduras.csv"

# Asegurar que el directorio exista
Path("data").mkdir(exist_ok=True)

def obtener_precios():
    """Obtiene los precios de todas las verduras desde la API"""
    # URL de tu API (ajusta según sea necesario)
    url = "https://sfl.world/api/v1/prices"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extraer los precios y el timestamp
        precios_verduras = data["data"]["p2p"]
        timestamp = data["updatedAt"]
        
        return timestamp, precios_verduras
    except Exception as e:
        print(f"Error al obtener precios: {e}")
        return None, {}

def registrar_precios():
    """Obtiene y registra los precios de todas las verduras"""
    timestamp, precios_verduras = obtener_precios()
    
    if not precios_verduras:
        print("No se pudieron obtener precios. Verifique la conexión o la API.")
        return
    
    # Convertir timestamp a formato legible
    fecha_hora = datetime.datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    
    # Crear o actualizar el archivo CSV
    file_exists = os.path.isfile(CSV_FILE)
    
    # Determinar encabezados (timestamp + todas las verduras)
    headers = ["Timestamp"] + list(precios_verduras.keys())
    
    # Preparar la nueva fila con el timestamp formateado y todos los precios
    nueva_fila = [fecha_hora]
    for verdura in headers[1:]:  # Todas las verduras excepto "Timestamp"
        nueva_fila.append(precios_verduras.get(verdura, ""))
    
    # Escribir al CSV
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Si el archivo no existe, escribir los encabezados primero
        if not file_exists:
            writer.writerow(headers)
        
        # Escribir la nueva fila con todos los precios
        writer.writerow(nueva_fila)
    
    print(f"Registrado nuevo conjunto de precios en {fecha_hora}")

if __name__ == "__main__":
    print("Ejecutando registro de precios de verduras...")
    registrar_precios()
    print("Registro completado")
