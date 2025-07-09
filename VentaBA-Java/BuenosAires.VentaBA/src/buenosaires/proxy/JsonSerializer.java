package buenosaires.proxy;

import com.google.gson.Gson;
import java.text.ParseException;
import java.util.Map;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

public class JsonSerializer {
    
    private static final Gson gson = new Gson();

    /**
     * Serializa un objeto Java simple (por ejemplo, Map, List, String, Integer...) a un String JSON.
     */
    public static String toJson(Object object) {
        if (object instanceof Map) {
            return JSONObject.toJSONString((Map<?, ?>) object);
        } else {
            throw new IllegalArgumentException("Sólo se pueden serializar objetos tipo Map con json-simple.");
        }
    }

    /**
     * Deserializa un String JSON a un Map<String, Object>
     */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> fromJsonToMap(String json) throws ParseException, org.json.simple.parser.ParseException {
        JSONParser parser = new JSONParser();
        Object obj = parser.parse(json);

        if (obj instanceof JSONObject) {
            return (Map<String, Object>) obj;
        } else {
            throw new IllegalArgumentException("El JSON no representa un objeto tipo JSONObject.");
        }
    }

    /**
     * Serializa un objeto Java a una cadena JSON.
     */
    public static String serialize(Object object) {
        return gson.toJson(object);
    }

    /**
     * Deserializa una cadena JSON a un objeto del tipo especificado.
     */
    public static <T> T deserialize(String json, Class<T> clazz) {
        return gson.fromJson(json, clazz);
    }
}
