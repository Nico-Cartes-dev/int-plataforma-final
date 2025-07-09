package buenosaires.proxy.stock;

import java.util.List;
import java.util.Map;
import javax.xml.ws.BindingProvider;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.Unmarshaller;
import java.io.StringReader;

import buenosaires.model.ListaProducto;
import buenosaires.model.Producto;

/**
 * Cliente wrapper para el Web Service WsStockProducto.
 * Invoca el método ObtenerEquiposEnBodega y parsea el XML de respuesta
 * a una List<Producto> usando las clases JAXB de tu modelo.
 */
public class ScStockProducto {
    public String Accion = "";
    public String Mensaje = "";
    public boolean HayErrores = false;
    public List<Producto> Lista = null;

    private final IWsStockProducto port;

    public ScStockProducto() {
        // Crear el stub del servicio y configurar timeout
        WsStockProducto service = new WsStockProducto();
        port = service.getBasicHttpBindingIWsStockProducto();
        Map<String, Object> ctx = ((BindingProvider) port).getRequestContext();
        ctx.put("com.sun.xml.ws.request.timeout", 60000);
        ctx.put("com.sun.xml.ws.connect.timeout", 60000);
    }

    private void copiarPropiedades(Respuesta resp) throws Exception {
        // Extraer los campos simples
        Accion     = resp.getAccion().getValue();
        Mensaje    = resp.getMensaje().getValue();
        HayErrores = resp.isHayErrores().booleanValue();

        // Obtener el XML que contiene la lista de productos
        String xmlLista = resp.getXmlListaStockProducto().getValue();

        // Parsear ese XML a ListaProducto con JAXB
        JAXBContext  jctx = JAXBContext.newInstance(ListaProducto.class);
        Unmarshaller un  = jctx.createUnmarshaller();
        StringReader reader = new StringReader(xmlLista);
        ListaProducto contenedor = (ListaProducto) un.unmarshal(reader);

        // Guardar la lista de Producto
        Lista = contenedor.getProductos();
    }

    /**
     * Ejecuta la operación ObtenerEquiposEnBodega del WS
     * y llena los campos Accion, Mensaje, HayErrores y Lista.
     */
    public void LeerTodos() {
        try {
            // Invocar el método tal cual aparece en tu IWsStockProducto
            Respuesta resp = port.obtenerEquiposEnBodega();
            copiarPropiedades(resp);
        } catch (Exception ex) {
            HayErrores = true;
            Mensaje    = "Error invocando WsStockProducto: " + ex.getMessage();
        }
    }
}
