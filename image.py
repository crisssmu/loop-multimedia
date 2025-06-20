import cv2
import time
import pygame
import ctypes
from screeninfo import get_monitors

monitores = get_monitors()

for i, monitor in enumerate(monitores):
    print(f"Monitor {i}: {monitor.name}")
    print(f"clsResolucion: {monitor.width}x{monitor.height}")
    print(f"Posicion: {monitor.x}x{monitor.y}")
    print()

index_moni = int(input("Ingrese el índice del monitor deseado: "))
monitor = monitores[index_moni]
pygame.init()
windowms = pygame.display.set_mode((monitor.width, monitor.height), pygame.NOFRAME)

hwnd = pygame.display.get_wm_info()["window"]
ctypes.windll.user32.SetWindowPos(hwnd, 0, monitor.x, monitor.y, 0, 0, 0x0001)


img = cv2.imread("imagen1.jpg", cv2.IMREAD_COLOR)

if img is None:
    print("Error opening video stream or file")
    exit()

cv2.resize(img, (1920, 1080))
pygame.init()

start_time = time.time()
img = pygame.surfarray.make_surface(img.swapaxes(0, 1))

running = True

while running and (time.time() - start_time) <= 10:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = False

    windowms.blit(img, (0, 0))
    pygame.display.update()
    
cv2.destroyAllWindows()
pygame.quit()