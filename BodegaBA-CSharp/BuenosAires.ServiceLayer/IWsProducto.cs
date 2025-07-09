using BuenosAires.Model;
using System.ServiceModel;

namespace BuenosAires.ServiceLayer
{
    [ServiceContract]
    public interface IWsProducto
    {
        [OperationContract]
        Respuesta Crear(Producto producto);

        [OperationContract]
        Respuesta LeerTodos();

        [OperationContract]
        Respuesta Leer(int id);

        [OperationContract]
        Respuesta Actualizar(Producto producto);

        [OperationContract]
        Respuesta Eliminar(int id);
    }
}