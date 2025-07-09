package buenosaires.proxy;

import java.beans.XMLDecoder;
import java.beans.XMLEncoder;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.ArrayList;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;

public class XmlSerializer {
    
    public static String serialize(Object object) throws JAXBException {
        JAXBContext context = JAXBContext.newInstance(object.getClass());
        Marshaller marshaller = context.createMarshaller();
        marshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
        StringWriter writer = new StringWriter();
        marshaller.marshal(object, writer);
        String xml = writer.toString();
        return xml;
    }

    public static <T> T deserialize(String xml, Class<T> clazz) throws JAXBException {
        JAXBContext context = JAXBContext.newInstance(clazz);
        Unmarshaller unmarshaller = context.createUnmarshaller();
        StringReader reader = new StringReader(xml);
        return clazz.cast(unmarshaller.unmarshal(reader));
    }
    
    public static <T> T deserialize(String xml, Class<T> clazz, String contextPath) throws JAXBException {
        JAXBContext context = JAXBContext.newInstance(contextPath);
        Unmarshaller unmarshaller = context.createUnmarshaller();
        StringReader reader = new StringReader(xml);
        return clazz.cast(unmarshaller.unmarshal(reader));
    }
    
    public static String toXMLString(Object obj) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        XMLEncoder e = new XMLEncoder(baos);
        e.writeObject(obj);
        e.close();
        return new String(baos.toByteArray());
    }

    public static Object fromXMLString(String str) {
        XMLDecoder d = new XMLDecoder(new ByteArrayInputStream(str.getBytes()));
        Object obj = (Object) d.readObject();
        d.close();
        return obj;
    }
    
    public static ArrayList<String> getXmlElelemnts(String xml, String xmlElement) throws XMLStreamException {
        ArrayList<String> productoStrings = new ArrayList<>();
        XMLInputFactory xmlInputFactory = XMLInputFactory.newInstance();
        XMLStreamReader xmlStreamReader = xmlInputFactory.createXMLStreamReader(new StringReader(xml));
        String productoXml = null;
        while (xmlStreamReader.hasNext()) {
            int event = xmlStreamReader.next();
            switch (event) {
                case XMLStreamConstants.START_ELEMENT:
                    if (xmlStreamReader.getLocalName().equals(xmlElement)) {
                        productoXml = "<" + xmlElement + ">";
                    } else if (productoXml != null) {
                        productoXml += "<" + xmlStreamReader.getLocalName() + ">";
                    }
                    break;
                case XMLStreamConstants.END_ELEMENT:
                    if (xmlStreamReader.getLocalName().equals(xmlElement)) {
                        productoXml += "</" + xmlElement + ">";
                        productoStrings.add(productoXml);
                        productoXml = null;
                    } else if (productoXml != null) {
                        productoXml += "</" + xmlStreamReader.getLocalName() + ">";
                    }
                    break;
                case XMLStreamConstants.CHARACTERS:
                    if (productoXml != null) {
                        productoXml += xmlStreamReader.getText();
                    }
                    break;
                default:
                    break;
            }
        }
        return productoStrings;
    }

}