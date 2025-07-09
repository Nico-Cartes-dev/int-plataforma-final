using System;
using System.Net.Http;
using BuenosAires.Model.Utiles;
using BuenosAires.Model;

namespace BuenosAires.ServiceLayer
{
    public class WsAutenticacion : IWsAutenticacion
    {
        public Respuesta Autenticar(string tipousu, string username, string password)
        {
            var resp = new Respuesta();
            resp.Accion = "autenticar al usuario";
            resp.Mensaje = "";
            resp.HayErrores = false;
            resp.JsonAutenticado = "";

            if (username.Trim() == "") username = "no-fue-digitado-el-username";
            if (password.Trim() == "") password = "no-fue-digitada-la-password";

            string apiUrl = "http://127.0.0.1:8001/BuenosAiresApiRest/autenticar/" + tipousu + "/" + username + "/" + password;

            try
            {
                using (HttpClient client = new HttpClient())
                {
                    HttpResponseMessage response = client.GetAsync(apiUrl).Result;
                    if (response.IsSuccessStatusCode)
                    {
                        resp.JsonAutenticado = response.Content.ReadAsStringAsync().Result;
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = "No fue posible autenticar al usuario, intente nuevamente más tarde "
                            + "o comuníquese con el Administrador del Sistema";
                    }
                    return resp;
                }
            }
            catch (Exception ex)
            {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsAutenticacion.Autenticar", ex);
                return resp;
            }
        }
    }
}