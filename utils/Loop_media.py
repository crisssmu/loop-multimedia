
import time
from utils.monitor_utils import Monitor 
from utils.image_utils import Image 
from utils.video_utils import Video 
import threading as th


# Modificado 12/06/2025 02:27 am
index_moni = 0
stop_event = th.Event()

def loop_video(path, intermediate_time, index_moni, duration_time, op):
    
    try:
        while not stop_event.is_set():
            if(op == 0):
                print('Reproduciendo video...')
                video =Video(path, stop_event)
                video.watch_video(index_moni)
                if stop_event.is_set():
                    print('Video pausado...')
                    break
                print('Esperando ', intermediate_time, ' segundos...')
            else:
                if(op == 1):
                    print('Reproduciendo imagen...')
                    image = Image(path, stop_event)
                    image.watch_image(index_moni, duration_time)
                    if stop_event.is_set():
                        print('Imagen pausada...')
                        break
                    print('Esperando ', intermediate_time, ' segundos...')
            for i in range(intermediate_time):
                if stop_event.is_set():
                        break
                print(intermediate_time - i, 'segundos restantes')
                time.sleep(1)
    except KeyboardInterrupt:
        print('\nPrograma finalizado por el usuario')
        stop_event.set()

