import cv2
import time
import datetime
import pygame
from screeninfo import get_monitors
import ctypes

# Modificado 12/06/2025 02:27 am
index_moni = 0
def get_moni():
    monitores = get_monitors()
    return monitores

def list_moni():
    for i, monitor in enumerate(get_moni()):
        print(f"Monitor {i}: {monitor.name}")
        print(f"Resolucion: {monitor.width}x{monitor.height}")
        print(f"Posicion: {monitor.x}x{monitor.y}")
        print()


def choose_monitor(index_moni):

    monitor = get_moni()[index_moni]
    pygame.init()
    windowms = pygame.display.set_mode((monitor.width, monitor.height), pygame.NOFRAME)

    hwnd = pygame.display.get_wm_info()["window"]
    ctypes.windll.user32.SetWindowPos(hwnd, 0, monitor.x, monitor.y, 0, 0, 0x0001)

    return monitor, windowms

def img_monitor(img_path, index_moni, duration_seconds):
    moni, windowms = choose_monitor(index_moni)
    img = cv2.imread(img_path)

    if img is None:
        print("Error opening video stream or file")
        exit()

    img =  cv2.resize(img, (moni.width, moni.height))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_s = pygame.surfarray.make_surface(img.swapaxes(0, 1))


    clock = pygame.time.Clock()
    start_time = time.time()
    running = True
    
    while running and (time.time() - start_time) <= duration_seconds:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            windowms.blit(img_s, (0, 0))
            pygame.display.update()
            clock.tick(60)
    pygame.quit()

def video_monitor(video_path, index_moni):
    moni, windowms = choose_monitor(index_moni)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error opening video stream or file")
        exit()

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    contador_frames = 0
    duracion_segundos = total_frames/fps
    duracion = str(datetime.timedelta(seconds=int(duracion_segundos)))
    print('Duración del video: ', duracion)
    def escalar_frame(frame):
        return cv2.resize(frame, (moni.width, moni.height))

    reloj = pygame.time.Clock()
    running = True
    while running and (contador_frames < total_frames):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        ret, frame = cap.read()
        if not ret:
            break

        contador_frames += 1

        frame = escalar_frame(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

        windowms.blit(frame, (0, 0))
        pygame.display.update()
        reloj.tick(fps)

    cap.release()
    pygame.quit()

def loop_video(video_path, img_path, time_current, index_moni, duration_seconds):
    get_moni()
    list_moni()
    index_moni = int(input("Ingrese el índice del monitor deseado: "))
    op = int(input("Elige el tipo: 1 video o 2 imagen:"))

    try:
        while True:
            if(op == 1):
                print('Reproduciendo video...')
                video_monitor(video_path, index_moni)
                print('Esperando ', time_current, ' segundos...')
            else:
                 if(op == 2):
                     print('Reproduciendo imagen...')
                     img_monitor(img_path, index_moni, duration_seconds)
                     print('Esperando ', time_current, ' segundos...')
            for i in range(time_current):
                print(time_current - i, 'segundos restantes')
                time.sleep(1)
    except KeyboardInterrupt:
        print('Programa finalizado por el usuario')

loop_video("precios-esq19.mp4","",10,index_moni,0)
