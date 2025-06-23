
import pygame
from screeninfo import get_monitors as screen_monitor
import ctypes

class Monitor:
    def __init__(self, name, width, height, x, y):
        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def __str__(self):
        return f"Monitor: {self.name}, Resolucion: {self.width}x{self.height}, Posicion: {self.x}x{self.y}"
    
    @staticmethod
    def get_monitores():
        monitores = []
        for i, monitor in enumerate(screen_monitor()):
            name = f"Monitor {i}"
            monitores.append(Monitor(name, monitor.width, monitor.height, monitor.x, monitor.y))
        return monitores

    @classmethod
    def list_monitors(cls):
        monitores = cls.get_monitores()
        for i, monitor in enumerate(monitores):
            print(f"Monitor {i}: {monitor.name}")
            print(f"Resolucion: {monitor.width}x{monitor.height}")
            print(f"Posicion: {monitor.x}x{monitor.y}")
            print()
    
    def select_monitor(index_moni):
        monitor = screen_monitor()[index_moni]
        
        return monitor
    def send_media_to_monitor(monitor):
        pygame.init()
        
        windowms = pygame.display.set_mode((monitor.width, monitor.height), pygame.NOFRAME)
        
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SetWindowPos(hwnd, 0, monitor.x, monitor.y, 0, 0, 0x0001 )
        
        return windowms

