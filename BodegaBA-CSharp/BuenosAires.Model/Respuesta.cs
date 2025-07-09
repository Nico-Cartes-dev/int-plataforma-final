using System;
using System.Runtime.Serialization;

namespace BuenosAires.Model
{
    [DataContract]
    [Serializable]
    public class Respuesta
    {
        [DataMember]
        public string Accion { get; set; }
        [DataMember]
        public string Mensaje { get; set; }
        [DataMember]
        public bool HayErrores { get; set; }
        [DataMember]
        public string XmlFactura { get; set; }
        [DataMember]
        public string XmlListaFactura { get; set; }
        [DataMember]
        public string XmlGuiaDespacho { get; set; }
        [DataMember]
        public string XmlListaGuiaDespacho { get; set; }
        [DataMember]
        public string XmlPerfilUsuario { get; set; }
        [DataMember]
        public string XmlListaPerfilUsuario { get; set; }
        [DataMember]
        public string XmlProducto { get; set; }
        [DataMember]
        public string XmlListaProducto { get; set; }
        [DataMember]
        public string XmlSolicitudServicio { get; set; }
        [DataMember]
        public string XmlListaSolicitudServicio { get; set; }
        [DataMember]
        public string XmlStockProducto { get; set; }
        [DataMember]
        public string XmlListaStockProducto { get; set; }
        [DataMember]
        public string JsonProducto { get; set; }
        [DataMember]
        public string JsonListaProducto { get; set; }
        [DataMember]
        public string JsonAutenticado { get; set; }
        [DataMember]
        public string XmlAnwoStockProducto { get; set; }
        [DataMember]
        public string XmlListaAnwoStockProducto { get; set; }
        [DataMember]
        public string JsonStockProducto { get; set; }

        [DataMember]
        public string JsonListaStockAnwo { get; set; }

    }
}