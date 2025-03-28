package DigitML_API;

import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import javax.imageio.ImageIO;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;

@WebServlet("/image")
public class ImageServlet extends BaseServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        setJsonResponse(response);
        String reqJson = new String(request.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
        ImageRequest req = gson.fromJson(reqJson, ImageRequest.class);

        BufferedImage originalImage = req.getImageAsBufferedImage();
        if (originalImage == null) {
            response.getWriter().write("{\"status\":400, \"message\":\"Nessuna immagine ricevuta.\"}");
            return;
        }

        BufferedImage resizedImage = resizeImage(originalImage, 28, 28);
        String outputType = req.endpoint().toLowerCase();
        String urlString;
        if ("number".equals(outputType)) {
            urlString = "http://localhost:5000/predictDigits";
        } else if ("letter".equals(outputType)) {
            urlString = "http://localhost:5000/predictLetters";
        } else {
            response.getWriter().write("{\"status\":400, \"message\":\"Endpoint non valido.\"}");
            return;
        }

        String mlResponseStr = callMLService(resizedImage, urlString);
        
        boolean validResponse = false;
        if ("number".equals(outputType)) {
            validResponse = mlResponseStr.matches("\\d+");
        } else if ("letter".equals(outputType)) {
            validResponse = mlResponseStr.matches("[A-Za-z]");
        }
        
        if (validResponse) {
            ImageStore.addImage(req.image(), mlResponseStr);
            response.getWriter().write("{\"status\":200, \"message\":\"OK\", \"prediction\":\"" + mlResponseStr + "\"}");
        } else {
            response.getWriter().write("{\"status\":500, \"message\":\"" + mlResponseStr + "\"}");
        }
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        setJsonResponse(response);
        response.getWriter().write(gson.toJson(ImageStore.getImageHistory()));
    }

    private BufferedImage resizeImage(BufferedImage originalImage, int width, int height) {
        BufferedImage resizedImage = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2d = resizedImage.createGraphics();
        g2d.setRenderingHint(java.awt.RenderingHints.KEY_INTERPOLATION, java.awt.RenderingHints.VALUE_INTERPOLATION_BILINEAR);
        g2d.drawImage(originalImage, 0, 0, width, height, null);
        g2d.dispose();
        return resizedImage;
    }

    /*
     * Comunica con il servizio ML:
     * - Converte l'immagine ridimensionata in Base64.
     * - Crea il payload JSON.
     * - Genera la firma HMAC sul payload.
     * - Invia la richiesta HTTP POST con gli header "X-Api-Key" e "X-Signature".
     * - Deserializza la risposta JSON in un oggetto MLResponse e restituisce il valore del campo "prediction".
     */
    private String callMLService(BufferedImage image, String urlString) {
        try {
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ImageIO.write(image, "png", baos);
            String encodedImage = Base64.getEncoder().encodeToString(baos.toByteArray());
            
            // Costruzione payload JSON
            String payload = "{\"image\": \"" + encodedImage + "\"}";

            // Genera la firma HMAC sul payload completo
            String hmacSignature = HMACGenerator.calculateHMAC(payload, "ciaoBax");

            // Configura la connessione
            URL url = new URL(urlString);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("X-Api-Key", "ciaoBax");
            conn.setRequestProperty("X-Signature", hmacSignature);
            conn.setDoOutput(true);

            try (OutputStream os = conn.getOutputStream()) {
                os.write(payload.getBytes(StandardCharsets.UTF_8));
            }

            if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                StringBuilder sb = new StringBuilder();
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line);
                }
                String jsonResponse = sb.toString();
                MLResponse mlRes = gson.fromJson(jsonResponse, MLResponse.class);
                return mlRes.getPrediction();
            }
        } catch (Exception e) {
            return "Errore di comunicazione con il ML!";
        }
        return "Errore";
    }
}