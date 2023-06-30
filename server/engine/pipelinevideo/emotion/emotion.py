import cv2
import sys
import pika
import json
import sys
import os
import numpy as np
from deepface import DeepFace as dp
#sys.path.append('../')S
#sys.path.append(''.join((os.getcwd(), '/server/pipeline-video/config')))
#sys.path.append(''.join((os.getcwd(), '/server/pipeline-video/helpers')))
import config.config as config
import helpers.helpers as helpers
conf= config.CONFIG
cont = 0

list_cords = []#Lista de coordenadas de las caras
list_aux = {}
var_aux =any
def main():
    
    channel = helpers.connect(conf["user"],conf["password"],conf["host"], conf["port"],conf["timeout"])
    channel = helpers.declare(channel,conf["exchange_direct"],"direct",conf["queue2"])
    print("PAso")
    def callback(ch, method, properties, body):
        print("LEgga calbdack")
        #faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        global list_cords#Lista de coordenadas de las caras
        global list_aux
        global var_aux
        #print("Entro callback")
        global cont 
        cont +=1
        
        body = body.decode("ISO-8859-1")
        body = json.loads(body)
        #print("*"*6+"BODY"+"*"*6)
        #print(body)
        data = body["face"].encode("ISO-8859-1")
        i = np.frombuffer(data,dtype=np.uint8)

        data = np.fromstring(data, np.uint8)
        
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        #cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
        cv2.imwrite("result.jpg",data)
        try:
            data_face = dp.analyze(img_path=data, detector_backend="mediapipe" , actions = ['age', 'gender', 'race', 'emotion'], enforce_detection=True)
            var_aux = data_face
            print(" [x] Received %d" % cont)
        except:
            data_face = var_aux
            print('Cara no encontrada, estimacion anterior generada')
        body['age']=data_face['age']
        body['gender']=data_face['gender']
        body['race']=data_face['dominant_race']
        body['emotion']=data_face['dominant_emotion']
        channel.basic_publish(exchange=conf["exchange_direct"], routing_key=conf["queue4"], body=json.dumps(body))
        #print(list_cords)
        #print("*"*6+"Data"+"*"*6)
        print('Emocion principal=> '+data_face['dominant_emotion']+'\nRaza =>' + data_face['dominant_race']+'\nEdad=> '+str(data_face['age'])+'\nGenero =>'+data_face['gender'])
    channel.basic_consume(queue=conf["queue2"], on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
