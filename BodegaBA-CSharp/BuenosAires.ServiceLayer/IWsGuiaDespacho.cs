using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;
using BuenosAires.Model;

namespace BuenosAires.ServiceLayer
{
    [ServiceContract]
    public interface IWsGuiaDespacho
    {
        [OperationContract]
        Respuesta ConsultarGuiasDespacho();

        [OperationContract]
        Respuesta ActualizarEstadoGuiaDespacho(int p_nrogd, string p_nuevo_estado);
    }
}