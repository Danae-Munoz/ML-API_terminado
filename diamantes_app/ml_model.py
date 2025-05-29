import requests

# Ruta local de la API Flask
API_URL = 'http://localhost:5000/predecir'  # Cambia el puerto si usas otro

# Función que envía JSON a la API Flask y devuelve el precio estimado
def predecir_precio_desde_json(json_data):
    try:
        response = requests.post(API_URL, json=json_data)
        if response.status_code == 200:
            resultado = response.json()
            return resultado['precio_estimado']
        else:
            raise ValueError(f"Error en API: {response.status_code} - {response.text}")
    except Exception as e:
        raise RuntimeError(f"Error al contactar la API Flask: {e}")
