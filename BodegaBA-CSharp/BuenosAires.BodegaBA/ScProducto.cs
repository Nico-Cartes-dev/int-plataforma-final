//using system.collections.generic;
//using buenosaires.model.utiles;
//using buenosaires.model;
//using system;
////using buenosaires.bodegaba.wsproductoreference;

//namespace buenosaires.serviceproxy
//{
//    public class scproducto
//    {
//        public string accion = "";
//        public string mensaje = "";
//        public bool hayerrores = false;
//        public producto producto = null;
//        public list<producto> lista = null;

//        public void copiarpropiedades(respuesta resp)
//        {
//            this.accion = resp.accion;
//            this.mensaje = resp.mensaje;
//            this.hayerrores = resp.hayerrores;
//            this.producto = util.deserializarxml<producto>(resp.xmlproducto);
//            this.lista = util.deserializarxml<list<producto>>(resp.xmllistaproducto);
//        }

//        public wsproductoclient getws()
//        {
//            var ws = new wsproductoclient();
//            ws.innerchannel.operationtimeout = new timespan(1, 0, 0);
//            return ws;
//        }

//        public void crear(producto producto)
//        {
//            copiarpropiedades(getws().crear(producto));
//        }

//        public void leertodos()
//        {
//            copiarpropiedades(getws().leertodos());
//        }

//        public void leer(int id)
//        {
//            copiarpropiedades(getws().leer(id));
//        }

//        public void actualizar(producto producto)
//        {
//            copiarpropiedades(getws().actualizar(producto));
//        }

//        public void eliminar(int id)
//        {
//            copiarpropiedades(getws().eliminar(id));
//        }
//    }
//}
