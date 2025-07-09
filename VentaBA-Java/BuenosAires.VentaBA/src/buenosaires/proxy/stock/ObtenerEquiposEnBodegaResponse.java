
package buenosaires.proxy.stock;

import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElementRef;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Clase Java para anonymous complex type.
 * 
 * <p>El siguiente fragmento de esquema especifica el contenido que se espera que haya en esta clase.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="ObtenerEquiposEnBodegaResult" type="{http://schemas.datacontract.org/2004/07/BuenosAires.Model}Respuesta" minOccurs="0"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "obtenerEquiposEnBodegaResult"
})
@XmlRootElement(name = "ObtenerEquiposEnBodegaResponse")
public class ObtenerEquiposEnBodegaResponse {

    @XmlElementRef(name = "ObtenerEquiposEnBodegaResult", namespace = "http://tempuri.org/", type = JAXBElement.class, required = false)
    protected JAXBElement<Respuesta> obtenerEquiposEnBodegaResult;

    /**
     * Obtiene el valor de la propiedad obtenerEquiposEnBodegaResult.
     * 
     * @return
     *     possible object is
     *     {@link JAXBElement }{@code <}{@link Respuesta }{@code >}
     *     
     */
    public JAXBElement<Respuesta> getObtenerEquiposEnBodegaResult() {
        return obtenerEquiposEnBodegaResult;
    }

    /**
     * Define el valor de la propiedad obtenerEquiposEnBodegaResult.
     * 
     * @param value
     *     allowed object is
     *     {@link JAXBElement }{@code <}{@link Respuesta }{@code >}
     *     
     */
    public void setObtenerEquiposEnBodegaResult(JAXBElement<Respuesta> value) {
        this.obtenerEquiposEnBodegaResult = value;
    }

}
