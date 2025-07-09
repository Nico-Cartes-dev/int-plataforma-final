# type: ignore
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Producto, PerfilUsuario, SolicitudServicio, Factura
from .forms import ProductoForm, IniciarSesionForm
from .forms import RegistrarUsuarioForm, PerfilUsuarioForm
from django.db.models import Count, Case, When, Value, CharField, Q
#from .error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from django.db import connection
import random
import requests
from .utils import get_exchange_clp_usd
import logging

def get_user_cookies(request):
    """
    Función auxiliar para obtener información de las cookies del usuario
    """
    return {
        'remembered_username': request.COOKIES.get('remembered_username', ''),
        'user_type': request.COOKIES.get('user_type', ''),
        'last_login': request.COOKIES.get('last_login', ''),
        'user_full_name': request.COOKIES.get('user_full_name', '')
    }

def home(request):
    return render(request, "core/home.html")

@csrf_exempt
def iniciar_sesion(request):
    data = {"mesg": "", "form": IniciarSesionForm()}

    if request.method == "POST":
        form = IniciarSesionForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    tipousu = PerfilUsuario.objects.get(user=user).tipousu
                    if tipousu != 'Bodeguero':
                        # Crear respuesta con redirect
                        response = redirect(home)
                        
                        # Guardar información en cookies
                        from datetime import datetime, timedelta
                        
                        # Cookie para recordar el username (30 días)
                        response.set_cookie(
                            'remembered_username', 
                            username, 
                            max_age=30*24*60*60,  # 30 días en segundos
                            httponly=True,  # Protege contra XSS
                            samesite='Lax'  # Protege contra CSRF
                        )
                        
                        # Cookie para el tipo de usuario
                        response.set_cookie(
                            'user_type', 
                            tipousu, 
                            max_age=30*24*60*60,
                            httponly=True,
                            samesite='Lax'
                        )
                        
                        # Cookie para la última fecha de login
                        response.set_cookie(
                            'last_login', 
                            datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                            max_age=30*24*60*60,
                            httponly=True,
                            samesite='Lax'
                        )
                        
                        # Cookie para el nombre completo del usuario
                        full_name = f"{user.first_name} {user.last_name}".strip()
                        if full_name:
                            response.set_cookie(
                                'user_full_name', 
                                full_name, 
                                max_age=30*24*60*60,
                                httponly=True,
                                samesite='Lax'
                            )
                        
                        return response
                    else:
                        data["mesg"] = "¡La cuenta o la password no son correctos!"    
                else:
                    data["mesg"] = "¡La cuenta o la password no son correctos!"
            else:
                data["mesg"] = "¡La cuenta o la password no son correctos!"
    else:
        # Si es GET, verificar si hay cookies para autocompletar
        remembered_username = request.COOKIES.get('remembered_username', '')
        if remembered_username:
            data["form"] = IniciarSesionForm(initial={'username': remembered_username})
    
    return render(request, "core/iniciar_sesion.html", data)

def cerrar_sesion(request):
    logout(request)
    response = redirect(home)
    
    # Eliminar todas las cookies relacionadas con la sesión
    cookies_to_delete = [
        'remembered_username',
        'user_type', 
        'last_login',
        'user_full_name'
    ]
    
    for cookie_name in cookies_to_delete:
        response.delete_cookie(cookie_name)
    
    return response

def tienda(request):
    data = {
        "list": Producto.objects.all().order_by('idprod'),
        "active_page": "tienda"
    }
    return render(request, "core/tienda.html", data)

# https://www.transbankdevelopers.cl/documentacion/como_empezar#como-empezar
# https://www.transbankdevelopers.cl/documentacion/como_empezar#codigos-de-comercio
# https://www.transbankdevelopers.cl/referencia/webpay
# https://www.transbankdevelopers.cl/referencia/webpay#ambientes-y-credenciales

