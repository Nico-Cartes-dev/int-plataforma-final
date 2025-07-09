package buenosaires.utils;

import buenosaires.model.ListaProducto;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import java.io.InputStream;

public class XmlLoader {
   public static ListaProducto cargarProductosDesdeXml(String nombreArchivo) {
        try {
            JAXBContext context = JAXBContext.newInstance(ListaProducto.class);
            Unmarshaller unmarshaller = context.createUnmarshaller();

            //cargar desde classpath
            InputStream input = XmlLoader.class.getClassLoader().getResourceAsStream(nombreArchivo);
            if (input == null) {
                throw new IllegalArgumentException(nombreArchivo + " no encontrado en classpath.");
            }

            return (ListaProducto) unmarshaller.unmarshal(input);

        } catch (JAXBException e) {
            return null;
        }
    }

    
}
