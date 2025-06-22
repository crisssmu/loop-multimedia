
import interfaz.Gui as gui
from utils.Extension_media import ExtensionMedia as ext
from utils.Monitor_utils import Monitor as monitor

path = ext.get_path()
imagenes = ext.list_file_imagen(path)
videos = ext.list_file_videos(path)
monitors = monitor.get_monitores()
list_monitor = monitor.list_monitors()

print(path)
print(imagenes)
print(videos)

gui.start_interface(videos, imagenes, monitors)