# Tipo de tarjeta   Detalle                        Resultado
# ---------------   -----------------------------  ------------------------------
# VISA              4051885600446623
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# AMEX              3700 0000 0002 032
#                   CVV 1234
#                   cualquier fecha de expiración  Genera transacciones aprobadas.
# MASTERCARD        5186 0595 5959 0568
#                   CVV 123
#                   cualquier fecha de expiración  Genera transacciones rechazadas.
# Redcompra         4051 8842 3993 7763            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         4511 3466 6003 7060            Genera transacciones aprobadas (para operaciones que permiten débito Redcompra y prepago)
# Redcompra         5186 0085 4123 3829            Genera transacciones rechazadas (para operaciones que permiten débito Redcompra y prepago)

@csrf_exempt
def ficha(request, id):
    data = {"mesg": "", "producto": None}
    exchange_rate = get_exchange_clp_usd()
    if exchange_rate is None:
        exchange_rate = 942.9500
        logger.warning("Using fallback exchange rate: 942.9500")

    if request.method == "POST":
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(iniciar_pago, id)
        else:
            data["mesg"] = "¡Para poder comprar debe iniciar sesión como cliente!"

    producto = Producto.objects.annotate(
        cantidad=Count(
            'stockproducto__idprod',
            filter=Q(stockproducto__nrofac__isnull=True)
        ),
        disponibilidad=Case(
            When(cantidad=0, then=Value('AGOTADO')),
            default=Value('DISPONIBLE'),
            output_field=CharField()
        )
    ).get(idprod=id)

    # Add USD price
    producto_dict = {
        'idprod': producto.idprod,
        'nomprod': producto.nomprod,
        'descprod': producto.descprod,
        'precio': producto.precio,
        'precio_usd': round(float(producto.precio) / exchange_rate, 2),
        'imagen': producto.imagen,
        'cantidad': producto.cantidad,
        'disponibilidad': producto.disponibilidad
    }
    data["producto"] = producto_dict
    data["exchange_rate"] = exchange_rate
    return render(request, "core/ficha.html", data)

@csrf_exempt
def iniciar_pago(request, id):

    # Esta es la implementacion de la VISTA iniciar_pago, que tiene la responsabilidad
    # de iniciar el pago, por medio de WebPay. Lo primero que hace es seleccionar un 
    # número de orden de compra, para poder así, identificar a la propia compra.
    # Como esta tienda no maneja, en realidad no tiene el concepto de "orden de compra"
    # pero se indica igual
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = Producto.objects.get(idprod=id).precio
    return_url = request.build_absolute_uri('/pago_exitoso/')

    # response = Transaction.create(buy_order, session_id, amount, return_url)
    commercecode = "597055555532"
    apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"

    tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
    response = tx.create(buy_order, session_id, amount, return_url)
    print(response['token'])

    perfil = PerfilUsuario.objects.get(user=request.user)
    form = PerfilUsuarioForm()

    context = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url,
        "response": response,
        "token_ws": response['token'],
        "url_tbk": response['url'],
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "email": request.user.email,
        "rut": perfil.rut,
        "dirusu": perfil.dirusu,
    }

    return render(request, "core/iniciar_pago.html", context)

