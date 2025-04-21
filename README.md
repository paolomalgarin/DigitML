## HOW IT WORKS

Tutte le componenti (Web‑App, API, ML Server e App Android) comunicano tra loro sullo stesso host per semplificare autenticazione e configurazione.

- **Web‑App (PHP + HTML/JS)**
  - Ospitata su Apache (es. XAMPP).
  - **URL principale**: `http://<host>/DigitML/`
  - **Sezione Admin** (`ctrl_panel/`): gestione utenti e visualizzazione delle ultime 50 immagini con predizioni.
  - **Sezione App** (`app.php`): canvas per disegnare cifre/lettere; invia al server via POST:
    ```json
    {
      "image": "data:image/png;base64,iVBORw0KG...",
      "endpoint": "number"
    }
    ```
    **Campi modificabili**  
    - `endpoint`: `"number"` o `"letter"` → cambia il modello di predizione.

- **API (Java Servlet)**
  - Deploy su Tomcat (porta 8080).
  - **Endpoint**: `http://<host>:8080/DigitML_API/image`
    - **POST**: riceve lo stesso JSON della Web‑App, ridimensiona l’immagine a 28×28 px, chiama il ML Server e risponde:
      ```json
      {
        "status": 200,
        "message": "OK",
        "prediction": "7"
      }
      ```
      **Campi modificabili**  
      - `prediction`: stringa con il valore predetto.
    - **GET**: restituisce array JSON con gli ultimi 50 tentativi, es.:
      ```json
      [
        { "timestamp": "2025-04-20T14:23:00Z", "endpoint": "number", "prediction": "5" },
        …
      ]
      ```
      **Campi**  
      - `timestamp`: data/ora del tentativo  
      - `endpoint`: modello usato (`number`/`letter`)  
      - `prediction`: risultato.

- **ML Server (Flask + TensorFlow)**
  - Ascolta su `http://localhost:5000`
  - Endpoints POST:
    - `/predictDigits`
    - `/predictLetters`
  - Riceve JSON con chiave `image` e header `X-Signature` (HMAC):
    ```json
    {
      "image": "iVBORw0KG..."
    }
    ```
    **Campi**  
    - `image`: stringa Base64 dell’immagine PNG senza prefisso.
  - Restituisce:
    ```json
    {
      "prediction": 4,
      "probabilities": [0.01, 0.03, 0.95, …]
    }
    ```
    **Campi modificabili**  
    - `probabilities`: array di float; cambiano in base al modello e alla qualità dell’immagine.

- **App Android**
  - APK in `WebApp/apk/`.
  - Permette di disegnare e inviare immagini all’API (impostare l’IP del server nelle preferenze).

---

## INSTALLING

### 1. Apertura con IDE e test
1. **Web‑App (PHP)**  
   - Apri `DigitML/WebApp` in Visual Studio Code, NetBeans o simile.  
   - Esegui sul tuo server Apache integrato (es. configurando un Virtual Host “DigitML”).
2. **API (Java Servlet)**  
   - Apri `DigitML/DigitML_API` in IntelliJ IDEA o NetBeans.  
   - Esegui la build con:
     ```
     gradlew build
     ```
   - Testa direttamente in modalità debug sul Tomcat integrato all’interno dell’IDE.
3. **ML Server (Python)**  
   - Apri `DigitML/MachineLearning` in PyCharm.  
   - Crea ed attiva un virtualenv, poi:
     ```
     pip install -r requirements.txt
     python app.py
     ```
4. **Android**  
   - Importa `DigitML-Android` in Android Studio.  
   - Avvia su emulator o device.

### 2. Installazione con XAMPP
1. **Web‑App**  
   - Copia `DigitML/WebApp` in `C:\xampp\htdocs\DigitML`.  
   - Avvia Apache da XAMPP Control Panel e visita `http://localhost/DigitML/`.
2. **API + Tomcat**  
   - Dopo `gradlew build`, copia `DigitML_API\build\libs\DigitML_API.war` in `C:\xampp\tomcat\webapps\`.  
   - Avvia Tomcat da XAMPP Control Panel.
3. **ML Server**  
   - Nella cartella `MachineLearning` lancia il batch incluso (es. `start_ml.bat`) o:
     ```
     python app.py
     ```
4. **Android**  
   - Installa l’APK da `C:\xampp\htdocs\DigitML\apk\` direttamente su dispositivo via USB.

### 3. Installazione manuale su server Windows
1. **Apache HTTP Server**  
   - Scarica e installa da apache.org.  
   - Punta il `DocumentRoot` alla cartella `WebApp`.
2. **Apache Tomcat**  
   - Scarica Tomcat 9/10 da tomcat.apache.org.  
   - Estrai e copia il WAR (`DigitML_API.war`) in `webapps\`.
   - Avvia `bin\startup.bat`.
3. **Python/ML**  
   - Installa Python 3.8+.  
   - In `MachineLearning`:
     ```
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     venv\Scripts\activate && python app.py
     ```
4. **Firewall & porte**  
   - Apri le porte 80, 8080 e 5000 nel firewall di Windows.

---

*Nota:* dopo l’installazione, verifica sempre:
- `http://<host>/DigitML/`  
- `http://<host>:8080/DigitML_API/image`  
- `http://<host>:5000/predictDigits` e `/predictLetters`  
- Connessione dall’app Android inserendo l’IP server.  
