package DigitML_API;

import java.io.*;
import java.awt.image.BufferedImage;
import java.util.Base64;
import javax.imageio.ImageIO;

/*
 * Record che rappresenta una richiesta contenente un'immagine e l'OutputType.
 *
 * Contiene:
 *  - image: Una stringa in Base64 che rappresenta l'immagine. Puo' contenere anche il prefisso
 *           "data:image/png;base64," che viene rimosso prima della conversione.
 *  - OutputType: Una stringa che indica il tipo di output desiderato. Puo' assumere il valore "number" o "letter".
 */
public record ImageRequest(String image, String endpoint) {
    
    /*
     * Converte la stringa Base64 in un oggetto BufferedImage.
     *
     * Procedura:
     * 1. Se la stringa contiene un prefisso (ad esempio "data:image/png;base64,"), lo rimuove.
     * 2. Decodifica la stringa Base64 in un array di byte.
     * 3. Converte l'array di byte in un BufferedImage.
    */
    public BufferedImage getImageAsBufferedImage() {
        try {
            String base64Image = image;
            if (base64Image.contains(",")) {
                base64Image = base64Image.split(",")[1];
            }
            byte[] imageBytes = Base64.getDecoder().decode(base64Image);
            return ImageIO.read(new ByteArrayInputStream(imageBytes));
        } catch (IOException ignored) {
        }
        return null;
    }
}