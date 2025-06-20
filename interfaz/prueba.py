import threading
import time

def tarea():
    for i in range(5):
        print("Tarea ejecutandose")
        time.sleep(1)

mi_hilo = threading.Thread(target=tarea)
mi_hilo.start()

print("Hilo principal ejecutandose")