@csrf_exempt
def pago_exitoso(request):
    if request.method == "GET":
        token = request.GET.get("token_ws")
        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.commit(token=token)

        user = User.objects.get(username=response['session_id'])
        perfil = PerfilUsuario.objects.get(user=user)

        # --- FLUJO DE SOLICITUD DE SERVICIO ---
        if response['response_code'] == 0 and request.session.get('servicio_tipo_solicitud'):
            tipo_solicitud = request.session.get('servicio_tipo_solicitud')
            descripcion = request.session.get('servicio_descripcion')
            fecha_visita = request.session.get('servicio_fecha_visita')
            tecnico_rut = request.session.get('servicio_tecnico_rut')
            precio = request.session.get('servicio_precio')

            tecnico = None
            if tecnico_rut:
                try:
                    tecnico = PerfilUsuario.objects.get(rut=tecnico_rut)
                except PerfilUsuario.DoesNotExist:
                    tecnico = None

            # 1. Crear la factura usando tu SP
            with connection.cursor() as cursor:
                cursor.execute(
                    "EXEC SP_CREAR_FACTURA @rutcli=%s, @idprod=%s, @monto=%s, @descfac=%s",
                    [perfil.rut, None, precio, 'Solicitud de servicio']
                )
                nrofac_num = cursor.fetchone()[0]  # Recupera el nrofac generado

            # 2. Obtener la instancia de Factura
            factura = Factura.objects.get(nrofac=nrofac_num)

            # 3. Crear la solicitud de servicio
            SolicitudServicio.objects.create(
                nrofac=factura,
                tiposol=tipo_solicitud,
                fechavisita=fecha_visita,
                ruttec=tecnico,
                descsol=descripcion,
                estadosol='Pendiente'
            )

            # Limpia la sesión si quieres
            for key in [
                'servicio_tipo_solicitud', 'servicio_descripcion', 'servicio_fecha_visita',
                'servicio_tecnico_rut', 'servicio_precio'
            ]:
                if key in request.session:
                    del request.session[key]

        # ...tu contexto y render...
        context = {
            "buy_order": response['buy_order'],
            "session_id": response['session_id'],
            "amount": response['amount'],
            "response": response,
            "token_ws": token,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "rut": perfil.rut,
            "dirusu": perfil.dirusu,
            "response_code": response['response_code']
        }

        return render(request, "core/pago_exitoso.html", context)
    else:
        return redirect(home)

@csrf_exempt
def administrar_productos(request, action, id):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(home)

    data = {
    "mesg": "",
    "form": ProductoForm,
    "action": action,
    "id": id,
    "formsesion": IniciarSesionForm,
    "active_page": "administrar_productos"
}

    if action == 'ins':
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            if form.is_valid:
                try:
                    form.save()
                    data["mesg"] = "¡El producto fue creado correctamente!"
                except:
                    data["mesg"] = "¡No se puede crear dos vehículos con el mismo ID!"

    elif action == 'upd':
        objeto = Producto.objects.get(idprod=id)
        if request.method == "POST":
            form = ProductoForm(data=request.POST, files=request.FILES, instance=objeto)
            if form.is_valid:
                form.save()
                data["mesg"] = "¡El producto fue actualizado correctamente!"
        data["form"] = ProductoForm(instance=objeto)

    elif action == 'del':
        try:
            Producto.objects.get(idprod=id).delete()
            data["mesg"] = "¡El producto fue eliminado correctamente!"
            return redirect(administrar_productos, action='ins', id = '-1')
        except:
            data["mesg"] = "¡El producto ya estaba eliminado!"

    data["list"] = Producto.objects.all().order_by('idprod')
    return render(request, "core/administrar_productos.html", data, )

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            try:
                # Crear usuario pero no guardarlo aún
                user = form.save(commit=False)
                # Asegurarse que el usuario sea un cliente normal
                user.is_staff = False
                user.is_superuser = False
                user.save()

                # Crear perfil de usuario
                rut = request.POST.get("rut")
                dirusu = request.POST.get("dirusu")
                
                tipousu = "Cliente"

                PerfilUsuario.objects.create(
                    user=user,
                    rut=rut,
                    tipousu=tipousu,
                    dirusu=dirusu
                )
 
                return redirect(iniciar_sesion)
            except Exception as e:
                if user.pk:
                    user.delete()
                form.add_error(None, f"Error al registrar usuario: {str(e)}")
    else:
        form = RegistrarUsuarioForm()
    
    return render(request, "core/registrar_usuario.html", {
        'form': form,
        'titulo': 'Registro de Cliente Nuevo',
        'active_page': 'registrar_usuario'
    })



