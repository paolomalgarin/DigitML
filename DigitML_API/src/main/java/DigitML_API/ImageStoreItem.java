package DigitML_API;

/*
 * Record che rappresenta un elemento della cronologia delle immagini.
 *
 * Contiene le seguenti informazioni:
 *  - image: La stringa in Base64 che rappresenta l'immagine.
 *  - date: Il timestamp (in formato "dd/MM/yyyy HH:mm:ss") in cui l'immagine è stata salvata.
 *  - prediction: La predizione numerica ottenuta dal servizio di Machine Learning per questa immagine.
 *
 * I record consentono di creare classi immutabili in modo conciso, generando automaticamente
 * costruttore, getter (il cui nome corrisponde al campo) e metodi equals, hashCode e toString.
 */
public record ImageStoreItem(String image, String date, String prediction) {}
