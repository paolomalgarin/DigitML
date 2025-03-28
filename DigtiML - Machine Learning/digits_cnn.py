from numpy import mean, std, argmax
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import BatchNormalization, Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import numpy as np
import cv2
import os

#Funzione per caricare il dataset MNIST e preparare i dati per la CNN
def load_dataset():
    #Carica il dataset MNIST e lo separa in dati di addestramento (train) e test
    (trainX, trainY), (testX, testY) = mnist.load_data()
    
    #Reshape dei dati per farli diventare immagini 28x28x1 (1 canale per la scala di grigi)
    trainX = trainX.reshape((trainX.shape[0], 28, 28, 1))
    testX = testX.reshape((testX.shape[0], 28, 28, 1))
    
    #Conversione delle etichette da numeri a categorie (one-hot encoding)
    trainY = to_categorical(trainY)
    testY = to_categorical(testY)
    
    return trainX, trainY, testX, testY

#Funzione per normalizzare i pixel delle immagini da valori tra 0-255 a un intervallo tra 0.0 e 1.0
def prep_pixels(train, test):
    #Converte i valori in float32 e li normalizza
    train_norm = train.astype('float32') / 255.0
    test_norm = test.astype('float32') / 255.0
    return train_norm, test_norm

#Funzione per definire l'augmentation dei dati
def define_data_augmentation():
    #Imposta una serie di trasformazioni randomiche sulle immagini di addestramento per migliorare la generalizzazione
    datagen = ImageDataGenerator(
        rotation_range=10,        
        width_shift_range=0.1,    
        height_shift_range=0.1,    
        shear_range=0.2,           
        zoom_range=0.2,            
        horizontal_flip=False,     
        fill_mode='nearest'       
    )
    return datagen

#Funzione per definire la CNN per la classificazione delle cifre
def define_model():
    # Costruisce un modello sequenziale con 2 convoluzioni seguite da max pooling e un layer fully connected
    model = Sequential()
    
    #Primo layer convoluzionale con 32 filtri 3x3 e ReLU come attivazione
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(28, 28, 1)))
    model.add(BatchNormalization())  # Normalizzazione del batch
    model.add(MaxPooling2D((2, 2)))  # Max pooling 2x2
    
    #Secondo layer convoluzionale con 64 filtri 3x3
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(BatchNormalization())  # Normalizzazione del batch
    
    #Terzo layer convoluzionale con 64 filtri 3x3
    model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
    model.add(MaxPooling2D((2, 2)))  # Max pooling 2x2
    
    #Appiattimento delle caratteristiche per passare al layer fully connected
    model.add(Flatten())
    
    #Fully connected con 100 neuroni
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(BatchNormalization())  # Normalizzazione del batch
    
    #Output layer con 10 neuroni (per le 10 cifre da 0 a 9) e softmax come attivazione
    model.add(Dense(10, activation='softmax'))
    
    #Compilazione del modello con l'ottimizzatore Adam e la loss function categorical_crossentropy
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

#Funzione per valutare il modello utilizzando la k-fold cross-validation
def evaluate_model(dataX, dataY, n_folds=5):
    print("Avvio della valutazione del modello")
    scores, histories = list(), list()  #Lista per memorizzare i punteggi e le storie degli allenamenti
    kfold = KFold(n_folds, shuffle=True, random_state=1)  #Impostazione della cross-validation
    datagen = define_data_augmentation() 
    
    #Esegui il k-fold cross-validation
    for train_ix, test_ix in kfold.split(dataX):
        print("Allenamento del fold")
        
        model = define_model()  
        trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
        datagen.fit(trainX)  

        #Early stopping: ferma l'allenamento se la validazione non migliora dopo 3 epoche
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

        #Allenamento con il generatore di dati (data augmentation)
        history = model.fit(datagen.flow(trainX, trainY, batch_size=32), epochs=10, 
                            validation_data=(testX, testY), callbacks=[early_stopping], verbose=0)
        
        #Valutazione delle prestazioni sul test set
        _, acc = model.evaluate(testX, testY, verbose=0)
        print('> Accuratezza: %.3f' % (acc * 100.0))
        scores.append(acc)  
        histories.append(history) 

    print("Valutazione completata")
    return scores, histories

#Funzione per generare grafici sull'andamento della perdita e dell'accuratezza durante l'allenamento
def summarize_diagnostics(histories):
    for i in range(len(histories)):
        plt.subplot(2, 1, 1)
        plt.title('Perdita di Entropia Cross')
        plt.plot(histories[i].history['loss'], color='blue', label='allenamento')
        plt.plot(histories[i].history['val_loss'], color='orange', label='test')
        
        plt.subplot(2, 1, 2)
        plt.title('Accuratezza di Classificazione')
        plt.plot(histories[i].history['accuracy'], color='blue', label='allenamento')
        plt.plot(histories[i].history['val_accuracy'], color='orange', label='test')
    
    plt.show()

#Funzione per visualizzare la sintesi delle prestazioni del modello (accuratezza media e deviazione standard)
def summarize_performance(scores):
    print('Accuratezza: media=%.3f std=%.3f, n=%d' % (mean(scores)*100, std(scores)*100, len(scores)))
    plt.boxplot(scores) 
    plt.show()

#Funzione principale per addestrare e valutare il modello
def run_test_harness():
    try:
        #Caricamento e preparazione dei dati
        trainX, trainY, testX, testY = load_dataset()
        trainX, testX = prep_pixels(trainX, testX)
        
        #Valutazione del modello con k-fold cross-validation
        scores, histories = evaluate_model(trainX, trainY)
        datagen = define_data_augmentation()
        
        #Visualizzazione dei risultati dell'allenamento
        summarize_diagnostics(histories)
        summarize_performance(scores)
        
        print("Preparazione per salvare il modello finale")
        
        #Addestramento finale sul dataset completo prima di salvare il modello
        model = define_model()
        early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
        model.fit(datagen.flow(trainX, trainY, batch_size=32), epochs=10, 
                  validation_data=(testX, testY), callbacks=[early_stopping], verbose=0)
        
        #Salvataggio del modello addestrato
        model.save('digits_model.h5')
        print("Modello salvato correttamente")
    
    except Exception as e:
        print("Si è verificato un errore:", e)

run_test_harness()
