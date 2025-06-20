import cv2
import time as t
import datetime
import pygame
import ctypes
import monitor_utils as monit
import threading as th

# Evento de cierre compartido
stop_event = th.Event()

def send_video(video_path, index_moni):
   try:
        monitor = monit.get_moni()[index_moni]

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error opening video stream or file")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        contador_frames = 0
        duracion_segundos = total_frames / fps
        duracion = str(datetime.timedelta(seconds=int(duracion_segundos)))

        print('Duración del video: ', duracion)

        pygame.init()
        ventana = pygame.display.set_mode((monitor.width, monitor.height), pygame.NOFRAME)

        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SetWindowPos(hwnd, 0, monitor.x, monitor.y, 0, 0, 0x0001)
        def escalar_frame(frame):
            return cv2.resize(frame, (monitor.width, monitor.height))

        reloj = pygame.time.Clock()

        while not stop_event.is_set() and contador_frames < total_frames:
            ret, frame = cap.read()
            if not ret:
                break

            contador_frames += 1

            frame = escalar_frame(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            ventana.blit(frame, (0, 0))
            pygame.display.update()
            reloj.tick(fps)

            # Permitir cerrar ventana con evento de pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_event.set()
        print("Video finalizado o detenido.")
        cap.release()
        pygame.quit()
   except Exception as e:
        print('Programa finalizado por el usuario', e)
   finally:
        cap.release()
        pygame.quit()

def loop_video(video_path, tiempo_intermedio, index_moni):
    monit.get_moni()
    try:
        while not stop_event.is_set():
            print('Reproduciendo video...')
            send_video(video_path, index_moni)
            if stop_event.is_set():
                break
            print('Esperando', tiempo_intermedio, 'segundos...')
            for i in range(tiempo_intermedio):
                if stop_event.is_set():
                    break
                print(tiempo_intermedio - i, 'segundos restantes')
                t.sleep(1)
    except KeyboardInterrupt:
        print('Programa finalizado por el usuario')
        stop_event.set()

# Función para detener todo externamente
def cerrar_reproduccion():
    stop_event.set()
