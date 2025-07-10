# type: ignore
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Producto, PerfilUsuario, SolicitudServicio, Factura, GuiaDespacho
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

def asignar_tecnico_automaticamente():
    """
    Función auxiliar para asignar un técnico automáticamente a una solicitud.
    Implementa una lógica simple de round-robin para distribuir la carga.
    """
    try:
        # Obtener todos los técnicos disponibles
        tecnicos = PerfilUsuario.objects.filter(tipousu='Técnico')
        
        if not tecnicos.exists():
            logger.warning("No hay técnicos disponibles para asignación automática")
            return None
        
        # Obtener el técnico con menos solicitudes activas
        tecnico_menos_cargado = None
        menor_carga = float('inf')
        
        for tecnico in tecnicos:
            # Contar solicitudes activas del técnico (Aceptada, Asignada, Modificada)
            solicitudes_activas = SolicitudServicio.objects.filter(
                ruttec=tecnico,
                estadosol__in=['Aceptada', 'Asignada', 'Modificada']
            ).count()
            
            if solicitudes_activas < menor_carga:
                menor_carga = solicitudes_activas
                tecnico_menos_cargado = tecnico
        
        logger.info(f"Técnico asignado automáticamente: {tecnico_menos_cargado.user.first_name} {tecnico_menos_cargado.user.last_name} (RUT: {tecnico_menos_cargado.rut}) - Carga actual: {menor_carga}")
        return tecnico_menos_cargado
        
    except Exception as e:
        logger.error(f"Error en asignación automática de técnico: {str(e)}")
        return None

