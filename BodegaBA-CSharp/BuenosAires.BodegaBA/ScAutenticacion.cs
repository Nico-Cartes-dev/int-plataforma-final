using System.Collections.Generic;
using BuenosAires.Model.Utiles;
using BuenosAires.Model;
using System;
using BuenosAires.BodegaBA.WsAutenticacionReference;
using Newtonsoft.Json;


namespace BuenosAires.ServiceProxy
{
    public class ScAutenticacion
    {
        public class RespuestaAutenticacion
        {
            public bool Autenticado { get; set; }
            public string NombreUsuario { get; set; }
            public string TipoUsuario { get; set; }
            public string Mensaje { get; set; }
        }


        public string Accion = "";
        public string Mensaje = "";
        public bool HayErrores = false;
        public string JsonAutenticado = "";
        public bool Autenticado = false;
        public string NombreUsuario = "";
        public string TipoUsuario = "";


        public void CopiarPropiedades(Respuesta resp)
        {
            this.Accion = resp.Accion;
            this.Mensaje = resp.Mensaje;
            this.HayErrores = resp.HayErrores;
            this.JsonAutenticado = resp.JsonAutenticado;
            this.Autenticado = false;
            this.NombreUsuario = "";
            this.TipoUsuario = "";


            if (resp.JsonAutenticado != "")
            {
                RespuestaAutenticacion respAutenticacion =
                    JsonConvert.DeserializeObject<RespuestaAutenticacion>(resp.JsonAutenticado);
                this.Autenticado = respAutenticacion.Autenticado;
                this.NombreUsuario = respAutenticacion.NombreUsuario;
                this.TipoUsuario = respAutenticacion.TipoUsuario;
                this.Mensaje = respAutenticacion.Mensaje;
            }
        }


        public WsAutenticacionClient GetWs()
        {
            var ws = new WsAutenticacionClient("BasicHttpBinding_IWsAutenticacion1");
            ws.InnerChannel.OperationTimeout = new TimeSpan(1, 0, 0);
            return ws;
        }


        public void Autenticar(string tipousu, string username, string password)
        {
            CopiarPropiedades(GetWs().Autenticar(tipousu, username, password));
        }
    }
}
