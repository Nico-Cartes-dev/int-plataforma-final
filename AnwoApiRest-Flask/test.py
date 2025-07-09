import requests
import os

os.system('cls')

def execute_http_method(method, url, data):
    try:
        response = requests.request(method, url, json=data)
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {'error': 'Error de conexión'}

url = "http://127.0.0.1:5000/reservar_equipo_anwo"

print(f'Realizar un reserva:')

status_code, response_json = execute_http_method('POST', url, {'nroserieanwo': 'A1', 'reservado': 'S'})

print(f'    Status code: {status_code}')
print(f'    Respuesta  : {response_json}')
print()

print(f'Realizar una anulación de reserva:')

status_code, response_json = execute_http_method('POST', url, {'nroserieanwo': 'A1', 'reservado': 'N'})

print(f'    Status code: {status_code}')
print(f'    Respuesta  : {response_json}')