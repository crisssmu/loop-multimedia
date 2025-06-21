import tkinter as tk 
from tkinter import *
import sys
from pathlib import Path

# Agrega el path a la raíz del proyecto (donde está la carpeta utils/)
sys.path.append(str(Path(__file__).resolve().parent.parent))

import loop_media 
from utils.monitor_utils import Monitor
import threading as th
import FormaterTime as ft
from extension_media import ExtensionMedia as ext

video_thread = None

def out_entry(event):
    
    root.focus_set()

path = ext.get_path()

file_video = ext.list_file_videos()

file_image = ext.list_file_imagen()

moni = Monitor.get_monitores()


def select_file():
    if(select_media.get() == 0):
        for i, file in enumerate(file_video):
            if(select_archive.get() == i):
                menu_button_archive.config(text=file)
                print(f"Seleccionaste: {file}")
                return file
    else:
        for i, file in enumerate(file_image):
            if(select_archive.get() == i):
                menu_button_archive.config(text=file)
                print(f"Seleccionaste: {file}")
                return file


def select_monitor():
    for i, monitor in enumerate(moni):
        if(select_moni.get() == i):
            menu_button_moni.config(text=monitor.name)
            print(f"Seleccionaste: {monitor.name} indice: {i}")
            return i

def play_media():
    loop_media.stop_event.clear()
    video_path = select_file()
    image_path = select_file()
    tiempo_intermedio = ft.convert_seconds(loop_hour.get(), loop_min.get(), loop_seg.get())
    index_moni = select_monitor()
    image_duration = ft.convert_seconds(time_hr_im.get(), time_min_im.get(), time_seg_im.get())
    type_media = select_media.get()
    loop_media.loop_video(video_path, image_path, tiempo_intermedio, index_moni, image_duration, type_media)

def block_entry():
    menu_button_moni.config(state=DISABLED)
    menu_button_archive.config(state=DISABLED)
    loop_hour.config(state=DISABLED)
    loop_min.config(state=DISABLED)
    loop_seg.config(state=DISABLED)
    time_hr_im.config(state=DISABLED)
    time_min_im.config(state=DISABLED)
    time_seg_im.config(state=DISABLED)
    menu_button_media.config(state=DISABLED)

def button_play(event=None):
    global video_thread
    if video_thread and video_thread.is_alive():
        print("Video is already playing")
        return
    out_entry(event)
    thread = th.Thread(target=play_media)
    thread.daemon = False
    thread.start()
    
def on_closing():
    loop_media.stop_event.set()
    if video_thread and video_thread.is_alive():
        video_thread.join()
    root.destroy()

def see_widgets():
    y_time_img = center_y-10
    time_img_label.place(x=center_x-250, y=y_time_img)
    separate3.place(x=center_x-100, y=y_time_img)
    separate4.place(x=center_x-50, y=y_time_img)
    time_hr_im.place(x=center_x-130, y=y_time_img)
    time_min_im.place(x=center_x-80, y=y_time_img)
    time_seg_im.place(x=center_x-30, y=y_time_img)

def hide_widgets():
    time_img_label.place_forget()
    separate3.place_forget()
    separate4.place_forget()
    time_hr_im.place_forget()
    time_min_im.place_forget()
    time_seg_im.place_forget()

def choose_type():
    menu_archive.delete(0, 'end')
    if(select_media.get() == 0):
        menu_button_media.config(text="Video")
        file = file_video
        hide_widgets()
        y_new_moni = y_moni
    else:
        menu_button_media.config(text="Imagen")
        file = file_image
        see_widgets()
        y_new_moni = center_y+50
    choose_moni.place(x=center_x-250, y=y_new_moni)
    menu_button_moni.place(x=center_x-130, y=y_new_moni)   

    for i, file in enumerate(file):
        menu_archive.add_radiobutton(label=file, value=i, variable=select_archive, command=select_file) 
    
    return file
    
    
# Raiz de la interfaz
root = Tk()
# Tamaño de la ventana
window_width = 650  
window_height = 450

