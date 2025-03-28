package DigitML_API;

import com.google.gson.*;
import javax.servlet.http.*;
import javax.servlet.ServletException;

/*
 * Classe astratta che fornisce metodi comuni alle servlet, come la configurazione degli header per CORS
 * e la gestione della serializzazione JSON tramite Gson.
 */
public abstract class BaseServlet extends HttpServlet {
    
    protected final Gson gson = new GsonBuilder().create();
    
    protected void setJsonResponse(HttpServletResponse response) {
        response.setHeader("Access-Control-Allow-Origin", "*");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
        response.setContentType("application/json");
    }
    
    @Override
    protected void doOptions(HttpServletRequest request, HttpServletResponse response) throws ServletException {
        setJsonResponse(response);
        response.setStatus(HttpServletResponse.SC_OK);
    }
}