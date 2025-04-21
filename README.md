<p align=center>
<img src="https://github.com/paolomalgarin/DigitML/blob/main/README%20-%20Stuff/animated-logo.svg" alt='logo animato' width=50%> <br>
<i width=80%>Progetto scolastico per il riconoscimento di cifre e lettere attraverso Machine Learning, con backend Java, frontend PHP, app Android e server Python.</i>
</p>

# 🤝 Contributors
<i>Un grazie speciale a queste fantastiche persone che hanno contribuito al progetto:</i>
<br>
<p>
  <a href="https://github.com/paolomalgarin/DigitML/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=paolomalgarin/DigitML" />
  </a>
</p>

> [!NOTE]
> | PROFILO | RUOLO ||
> |---|---|---|
> | [@paolomalgarin](https://github.com/paolomalgarin) | Design e web-app | ✨ |
> | [@anItalianGeek](https://github.com/anItalianGeek) | Project manager | 💼 |
> | [@michelecortiana](https://github.com/michelecortiana) | Machine learning | 🧠 |
> | [@Phoeyuh](https://github.com/Phoeyuh) | API | 🐝 |
> | [@Benti06](https://github.com/Benti06) | Android app | 📱 |

---

# 📖 Indice

1. [Panoramica](#panoramica)  
2. [Architettura & Flusso dei Dati](#architettura--flusso-dei-dati)  
3. [Tecnologie Utilizzate](#tecnologie-utilizzate)  
4. [Installazione](#installazione)  
5. [Configurazione](#configurazione)  
6. [Avvio del Progetto](#avvio-del-progetto)  
7. [Esempi d’Uso](#esempi-duso)  
8. [Test e Valutazione](#test-e-valutazione)  
9. [Sviluppi Futuri](#sviluppi-futuri)  
10. [Contribuire](#contribuire)  
11. [Licenza](#licenza)  
12. [Contatti](#contatti)  

---

# 📌 Panoramica

Descrivi brevemente l’obiettivo del progetto, il contesto scolastico e i principali casi d’uso (es. riconoscimento in tempo reale da browser e da mobile).

---

# 🏗️ Architettura & Flusso dei Dati

1. **Client Web (PHP)**  
   - Interfaccia utente: form per il disegno/inserimento delle cifre  
   - Comunicazione via HTTP con la servlet Java  
2. **Backend Java (Servlet)**  
   - Endpoints REST per ricevere immagini/dati  
   - Logica di pre-processing e inoltro al server ML  
3. **Server ML (Flask + TensorFlow)**  
   - API Flask per classificazione  
   - Modello di rete neurale (CNN) addestrato su MNIST/EMNIST  
4. **App Mobile (Android)**  
   - Schermata di disegno e invio  
   - Visualizzazione del risultato di classificazione  
5. **Diagramma**  
   - Inserisci un diagramma a blocchi o sequenza per chiarire il flusso  

---

# 🛠️ Tecnologie Utilizzate

- **Java Servlet**: gestione delle richieste HTTP  
- **PHP 8+**: interfaccia web e autenticazione base  
- **Android (Kotlin/Java)**: app mobile cross-device  
- **Python 3.8+**: server Flask  
- **TensorFlow/Keras**: modello di apprendimento  

---

# 📷 Esempi d’Uso

- Web: screenshot del disegno e risultato
- Android: schermate principali
- Brevi GIF o link a un video demo

---

# ✅ Test e Valutazione
- Dataset di test
- Metriche (accuracy, precision, recall)
- Valori ottenuti e confronto con baseline

---

## 📄 Licenza
Questo progetto è rilasciato sotto MIT License.
