package buenosaires.proxy.rest;

import buenosaires.model.FilaStockProducto;
import buenosaires.model.StockProducto;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;

public class ScStockProductoRest {
    private static final String ENDPOINT = "http://127.0.0.1:8001/BuenosAiresApiRest/obtener_equipos_en_bodega";

    public List<FilaStockProducto> listar() throws Exception {
        URL url = new URL(ENDPOINT);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(5000);

        if (conn.getResponseCode() != 200) {
            throw new RuntimeException("HTTP error: " + conn.getResponseCode());
        }

        BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = in.readLine()) != null) {
            sb.append(line);
        }
        in.close();
        conn.disconnect();

        String json = sb.toString();
        Type listType = new TypeToken<List<FilaStockProducto>>() {}.getType();
        return new Gson().fromJson(json, listType);
    }
}
