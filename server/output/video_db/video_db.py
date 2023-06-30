#import pandas as pd
import json
import config
import helpers
conf = config.CONFIG

#Configurations for the pipeline
exchange_in = "Exchange_direct_video"
type_exchange_in = "direct"
queue_in = "Buffer_output"

def video_output():
    # Connection
    con, channel = helpers.connect(conf["user"], conf["password"], conf["host"], conf["port"], conf["timeout"])
    # Declare
    channel = helpers.declare(channel, conf[exchange_in], type_exchange_in, conf[queue_in])
    
    def callback(ch, method, properties, body):
        if helpers.is_reset(body):
            return
        if helpers.is_save(body):
            return
        datos = json.loads(body)
        datos.pop("data")
        #print(datos, flush=True)
        features = {
            "position": datos["position"],
            "users": datos["users"],
        }
        helpers.send_post(
            host=config.CONFIG["host_backend"],
            nameIndicator="video_output",
            data= helpers.indicator_measure(id_analysis=datos.get("id_device"),measures=features,start_time=datos.get("time"),end_time=datos.get("time"))
        )
    try:
        channel.basic_consume(queue=conf[queue_in], on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
        channel.start_consuming()

    except KeyboardInterrupt:
        print('Interrupted', flush=True)
        channel.close()
        con.close()
        
if __name__ == '__main__':
    video_output()
