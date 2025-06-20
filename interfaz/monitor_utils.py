from screeninfo import get_monitors
def get_moni():
    monitores = get_monitors()
    return monitores

def list_moni():
    for i, monitor in enumerate(get_moni()):
        print(f"Monitor {i}: {monitor.name}")
        print(f"Resolucion: {monitor.width}x{monitor.height}")
        print(f"Posicion: {monitor.x}x{monitor.y}")
        print()
