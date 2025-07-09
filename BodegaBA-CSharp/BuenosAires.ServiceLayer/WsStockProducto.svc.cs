using System;
using System.Net.Http;
using BuenosAires.Model.Utiles;
using BuenosAires.Model;
using BuenosAires.BusinessLayer;



namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de clase "WsStockProducto" en el código, en svc y en el archivo de configuración a la vez.
    // NOTA: para iniciar el Cliente de prueba WCF para probar este servicio, seleccione WsStockProducto.svc o WsStockProducto.svc.cs en el Explorador de soluciones e inicie la depuración.
    public class WsStockProducto : IWsStockProducto
    {
        public Respuesta ObtenerEquiposEnBodega()
        {
            var resp = new Respuesta();
            resp.Accion = "obtener equipos en bodega";
            resp.Mensaje = "";
            resp.HayErrores = false;
            resp.JsonAutenticado = "";

            string apiUrl = "http://127.0.0.1:8001/BuenosAiresApiRest/obtener_equipos_en_bodega";

            try
            {
                using (HttpClient client = new HttpClient() ) 
                {
                    HttpResponseMessage response = client.GetAsync(apiUrl).Result;
                    if (response.IsSuccessStatusCode)
                    {
                        resp.JsonStockProducto = response.Content.ReadAsStringAsync().Result;
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = "No fue Posible " + resp.Accion + ", intente nuevamente más tarde " +
                            "o comuniquese con el Administrador del Sistema";
                    }
                    return resp;
                }
            }
            catch (Exception ex)
            {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsStockProducto.ObtenerEquiposEnBodega", ex);
                return resp;
            }
        }


    }
}
