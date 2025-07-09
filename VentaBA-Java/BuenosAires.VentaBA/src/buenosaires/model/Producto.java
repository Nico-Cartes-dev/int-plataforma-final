package buenosaires.model;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement(name = "Producto")
public class Producto {
    private int idprod;
    private String nomprod;
    private String descprod;
    private int precio;


    public int getIdprod() {
        return idprod;
    }

    @XmlElement(name = "idprod")
    public void setIdprod(int idprod) {
        this.idprod = idprod;
    }

    public String getNomprod() {
        return nomprod;
    }

    @XmlElement(name = "nomprod")
    public void setNomprod(String nomprod) {
        this.nomprod = nomprod;
    }

    public String getDescprod() {
        return descprod;
    }

    @XmlElement(name = "descprod")
    public void setDescprod(String descprod) {
        this.descprod = descprod;
    }

    public int getPrecio() {
        return precio;
    }

    @XmlElement(name = "precio")
    public void setPrecio(int precio) {
        this.precio = precio;
    }


}
