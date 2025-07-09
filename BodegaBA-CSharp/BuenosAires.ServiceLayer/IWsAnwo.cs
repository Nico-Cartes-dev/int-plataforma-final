using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;

using BuenosAires.Model;

namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de interfaz "IWsAnwo" en el código y en el archivo de configuración a la vez.
    [ServiceContract]
    public interface IWsAnwo
    {
        [OperationContract]
        Respuesta Consultar_productos_disponibles();

        [OperationContract]
        Respuesta reservar_equipo_anwo(string nroserieanwo, char charReservado);
        //Respuesta reservar_equipo_anwo(string nroserieanwo, string charReservado);
    }
}
