# A continuación se definen las rutas de la API REST. Los números de mensajes
#
# Los códigos de estado HTTP se clasifican en cinco categorías:
#
#     1xx (Respuesta Informativa): Indica que la solicitud fue recibida y el proceso continúa.
#     2xx (Éxito): La solicitud fue recibida, entendida y aceptada con éxito.
#     3xx (Redirección): Se requieren más acciones para completar la solicitud.
#     4xx (Error del Cliente): La solicitud contiene una sintaxis incorrecta o no puede ser procesada.
#     5xx (Error del Servidor): El servidor falló al intentar procesar una solicitud válida.
#
# En los métodos que siguen se usarán los siguientes valores:
#
#     200: OK (correcto)
#     201: Created (creado)
#     400: Bad Request (error del cliente)
#     500: Internal Server Error (error del servidor)
#

from flask import Flask, jsonify, request
import pyodbc
import os

pc="NICO"
conn_str = conn_str = f'DRIVER=ODBC Driver 17 for SQL Server; SERVER={pc}\\SQLEXPRESS; DATABASE=base_datos; UID=sa; PWD=123;'

app = Flask(__name__)

def EJECUTAR_SP_RESERVAR_EQUIPO_ANWO(nroserieanwo, reservar_si_o_no):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('EXEC dbo.SP_RESERVAR_EQUIPO_ANWO ?, ?', (nroserieanwo, reservar_si_o_no))
        conn.commit()
        conn.close()
        return True, ''
    except Exception as e:
        return False, str(e)

# Reservar o anular la reserva de un equipo ANWO
@app.route('/reservar_equipo_anwo', methods=['POST'])
def reservar_equipo_anwo():

    nroserieanwo = request.json.get('nroserieanwo')
    reservado = request.json.get('reservado').upper()

    mensaje1 = {'error': 'Falta el número de serie del equipo cuya reserva quiere aceptar o anular'}
    mensaje2 = {'error': 'Falta el valor "S" o "N" para indicar si la reserva la quiere aceptar o anular'}
    mensaje3 = {'error': 'El valor "{reservado}" no es válido, debe indicar "S" si quiere aceptar la reserva o "N" para anularla'}
    mensaje4 = {'success': f'La reserva del equipo {nroserieanwo} fue realizada con éxito'}
    mensaje5 = {'success': f'La reserva del equipo {nroserieanwo} fue anulada con éxito'}

    if not nroserieanwo: return jsonify(mensaje1), 400
    if not reservado: return jsonify(mensaje2), 400
    if reservado not in ['S', 'N']: return jsonify(mensaje3), 400

    # RESERVAR EQUIPO ANWO
    if reservado == 'S':
        exito, resultado = EJECUTAR_SP_RESERVAR_EQUIPO_ANWO(nroserieanwo, 'S')

    # ANULAR RESERVA DE EQUIPO ANWO
    if reservado == 'N':
        exito, resultado = EJECUTAR_SP_RESERVAR_EQUIPO_ANWO(nroserieanwo, 'N')

    if not exito: return jsonify({'error': resultado}), 500

    if reservado == 'S': return jsonify(mensaje4), 200
    if reservado == 'N': return jsonify(mensaje5), 200

    return jsonify({'error': 'Error desconocido'}), 500


#### creando la funcion para obtener todos los productos Anwo
def EJECUTAR_SP_LEER_TODOS_ANWO_STOCK_PRODUCTO():
    try:
        conn = pyodbc.connect(conn_str)

        # obtengo todos los productos Anwo
        cursor = conn.cursor()
        micursor = cursor.execute('EXEC dbo.SP_LEER_TODOS_ANWO_STOCK_PRODUCTO', ())
        productosanwo = micursor.fetchall()

        data = []
        for row in productosanwo:
            nroserieanwo = row[0]
            nomprodanwo = row[1]
            precioanwo = row[2]
            reservado = row[3]

            data.append({'nroserieanwo':nroserieanwo, 
                         'nomprodanwo': nomprodanwo,
                         'precioanwo': precioanwo,
                         'reservado': reservado
                         })

        conn.close()

        # retorna un json con los productos
        return jsonify({"data":data})
    except Exception as e:
        # retorna un json con el error
        return jsonify({"error":e})

@app.route('/consultar_productos_disponibles', methods=['GET'])
def consultar_productos_disponibles():
    respuesta = EJECUTAR_SP_LEER_TODOS_ANWO_STOCK_PRODUCTO()
    if isinstance(respuesta, tuple):
        return jsonify({"error": "Error inesperado, no se han podido cargar los productos ANWO"})
    return respuesta


app.run(debug=True)