# Configuración de la ventana
root.title("Interfaz Grafica")
root.iconbitmap("icono.ico")
root.resizable(False, False)
root.attributes('-topmost',1)
root.config(bg = "#FDF8E1")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(window_width // 2)
center_y = int(window_height // 2)

root.geometry(f"{window_width}x{window_height}")

# Cuerpo de la interfaz

# Type of media archive
select_media = IntVar(value=0)

menu_media_label = Label(root, text='Tipo:', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x+100, y=center_y-150)

menu_button_media = Menubutton(root,bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_button_media.place(x=center_x+150, y=center_y-150)
menu_media = tk.Menu(menu_button_media, tearoff=False)
menu_button_media["menu"] = menu_media

menu_media.add_radiobutton(label="Video", value=0, variable=select_media, command=choose_type)
menu_media.add_radiobutton(label="Imagen", value=1, variable=select_media, command=choose_type)

# time duration to image

time_img_label = ft.format_time_label(root, 'Tiempo ' + '\n de la imagen:')
time_hr_im = ft.format_hour(root)
separate3 = ft.separate(root)
time_min_im = ft.format_minute(root)
separate4 = ft.separate(root)
time_seg_im = ft.format_second(root)

time_hr_im.bind("<Return>", out_entry)
time_min_im.bind("<Return>", out_entry)
time_seg_im.bind("<Return>", out_entry)

# Drop-down menu to choose archive
archive_label = Label(root, text='Archivo:', bg="#FDF8E1", fg="black", font=("Arial", 16)).place(x=center_x-250, y=center_y-150)

select_archive = IntVar()

menu_button_archive = Menubutton(root, text='Selecciona el archivo' ,bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_button_archive.place(x=center_x-130, y=center_y-150)
menu_archive = tk.Menu(menu_button_archive, tearoff=False)
menu_button_archive["menu"] = menu_archive

# #Time duration to loop
y_loop = center_y-80

loop_time_label = ft.format_time_label(root, 'Tiempo ' +'\nloop: ')
loop_time_label.place(x=center_x-250, y=y_loop)
loop_hour = ft.format_hour(root)

loop_separate = ft.separate(root)

loop_min = ft.format_minute(root)

loop_separate2 = ft.separate(root)
loop_seg = ft.format_second(root)


loop_hour.place(x=center_x-130, y=y_loop)
loop_hour.bind("<Return>", out_entry)

loop_separate.place(x=center_x-100, y=y_loop)

loop_min.place(x=center_x-80, y=y_loop)
loop_min.bind("<Return>", out_entry)

loop_separate2.place(x=center_x-50, y=y_loop)

loop_seg.place(x=center_x-30, y=y_loop)
loop_seg.bind("<Return>", out_entry)

for widget in (loop_hour, loop_min, loop_seg, time_hr_im, time_min_im, time_seg_im):
    widget.bind("<FocusIn>", ft.focus_time)
    widget.bind("<FocusOut>", ft.lost_focus_time)

# drop-down menu to choose monitor
y_moni = center_y - 10

choose_moni = Label(root, text='Monitor:', bg="#FDF8E1", fg="black", font=("Arial", 16))
choose_moni.place(x=center_x-250, y=y_moni)

# drop-down menu
select_moni = tk.IntVar()
menu_button_moni = Menubutton(root, text='Selecciona el monitor' ,bg="#FFFFFF", fg="black", font=("Arial", 16))
menu_moni  = tk.Menu(menu_button_moni , tearoff=False)
menu_button_moni ["menu"] = menu_moni

for i, monitor in enumerate(moni):
    menu_moni.add_radiobutton(label=monitor.name, value=i, variable = select_moni, command=select_monitor)

menu_button_moni.grid(row=len(moni), column=1)
menu_button_moni.place(x=center_x-130, y=y_moni)

choose_type() #Eliges el tipo de archivo y se agregar la lista despegable

# Boton para reproducir
button = Button(root, text='Reproducir', command=block_entry)
button.place(x=center_x+50, y=center_y+100)
button.bind("<Button-1>", button_play)

button_exit = Button(root, text='Salir', command=on_closing)
button_exit.place(x=center_x-50, y=center_y+100)


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

#prueba