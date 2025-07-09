using BuenosAires.BusinessLayer;
using BuenosAires.Model.Utiles;
using BuenosAires.Model;

namespace BuenosAires.ServiceLayer
{
    public class WsProducto : IWsProducto
    {
        private Respuesta ObtenerRespuesta(BcProducto bc)
        {
            var respuesta = new Respuesta();
            respuesta.Accion = bc.Accion;
            respuesta.Mensaje = bc.Mensaje;
            respuesta.HayErrores = bc.HayErrores;
            respuesta.XmlProducto = Util.SerializarXML(bc.Producto);
            respuesta.XmlListaProducto = Util.SerializarXML(bc.Lista);
            return respuesta;
        }

        public Respuesta Crear(Producto producto)
        {
            var bc = new BcProducto();
            bc.Crear(producto);
            return ObtenerRespuesta(bc);
        }

        public Respuesta LeerTodos()
        {
            var bc = new BcProducto();
            bc.LeerTodos();
            return ObtenerRespuesta(bc);
        }

        public Respuesta Leer(int id)
        {
            var bc = new BcProducto();
            bc.leer(id);
            return ObtenerRespuesta(bc);
        }

        public Respuesta Actualizar(Producto producto)
        {
            var bc = new BcProducto();
            bc.Actualizar(producto);
            return ObtenerRespuesta(bc);
        }

        public Respuesta Eliminar(int id)
        {
            var bc = new BcProducto();
            bc.Eliminar(id);
            return ObtenerRespuesta(bc);
        }
    }
}
