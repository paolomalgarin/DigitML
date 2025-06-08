<p align=center>
<img src="https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/animated-logo.svg" alt='logo animato' width=50%> <br>
<i width=80%>Progetto scolastico per il riconoscimento di cifre e lettere attraverso Machine Learning, con backend Java, frontend PHP, app Android e server Python.</i>
</p>
<br>

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

<br>
<br>

# 📖 INDICE  
 * 📥 [Installation guide](https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/Documentation/INSTALLATION-OPTIONS.md)
 * 📌 [Panoramica](#-panoramica)
 * 🏗️ [Architettura & Flusso dei Dati](#%EF%B8%8F-architettura--flusso-dei-dati)  
 * 🛠️ [Tecnologie Utilizzate](#%EF%B8%8F-tecnologie-utilizzate)  
 * 📷 [Esempi d’Uso](#-esempi-duso)  
 * 📊 [Dati](#-dati)  
 * 📄 [Licenza](#-licenza)  

<br>
<br>

# 📌 Panoramica

Il progetto DigitML ci è stato assegnato come attività didattica con l’obiettivo di realizzare un’applicazione distribuita per il riconoscimento di cifre manoscritte.  
La consegna prevedeva la creazione di un sistema capace di identificare numeri scritti a mano, da utilizzare durante gli open‑day scolastici per mostrare le competenze acquisite nel triennio di Informatica.  
Spinti dalla nostra curiosità e dalla voglia di sperimentare, abbiamo esteso il progetto aggiungendo numerose funzionalità extra, tra cui il riconoscimento delle lettere dell’alfabeto.
> [!TIP]
> [Installation guide](https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/Documentation/INSTALLATION-OPTIONS.md)

<br>

---
<br>

# 🏗️ Architettura & Flusso dei Dati

 *Le applicazioni front-end mandano le richieste all'API che è l'unico che può comunicare con il ML grazie ad un **HMAC***
 <img src="https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/data-flow.svg" alt='logo animato' width=70%> <br>

<br>

---
<br>

# 🛠️ Tecnologie Utilizzate

<img src="https://skillicons.dev/icons?i=php,html,css,js,python,tensorflow,java" /> <br>

- **Java Servlet**: comunicazione front-end e back-end  
- **PHP 8+**: interfaccia web e autenticazione  
- **Android (*Java*)**: app mobile (*Android*)  
- **Python 3.8+**: server Flask  
- **TensorFlow/Keras**: rete neurale  

<br>

---
<br>

# 📷 Esempi d’Uso  
> *Qui sotto un esempio della web-app e dell'app Android:*

<img src="https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/guessing.gif" alt='Web-app gui' width=79%><img src="https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/Android-gui.jpg" alt='Android gui' width=21%>

> [!WARNING]
> Per provarla vedi [installation guide](https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/Documentation/INSTALLATION-OPTIONS.md).

<br>

---
<br>

# 📊 Dati
Dataset utilizzati:
|NOME| MNIST | A-Z Handwritten Alphabets |
|---|---|---|
|IMG|<img src='https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/MNIST.png' alt='mnist'>|<img src='https://github.com/paolomalgarin/DigitML/blob/main/docs/README%20-%20Stuff/A-Z%20Handwritten%20Alphabets.png' alt='A-Z Handwritten Alphabets'>|
|TIPO DI RETE|CNN _(Convolutional Neural Network)_|CNN _(Convolutional Neural Network)_|
|VAL ACCURACY|**98.6%**|**98.8%**|
|TRAIN ACCURACY|99.3%|99.5%|

<br>

---
<br>

# 📄 Licenza
Questo progetto è rilasciato sotto [MIT License](https://github.com/paolomalgarin/DigitML/blob/main/LICENSE.txt).
