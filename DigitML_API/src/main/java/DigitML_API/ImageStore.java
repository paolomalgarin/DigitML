package DigitML_API;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;

/*
 * @author Kevin Bax
 */
public class ImageStore {

    private static final ArrayList<ImageStoreItem> imageHistory = new ArrayList<>();
    private static final int MAX_HISTORY = 50;

    public static synchronized void addImage(String image, String prediction) {
        imageHistory.add(new ImageStoreItem(image,
                LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss")),
                prediction));
        if (imageHistory.size() > MAX_HISTORY) {
            imageHistory.remove(0);
        }
    }

    public static synchronized ArrayList<ImageStoreItem> getImageHistory() {
        return new ArrayList<>(imageHistory);
    }
}