def guardar_compra_en_bd(producto_id, perfil_cliente, precio=None):
    """
    Función auxiliar para guardar una compra directamente en la base de datos
    sin depender de WebPay. Útil para testing y debugging.
    """
    try:
        logger.info(f"=== GUARDANDO COMPRA EN BD ===")
        logger.info(f"Producto ID: {producto_id}, Cliente: {perfil_cliente.rut}")
        
        # Obtener el producto
        producto = Producto.objects.get(idprod=producto_id)
        logger.info(f"Producto obtenido: {producto.nomprod}")
        
        # Usar precio del producto si no se especifica
        if precio is None:
            precio = producto.precio
        
        # 1. Crear la factura
        from datetime import date
        
        # Generar un número de factura único
        ultima_factura = Factura.objects.order_by('-nrofac').first()
        nrofac_num = (ultima_factura.nrofac + 1) if ultima_factura else 1
        logger.info(f"Generando número de factura: {nrofac_num}")
        
        # Crear la factura
        factura = Factura.objects.create(
            nrofac=nrofac_num,
            rutcli=perfil_cliente,
            idprod=producto,
            fechafac=date.today(),
            descfac=f'Compra de {producto.nomprod}',
            monto=precio
        )
        logger.info(f"Factura creada exitosamente: {factura.nrofac}")
        
        # 2. Crear la guía de despacho
        ultima_guia = GuiaDespacho.objects.order_by('-nrogd').first()
        nrogd_num = (ultima_guia.nrogd + 1) if ultima_guia else 1
        logger.info(f"Generando número de guía: {nrogd_num}")
        
        guia_despacho = GuiaDespacho.objects.create(
            nrogd=nrogd_num,
            nrofac=factura,
            idprod=producto,
            estadogd='En bodega'
        )
        logger.info(f"Guía de despacho creada exitosamente: {guia_despacho.nrogd}")
        
        # 3. Crear solicitud de servicio automática para TODA compra
        solicitud_creada = False
        # Asignar técnico automáticamente usando la nueva función
        tecnico = asignar_tecnico_automaticamente()
        
        if tecnico:
            # Generar un número de solicitud único
            ultima_solicitud = SolicitudServicio.objects.order_by('-nrosol').first()
            nrosol_num = (ultima_solicitud.nrosol + 1) if ultima_solicitud else 1
            
            # Calcular fecha de visita (7 días después)
            from datetime import timedelta
            fecha_visita = date.today() + timedelta(days=7)
            
            # Determinar el tipo de servicio basado en el producto
            if producto.nomprod.lower() in ['aire acondicionado', 'ac', 'climatizador', 'split']:
                tipo_servicio = 'Instalación'
                descripcion = f'Instalación de {producto.nomprod}'
            else:
                tipo_servicio = 'Mantención'
                descripcion = f'Mantención de {producto.nomprod}'
            
            solicitud = SolicitudServicio.objects.create(
                nrosol=nrosol_num,
                nrofac=factura,
                tiposol=tipo_servicio,
                fechavisita=fecha_visita,
                ruttec=tecnico,
                descsol=descripcion,
                estadosol='Pendiente',
                guia=guia_despacho  # Vincular a la guía de despacho
            )
            print(solicitud)
            logger.info(f"Solicitud de servicio automática creada: {solicitud.nrosol} - Tipo: {tipo_servicio} - Vinculada a guía: {guia_despacho.nrogd}")
            solicitud_creada = True
        else:
            logger.warning("No se encontró técnico disponible para crear solicitud de servicio")
        
        logger.info("=== COMPRA GUARDADA EXITOSAMENTE ===")
        
        return {
            'success': True,
            'factura': factura,
            'guia_despacho': guia_despacho,
            'solicitud_creada': solicitud_creada
        }
        
    except Exception as e:
        logger.error(f"=== ERROR GUARDANDO COMPRA ===")
        logger.error(f"Error: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return {
            'success': False,
            'error': str(e)
        }

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
    # Verificar estado de la base de datos
    try:
        productos_count = Producto.objects.count()
        facturas_count = Factura.objects.count()
        guias_count = GuiaDespacho.objects.count()
        tecnicos_count = PerfilUsuario.objects.filter(tipousu='Técnico').count()
        
        logger.info(f"Estado BD - Productos: {productos_count}, Facturas: {facturas_count}, Guías: {guias_count}, Técnicos: {tecnicos_count}")
    except Exception as e:
        logger.error(f"Error verificando BD: {str(e)}")
    
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
    
    # Obtener información del producto
    producto = Producto.objects.get(idprod=id)
    
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = request.user.username
    amount = producto.precio
    return_url = request.build_absolute_uri('/pago_exitoso/')

    # Guardar información del producto en la sesión para procesarlo después del pago
    request.session['compra_producto_id'] = id
    request.session['compra_producto_nombre'] = producto.nomprod
    request.session['compra_producto_precio'] = amount
    request.session['compra_buy_order'] = buy_order
    
    logger.info(f"Compra iniciada - Producto: {producto.nomprod}, ID: {id}, Precio: {amount}")

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
        "producto": producto,
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

        # Log para debuggear
        logger.info(f"=== DEBUG INFO ===")
        logger.info(f"Usuario: {user.username}")
        logger.info(f"Perfil: {perfil.rut} - {perfil.tipousu}")
        logger.info(f"Pago exitoso - Response code: {response['response_code']}")
        logger.info(f"Datos de sesión disponibles: {dict(request.session)}")
        logger.info(f"¿Existe servicio_tipo_solicitud?: {request.session.get('servicio_tipo_solicitud')}")
        logger.info(f"¿Existe compra_producto_id?: {request.session.get('compra_producto_id')}")
        logger.info(f"Productos en BD: {Producto.objects.count()}")
        logger.info(f"Facturas en BD: {Factura.objects.count()}")
        logger.info(f"Guias en BD: {GuiaDespacho.objects.count()}")
        logger.info(f"Técnicos en BD: {PerfilUsuario.objects.filter(tipousu='Técnico').count()}")
        logger.info(f"=== FIN DEBUG INFO ===")

        # Variables para rastrear el procesamiento
        servicio_procesado = False
        compra_procesada = False
        
        # --- FLUJO DE COMPRA DE PRODUCTO ---
        if response['response_code'] == 0 and request.session.get('compra_producto_id'):
            logger.info("=== INICIANDO FLUJO DE COMPRA ===")
            try:
                producto_id = request.session.get('compra_producto_id')
                producto_nombre = request.session.get('compra_producto_nombre')
                producto_precio = request.session.get('compra_producto_precio')
                buy_order = request.session.get('compra_buy_order')
                
                logger.info(f"Procesando compra de producto - ID: {producto_id}, Nombre: {producto_nombre}, Precio: {producto_precio}")
                logger.info(f"Tipo de producto_id: {type(producto_id)}")
                logger.info(f"Tipo de producto_precio: {type(producto_precio)}")
                
                # Obtener el producto
                producto = Producto.objects.get(idprod=producto_id)
                logger.info(f"Producto obtenido: {producto.nomprod} (ID: {producto.idprod})")
                
                # 1. Crear la factura
                from datetime import date
                
                # Generar un número de factura único
                ultima_factura = Factura.objects.order_by('-nrofac').first()
                nrofac_num = (ultima_factura.nrofac + 1) if ultima_factura else 1
                logger.info(f"Generando número de factura: {nrofac_num} (última factura: {ultima_factura.nrofac if ultima_factura else 'Ninguna'})")
                
                # Crear la factura
                logger.info("Intentando crear factura...")
                factura = Factura.objects.create(
                    nrofac=nrofac_num,
                    rutcli=perfil,
                    idprod=producto,
                    fechafac=date.today(),
                    descfac=f'Compra de {producto.nomprod}',
                    monto=producto_precio
                )
                logger.info(f"Factura creada exitosamente con número: {nrofac_num}")
                
                # 2. Crear la guía de despacho
                ultima_guia = GuiaDespacho.objects.order_by('-nrogd').first()
                nrogd_num = (ultima_guia.nrogd + 1) if ultima_guia else 1
                logger.info(f"Generando número de guía de despacho: {nrogd_num} (última guía: {ultima_guia.nrogd if ultima_guia else 'Ninguna'})")
                
                guia_despacho = GuiaDespacho.objects.create(
                    nrogd=nrogd_num,
                    nrofac=factura,
                    idprod=producto,
                    estadogd='En bodega'
                )
                logger.info(f"Guía de despacho creada exitosamente con número: {nrogd_num}")
                
                # 3. Crear solicitud de servicio automática si el producto requiere instalación
                if producto.nomprod.lower() in ['aire acondicionado', 'ac', 'climatizador', 'split']:
                    # Asignar técnico automáticamente usando la nueva función
                    tecnico = asignar_tecnico_automaticamente()
                    
                    if tecnico:
                        # Generar un número de solicitud único
                        ultima_solicitud = SolicitudServicio.objects.order_by('-nrosol').first()
                        nrosol_num = (ultima_solicitud.nrosol + 1) if ultima_solicitud else 1
                        
                        # Calcular fecha de visita (7 días después)
                        from datetime import timedelta
                        fecha_visita = date.today() + timedelta(days=7)
                        
                        solicitud = SolicitudServicio.objects.create(
                            nrosol=nrosol_num,
                            nrofac=factura,
                            tiposol='Instalación',
                            fechavisita=fecha_visita,
                            ruttec=tecnico,
                            descsol=f'Instalación automática de {producto.nomprod}',
                            estadosol='Pendiente',
                            guia=guia_despacho  # Vincular a la guía de despacho
                        )
                        logger.info(f"Solicitud de servicio automática creada con ID: {solicitud.nrosol} - Vinculada a guía: {guia_despacho.nrogd}")
                
                # Limpiar datos de sesión de compra
                for key in ['compra_producto_id', 'compra_producto_nombre', 'compra_producto_precio', 'compra_buy_order']:
                    if key in request.session:
                        del request.session[key]
                
                logger.info("Datos de sesión de compra limpiados correctamente")
                compra_procesada = True
                logger.info("=== FLUJO DE COMPRA COMPLETADO EXITOSAMENTE ===")
                
            except Exception as e:
                logger.error(f"=== ERROR EN FLUJO DE COMPRA ===")
                logger.error(f"Error al procesar compra de producto: {str(e)}")
                logger.error(f"Tipo de error: {type(e).__name__}")
                import traceback
                logger.error(f"Traceback completo: {traceback.format_exc()}")
                compra_procesada = False
        
        # --- FLUJO DE SOLICITUD DE SERVICIO ---
        if response['response_code'] == 0 and request.session.get('servicio_tipo_solicitud'):
            try:
                tipo_solicitud = request.session.get('servicio_tipo_solicitud')
                descripcion = request.session.get('servicio_descripcion')
                fecha_visita = request.session.get('servicio_fecha_visita')
                tecnico_rut = request.session.get('servicio_tecnico_rut')
                precio = request.session.get('servicio_precio')

                logger.info(f"Procesando solicitud de servicio - Tipo: {tipo_solicitud}, Descripción: {descripcion}, Fecha: {fecha_visita}, Precio: {precio}")
                
                # Convertir la fecha de string a objeto date
                from datetime import datetime
                try:
                    fecha_visita_obj = datetime.strptime(fecha_visita, '%Y-%m-%d').date()
                    logger.info(f"Fecha convertida correctamente: {fecha_visita_obj}")
                except Exception as e:
                    logger.error(f"Error al convertir fecha: {str(e)}")
                    fecha_visita_obj = date.today()  # Usar fecha actual como fallback

                tecnico = None
                if tecnico_rut:
                    try:
                        tecnico = PerfilUsuario.objects.get(rut=tecnico_rut)
                        logger.info(f"Técnico asignado: {tecnico.user.first_name} {tecnico.user.last_name}")
                    except PerfilUsuario.DoesNotExist:
                        logger.warning(f"No se encontró técnico con RUT: {tecnico_rut}")
                        tecnico = None

                # 1. Crear la factura directamente usando Django ORM
                from datetime import date
                
                # Generar un número de factura único
                ultima_factura = Factura.objects.order_by('-nrofac').first()
                nrofac_num = (ultima_factura.nrofac + 1) if ultima_factura else 1
                
                # Crear la factura
                factura = Factura.objects.create(
                    nrofac=nrofac_num,
                    rutcli=perfil,
                    idprod=None,  # Para solicitudes de servicio no hay producto específico
                    fechafac=date.today(),
                    descfac='Solicitud de servicio',
                    monto=precio
                )
                logger.info(f"Factura creada con número: {nrofac_num}")

                # 3. Crear la solicitud de servicio
                # Generar un número de solicitud único
                ultima_solicitud = SolicitudServicio.objects.order_by('-nrosol').first()
                nrosol_num = (ultima_solicitud.nrosol + 1) if ultima_solicitud else 1
                
                solicitud = SolicitudServicio.objects.create(
                    nrosol=nrosol_num,
                    nrofac=factura,
                    tiposol=tipo_solicitud,
                    fechavisita=fecha_visita_obj,
                    ruttec=tecnico,
                    descsol=descripcion,
                    estadosol='Pendiente'
                )
                logger.info(f"Solicitud de servicio creada con ID: {solicitud.nrosol}")

                # Limpia la sesión
                for key in [
                    'servicio_tipo_solicitud', 'servicio_descripcion', 'servicio_fecha_visita',
                    'servicio_tecnico_rut', 'servicio_precio'
                ]:
                    if key in request.session:
                        del request.session[key]
                
                logger.info("Datos de sesión limpiados correctamente")
                servicio_procesado = True

            except Exception as e:
                logger.error(f"Error al procesar solicitud de servicio: {str(e)}")
                servicio_procesado = False

        # Contexto para el template
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
            "response_code": response['response_code'],
            "pago_exitoso": response['response_code'] == 0,
            "servicio_procesado": servicio_procesado,
            "compra_procesada": compra_procesada
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
        # Mostrar solicitudes asignadas al técnico Y solicitudes pendientes sin asignar
        solicitudes_asignadas = SolicitudServicio.objects.filter(ruttec=request.user.perfilusuario)
        solicitudes_pendientes = SolicitudServicio.objects.filter(ruttec__isnull=True, estadosol='Pendiente')
        solicitudes = solicitudes_asignadas | solicitudes_pendientes
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
            'nomtec': f"{sol.ruttec.user.first_name} {sol.ruttec.user.last_name}" if sol.ruttec else 'Sin asignar',
            'ruttec': sol.ruttec.rut if sol.ruttec else None,
            'descser': sol.descsol,
            'estadosol': sol.estadosol,
        })
    
    # Obtener lista de técnicos para el administrador
    tecnicos = []
    if request.user.perfilusuario.tipousu == 'Administrador':
        tecnicos = PerfilUsuario.objects.filter(tipousu='Técnico').values('rut', 'user__first_name', 'user__last_name')
    
    return render(request, 'core/obtener_solicitudes_de_servicio.html',
    {
        'lista': lista, 
        'active_page': 'obtener_solicitudes_de_servicio',
        'tecnicos': tecnicos,
        'es_admin': request.user.perfilusuario.tipousu == 'Administrador'
    }
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
    user_perfil = request.user.perfilusuario

    if request.method == 'POST':
        accion = request.POST.get('accion')
        nueva_fecha = request.POST.get('fechavisita')
        tecnico_asignar = request.POST.get('tecnico_asignar')  # Para administradores

        # Modificar fecha (opcional)
        if nueva_fecha:
            solicitud.fechavisita = nueva_fecha
            if solicitud.estadosol != 'Aceptada':
                solicitud.estadosol = 'Modificada'

        # Lógica para administradores - asignar técnico manualmente
        if accion == 'asignar_tecnico' and user_perfil.tipousu == 'Administrador' and tecnico_asignar:
            try:
                tecnico = PerfilUsuario.objects.get(rut=tecnico_asignar, tipousu='Técnico')
                solicitud.ruttec = tecnico
                solicitud.estadosol = 'Asignada'
                logger.info(f"Administrador {user_perfil.rut} asignó técnico {tecnico.rut} a solicitud {nrosol}")
            except PerfilUsuario.DoesNotExist:
                logger.error(f"Técnico con RUT {tecnico_asignar} no encontrado")

        # Lógica para técnicos - aceptar solicitud
        elif accion == 'aceptar' and solicitud.ruttec is None and user_perfil.tipousu == 'Técnico':
            solicitud.ruttec = user_perfil
            solicitud.estadosol = 'Aceptada'
            logger.info(f"Técnico {user_perfil.rut} aceptó solicitud {nrosol}")

        # Lógica para técnicos - soltar solicitud
        elif accion == 'soltar' and solicitud.ruttec == user_perfil and user_perfil.tipousu == 'Técnico':
            solicitud.ruttec = None
            solicitud.estadosol = 'Pendiente'
            logger.info(f"Técnico {user_perfil.rut} soltó solicitud {nrosol}")

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
        
        logger.info(f"Recibiendo solicitud de servicio - Tipo: {tipo_solicitud}, Descripción: {descripcion}, Fecha: {fecha_visita}")
        
        # Guardar datos en sesión para usarlos después del pago
        tecnico = asignar_tecnico_automaticamente()
        
        # Guardar datos en sesión
        request.session['servicio_tipo_solicitud'] = tipo_solicitud
        request.session['servicio_descripcion'] = descripcion
        request.session['servicio_fecha_visita'] = fecha_visita
        request.session['servicio_precio'] = PRECIO_SERVICIO
        
        if tecnico:
            request.session['servicio_tecnico_rut'] = tecnico.rut
            logger.info(f"Técnico asignado automáticamente: {tecnico.user.first_name} {tecnico.user.last_name} (RUT: {tecnico.rut})")
        else:
            request.session['servicio_tecnico_rut'] = None
            logger.warning("No se encontró técnico disponible para asignación automática")
        
        # Verificar que los datos se guardaron correctamente en la sesión
        logger.info(f"Datos guardados en sesión: {dict(request.session)}")

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

@login_required
def dashboard_tecnicos(request):
    """
    Dashboard para administradores con estadísticas de asignación de técnicos
    """
    if request.user.perfilusuario.tipousu != 'Administrador':
        return redirect('home')
    
    # Obtener estadísticas de técnicos
    tecnicos_stats = []
    tecnicos = PerfilUsuario.objects.filter(tipousu='Técnico')
    
    for tecnico in tecnicos:
        solicitudes_asignadas = SolicitudServicio.objects.filter(ruttec=tecnico).count()
        solicitudes_activas = SolicitudServicio.objects.filter(
            ruttec=tecnico,
            estadosol__in=['Aceptada', 'Asignada', 'Modificada']
        ).count()
        solicitudes_completadas = SolicitudServicio.objects.filter(
            ruttec=tecnico,
            estadosol='Cerrado'
        ).count()
        
        tecnicos_stats.append({
            'tecnico': tecnico,
            'nombre': f"{tecnico.user.first_name} {tecnico.user.last_name}",
            'rut': tecnico.rut,
            'total_asignadas': solicitudes_asignadas,
            'activas': solicitudes_activas,
            'completadas': solicitudes_completadas,
            'carga_actual': solicitudes_activas
        })
    
    # Ordenar por carga actual (menor a mayor)
    tecnicos_stats.sort(key=lambda x: x['carga_actual'])
    
    # Estadísticas generales
    total_solicitudes = SolicitudServicio.objects.count()
    solicitudes_pendientes = SolicitudServicio.objects.filter(ruttec__isnull=True, estadosol='Pendiente').count()
    solicitudes_activas = SolicitudServicio.objects.filter(estadosol__in=['Aceptada', 'Asignada', 'Modificada']).count()
    solicitudes_completadas = SolicitudServicio.objects.filter(estadosol='Cerrado').count()
    
    context = {
        'tecnicos_stats': tecnicos_stats,
        'total_solicitudes': total_solicitudes,
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_activas': solicitudes_activas,
        'solicitudes_completadas': solicitudes_completadas,
        'active_page': 'dashboard_tecnicos'
    }
    
    return render(request, 'core/dashboard_tecnicos.html', context)

@login_required
def probar_compra_directa(request, producto_id):
    """
    Vista para probar el guardado de compra directamente en la BD
    sin pasar por WebPay. Solo para testing/debugging.
    """
    try:
        # Obtener el perfil del usuario
        perfil = PerfilUsuario.objects.get(user=request.user)
        
        # Llamar a la función auxiliar
        resultado = guardar_compra_en_bd(producto_id, perfil)
        
        if resultado['success']:
            context = {
                'mensaje': 'Compra guardada exitosamente',
                'factura': resultado['factura'],
                'guia_despacho': resultado['guia_despacho'],
                'solicitud_creada': resultado['solicitud_creada'],
                'success': True
            }
            
            # Si se creó una solicitud, agregar sus detalles al contexto
            if resultado['solicitud_creada']:
                # Buscar la solicitud creada para esta factura
                solicitud = SolicitudServicio.objects.filter(nrofac=resultado['factura']).first()
                if solicitud:
                    context['solicitud'] = solicitud
        else:
            context = {
                'mensaje': f'Error al guardar compra: {resultado["error"]}',
                'success': False
            }
            
    except Exception as e:
        context = {
            'mensaje': f'Error: {str(e)}',
            'success': False
        }
    
    return render(request, "core/resultado_compra.html", context)
    