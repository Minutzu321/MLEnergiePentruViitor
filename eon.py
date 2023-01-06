import requests
import json
import numpy as np
from datetime import datetime
import pickle
import socket
from configparser import ConfigParser
from os import path
import time

#functia care cere de la server datele cu privire la vreme
def getData():
    URL = 'secret'
    raspuns = requests.get(URL)
    return json.loads(raspuns.text)

#functiile care aranjeaza datele intr-o lista pentru ca algoritmul sa le aiba la indemana

#ia lista de date care corespunde cu data curenta
def getAcum(jsn):
    nori = jsn['current']['clouds']
    for p in jsn['hourly']:
        if p['dt'] <= jsn['current']['sunset']:
            print("ora "+str(datetime.utcfromtimestamp(p['dt']).hour))
            nori = (nori + p['clouds']) / 2
    return [
    jsn['current']['dt'],
    jsn['current']['sunrise'],
    jsn['current']['sunset'],
    jsn['current']['pressure'],
    jsn['current']['humidity'],
    jsn['current']['dew_point'],
    jsn['current']['uvi'],
    nori
    ]

def toDatasetFormat(lista):
    rezultat = []
    dt = datetime.utcfromtimestamp(lista[0])
    rezultat.append(dt.hour)
    rezultat.append(dt.day)
    rezultat.append(dt.month)
    rasarit_dt = datetime.utcfromtimestamp(lista[1])
    rezultat.append(rasarit_dt.hour)
    apus_dt = datetime.utcfromtimestamp(lista[2])
    rezultat.append(apus_dt.hour)
    for i in range(3,len(lista)):
        rezultat.append(lista[i])
    return rezultat
    

#ia listele de date pentru zilele urmatoare
def getZilnic(jsn):
    date = []
    for p in jsn['daily']:
        date.append(
        [
            p['dt'],
            p['sunrise'],
            p['sunset'],
            p['pressure'],
            p['humidity'],
            p['dew_point'],
            p['uvi'],
            p['clouds'],
        ]
        )
    return date

def getCurrentDataF():
    return toDatasetFormat(getAcum(getData()))





def getDataDinFisier():
    Xs = []
    ys = []
    with open('datex copy.data', 'rb') as fisier:
        Xs =  pickle.load(fisier)
    with open('datey copy.data', 'rb') as fisier:
        ys =  pickle.load(fisier)
    return Xs, ys

def saveDataInFisier(Xs, ys):
    with open('datex.data', 'wb') as fisier:
        pickle.dump(Xs, fisier)
    with open('datey.data', 'wb') as fisier:
        pickle.dump(ys, fisier)

def addDataInFisier(X,y):
    try:
        Xs, ys = getDataDinFisier()
        Xs.append(X)
        ys.append(y)
        saveDataInFisier(Xs,ys)
    except:
        saveDataInFisier([X],[y])



# curent = getCurrentDataF()
# addDataInFisier(curent,[3027])
# Xs, ys = getDataDinFisier()
# print(Xs, ys)
# exit()

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers.experimental import preprocessing
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

#lista pentru datele pe care le introducem
Xs = []
#lista pentru datele cu care antrenam algoritmul(in zacul nostru, energia totala a panourilor solare)
ys = []

def modeleaza_datasetul(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:(i + time_steps)]
        Xs.append(v)        
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

#modelul de inteligenta artificiala care va trebui sa prezica valoarea data de panourile solare

#acest model foloseste doua randuri de neuroni bidirectionali LSTM(Long Short Term Memory)
#pentru a detecta tipare sau anomalii care depind de o anumita data sau ora.
model = keras.Sequential([
    keras.layers.Bidirectional(
        keras.layers.LSTM(32, input_shape=(1,6)),
        # keras.layers.LSTM(32, input_shape=(1,6)),
        ),
    
    keras.layers.Dense(120, activation="sigmoid"),
    keras.layers.Dense(120, activation="relu"),
    keras.layers.Dense(10, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")
])

#ii setam modelului un optimizer care va avea grija de procesul de "invatare" al algoritmului
model.compile(optimizer="adam", loss="mean_squared_error", metrics=['accuracy'])

def saveplot(istoric):
    from datetime import date
    today = date.today()
    data = today.strftime("%d%m%Y")

    plt.plot(istoric.history['accuracy'])
    plt.plot(istoric.history['val_accuracy'])
    plt.title('acuratetea modelului')
    plt.ylabel('acuratete')
    plt.xlabel('epoca')
    plt.legend(['antrenament', 'validare'], loc='upper left')
    plt.savefig('z/acc'+data+'.png')
    plt.clf()
    plt.plot(istoric.history['loss'])
    plt.plot(istoric.history['val_loss'])
    plt.title('valorile de pierdere ale modelului')
    plt.ylabel('pierdere')
    plt.xlabel('epoca')
    plt.legend(['antrenament', 'validare'], loc='upper left')
    plt.savefig('z/pierdere'+data+'.png')

def getLuminozitateGenerala():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.0.178', 9057))
        data = sock.recv(1024)
        data = data.decode()
        sock.close()
        return data
    except:
        return 45555


def saveConf(config_object):
    with open('eon.ini', 'w') as conf:
        config_object.write(conf)

def antreneaza(Xs, ys):
    transfx = RobustScaler()
    transfy = RobustScaler()
    transfx.fit(np.array(Xs))
    transfy.fit(np.array(ys))
    Xs = transfx.transform(Xs)
    ys = transfy.transform(ys)
    Xs, ys = modeleaza_datasetul(Xs, ys, 10)
    istoric = model.fit(Xs, ys, epochs=50, validation_split=0.2, shuffle=False)
    saveplot(istoric)

# Xs, ys = getDataDinFisier()
# antreneaza(Xs, ys)
# print(model.predict(modeleaza_datasetul([getCurrentDataF()],[1],1)[0]))

def start():
    config_object = ConfigParser()
    if not path.exists("eon.ini"):
        luminozitate = getLuminozitateGenerala()
        curent = getCurrentDataF()
        addDataInFisier(curent,[luminozitate])
        config_object["TIMP"] = {
            "ultima": str(time.time())
        }
        saveConf(config_object)
    else:
        config_object.read("eon.ini")

    while True:
        try:
            if time.time() - float(config_object["TIMP"]["ultima"]) >= 3600:
                luminozitate = getLuminozitateGenerala()
                curent = getCurrentDataF()
                addDataInFisier(curent,[luminozitate])
                config_object["TIMP"] = {
                    "ultima": str(time.time())
                }
                saveConf(config_object)
                Xs, ys = getDataDinFisier()
                if len(ys) > 100:
                    antreneaza(Xs, ys)
        except:
            pass

Xs, ys = getDataDinFisier()
print(len(Xs), len(ys))
pops = []
for i,jsx in enumerate(ys):
    try:
        num = float(jsx[0])
        if num == 45555 or num == 0:
            pops.append(i)
    except:
        pops.append(i)


Xs = [x for j, x in enumerate(Xs) if j not in pops]
ys = [y for j, y in enumerate(ys) if j not in pops]
print("ys",len(ys))
print("xs",len(Xs))
antreneaza(Xs, ys)
