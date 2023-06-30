#import libraries
import cv2
from deepface.detectors import FaceDetector
import json
import numpy as np
import sys
import os

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
detector_name=conf["detector_name"] #change model name to get diferents results: "opencv", "ssd", "dlib", "mtcnn", "retinaface" or "mediapipe"
detector = FaceDetector.build_model(detector_name)
users= dict() #Memory of all users

#Configurations for the pipeline
exchange_in = "Exchange_in_userR"
type_exchange_in = "fanout"
queue_in = "Buffer_userR"
exchange_out = "Exchange_out_userR"
queue_out = ""

#Main function userRecognition
"""
Elementos de Entrada
img= imagen de un frame en arreglo np.array
detector = Modelo de deteccion de deepface, por defecto es mediapipe en el archivo conf
detector_name = nombre del modelo de deteccion entre 6 posibles, por defecto es mediapipe en el archivo conf
contador= numero del frame actual

Elementos de salida
image_data= diccionario cuyas keys equivalen al numero de usuario (desde 1 hasta la cantidad maxima) y con su valor una lista de tuplas con los siguientes elementos
-face: np array correspondiente a la imagen de la cara detectada
-x: punto x correspondiente a la esquina superior izquierda de la cara detectada
-y: punto y correspondiente a la esquina superior izquierda de la cara detectada
-w: ancho de la imagen de la cara detectada
-h: alto de la imagen de la cara detectada
-x_medium: punto x del centro de la cara detectada
-y_medium: punto y del centro de la cara detectada
-frame_position: valor int del frame correspondiente
-visible: valor booleano que indica si la cara fue detectada o no. En caso de no ser detectada, es false y la cara corresponde al del último frame donde si se encontro la cara
"""

def userRecognition(img,detector,detector_name,contador):
  image_data= dict()
  # To improve performance, optionally mark the image as not writeable to pass by reference.
  image=img
  image.flags.writeable = False
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  obj = FaceDetector.detect_faces(detector, detector_name, image)

  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  duplicate=True

  #Modify first time
  if len(obj) == 0 and len(users) == 0:
    firstTime= True
  else:
    firstTime= False

  #Duplicate previous frames if there is not detection
  if len(obj)== 0 and not firstTime:
    for number,info in users.items():
        users[number].append((info[-1][0],info[-1][1],info[-1][2],info[-1][3],info[-1][4],info[-1][5],info[-1][6],contador, False))
    duplicate=False

  #Detect faces in the frame
  for num in range(0,len(obj)):
    face, region = obj[num]
    x,y,w,h=region[0],region[1],region[2],region[3]
    x_medium,y_medium= (x+x+w)/2,(y+y+h)/2

    if firstTime: #If first frame, add new users to dictionary
      users[str(num+1)]=list()
      users[str(num+1)].append((face,x,y,w,h,x_medium,y_medium,contador,True))
    else:
      if duplicate: #Duplicate previous frames for users with not detection
        for number,info in users.items():
          users[number].append((info[-1][0],info[-1][1],info[-1][2],info[-1][3],info[-1][4],info[-1][5],info[-1][6],contador, False))
        duplicate=False
      flag = True
      for number,info in users.items(): #Detect new face position of previous detected user
        if (abs(x_medium-info[-2][5]) < 280 and abs(y_medium-info[-2][6]) < 160):
          del users[number][-1]
          users[number].append((face,x,y,w,h,x_medium,y_medium,contador,True))
          flag = False
          break
      if flag: #Add a new non existing face
        users[str(len(users.keys())+1)]=list()
        if num < len(obj):
          users[str(len(users.keys()))].append((face,x,y,w,h,x_medium,y_medium,contador-1,True))
          users[str(len(users.keys()))].append((face,x,y,w,h,x_medium,y_medium,contador,True))
        else:
          users[str(len(users.keys()))].append((face,x,y,w,h,x_medium,y_medium,contador,True))

  #Change numbers of users
  for num1, info in users.items():
    for num2, info in users.items():
      if (num1!=num2 and (not firstTime)):
        new_y_medium= users[str(num1)][-1][6]
        new_x_medium= users[str(num1)][-1][5]
        y_medium_other= users[str(num2)][-1][6]
        x_medium_other= users[str(num2)][-1][5]
        image_h= 320 #Y position
        if ((new_y_medium < image_h and y_medium_other < image_h) or (new_y_medium >= image_h and y_medium_other >= image_h)):
          if (new_x_medium < x_medium_other and int(num1) > int(num2)):
            test= users[str(num1)]
            test2= users[str(num2)]
            users[str(num2)]= test
            users[str(num1)]=test2
        elif(new_y_medium < image_h and y_medium_other >= image_h):
          if(int(num1)> int(num2)):
            test= users[str(num1)]
            test2= users[str(num2)]
            users[str(num2)]= test
            users[str(num1)]=test2
        elif(new_y_medium >= image_h and y_medium_other < image_h):
          if(int(num1) < int(num2)):
            test= users[str(num1)]
            test2= users[str(num2)]
            users[str(num2)]= test
            users[str(num1)]=test2
  
  #Send last detection
  for num, info in users.items():
    image_data[num]=info[-1]
  return dict(sorted(image_data.items()))


def main():
  #Connection
  channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
  channel = helpers.declare(channel, conf[exchange_in], type_exchange_in, conf[queue_in])

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      users.clear()
      channel.basic_publish(exchange=conf[exchange_out], routing_key="", body=body)
      return
    if helpers.is_save(body):
      channel.basic_publish(exchange=conf[exchange_out], routing_key="", body=body)
      return
    
    datos = json.loads(body)
    #Extract image and decode to use on userRecognition function
    image= np.frombuffer(helpers.encode(datos["data"], datos["format_byte"]), dtype=np.uint8)
    image = cv2.imdecode(image,cv2.IMREAD_COLOR)
    position= datos["position"]
    data = userRecognition(image,detector,detector_name,int(position))
    users_frame=dict()

    #Send elements of the userRecognition function
    for num,info in data.items():
      face,x,y,w,h,x_medium,y_medium,frame_position,visible=info
      users_frame[num]=dict()
      users_frame[num]["x"]=int(x)
      users_frame[num]["y"]=int(y)
      users_frame[num]["width"]=int(w)
      users_frame[num]["height"]=int(h)
      users_frame[num]["x_medium"]=float(x_medium)
      users_frame[num]["y_medium"]=float(y_medium)
      users_frame[num]["position"]=frame_position
      users_frame[num]["visible"]=visible
    datos["users"]=users_frame

    #Publishing info to exchange_userr
    channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=json.dumps(datos))
    if(len(datos["users"])> 0):
      print("[x] Sent userrecognition data of users ", datos["users"].keys(), " on frame ", datos["position"], flush=True)

  channel.basic_consume(queue=conf[queue_in], on_message_callback=callback, auto_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C',flush=True)
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