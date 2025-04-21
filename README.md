<p align="center">
  <img src="README - Stuff/animated-logo.svg" alt="DigitML Banner" width="600"/>
</p>
<hr>


<br><br>
blablabla blabla ble
<br><br>

<p align="center">
  <img src="README - Stuff/guessing.gif" alt="DigitML Banner" width="800"/>
</p>

<p align="center">
  <video width="800" controls>
    <source src="README - Stuff/guessing-vid.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>



## HOW IT WORKS

Questo progetto è composto da quattro componenti principali che comunicano tra loro per fornire una piattaforma completa di riconoscimento di cifre e lettere:

1. **Web‑App (PHP + HTML/JS)**  
   - Accessibile via browser: basta aprire `landing.html` per entrare nella pagina iniziale.  
   - **Sezione Admin** (`ctrl_panel/`): gestione utenti, monitoraggio delle ultime 50 immagini inviate e dei relativi guess, creazione/eliminazione utenti.  
   - **Sezione App** (`app.html`): area in cui l’utente disegna un numero o una lettera su un canvas. Al submit:
     1. il client inverte i colori del canvas (`scripts/elabora_img.js`)
     2. converte l’immagine in Base64
     3. invia una richiesta **POST** al servlet Java API con body JSON:
        ```json
        {
          "image": "data:image/png;base64,iVBORw0KG…",
          "endpoint": "number"   // o "letter"
        }
        ```
     4. riceve e mostra la predizione sullo schermo

2. **API (Java Servlet)**  
   - Espone un unico servlet su `http://<host>:8080/DigitML_API/image`  
     - **POST**: accetta il JSON con `image` e `endpoint` (number|letter), ridimensiona l’immagine a 28×28, chiama il server ML in localhost:5000, aggiunge la predizione allo storico e restituisce:
       ```json
       {
         "status": 200,
         "message": "OK",
         "prediction": "7"
       }
       ```
     - **GET**: ritorna in JSON l’array degli ultimi 50 guess salvati.

3. **ML Server (Flask + TensorFlow)**  
   - Ascolta su `http://localhost:5000/`  
   - Due endpoint **POST**:
     - `/predictDigits`
     - `/predictLetters`  
   - Riceve JSON con campo `"image"` (Base64) e header HMAC (`X-Signature`) per autenticazione.  
   - Prepara l’immagine (converti in scala di grigi, ridimensiona, normalizza), esegue `modelDigits.predict()` o `modelLetters.predict()`, e restituisce:
     ```json
     {
       "prediction": 4,                  // o "A","B",…
       "probabilities": […]             
     }
     ```

4. **App Android**  
   - Applicazione nativa (codice in `DigitML - Android`) o semplicemente installando l’**APK** presente in `WebApp/apk/`.  
   - Permette di disegnare direttamente sullo schermo e inviare l’immagine al server API.  
   - Prima di inviare, nell’app va configurato l’**IP** del server (es. `192.168.1.10`).  

---

## INSTALLING

Di seguito tre modalità di setup, da locale (IDE), con XAMPP e in ambiente server/produzione.

### 1. Aprire le componenti su IDE e testarle
- **Web‑App**  
  1. Copia la cartella `DigitML ‑ WebApp` nel tuo workspace.  
  2. Apri i file HTML/PHP con **Visual Studio Code** o **NetBeans**.  
  3. Verifica che il JS (`scripts/`) venga caricato correttamente aprendo `index.html` in un browser.

- **API (Java)**  
  1. Apri il progetto `DigitML ‑ API` con **IntelliJ IDEA** o **NetBeans**.  
  2. Esegui `./gradlew build` per generare il WAR.  
  3. Configura un server Tomcat in locale e deploya il WAR in `webapps/DigitML_API`.

- **ML Server (Python)**  
  1. Apri `DigtiML ‑ Machine Learning` in **PyCharm** o simile.  
  2. Crea un virtualenv, poi:
     ```bash
     pip install -r requirements.txt
     ```
  3. Avvia:
     ```bash
     python app.py
     ```
     il server ascolterà su `http://localhost:5000`.

- **Android**  
  1. Importa la cartella `DigitML ‑ Android` in **Android Studio**.  
  2. Collega un emulatore o dispositivo e premi “Run”.  
  3. In alternativa, installa direttamente l’APK da `WebApp/apk/`.

---

### 2. Usando XAMPP
1. **Web‑App e API**  
   - Copia `DigitML ‑ WebApp` in `C:\xampp\htdocs\DigitML_WebApp`.  
   - Copia `DigitML ‑ API` (la cartella con `build.gradle`, `src/`, ecc.) in `htdocs\DigitML_API` se vuoi emulare il deploy, ma **attenzione**: le servlet Java vanno in Tomcat (incluso in XAMPP se abiliti il modulo Tomcat).

2. **ML Server**  
   - In una console, entra in `DigtiML ‑ Machine Learning` e lancia:
     ```bash
     pip install -r requirements.txt
     python app.py
     ```
   - Rimane indipendente da XAMPP.

3. **Android**  
   - Installa l’APK su uno smartphone Android via USB o QR.

---

### 3. Su Server (Tomcat + Apache manuale)
1. **Apache HTTPD (PHP)**  
   - Installa Apache e PHP (`sudo apt install apache2 php libapache2-mod-php`).  
   - Copia `DigitML ‑ WebApp` in `/var/www/html/DigitML`.

2. **Tomcat (Java API)**  
   - Scarica e scompatta Tomcat in `/opt/tomcat`.  
   - Copia il WAR generato (`DigitML_API.war`) in `/opt/tomcat/webapps`.  
   - Avvia Tomcat:
     ```bash
     /opt/tomcat/bin/startup.sh
     ```

3. **ML Server**  
   - Sullo stesso server o un host separato, configura Python e:
     ```bash
     pip install -r /percorso/DigtiML‑Machine\ Learning/requirements.txt
     python /percorso/app.py
     ```
   - Assicurati che il firewall permetta le porte **5000** (Flask) e **8080** (Tomcat).

4. **Configurazioni finali**  
   - Modifica negli HTML/JS l’IP e le porte dei servizi se non sono in `localhost`.  
   - Verifica che tutti i servizi siano raggiungibili (browser → Apache, `/DigitML_API/image` → Tomcat, `/predictDigits` → Flask).

