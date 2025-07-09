# type: ignore
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from core.models import PerfilUsuario
from django.db import connection
import threading

semaforo = threading.Semaphore(10)
@csrf_exempt
@api_view(['GET'])
def autenticar(request, tipousu, username, password):
    user = authenticate(username=username, password=password)
    if user:
        perfil = PerfilUsuario.objects.get(user=user)
        nombre = f'{user.first_name} {user.last_name}'
        tipo = perfil.tipousu
        if tipo in [tipousu, 'Administrador']:
            return JsonResponse({'Autenticado': True, 'NombreUsuario': nombre, 'TipoUsuario': tipo, 'Mensaje': ''}, status=200)
        return JsonResponse({'Autenticado': False, 'NombreUsuario': nombre, 'TipoUsuario': tipo, 'Mensaje': 'Rol no autorizado'}, status=403)
    return JsonResponse({'Autenticado': False, 'NombreUsuario': '', 'TipoUsuario': '', 'Mensaje': 'Credenciales inválidas'}, status=401)

@csrf_exempt
def obtener_equipos_en_bodega(request):
    if request.method == 'GET':
        acquired = semaforo.acquire(timeout=10)  # Espera hasta 10 segundos
        if not acquired:
            return JsonResponse({'error': 'Servidor ocupado, intenta de nuevo en unos segundos.'}, status=503)
        try:
            cursor = connection.cursor()
            cursor.execute("exec sp_obtener_equipos_en_bodega")
            resultados = cursor.fetchall()
            data = []
            for row in resultados:
                idstock = row[0]
                nomprod = row[2]
                cantidad = row[4]
                estado = row[5]
                data.append({
                    'idstock': idstock,
                    'nomprod': nomprod,
                    'cantidad': cantidad,
                    'estado': estado
                })
            return JsonResponse(data, safe=False)
        finally:
            semaforo.release()

@api_view(['GET'])
def obtener_productos(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC SP_OBTENER_PRODUCTOS")
            productos = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            productos_list = [
                {
                    'idprod': producto[0],
                    'nomprod': producto[1],
                    'descprod': producto[2],
                    'precio': float(producto[3]),
                    'imagen': producto[4] if producto[4] else None
                }
                for producto in productos
            ]
            return JsonResponse({'productos': productos_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@api_view(['GET'])
def consultar_guias_despacho(request):
    """
    GET /api/guias-despacho/
    Llama a SP_OBTENER_GUIAS_DE_DESPACHO y devuelve una lista de guías:
      - nrogd
      - nrofac
      - idprod
      - estadogd
      - nomprod
      - rutcli
    """
    try:
        with connection.cursor() as cursor:
            # Ejecuta el SP
            cursor.execute("EXEC SP_OBTENER_GUIAS_DE_DESPACHO")
            # Lee nombres de columnas
            columns = [col[0] for col in cursor.description]
            # Lee todas las filas
            rows = cursor.fetchall()

        # Mapea cada fila a un dict usando los nombres
        guias = [dict(zip(columns, row)) for row in rows]

        # Devuelve directamente la lista
        return JsonResponse(guias, safe=False)

    except Exception as e:
        # Captura y reporta el error
        return JsonResponse({'error': str(e)}, status=500)

def actualizar_estado_guia(request, nrogd, nuevo_estado):
    """
    Actualiza el estado de una Guía de Despacho llamando al procedimiento SP_ACTUALIZAR_ESTADO_GUIA_DESPACHO.
    Se espera que 'nrogd' sea un número entero y 'nuevo_estado' una cadena, (Ej. 'Despachado' o 'Entregado').
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"EXEC SP_ACTUALIZAR_ESTADO_GUIA_DESPACHO @p_nrogd={nrogd}, @p_nuevo_estado='{nuevo_estado}'")
            resultados = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            guia_actualizada = [dict(zip(columns, row)) for row in resultados]
        return JsonResponse({'guia_actualizada': guia_actualizada})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 