def perfil_usuario(request):
    data = {"mesg": ""}

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            perfil = PerfilUsuario.objects.get(user=user)
            perfil.rut = form.cleaned_data['rut']
            perfil.dirusu = form.cleaned_data['dirusu']
            perfil.tipousu = form.cleaned_data['tipousu'] 
            perfil.save()

            data["mesg"] = "¡Sus datos fueron actualizados correctamente!"

            # Mostrar el formulario con datos actualizados
            form = PerfilUsuarioForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'rut': perfil.rut,
                'tipousu': perfil.tipousu,
                'dirusu': perfil.dirusu
            })
    else:
        user = request.user
        perfil = PerfilUsuario.objects.get(user=user)
        form = PerfilUsuarioForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'rut': perfil.rut,
            'tipousu': perfil.tipousu,
            'dirusu': perfil.dirusu
        })

    data["form"] = form
    data["active_page"] = "perfil_usuario"
    return render(request, "core/perfil_usuario.html", data)

# #*
# def obtener_solicitudes_de_servicio(request):
#     tipousu = PerfilUsuario.objects.get(user=request.user).tipousu
#     data = {'tipousu': tipousu }
#     return render(request, "core/obtener_solicitudes_de_servicio.html", data)


def equipos_bodega(request):
    # *obtener los equipos de la bodega
    productos = Producto.objects.annotate(
        cantidad=Count(
            'stockproducto__idprod',
            filter=models.Q(stockproducto__nrofac__isnull=True)
        ),
        disponibilidad=Case(
            When(cantidad=0, then=Value('AGOTADO')),
            default=Value('DISPONIBLE'),
            output_field=CharField()
        )
    ).values(
        'idprod',
        'nomprod',
        'descprod',
        'precio',
        'imagen',
        'cantidad',
        'disponibilidad'
    ).order_by('idprod')

    productos_list = list(productos)
    print(productos_list)
    
    return JsonResponse({'productos': productos_list})

logger = logging.getLogger(__name__)

@csrf_exempt
def tienda(request):
    # Fetch exchange rate
    exchange_rate = get_exchange_clp_usd()
    if exchange_rate is None:
        exchange_rate = 942.9500  
        logger.warning(f"Using fallback exchange rate: {exchange_rate}")

    
    productos = Producto.objects.annotate(
        cantidad=Count(
            'stockproducto__idprod',
            filter=Q(stockproducto__nrofac__isnull=True)
        ),
        disponibilidad=Case(
            When(cantidad=0, then=Value('AGOTADO')),
            default=Value('DISPONIBLE'),
            output_field=CharField()
        )
    ).values(
        'idprod',
        'nomprod',
        'descprod',
        'precio',
        'imagen',
        'cantidad',
        'disponibilidad'
    ).order_by('idprod')

    
    productos_with_usd = [
        {
            **producto,
            'precio_usd': round(float(producto['precio']) / exchange_rate, 2)
        }
        for producto in productos
    ]
    # ? print(productos_with_usd)
    

    return render(
        request,
        'core/tienda.html',
        {
            'productos': productos_with_usd,
            'exchange_rate': exchange_rate,
            'active_page': 'tienda'
        }
    )

