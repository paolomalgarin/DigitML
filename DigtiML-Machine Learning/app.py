import base64
import hashlib
import hmac
from io import BytesIO
from flask import Flask, request, jsonify
from waitress import serve
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

tf.get_logger().setLevel('ERROR')

#Inizializza l'app Flask
app = Flask(__name__)

#Carica i modelli
modelDigits = load_model('digits_model.h5')
modelLetters = load_model('letters_model.h5')

#Dizionario per mappare l'indice della predizione alla lettera
word_dict = {i: chr(65 + i) for i in range(26)}  #Mappa 0 -> 'A', 1 -> 'B', ..., 25 -> 'Z'

SECRET_KEY = "ciaoBax" #Token dovrà essere inserito nell header dall API

#Funzione per decondificare token
def verify_hmac(data, signature):
    computed_hmac = hmac.new(SECRET_KEY.encode("utf-8"), data.encode("utf-8"), hashlib.sha256).digest()
    computed_signature = base64.b64encode(computed_hmac).decode()
    print(f"Computed signature: {computed_signature}")
    print(f"Received signature: {signature}")
    return hmac.compare_digest(computed_signature, signature)


    
#Funzione per preparare l'immagine
def prepare_image(image):
    if not isinstance(image, Image.Image):
        image = Image.open(BytesIO(image))

    #Converte in RGB e ridimensiona
    image = image.convert('RGB')
    img = image.resize((28, 28))
    img = img_to_array(img)

    #Scala di grigi
    img_gray = 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    img_gray = np.expand_dims(img_gray, axis=-1)

    #Inverte i colori se necessario
    if np.mean(img_gray) > 127:
        img_gray = 255 - img_gray

    #Normalizza
    img_gray = img_gray.reshape(1, 28, 28, 1).astype('float32') / 255.0

    return img_gray

#Endpoint GET per testare se il server è attivo
@app.route('/', methods=['GET'])
def index():
    return "Server Flask attivo. Usa un POST per inviare le immagini."

#Endpoint POST per ricevere le immagini di numeri
@app.route('/predictDigits', methods=['POST'])
def predict_digits():
    # #Controllo del token
    signature = request.headers.get('X-Signature')
    data = request.get_data(as_text=True)  # Dati grezzi della richiesta

    if not verify_hmac(data, signature):
        return jsonify({'error': 'Firma non valida'}), 403

    json_data = request.get_json()
    if 'image' not in json_data:
        return jsonify({'error': 'Nessun dato immagine fornito'}), 400

    image_data = json_data['image']
    try:
        #Legge l'immagine e preparala
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        img_array = prepare_image(image)

        #Predizione
        prediction = modelDigits.predict(img_array)
        predicted_class = np.argmax(prediction)

        return jsonify({
            'prediction': int(predicted_class),
            'probabilities': prediction.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Endpoint POST per ricevere le immagini di lettere
@app.route('/predictLetters', methods=['POST'])
def predict_letters():
    #Controlla token
    signature = request.headers.get('X-Signature')
    data = request.get_data(as_text=True)  # Dati grezzi della richiesta

    if not verify_hmac(data, signature):
        return jsonify({'error': 'Firma non valida'}), 403

    json_data = request.get_json()
    if 'image' not in json_data:
        return jsonify({'error': 'Nessun dato immagine fornito'}), 400

    image_data = json_data['image']

    try:
        #Legge l'immagine e preparala
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        img_array = prepare_image(image)

        #Predizione
        prediction = modelLetters.predict(img_array)
        predicted_class = np.argmax(prediction)

        #Mappa l'indice della predizione alla lettera
        predicted_letter = word_dict[predicted_class]

        return jsonify({
            'prediction': predicted_letter,
            'probabilities': prediction.tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Avvia il server Flask
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server Flask in ascolto su http://localhost:{port}/")
    serve(app, host="0.0.0.0", port=port)