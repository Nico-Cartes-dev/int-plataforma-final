using BuenosAires.Model;
using BuenosAires.Model.Utiles;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;
using System.Net.Http;
using System.Threading.Tasks;

namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de clase "WsAnwo" en el código, en svc y en el archivo de configuración a la vez.
    // NOTA: para iniciar el Cliente de prueba WCF para probar este servicio, seleccione WsAnwo.svc o WsAnwo.svc.cs en el Explorador de soluciones e inicie la depuración.
    public class WsAnwo : IWsAnwo
    {
        public Respuesta Consultar_productos_disponibles()
        {
            var resp = new Respuesta();
            resp.Accion = "Obtener equipos Anwo";
            resp.Mensaje = "";
            resp.HayErrores = false;
            //resp.JsonAutenticado = "";

            string apiUrl = "http://127.0.0.1:5000/consultar_productos_disponibles";


            try
            {
                using (HttpClient client = new HttpClient())
                {
                    HttpResponseMessage response = client.GetAsync(apiUrl).Result;
                    if (response.IsSuccessStatusCode)
                    {
                        resp.JsonListaStockAnwo = response.Content.ReadAsStringAsync().Result;
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
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsAnwo.Consultar_productos_disponibles", ex);
                return resp;
            }
        }

        public Respuesta reservar_equipo_anwo(string nroserieanwo, char charReservado)
        {
            var resp = new Respuesta();
            resp.Accion = "Reservar equipo Anwo: ";
            resp.Mensaje = "";
            resp.HayErrores = false;

            string apiUrl = "http://127.0.0.1:5000/reservar_equipo_anwo";// + $"{nroserieanwo}/{charReserva}";

            try
            {
                using (HttpClient client = new HttpClient())
                {
                    var json = $"{{ \"nroserieanwo\": \"{nroserieanwo}\", \"reservado\": \"{charReservado}\" }}";
                    //var json = $"{{ \"nroserieanwo\": \"{nroserieanwo}\", \"reservado\": \"{charReservado}\" }}";
                    var content = new StringContent(json, Encoding.UTF8, "application/json");
                    HttpResponseMessage response = client.PostAsync(apiUrl, content).Result;
                    if (response.IsSuccessStatusCode)
                    {
                        resp.JsonListaStockAnwo = response.Content.ReadAsStringAsync().Result;
                        resp.Mensaje = $"Se reservó el equipo {nroserieanwo}";
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = "No fue posible " + resp.Accion + nroserieanwo + ", intente nuevamente más tarde " +
                            "o comuníquese con el Administrador del Sistema";
                    }

                    return resp;
                }
            }
            catch (Exception ex)
            {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(resp.Accion, "WsAnwo.reservar_equipo_anwo", ex);
                return resp;
            }
        }
    }
}
