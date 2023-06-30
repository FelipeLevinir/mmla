#Import libraries
import json
import sys
import os
from person_looking import PersonLooking

import config as config
import helpers as helpers
conf= config.CONFIG

#Global elements
users_data={}

#Configurations for the pipeline
exchange_in = "Exchange_direct_video"
type_exchange_in = "direct"
queue_in = "Buffer_lh"
exchange_out = "Exchange_direct_video"
queue_out = "Buffer_output"

def main():
  #Connection
  channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
  channel = helpers.declare(channel, conf[exchange_in], type_exchange_in, conf[queue_in])

  #Callback function
  def callback(ch, method, properties, body):
    if helpers.is_reset(body):
      users_data.clear()
      channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=body)
      return
    if helpers.is_save(body):
      channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=body)
      return
    datos = json.loads(body)

    
    # #Main function
    # for i in range(0,len(datos["users"])):
    #   if str(i+1) not in users_data:
    #     users_data[str(i+1)]= (str(i+1), 0)
    #   #Obtain data from PersonLooking
    #   looking_user,looking_status,x,y,looking_time= PersonLooking.looking_position(datos["users"], i, len(datos["users"]),users_data)
    #   datos["users"][str(i+1)]["looking_user"]= looking_user
    #   datos["users"][str(i+1)]["looking_status"]= looking_status
    #   datos["users"][str(i+1)]["looking_angle"]= [x,y]
    #   datos["users"][str(i+1)]["looking_time"]= looking_time
    #   users_data[str(i+1)]= (looking_user,looking_time)
    channel.basic_publish(exchange=conf[exchange_out], routing_key=queue_out, body=json.dumps(datos))
    if len(datos["users"]) > 0:
      print("[x] Sent lookingposition data of users ", datos["users"].keys(), " on frame ", datos["position"], flush=True)
  
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