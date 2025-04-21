## HOW IT WORKS

Tutte le componenti (Web‑App, API, ML Server e App Android) sono pensate per essere hostate **sullo stesso server**, semplificando comunicazione, autenticazione e configurazioni.

1. **Web‑App (PHP + HTML/JS)**

   - **Hosting**: richiede un server Apache con PHP (es. XAMPP).
   - **Sezione Admin** (`ctrl_panel/`): gestione utenti, monitoraggio delle ultime 50 immagini inviate and guess, creazione/eliminazione utenti.
   - **Sezione App** (`app.php`): area in cui l’utente disegna una cifra o una lettera su un canvas. Al submit:
     - il client inverte i colori del canvas (`scripts/elabora_img.js`)
     - converte l’immagine in Base64
     - invia una richiesta **POST** all’API Java con body JSON:
       ```json
       {
         "image": "data:image/png;base64,iVBORw0KG…",
         "endpoint": "number"   // o "letter"
       }
       ```
     - riceve e mostra la predizione sullo schermo

2. **API (Java Servlet)**

   - Deploy su Tomcat (porta 8080) nello stesso host del Web‑App.
   - **Endpoint**: `http://<host>:8080/DigitML_API/image`
     - **POST**: riceve JSON con `image` e `endpoint`, ridimensiona a 28×28, chiama il server ML su `localhost:5000`, salva prediction nello storico e risponde con:
       ```json
       {
         "status": 200,
         "message": "OK",
         "prediction": "7"
       }
       ```
     - **GET**: restituisce JSON con gli ultimi 50 guess salvati

3. **ML Server (Flask + TensorFlow)**

   - Esegue in background su `http://localhost:5000/` sullo stesso server.
   - Due endpoint **POST**:
     - `/predictDigits`
     - `/predictLetters`
   - Riceve JSON con chiave `image` (Base64) e header HMAC (`X-Signature`) per autenticazione.
   - Converte l’immagine in scala di grigi, ridimensiona, normalizza e invoca il modello ML.
   - Restituisce JSON:
     ```json
     {
       "prediction": 4,               // o "A","B",…
       "probabilities": […]
     }
     ```

4. **App Android**

   - Nativa o tramite APK (`WebApp/apk/`).
   - Permette di disegnare e inviare l’immagine al server API.
   - Configurare l’IP del server (es. `192.168.1.10`) nelle impostazioni.

---

## INSTALLING (Windows)

Tutte le componenti vanno hostate sullo stesso server (Windows) per funzionare correttamente.

### 1. Configurazione locale con IDE
- **Web‑App (PHP)**
  1. Copia la cartella `DigitML_WebApp` in `C:\xampp\htdocs\DigitML_WebApp`.
  2. Apri il progetto in **Visual Studio Code**, **NetBeans** o simile.
  3. Avvia XAMPP Control Panel e avvia i servizi **Apache** (e **Tomcat** se abilitato).
  4. Visita `http://localhost/DigitML_WebApp/` nel browser.

- **API (Java Servlet)**
  1. Apri `DigitML_API` in **IntelliJ IDEA** o **NetBeans**.
  2. Esegui nel terminale del progetto:
     ```bat
     gradlew build
     ```
  3. Copia `build\libs\DigitML_API.war` in `C:\xampp\tomcat\webapps\` (se usi Tomcat incluso in XAMPP) o nella cartella `webapps` del Tomcat stand‑alone.
  4. Riavvia Tomcat dal XAMPP Control Panel.

- **ML Server (Python)**
  1. Apri `MachineLearning` in **PyCharm** o similare.
  2. Crea un virtualenv e installa dipendenze:
     ```bat
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```
  3. Avvia il server:
     ```bat
     python app.py
     ```
  4. Verifica in `http://localhost:5000/`.

- **Android**
  1. Importa `DigitML-Android` in **Android Studio**.
  2. Collega un dispositivo/emulatore e premi “Run”, oppure installa l’**APK** da `WebApp\apk\`.

---

## INSTALLING (Linux)

Tutte le componenti vanno hostate sullo stesso server (Linux) per funzionare correttamente.

### 1. Configurazione locale con IDE
- **Web‑App (PHP)**
  1. Copia la cartella `DigitML_WebApp` in `/opt/lampp/htdocs/DigitML_WebApp`.
  2. Apri il progetto in **Visual Studio Code**, **NetBeans** o simile.
  3. Avvia XAMPP (oppure Apache) con:
     ```bash
     sudo /opt/lampp/lampp start
     ```
  4. Visita `http://localhost/DigitML_WebApp/`.

- **API (Java Servlet)**
  1. Apri `DigitML_API` in **IntelliJ IDEA** o **NetBeans**.
  2. Costruisci il WAR:
     ```bash
     ./gradlew build
     ```
  3. Copia `build/libs/DigitML_API.war` in `/opt/tomcat/webapps/`.
  4. Avvia Tomcat:
     ```bash
     /opt/tomcat/bin/startup.sh
     ```

- **ML Server (Python)**
  1. Apri `MachineLearning` in **PyCharm** o similare.
  2. Crea virtualenv e installa dipendenze:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```
  3. Avvia il server:
     ```bash
     python app.py
     ```
  4. Verifica in `http://localhost:5000/`.

- **Android**
  1. Importa `DigitML-Android` in **Android Studio**.
  2. Collega emulatore/dispositivo e premi “Run” o installa l’APK da `WebApp/apk/`.

---

> **Nota**: in entrambi gli ambienti, dopo il deploy, assicurati di configurare gli IP e le porte nei file PHP/JS se i servizi non sono in `localhost`. Verifica il corretto funzionamento di:
> - `http://<host>/DigitML_WebApp/`
> - `http://<host>:8080/DigitML_API/image`
> - `http://<host>:5000/predictDigits` e `/predictLetters`

