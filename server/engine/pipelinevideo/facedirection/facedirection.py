#Import libraries
import json
import sys
import os
import math
import mediapipe as mp
import numpy as np
import cv2

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
face_mesh = []

#Configurations for the pipeline
exchange_in = "Exchange_out_userR"
type_exchange_in = "fanout"
queue_in = "Buffer_fd"
exchange_out = "Exchange_facedirection"
queue_out = "Buffer_test_video"

#Main function faceDirection
"""
Elementos de entrada
face: nparray correspondiente a la imagen de una cara
num: numero del usuario
frameRate: frameRate del video 
x_medium: punto x central de la imagen de la cara
y_medium: punto y central de la imagen de la cara
w: ancho de la imagen de la cara
h: alto de la imagen de la cara
alpha: valor de angulo de la camara, por defecto es 45°

Valores de salida
angles: arreglo con los angulos x,y de la cara
yaw: inclinacion del eje x
pitch: inclinacion del eje y
roll: inclinacion del eje z
landmark: arreglo de 468 puntos x,y,z en tuplas que poseen los puntos de deteccion de cara de mediapipe
"""
def rotation_matrix_to_angles(rotation_matrix):
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2))
    z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    return np.array([x, y, z]) * 180. / math.pi

face_coordination_in_real_world = np.array([
        [285, 528, 200],
        [285, 371, 152],
        [197, 574, 128],
        [173, 425, 108],
        [360, 574, 128],
        [391, 425, 108]
    ], dtype=np.float64)

def faceDirection(image, i, x_, y_, w_, h_):
    i = i - 1
    face = image[y_:y_ + h_, x_:x_ + w_]
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    if i >= len(face_mesh):
        face_mesh.append(mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5))
    
    results = face_mesh[i].process(face)
    h, w, _ = face.shape
    face_coordination_in_image = []
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [1, 9, 57, 130, 287, 359]:
                    x, y = int(lm.x * w), int(lm.y * h)
                    face_coordination_in_image.append([x, y])

            focal_length = 1 * w
            cam_matrix = np.array([[focal_length, 0, w / 2], [0, focal_length, h / 2], [0, 0, 1]])
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            face_coordination_in_image = np.array(face_coordination_in_image, dtype=np.float64)
            success, rotation_vec, transition_vec = cv2.solvePnP( face_coordination_in_real_world, face_coordination_in_image, cam_matrix, dist_matrix)
            rotation_matrix, jacobian = cv2.Rodrigues(rotation_vec)

        yaw, pitch, roll = rotation_matrix_to_angles(rotation_matrix)
        return yaw, pitch, roll, list(face_landmarks.landmark)
    return None, None, None, None

def main():
  #Connection
  channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
  channel = helpers.declare(channel, conf[exchange_in], type_exchange_in, conf[queue_in])

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      face_mesh.clear()
      channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=body)
      return
    if helpers.is_save(body):
      channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=body)
      return
    datos = json.loads(body)
    for user, data in datos["users"].items():
      image= np.frombuffer(helpers.encode(datos["data"], datos["format_byte"]), dtype=np.uint8)
      image = cv2.imdecode(image,cv2.IMREAD_COLOR)

      yaw, pitch, roll, landmark= faceDirection(image, int(user), data["x"], data["y"], data["width"], data["height"])
      angles = [0,0]
      angles_vision=(90,180)
      center = (int(data["y"] + data["height"] / 2), int(data["x"] + data["width"] / 2))
      if center[0] < image.shape[0] / 2:
        angles[0] = angles_vision[0] - ((center[0] * angles_vision[0]) / (image.shape[0] / 2))
        angles[1] = ((center[1] * angles_vision[1]) / image.shape[1])
      else:
        angles[0] = angles_vision[0] - ((center[0] * angles_vision[0]) / (image.shape[0] / 2) - angles_vision[0])
        angles[1] = ((center[1] * angles_vision[1]) / image.shape[1]) + angles_vision[1]
      datos["users"][user]["angles"]= angles
      datos["users"][user]["yaw"]= yaw
      datos["users"][user]["pitch"]= pitch
      datos["users"][user]["roll"]= roll
      #datos["users"][user]["landmark"]= landmark
    channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=json.dumps(datos))
    if len(datos["users"]) > 0:
      print("[x] Sent facedirection data of users ", datos["users"].keys(), " on frame ", datos["position"], flush=True)

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