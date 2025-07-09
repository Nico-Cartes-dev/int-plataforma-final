package buenosaires.proxy.auth;

import buenosaires.proxy.auth.IWsAutenticacion;
import buenosaires.proxy.auth.Respuesta;
import buenosaires.proxy.auth.WsAutenticacion;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

public class ScAutenticacion {
    
    private boolean autenticado;
    private String nombreUsuario;
    private String tipoUsuario;
    private String mensaje;

    public ScAutenticacion() {
        this.autenticado = false;
        this.nombreUsuario = "";
        this.tipoUsuario = "";
        this.mensaje = "";
    }

    public boolean isAutenticado() {
        return autenticado;
    }

    public void setAutenticado(boolean autenticado) {
        this.autenticado = autenticado;
    }

    public String getNombreUsuario() {
        return nombreUsuario;
    }

    public void setNombreUsuario(String nombreUsuario) {
        this.nombreUsuario = nombreUsuario;
    }

    public String getTipoUsuario() {
        return tipoUsuario;
    }

    public void setTipoUsuario(String tipoUsuario) {
        this.tipoUsuario = tipoUsuario;
    }

    public String getMensaje() {
        return mensaje;
    }

    public void setMensaje(String mensaje) {
        this.mensaje = mensaje;
    }
    
    public void ejecutarPruebas() {
        //Acceder al Web Service
        WsAutenticacion ws = new WsAutenticacion();
        IWsAutenticacion port = ws.getBasicHttpBindingIWsAutenticacion();
        
        // Probar con una cuenta de Vendedor
        Respuesta resp1 = port.autenticar("Vendedor", "bgates", "123");
        String json1 = resp1.getJsonAutenticado().getValue();
        System.out.println(json1);
        
        // Probar con una cuenta de Administrador
        Respuesta resp2 = port.autenticar("Administrador", "emusk", "123");
        String json2 = resp2.getJsonAutenticado().getValue();
        System.out.println(json2);
        
        // Probar con una cuenta de Bodeguero
        Respuesta resp3 = port.autenticar("Bodeguero", "emusk", "123");
        String json3 = resp3.getJsonAutenticado().getValue();
        System.out.println(json3);
        
        //Probar ScAutenticacion
        var bc = new ScAutenticacion();
        bc.autenticar("Vendedor", "bgates", "123");
        System.out.println(bc.toString());
    }
    
    public void autenticar(String tipousu, String username, String password) {
        var ws = new WsAutenticacion();
        var port = ws.getBasicHttpBindingIWsAutenticacion();
        Respuesta resp = port.autenticar(tipousu, username, password);
        String jsonAutenticado = resp.getJsonAutenticado().getValue();
        Object jsonObject = JSONValue.parse(jsonAutenticado);
        JSONObject jsonAutenticacion = (JSONObject) jsonObject;
        this.setAutenticado((Boolean)jsonAutenticacion.get("Autenticado"));
        this.setNombreUsuario((String)jsonAutenticacion.get("NombreUsuario"));
        this.setTipoUsuario((String)jsonAutenticacion.get("TipoUsuario"));
        this.setMensaje((String)jsonAutenticacion.get("Mensaje"));
    }

    @Override
    public String toString() {
        return "ScAutenticacion{" 
                + "autenticado=" + autenticado 
                + ", nombreUsuario=" + nombreUsuario 
                + ", tipoUsuario=" + tipoUsuario 
                + ", mensaje=" + mensaje + '}';
    }
}