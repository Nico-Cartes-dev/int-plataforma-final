using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using BuenosAires.DataLayer;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;

namespace BuenosAires.BusinessLayer
{
    public  class BcProducto
    {
        public string Accion = "";
        public string Mensaje = "";
        public bool HayErrores = false;
        public Producto Producto = null;
        public List<Producto> Lista = null;


        public BcProducto()
        {
            Inicializar("");
        }

        public void Inicializar(string accion)
        {
            this.Accion = accion;
            this.Mensaje = "";
            this.HayErrores = false;
            this.Producto = null;
            this.Lista = null;
        }
        private bool ErrCampoRequerido (string nombreCampo)
        {
            this.Mensaje = $"{nombreCampo} es un campo requerido por ello necesita un valor";
            return false;
        }
        private bool ErrPrecio()
        {
            this.Mensaje = "El precio debe ser un número entero mayor a 0";
            return false;
        }
        private bool ErrID()
        {
            this.Mensaje = "Cuando el producto es nuevo el campo ID deve vale cero.";
            return false;
        }
        private bool RetornarError(string mensaje)
        {
            this.HayErrores=true;
            this.Mensaje = mensaje;
            return false; 
        }
        private bool RetornarMensaja(string mensaje)
        {
            this.Mensaje = mensaje;
            return false;
        }
        public bool ValidarProducto(Producto producto)
        {
            this.HayErrores = true;
            if(producto.idprod < 0) return ErrID();
            if (producto.nomprod.Trim() == "") return ErrCampoRequerido("Nombre del producto");
            if (producto.descprod.Trim() == "") return ErrCampoRequerido("Descripció del producto");
            if (producto.precio <= 0) return ErrPrecio();
            if (producto.imagen.Trim() == "") return ErrCampoRequerido("Imagen del producto");
            this.HayErrores = false;
            return true;

            
        }   
        public void Crear (Producto producto)
        {
            if (ValidarProducto(producto) == false) return;
            var dc = new DcProducto();
            dc.Crear(producto);
            Util.CopiarPropiedades(dc, this);

        }
        public void LeerTodos()
        {
            var dc = new DcProducto();
            dc.LeerTodos();
            Util.CopiarPropiedades(dc, this);
        }
        public void leer(int id)
        {
            var dc = new DcProducto();
            dc.Leer(id);
            Util.CopiarPropiedades(dc, this);
        }
        public void Actualizar(Producto producto)
        {
            if (ValidarProducto(producto) == false) return;
            var dc = new DcProducto();     
            dc.Actualizar(producto);
            Util.CopiarPropiedades(dc, this);

        } 
        public bool Eliminar (int id)
        {
            this.Inicializar($"eliminar el producto con el id {id}"); ;


            /*
            *   Se debe verificar que el producto que se desea eliminar 
            *   no este asociado con otras tablas del sistema, por lo tanto se 
            *   debe verificar que este producto no tenga:
            *   -(dcStockProducto)  unidades de producto en la bodega
            *   -(DcFactura)        Facturas en las que haya sidop vendido
            *   -(DcGuiaDespacho)   Guias de despacho con las que ha sido trasladado el cliente
            *   -(DcSolicitudServicio) Solicitudes de servicio de ningún técnico 
            *   
            *   (para evitar datos huerfanos)
            */

            var dcprod = new DcProducto();
            dcprod.Eliminar(id);
            if (dcprod.HayErrores) return RetornarError(dcprod.Mensaje);
            Util.CopiarPropiedades(dcprod, this);
            return true;
        }

    }                              
}
