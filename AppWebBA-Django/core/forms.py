from django import forms
from django.forms import ModelForm, fields, Form
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, PerfilUsuario

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['idprod', 'nomprod', 'descprod', 'precio', 'imagen']

class IniciarSesionForm(Form):
    username = forms.CharField(widget=forms.TextInput(), label="Correo")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    class Meta:
        fields = ['username', 'password']

class RegistrarUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label='Nombre')
    last_name = forms.CharField(max_length=100, required=True, label='Apellido')
    email = forms.EmailField(required=True, label='Email')
    rut = forms.CharField(max_length=12, required=True, label='RUT')
    dirusu = forms.CharField(max_length=200, required=True, label='Dirección')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rut', 'dirusu')

class PerfilUsuarioForm(Form):
    first_name = forms.CharField(max_length=150, required=True, label="Nombres")
    last_name = forms.CharField(max_length=150, required=True, label="Apellidos")
    email = forms.CharField(max_length=254, required=True, label="Correo")
    rut = forms.CharField(max_length=20, required=False, label="Rut")
    tipousu = forms.CharField(
        max_length=50,
        required=True,
        label="Tipo de usuario",
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    dirusu = forms.CharField(max_length=300, required=False, label="Dirección")

    class Meta:
        fields = '__all__'

class SolicitudServicioForm(forms.Form):
    TIPO_SOLICITUD_CHOICES = [
        ('Mantención', 'Mantención'),
        ('Reparación', 'Reparación'),
    ]
    tipo_solicitud = forms.ChoiceField(choices=TIPO_SOLICITUD_CHOICES, label="Tipo de Solicitud")
    descripcion = forms.CharField(widget=forms.Textarea, label="Descripción")
    fecha_sugerida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Fecha Sugerida")
    hora_sugerida = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Hora Sugerida")