@csrf_exempt
def registrar_solicitud_servicio(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    if request.method == 'POST':
        form = SolicitudServicio(request.POST)
        if form.is_valid():
            tipo_solicitud = form.cleaned_data['tipo_solicitud']
            descripcion = form.cleaned_data['descripcion']
            fecha_sugerida = form.cleaned_data['fecha_sugerida']
            hora_sugerida = form.cleaned_data['hora_sugerida']
            rut_cliente = PerfilUsuario.objects.get(user=request.user).rut

            # Llamar al procedimiento almacenado
            with connection.cursor() as cursor:
                cursor.callproc('SP_CREAR_SOLICITUD_SERVICIO', [
                    rut_cliente,
                    tipo_solicitud,
                    descripcion,
                    fecha_sugerida,
                    hora_sugerida
                ])

            # Redirigir al pago
            return redirect('iniciar_pago')

    else:
        form = SolicitudServicio()

    return render(
        request,
        'core/registrar_solicitud_servicio.html',
        {'form': form, 'active_page': 'registrar_solicitud_servicio'}
    )

@csrf_exempt
def facturas(request):
    if not request.user.is_authenticated:
        return redirect('iniciar_sesion')

    try:
        # Obtener el perfil del usuario conectado
        perfil = PerfilUsuario.objects.get(user=request.user)
        rut_cliente = perfil.rut if perfil.tipousu != 'Administrador' else 'admin'

        # Obtener facturas usando el procedimiento almacenado
        facturas = obtener_facturas(rut_cliente)

        # Obtener guías de despacho si el usuario es un cliente
        guias_despacho = []
        if perfil.tipousu != 'Administrador':
            guias_despacho = obtener_guias_despacho()

        context = {
            'facturas': facturas,
            'guias_despacho': guias_despacho,
            'tipousu': perfil.tipousu,
            'active_page': 'facturas'
        }
        return render(request, 'core/facturas.html', context)

    except PerfilUsuario.DoesNotExist:
        return render(request, 'core/facturas.html', {
            'error': 'No se encontró el perfil del usuario.',
            'active_page': 'facturas'
        })

    except Exception as e:
        logger.error(f"Error al obtener facturas: {str(e)}")
        return render(request, 'core/facturas.html', {
            'error': 'Ocurrió un error inesperado al obtener las facturas.',
            'active_page': 'facturas'
        })


def obtener_facturas(rut_cliente):
    """Función auxiliar para obtener las facturas."""
    with connection.cursor() as cursor:
        cursor.callproc('SP_OBTENER_FACTURAS', [rut_cliente])
        facturas = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in facturas]

def obtener_guias_despacho():
    """Función auxiliar para obtener las guías de despacho."""
    with connection.cursor() as cursor:
        cursor.callproc('SP_OBTENER_GUIAS_DE_DESPACHO')
        guias_despacho = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in guias_despacho]

@login_required
def mis_compras(request):
    if request.user.perfilusuario.tipousu != 'Cliente':
        return redirect('home')
    
    facturas = Factura.objects.filter(rutcli=request.user.perfilusuario.rut)
    return render(
    request,
    'core/facturas.html',
    {'facturas': facturas, 'active_page': 'facturas'}
)

# @login_required
# def mis_solicitudes(request):
#     if request.user.perfilusuario.tipousu != 'Cliente':
#         return redirect('home')
    
#     solicitudes = SolicitudServicio.objects.filter(
#         factura__rutcli=request.user.perfilusuario.rut
#     )
#     return render(
#     request,
#     'core/obtener_solicitudes_de_servicio.html',
#     {'solicitudes': solicitudes, 'active_page': 'obtener_solicitudes'}
# )

# @login_required
# def perfil_usuario(request):
#     if request.method == 'POST':
#         form = PerfilUsuarioForm(request.POST, instance=request.user.perfilusuario)
#         if form.is_valid():
#             form.save()
#             return render(request, 'core/perfil_usuario.html', {'form': form, 'success': True})
#     else:
#         form = PerfilUsuarioForm(instance=request.user.perfilusuario)
#     return render(request, 'core/perfil_usuario.html', {'form': form})

@login_required
def obtener_solicitudes_de_servicio(request):
    if request.user.perfilusuario.tipousu == 'Técnico':
        # Mostrar solo solicitudes asignadas al técnico
        solicitudes = SolicitudServicio.objects.filter(ruttec=request.user.perfilusuario)
    elif request.user.perfilusuario.tipousu == 'Administrador':
        # Mostrar todas las solicitudes
        solicitudes = SolicitudServicio.objects.all()
    elif request.user.perfilusuario.tipousu == 'Cliente':
        # Mostrar solo las solicitudes del cliente
        solicitudes = SolicitudServicio.objects.filter(nrofac__rutcli=request.user.perfilusuario.rut)
    else:
        return redirect('home')
    
    lista = []
    for sol in solicitudes:
        lista.append({
            'nrosol': sol.nrosol,
            'nomcli': f"{sol.nrofac.rutcli.user.first_name} {sol.nrofac.rutcli.user.last_name}",
            'tiposol': sol.tiposol,
            'fechavisita': sol.fechavisita,
            'nomtec': f"{sol.ruttec.user.first_name} {sol.ruttec.user.last_name}",
            'descser': sol.descsol,  # <--- aquí está el nombre correcto
            'estadosol': sol.estadosol,
        })
    
    return render(request, 'core/obtener_solicitudes_de_servicio.html',
    {'lista': lista, 'active_page': 'obtener_solicitudes_de_servicio'}
)
@login_required
def aceptar_solicitud(request, nrosol):
    solicitud = SolicitudServicio.objects.get(nrosol=nrosol)
    solicitud.estadosol = 'Aceptado'
    solicitud.save()
    return redirect('obtener_solicitudes_de_servicio')

