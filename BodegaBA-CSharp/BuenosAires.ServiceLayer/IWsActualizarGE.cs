using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.ServiceModel;
using System.Text;

namespace BuenosAires.ServiceLayer
{
    // NOTA: puede usar el comando "Rename" del menú "Refactorizar" para cambiar el nombre de interfaz "IWsActualizarGE" en el código y en el archivo de configuración a la vez.
    [ServiceContract]
    public interface IWsActualizarGE
    {
        [OperationContract]
        void DoWork();
    }
}
