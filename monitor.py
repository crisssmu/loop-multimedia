import cv2
import pygame
from screeninfo import get_monitors
import ctypes

monitores = get_monitors()

for i, monitor in enumerate(monitores):
    print(f"Monitor {i}: {monitor.name}")
    print(f"clsResolucion: {monitor.width}x{monitor.height}")
    print(f"Posicion: {monitor.x}x{monitor.y}")
    print()

indice_monitor_deseado = int(input("Ingrese el índice del monitor deseado: "))
monitor = monitores[indice_monitor_deseado]

video_path = "precios-esq19.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

pygame.init()
ventana = pygame.display.set_mode((monitor.width, monitor.height), pygame.NOFRAME)

hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowPos(hwnd, 0, monitor.x, monitor.y, 0, 0, 0x0001)

def escalar_frame(frame):
    return cv2.resize(frame, (monitor.width, monitor.height))

reloj = pygame.time.Clock()
running = True

while running and cap.isOpened():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    ret, frame = cap.read()
    if not ret:
        break

    frame = escalar_frame(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    ventana.blit(frame, (0, 0))
    pygame.display.update()
    reloj.tick(fps)

cap.release()
pygame.quit()
