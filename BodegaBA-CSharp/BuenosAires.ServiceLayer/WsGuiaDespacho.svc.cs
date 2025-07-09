using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;
using System.Net.Http;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;

namespace BuenosAires.ServiceLayer
{
    public class WsGuiaDespacho : IWsGuiaDespacho
    {
        private const string BaseUrl = "http://127.0.0.1:8001/BuenosAiresApiRest/";

        public Respuesta ConsultarGuiasDespacho()
        {
            var resp = new Respuesta
            {
                Accion = "consultar guías",
                Mensaje = "",
                HayErrores = false
            };

            string apiUrl = BaseUrl + "guias-despacho/";

            try
            {
                // Usando el using clásico para C# 7.3
                using (var client = new HttpClient())
                {
                    HttpResponseMessage r = client.GetAsync(apiUrl).Result;
                    if (r.IsSuccessStatusCode)
                    {
                        // JsonStockProducto está definido en Respuesta
                        resp.JsonStockProducto = r.Content.ReadAsStringAsync().Result;
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = $"No fue posible {resp.Accion}, status {r.StatusCode}";
                    }
                }
            }
            catch (Exception ex)
            {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(
                    resp.Accion,
                    "WsGuiaDespacho.ConsultarGuiasDespacho",
                    ex
                );
            }

            return resp;
        }

        public Respuesta ActualizarEstadoGuiaDespacho(int p_nrogd, string p_nuevo_estado)
        {
            var resp = new Respuesta
            {
                Accion = "actualizar estado guía",
                Mensaje = "",
                HayErrores = false
            };

            string apiUrl = $"{BaseUrl}actualizar_guia/{p_nrogd}/{p_nuevo_estado}/";

            try
            {
                using (var client = new HttpClient())
                {
                    HttpResponseMessage r = client.GetAsync(apiUrl).Result;
                    if (r.IsSuccessStatusCode)
                    {
                        resp.JsonStockProducto = r.Content.ReadAsStringAsync().Result;
                    }
                    else
                    {
                        resp.HayErrores = true;
                        resp.Mensaje = $"No fue posible {resp.Accion}, status {r.StatusCode}";
                    }
                }
            }
            catch (Exception ex)
            {
                resp.HayErrores = true;
                resp.Mensaje = Util.MensajeError(
                    resp.Accion,
                    "WsGuiaDespacho.ActualizarEstadoGuiaDespacho",
                    ex
                );
            }

            return resp;
        }
    }
}