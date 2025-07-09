from django import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import (
    home, administrar_productos, tienda, ficha, iniciar_sesion,
    registrar_usuario, cerrar_sesion, perfil_usuario, iniciar_pago,
    pago_exitoso, obtener_solicitudes_de_servicio, mis_compras,
     facturas, ingresar_solicitud_servicio, aceptar_solicitud,
    modificar_solicitud, cerrar_solicitud
)

urlpatterns = [
    # General URLs
    path('', home, name="home"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    path('perfil_usuario/', perfil_usuario, name="perfil_usuario"),
    
    # Password management
    path('cambiar_password/', 
         auth_views.PasswordChangeView.as_view(
             template_name='core/cambiar_password.html',
             success_url='/password_cambiada'
         ),
         name='cambiar_password'),
    path('password_cambiada/',
         TemplateView.as_view(template_name='core/password_cambiada.html'),
         name='password_cambiada'),

    # Shop related
    path('tienda/', tienda, name="tienda"),
    path('ficha/<int:id>', ficha, name="ficha"),
    path('iniciar_pago/<int:id>', iniciar_pago, name="iniciar_pago"),
    path('pago_exitoso/', pago_exitoso, name="pago_exitoso"),
    
    # Product management
    path('administrar_productos/<action>/<id>',
         administrar_productos,
         name="administrar_productos"),

    # Cliente views
    path('mis-compras/', mis_compras, name='mis_compras'),
#     path('mis-solicitudes/', mis_solicitudes, name='mis_solicitudes'),
    
    # Técnico and Administrador views
    path('solicitudes/', obtener_solicitudes_de_servicio, 
         name='obtener_solicitudes'),  # Short name for template usage
    path('solicitudes-servicio/', obtener_solicitudes_de_servicio, 
         name='obtener_solicitudes_de_servicio'),  # Original name

     path('aceptar_solicitud/<int:nrosol>/', aceptar_solicitud, name='aceptar_solicitud'),
     path('modificar_solicitud/<int:nrosol>/', modificar_solicitud, name='modificar_solicitud'),
     path('cerrar_solicitud/<int:nrosol>/', cerrar_solicitud, name='cerrar_solicitud'),
    
    # Administrador views
    path('facturas/', facturas, name='facturas'),  # For admin to see all invoices
    
    path('ingresar_solicitud_servicio/', ingresar_solicitud_servicio, name='ingresar_solicitud_servicio'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