@login_required
def modificar_solicitud(request, nrosol):
    solicitud = SolicitudServicio.objects.get(nrosol=nrosol)
    if request.method == 'POST':
        nueva_fecha = request.POST.get('fechavisita')
        if nueva_fecha:
            solicitud.fechavisita = nueva_fecha
            solicitud.estadosol = 'Modificado'
            solicitud.save()
    return redirect('obtener_solicitudes_de_servicio')

@login_required
def cerrar_solicitud(request, nrosol):
    solicitud = SolicitudServicio.objects.get(nrosol=nrosol)
    solicitud.estadosol = 'Cerrado'
    solicitud.save()
    return redirect('obtener_solicitudes_de_servicio')


@login_required
def facturas(request):
    perfil = request.user.perfilusuario
    if perfil.tipousu == 'Administrador':
        facturas = Factura.objects.all()
    elif perfil.tipousu == 'Cliente':
        facturas = Factura.objects.filter(rutcli=perfil.rut)
    else:
        return redirect('home')
    
    return render(
        request,
        'core/facturas.html',
        {'facturas': facturas, 'active_page': 'facturas'}
    )


@login_required
def ingresar_solicitud_servicio(request):
    PRECIO_SERVICIO = 25000 

    if request.method == 'POST':
        tipo_solicitud = request.POST.get('tipo_solicitud')
        descripcion = request.POST.get('descripcion')
        fecha_visita = request.POST.get('fecha_visita')
        print(f"Tipo de solicitud: {tipo_solicitud}, Descripción: {descripcion}, Fecha: {fecha_visita}")
        # Guardar datos en sesión para usarlos después del pago
        tecnico = PerfilUsuario.objects.filter(tipousu='Técnico').first()
        # perfil_cliente = PerfilUsuario.objects.get(user=user)
        request.session['servicio_tipo_solicitud'] = tipo_solicitud
        request.session['servicio_descripcion'] = descripcion
        request.session['servicio_fecha_visita'] = fecha_visita
        request.session['servicio_precio'] = PRECIO_SERVICIO
        if tecnico:
            request.session['servicio_tecnico_rut'] = tecnico.rut
        else:
            request.session['servicio_tecnico_rut'] = None  # O maneja el caso sin técnico

        # Iniciar pago Webpay
        buy_order = str(random.randrange(1000000, 99999999))
        session_id = request.user.username
        amount = PRECIO_SERVICIO
        return_url = request.build_absolute_uri('/pago_exitoso/')

        commercecode = "597055555532"
        apikey = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"
        tx = Transaction(options=WebpayOptions(commerce_code=commercecode, api_key=apikey, integration_type="TEST"))
        response = tx.create(buy_order, session_id, amount, return_url)

        context = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url,
            "response": response,
            "token_ws": response['token'],
            "url_tbk": response['url'],
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "rut": request.user.perfilusuario.rut,
            "dirusu": request.user.perfilusuario.dirusu,
            "tecnico": tecnico,
        }
        return render(request, "core/iniciar_pago.html", context)

    return render(
    request,
    'core/ingresar_solicitud_servicio.html',
    {'precio_servicio': 25000, 'active_page': 'ingresar_solicitud_servicio'}
)
    