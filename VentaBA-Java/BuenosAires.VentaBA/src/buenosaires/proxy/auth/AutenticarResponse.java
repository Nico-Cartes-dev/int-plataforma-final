
package buenosaires.proxy.auth;

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
 *         &lt;element name="AutenticarResult" type="{http://schemas.datacontract.org/2004/07/BuenosAires.Model}Respuesta" minOccurs="0"/>
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
    "autenticarResult"
})
@XmlRootElement(name = "AutenticarResponse")
public class AutenticarResponse {

    @XmlElementRef(name = "AutenticarResult", namespace = "http://tempuri.org/", type = JAXBElement.class, required = false)
    protected JAXBElement<Respuesta> autenticarResult;

    /**
     * Obtiene el valor de la propiedad autenticarResult.
     * 
     * @return
     *     possible object is
     *     {@link JAXBElement }{@code <}{@link Respuesta }{@code >}
     *     
     */
    public JAXBElement<Respuesta> getAutenticarResult() {
        return autenticarResult;
    }

    /**
     * Define el valor de la propiedad autenticarResult.
     * 
     * @param value
     *     allowed object is
     *     {@link JAXBElement }{@code <}{@link Respuesta }{@code >}
     *     
     */
    public void setAutenticarResult(JAXBElement<Respuesta> value) {
        this.autenticarResult = value;
    }

}
