import requests
import csv
import datetime
from pathlib import Path

# Configuración
CSV_FILE = "data/precios_verduras.csv"

# Asegurar que el directorio exista
Path("data").mkdir(exist_ok=True)

# Crear el archivo CSV si no existe
if not Path(CSV_FILE).exists():
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Hora", "Verdura", "Precio"])

def obtener_precios():
    """Obtiene los precios de todas las verduras desde la API"""
    # URL de tu API (ajusta según sea necesario)
    url = "https://sfl.world/api/v1/prices"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extraer los precios de la sección p2p
        precios_verduras = data["data"]["p2p"]
        return precios_verduras
    except Exception as e:
        print(f"Error al obtener precios: {e}")
        return {}

def registrar_precios():
    """Obtiene y registra los precios de todas las verduras"""
    now = datetime.datetime.now()
    fecha = now.strftime("%Y-%m-%d")
    hora = now.strftime("%H:%M:%S")
    
    precios_verduras = obtener_precios()
    
    if not precios_verduras:
        print("No se pudieron obtener precios. Verifique la conexión o la API.")
        return
    
    nuevos_registros = []
    
    for verdura, precio in precios_verduras.items():
        nuevos_registros.append([fecha, hora, verdura, precio])
        print(f"Registrado: {verdura} a {precio} - {fecha} {hora}")
    
    # Guardar todos los registros al archivo CSV
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(nuevos_registros)

if __name__ == "__main__":
    print("Ejecutando registro de precios de verduras...")
    registrar_precios()
    print("Registro completado")
