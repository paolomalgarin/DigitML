## HOW IT WORKS

Tutte le componenti (Web‑App, API, ML Server e App Android) sono pensate per essere hostate **sullo stesso server**, semplificando comunicazione, autenticazione e configurazioni.

- **Web‑App (PHP + HTML/JS)**

  - **Hosting**: richiede **solo Apache** (anche quello di XAMPP, ma esclusivamente il modulo Apache).
  - **Accesso principale**: `http://<host>/DigitML/` (root `index.php`).
  - **Sezione Admin** (`ctrl_panel/`): gestione utenti e visualizzazione delle ultime 50 immagini inviate con relative predizioni.
  - **Sezione App** (`app.php`): area di disegno su canvas. Al submit invia una richiesta **POST** con body JSON:
    ```json
    {
      "image": "data:image/png;base64,iVBORw0KG...",
      "endpoint": "number"
    }
    ```
    I valori di `endpoint` (es. `number` o `letter`) possono essere modificati per ottenere risultati differenti.

- **API (Java Servlet)**

  - Deploy su Tomcat (porta 8080) nello stesso host della Web‑App.
  - **Endpoint**: `http://<host>:8080/DigitML_API/image`
    - **POST**: riceve JSON con campi `image` e `endpoint`, ridimensiona l’immagine a 28×28, chiama il ML Server e restituisce:
      ```json
      {
        "status": 200,
        "message": "OK",
        "prediction": "7"
      }
      ```
      Modificando `prediction` nel JSON di risposta si ottengono diverse predizioni.
    - **GET**: restituisce un array JSON con gli ultimi 50 guess.

- **ML Server (Flask + TensorFlow)**

  - Ascolta in background su `http://localhost:5000/`.
  - Due endpoint **POST**:
    - `/predictDigits`
    - `/predictLetters`
  - Riceve JSON con chiave `image` (Base64) e header `X-Signature` (HMAC) per autenticazione.
  - Converte l’immagine in scala di grigi, ridimensiona, normalizza e invoca il modello ML.
  - Restituisce JSON:
    ```json
    {
      "prediction": 4,
      "probabilities": [0.01, 0.03, 0.95, 0.005, ...]
    }
    ```
    L’array `probabilities` contiene la probabilità associata a ciascuna classe.

- **App Android**

  - APK disponibile in `WebApp/apk/`.
  - Permette di disegnare e inviare immagini all’API.
  - Configurare l’IP del server nelle impostazioni dell’app.

---

## INSTALLING (Windows)

Tutte le componenti vanno hostate sullo stesso server (Windows) per funzionare correttamente.

### 1. Configurazione locale con IDE

- **Web‑App (PHP)**

  1. Copia la cartella `DigitML - WebApp` in `C:\xampp\htdocs\`.
  2. Rinominala `DigitML`.
  3. Avvia XAMPP Control Panel e avvia il servizio **Apache**.
  4. Visita `http://localhost/DigitML/` nel browser.
  5. Per modificarla, apri il progetto (`C:\xampp\htdocs\DigitML`) in Visual Studio Code, NetBeans o simile.

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
>
> - `http://<host>/DigitML_WebApp/`
> - `http://<host>:8080/DigitML_API/image`
> - `http://<host>:5000/predictDigits` e `/predictLetters`

