import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

#Funzione per caricare e pre-processare i dati
def load_and_preprocess_data(file_path):
    #Carica il file CSV in un DataFrame
    df = pd.read_csv(file_path).astype('float32')  
    x = df.drop('0', axis=1)  #Rimuove la colonna '0' che rappresenta le etichette
    y = df['0']  #La colonna '0' contiene le etichette (le lettere)

    #Split dei dati in train e test (80% per il training, 20% per il test)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    
    #Ridimensiona e normalizza i dati delle immagini (28x28 pixel, scala da 0 a 1)
    x_train = np.reshape(x_train.values, (x_train.shape[0], 28, 28)) / 255.0
    x_test = np.reshape(x_test.values, (x_test.shape[0], 28, 28)) / 255.0
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    
    #Converte le etichette in formato one-hot encoding
    y_train = tf.keras.utils.to_categorical(y_train, 26)  #26 classi (A-Z)
    y_test = tf.keras.utils.to_categorical(y_test, 26)    #26 classi (A-Z)
    return train_test_split(x_train, y_train, test_size=0.1, random_state=42), (x_test, y_test)

#Funzione per costruire il modello CNN
def build_model():
    model = Sequential([  #Crea un modello sequenziale
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),  #Convolutional layer 1
        MaxPool2D((2, 2), strides=2),  #Max pooling layer 1
        
        Conv2D(64, (3, 3), activation='relu', padding='same'),  #Convolutional layer 2
        MaxPool2D((2, 2), strides=2),  #Max pooling layer 2
        
        Conv2D(128, (3, 3), activation='relu', padding='valid'),  #Convolutional layer 3
        MaxPool2D((2, 2), strides=2),  #Max pooling layer 3
        
        Dropout(0.2),  #Dropout per evitare overfitting
        
        Flatten(),  
        Dense(128, activation='relu'),  
        Dense(26, activation='softmax')  #Output layer con 26 classi (una per ogni lettera dell'alfabeto)
    ])
    
    #Compila il modello con l'ottimizzatore Adam, la funzione di perdita 'categorical_crossentropy' e la metrica 'accuracy'
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

#Funzione per tracciare i grafici di training
def plot_graph(epochs, acc, val_acc, loss, val_loss):
    plt.figure(figsize=(12, 5))
    
    #Grafico per l'accuratezza
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, 'b', label='Train Accuracy')  
    plt.plot(epochs, val_acc, 'r', label='Validation Accuracy')  
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    
    #Grafico per la loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, 'b', label='Train Loss')
    plt.plot(epochs, val_loss, 'r', label='Validation Loss')  
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.show()

#Funzione principale per allenare il modello
def main():
    #Carica e pre-processa i dati
    (X_train, X_val, y_train, y_val), (X_test, y_test) = load_and_preprocess_data('A_Z Handwritten Data.csv')
    model = build_model()
    
    #Imposta EarlyStopping per fermare l'allenamento se la loss non migliora
    early_stop = EarlyStopping(monitor='val_loss', patience=5, verbose=1)
    
    #Allena il modello
    history = model.fit(X_train, y_train, epochs=10, batch_size=200, validation_data=(X_val, y_val), callbacks=[early_stop])
    
    #Salva il modello allenato
    model.save('letters_model.h5', include_optimizer=True)
    print(model.summary())
    
    #Traccia i grafici di accuratezza e loss
    plot_graph(range(1, len(history.history['accuracy'])+1), history.history['accuracy'], history.history['val_accuracy'], history.history['loss'], history.history['val_loss'])
    
    #Valuta il modello sui dati di train, validazione e test
    print(f"Train Accuracy: {model.evaluate(X_train, y_train, verbose=0)[1] * 100:.2f}%")
    print(f"Validation Accuracy: {model.evaluate(X_val, y_val, verbose=0)[1] * 100:.2f}%")
    print(f"Test Accuracy: {model.evaluate(X_test, y_test, verbose=0)[1] * 100:.2f}%")

if __name__ == "__main__":
    main()
