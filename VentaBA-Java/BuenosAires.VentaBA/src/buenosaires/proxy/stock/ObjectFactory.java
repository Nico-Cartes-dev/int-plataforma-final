
package buenosaires.proxy.stock;

import java.math.BigDecimal;
import java.math.BigInteger;
import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlElementDecl;
import javax.xml.bind.annotation.XmlRegistry;
import javax.xml.datatype.Duration;
import javax.xml.datatype.XMLGregorianCalendar;
import javax.xml.namespace.QName;


/**
 * This object contains factory methods for each 
 * Java content interface and Java element interface 
 * generated in the buenosaires.proxy.stock package. 
 * <p>An ObjectFactory allows you to programatically 
 * construct new instances of the Java representation 
 * for XML content. The Java representation of XML 
 * content can consist of schema derived interfaces 
 * and classes representing the binding of schema 
 * type definitions, element declarations and model 
 * groups.  Factory methods for each of these are 
 * provided in this class.
 * 
 */
@XmlRegistry
public class ObjectFactory {

    private final static QName _UnsignedLong_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "unsignedLong");
    private final static QName _UnsignedByte_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "unsignedByte");
    private final static QName _UnsignedInt_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "unsignedInt");
    private final static QName _Char_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "char");
    private final static QName _Short_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "short");
    private final static QName _Guid_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "guid");
    private final static QName _UnsignedShort_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "unsignedShort");
    private final static QName _Decimal_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "decimal");
    private final static QName _Boolean_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "boolean");
    private final static QName _Duration_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "duration");
    private final static QName _Respuesta_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "Respuesta");
    private final static QName _Base64Binary_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "base64Binary");
    private final static QName _Int_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "int");
    private final static QName _Long_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "long");
    private final static QName _AnyURI_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "anyURI");
    private final static QName _Float_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "float");
    private final static QName _DateTime_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "dateTime");
    private final static QName _Byte_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "byte");
    private final static QName _Double_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "double");
    private final static QName _QName_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "QName");
    private final static QName _AnyType_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "anyType");
    private final static QName _String_QNAME = new QName("http://schemas.microsoft.com/2003/10/Serialization/", "string");
    private final static QName _ObtenerEquiposEnBodegaResponseObtenerEquiposEnBodegaResult_QNAME = new QName("http://tempuri.org/", "ObtenerEquiposEnBodegaResult");
    private final static QName _RespuestaMensaje_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "Mensaje");
    private final static QName _RespuestaXmlAnwoStockProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlAnwoStockProducto");
    private final static QName _RespuestaXmlListaPerfilUsuario_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaPerfilUsuario");
    private final static QName _RespuestaXmlListaSolicitudServicio_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaSolicitudServicio");
    private final static QName _RespuestaXmlFactura_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlFactura");
    private final static QName _RespuestaAccion_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "Accion");
    private final static QName _RespuestaXmlListaStockProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaStockProducto");
    private final static QName _RespuestaXmlPerfilUsuario_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlPerfilUsuario");
    private final static QName _RespuestaXmlListaFactura_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaFactura");
    private final static QName _RespuestaXmlStockProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlStockProducto");
    private final static QName _RespuestaJsonListaProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "JsonListaProducto");
    private final static QName _RespuestaXmlGuiaDespacho_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlGuiaDespacho");
    private final static QName _RespuestaXmlListaProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaProducto");
    private final static QName _RespuestaXmlProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlProducto");
    private final static QName _RespuestaJsonListaStockAnwo_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "JsonListaStockAnwo");
    private final static QName _RespuestaJsonStockProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "JsonStockProducto");
    private final static QName _RespuestaJsonProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "JsonProducto");
    private final static QName _RespuestaXmlListaAnwoStockProducto_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaAnwoStockProducto");
    private final static QName _RespuestaXmlListaGuiaDespacho_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlListaGuiaDespacho");
    private final static QName _RespuestaXmlSolicitudServicio_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "XmlSolicitudServicio");
    private final static QName _RespuestaJsonAutenticado_QNAME = new QName("http://schemas.datacontract.org/2004/07/BuenosAires.Model", "JsonAutenticado");

    /**
     * Create a new ObjectFactory that can be used to create new instances of schema derived classes for package: buenosaires.proxy.stock
     * 
     */
    public ObjectFactory() {
    }

    /**
     * Create an instance of {@link ObtenerEquiposEnBodega }
     * 
     */
    public ObtenerEquiposEnBodega createObtenerEquiposEnBodega() {
        return new ObtenerEquiposEnBodega();
    }

    /**
     * Create an instance of {@link ObtenerEquiposEnBodegaResponse }
     * 
     */
    public ObtenerEquiposEnBodegaResponse createObtenerEquiposEnBodegaResponse() {
        return new ObtenerEquiposEnBodegaResponse();
    }

    /**
     * Create an instance of {@link Respuesta }
     * 
     */
    public Respuesta createRespuesta() {
        return new Respuesta();
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link BigInteger }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "unsignedLong")
    public JAXBElement<BigInteger> createUnsignedLong(BigInteger value) {
        return new JAXBElement<BigInteger>(_UnsignedLong_QNAME, BigInteger.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Short }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "unsignedByte")
    public JAXBElement<Short> createUnsignedByte(Short value) {
        return new JAXBElement<Short>(_UnsignedByte_QNAME, Short.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Long }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "unsignedInt")
    public JAXBElement<Long> createUnsignedInt(Long value) {
        return new JAXBElement<Long>(_UnsignedInt_QNAME, Long.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Integer }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "char")
    public JAXBElement<Integer> createChar(Integer value) {
        return new JAXBElement<Integer>(_Char_QNAME, Integer.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Short }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "short")
    public JAXBElement<Short> createShort(Short value) {
        return new JAXBElement<Short>(_Short_QNAME, Short.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "guid")
    public JAXBElement<String> createGuid(String value) {
        return new JAXBElement<String>(_Guid_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Integer }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "unsignedShort")
    public JAXBElement<Integer> createUnsignedShort(Integer value) {
        return new JAXBElement<Integer>(_UnsignedShort_QNAME, Integer.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link BigDecimal }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "decimal")
    public JAXBElement<BigDecimal> createDecimal(BigDecimal value) {
        return new JAXBElement<BigDecimal>(_Decimal_QNAME, BigDecimal.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Boolean }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "boolean")
    public JAXBElement<Boolean> createBoolean(Boolean value) {
        return new JAXBElement<Boolean>(_Boolean_QNAME, Boolean.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Duration }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "duration")
    public JAXBElement<Duration> createDuration(Duration value) {
        return new JAXBElement<Duration>(_Duration_QNAME, Duration.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Respuesta }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "Respuesta")
    public JAXBElement<Respuesta> createRespuesta(Respuesta value) {
        return new JAXBElement<Respuesta>(_Respuesta_QNAME, Respuesta.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link byte[]}{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "base64Binary")
    public JAXBElement<byte[]> createBase64Binary(byte[] value) {
        return new JAXBElement<byte[]>(_Base64Binary_QNAME, byte[].class, null, ((byte[]) value));
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Integer }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "int")
    public JAXBElement<Integer> createInt(Integer value) {
        return new JAXBElement<Integer>(_Int_QNAME, Integer.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Long }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "long")
    public JAXBElement<Long> createLong(Long value) {
        return new JAXBElement<Long>(_Long_QNAME, Long.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "anyURI")
    public JAXBElement<String> createAnyURI(String value) {
        return new JAXBElement<String>(_AnyURI_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Float }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "float")
    public JAXBElement<Float> createFloat(Float value) {
        return new JAXBElement<Float>(_Float_QNAME, Float.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link XMLGregorianCalendar }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "dateTime")
    public JAXBElement<XMLGregorianCalendar> createDateTime(XMLGregorianCalendar value) {
        return new JAXBElement<XMLGregorianCalendar>(_DateTime_QNAME, XMLGregorianCalendar.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Byte }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "byte")
    public JAXBElement<Byte> createByte(Byte value) {
        return new JAXBElement<Byte>(_Byte_QNAME, Byte.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Double }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "double")
    public JAXBElement<Double> createDouble(Double value) {
        return new JAXBElement<Double>(_Double_QNAME, Double.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link QName }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "QName")
    public JAXBElement<QName> createQName(QName value) {
        return new JAXBElement<QName>(_QName_QNAME, QName.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Object }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "anyType")
    public JAXBElement<Object> createAnyType(Object value) {
        return new JAXBElement<Object>(_AnyType_QNAME, Object.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.microsoft.com/2003/10/Serialization/", name = "string")
    public JAXBElement<String> createString(String value) {
        return new JAXBElement<String>(_String_QNAME, String.class, null, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link Respuesta }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://tempuri.org/", name = "ObtenerEquiposEnBodegaResult", scope = ObtenerEquiposEnBodegaResponse.class)
    public JAXBElement<Respuesta> createObtenerEquiposEnBodegaResponseObtenerEquiposEnBodegaResult(Respuesta value) {
        return new JAXBElement<Respuesta>(_ObtenerEquiposEnBodegaResponseObtenerEquiposEnBodegaResult_QNAME, Respuesta.class, ObtenerEquiposEnBodegaResponse.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "Mensaje", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaMensaje(String value) {
        return new JAXBElement<String>(_RespuestaMensaje_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlAnwoStockProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlAnwoStockProducto(String value) {
        return new JAXBElement<String>(_RespuestaXmlAnwoStockProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaPerfilUsuario", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaPerfilUsuario(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaPerfilUsuario_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaSolicitudServicio", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaSolicitudServicio(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaSolicitudServicio_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlFactura", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlFactura(String value) {
        return new JAXBElement<String>(_RespuestaXmlFactura_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "Accion", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaAccion(String value) {
        return new JAXBElement<String>(_RespuestaAccion_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaStockProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaStockProducto(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaStockProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlPerfilUsuario", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlPerfilUsuario(String value) {
        return new JAXBElement<String>(_RespuestaXmlPerfilUsuario_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaFactura", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaFactura(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaFactura_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlStockProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlStockProducto(String value) {
        return new JAXBElement<String>(_RespuestaXmlStockProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "JsonListaProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaJsonListaProducto(String value) {
        return new JAXBElement<String>(_RespuestaJsonListaProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlGuiaDespacho", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlGuiaDespacho(String value) {
        return new JAXBElement<String>(_RespuestaXmlGuiaDespacho_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaProducto(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlProducto(String value) {
        return new JAXBElement<String>(_RespuestaXmlProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "JsonListaStockAnwo", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaJsonListaStockAnwo(String value) {
        return new JAXBElement<String>(_RespuestaJsonListaStockAnwo_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "JsonStockProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaJsonStockProducto(String value) {
        return new JAXBElement<String>(_RespuestaJsonStockProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "JsonProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaJsonProducto(String value) {
        return new JAXBElement<String>(_RespuestaJsonProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaAnwoStockProducto", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaAnwoStockProducto(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaAnwoStockProducto_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlListaGuiaDespacho", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlListaGuiaDespacho(String value) {
        return new JAXBElement<String>(_RespuestaXmlListaGuiaDespacho_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "XmlSolicitudServicio", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaXmlSolicitudServicio(String value) {
        return new JAXBElement<String>(_RespuestaXmlSolicitudServicio_QNAME, String.class, Respuesta.class, value);
    }

    /**
     * Create an instance of {@link JAXBElement }{@code <}{@link String }{@code >}}
     * 
     */
    @XmlElementDecl(namespace = "http://schemas.datacontract.org/2004/07/BuenosAires.Model", name = "JsonAutenticado", scope = Respuesta.class)
    public JAXBElement<String> createRespuestaJsonAutenticado(String value) {
        return new JAXBElement<String>(_RespuestaJsonAutenticado_QNAME, String.class, Respuesta.class, value);
    }

}
