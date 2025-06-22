import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
import sys
import os
from pathlib import Path
import traceback
# Agrega el path a la raíz del proyecto (donde está la carpeta utils/)
sys.path.append(str(Path(__file__).resolve().parent.parent))
import utils.Loop_media as loop
from utils.Monitor_utils import Monitor
from exceptions.EmptyArgs import EmptyArgs as exceptions
import threading as th
import utils.FormaterTime as ft
from utils.Extension_media import ExtensionMedia as ext


video_thread = None
def start_interface(file_video, file_image, moni):
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    def out_entry(event):
        root.focus_set()

    def select_file():
        try:
            file_media = select_media.get()
            if(file_media == 0):
                for i, file in enumerate(file_video):
                    if(select_archive.get() == i):
                        menu_button_archive.config(text=file)
                        print(f"Seleccionaste: {file}")
                        exceptions.empty_file(file)
                        return file
            elif file_media == 1:
                for i, file in enumerate(file_image):
                    if(select_archive.get() == i):
                        menu_button_archive.config(text=file)
                        print(f"Seleccionaste: {file}")
                        exceptions.empty_file(file)
                        return file
            else:
                return
        except exceptions as ep:
            root.after(0, lambda e=ep:messagebox.showerror("Error", str(e)))
            print(ep)
            
        except Exception as e:
            root.after(0, lambda e=e:messagebox.showerror("Error", str(e)))
            print(e)


    def select_monitor():
        for i, monitor in enumerate(moni):
            if(select_moni.get() == i):
                menu_button_moni.config(text=monitor.name)
                print(f"Seleccionaste: {monitor.name} indice: {i}")
                return i


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

    def unblock_entry():
        menu_button_moni.config(state=NORMAL)
        menu_button_archive.config(state=NORMAL)
        loop_hour.config(state=NORMAL)
        loop_min.config(state=NORMAL)
        loop_seg.config(state=NORMAL)
        time_hr_im.config(state=NORMAL)
        time_min_im.config(state=NORMAL)
        time_seg_im.config(state=NORMAL)
        menu_button_media.config(state=NORMAL)

    def play_media():
        try:    
            loop.stop_event.clear()

            path = select_file()
            tiempo_intermedio = ft.convert_seconds(loop_hour.get(), loop_min.get(), loop_seg.get())
            index_moni = select_monitor()
            duration_time = ft.convert_seconds(time_hr_im.get(), time_min_im.get(), time_seg_im.get())
            type_media = select_media.get()

            exceptions.empty_selection(path, index_moni, type_media)

            if type_media == 0:
                exceptions.empty_time(tiempo_intermedio)
                exceptions.empty_file(path)
            else:
                exceptions.empty_time(tiempo_intermedio)
                exceptions.empty_time(duration_time)
                exceptions.empty_file(path)

            block_entry()
            loop.loop_video(path, tiempo_intermedio, index_moni, duration_time, type_media)
            
        except exceptions as ep:
            root.after(0, lambda e=ep:messagebox.showerror("Error", str(e)))
            print(ep)
            
        except Exception as e:
            root.after(0, lambda e=e:messagebox.showerror("Error", str(e)))
            print(e)
            

    def button_play(event=None):
        global video_thread
        try:
            if video_thread and video_thread.is_alive():
                print("Video is already playing")
                return
            out_entry(event)
            video_thread = th.Thread(target=play_media)
            video_thread.daemon = True
            video_thread.start()

        except Exception as e:
            print(e)

    def on_closing():
        loop.stop_event.set()
        if video_thread and video_thread.is_alive():
           video_thread.join()
        root.destroy()

    def stop():
        loop.stop_event.set()
        unblock_entry()

    def see_widgets():
        y_time_img = center_y-10
        time_img_label.place(x=x_windget, y=y_time_img)
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
        value_media = select_media.get()
        if value_media == 0:
            menu_button_archive.config(text="Selecciona el archivo")
            menu_button_media.config(text="Video")
            file = file_video
            hide_widgets()
            y_new_moni = y_moni
        elif value_media == 1:
            menu_button_archive.config(text="Selecciona el archivo")
            menu_button_media.config(text="Imagen")
            file = file_image
            see_widgets()
            y_new_moni = center_y+50
        else:
            return
        choose_moni.place(x=x_windget, y=y_new_moni)
        menu_button_moni.place(x=center_x-130, y=y_new_moni)
        menu_archive.delete(0, 'end')

        for i, file in enumerate(file):
            menu_archive.add_radiobutton(label=file, value=i, variable=select_archive, command=select_file)

        return file
    
    def on_hover(event):
        event.widget.config(cursor="hand2")
        event.widget.config(fg="white",bg="#0077b6")

    def on_leave(event):
        event.widget.config(cursor="arrow")
        event.widget.config(fg="black",bg="#48cae4")

    def on_hover2(event):
        event.widget.config(cursor="hand2")
        event.widget.config(fg="white",bg="#e5383b")

    def on_leave2(event):
        event.widget.config(cursor="arrow")
        event.widget.config(fg="black",bg="#48cae4")

    def on_leave3(event):
        event.widget.config(cursor="arrow")
        event.widget.config(fg="black",bg="#48cae4")

    def on_hover3(event):
        event.widget.config(cursor="hand2")
        event.widget.config(fg="white",bg="#0077b6")

    # Raiz de la interfaz


    root = Tk()


    # Tamaño de la ventana
    window_width = 650
    window_height = 450

    # Configuración de la ventana
    root.title("Loop Media")
    root.iconbitmap(resource_path("loopMedia_logo.ico"))
    root.resizable(False, False)
    root.attributes('-topmost',1)
    root.config(bg = "#caf0f8")
   
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(window_width // 2)
    center_y = int(window_height // 2)

    root.geometry(f"{window_width}x{window_height}")
    x_windget = center_x-260
   

    # Cuerpo de la interfaz

    # Type of media archive
    select_media = IntVar(value=-1)

    menu_media_label = Label(root, text='Tipo:', bg="#caf0f8", fg="black", font=("Arial", 16))
    menu_media_label.place(x=center_x+100, y=center_y-150)

    menu_button_media = Menubutton(root,text="Media",bg="#48cae4", fg="black", font=("Arial", 16), bd=2, relief="ridge")
    menu_button_media.place(x=center_x+150, y=center_y-150)

    menu_media = tk.Menu(menu_button_media, tearoff=False)
    menu_button_media["menu"] = menu_media

    menu_media.add_radiobutton(label="Video", value=0, variable=select_media, command=choose_type)
    menu_media.add_radiobutton(label="Imagen", value=1, variable=select_media, command=choose_type)

    # time duration to image

    time_img_label = ft.format_time_label(root, 'Tiempo ' + '\nde la imagen:')
    time_hr_im = ft.format_hour(root)
    separate3 = ft.separate(root)
    time_min_im = ft.format_minute(root)
    separate4 = ft.separate(root)
    time_seg_im = ft.format_second(root)

    time_hr_im.bind("<Return>", out_entry)
    time_min_im.bind("<Return>", out_entry)
    time_seg_im.bind("<Return>", out_entry)

    # Drop-down menu to choose archive
    archive_label = Label(root, text='Archivo:', bg="#caf0f8", fg="black", font=("Arial", 16))
    archive_label.place(x=x_windget, y=center_y-150)

    select_archive = IntVar(value=-1)

    menu_button_archive = Menubutton(root, text='Selecciona el archivo',bg="#48cae4", fg="black", font=("Arial", 16), bd=2, relief="ridge")
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

    choose_moni = Label(root, text='Monitor:', bg="#caf0f8", fg="black", font=("Arial", 16))
    choose_moni.place(x=x_windget, y=y_moni)

    # drop-down menu
    select_moni = tk.IntVar(value=-1)
    menu_button_moni = Menubutton(root, text='Selecciona el monitor' ,bg="#48cae4", fg="black", font=("Arial", 16), bd=2, relief="ridge", width=18)
    menu_moni  = tk.Menu(menu_button_moni , tearoff=False)
    menu_button_moni ["menu"] = menu_moni

    for i, monitor in enumerate(moni):
        menu_moni.add_radiobutton(label=monitor.name, value=i, variable = select_moni, command=select_monitor)

    menu_button_moni.pack()
    menu_button_moni.place(x=center_x-130, y=y_moni)

    choose_type() #Eliges el tipo de archivo y se agregar la lista despegable

    # Boton para reproducir
    y_button = center_y+110
    button = Button(root, text='Reproducir', bg="#48cae4", fg="black", font=("Arial", 16), bd=2, relief="ridge", width=10)
    button.place(x=center_x-200, y=y_button)
    button.bind("<Button-1>", button_play)

    button_exit = Button(root, text='Salir',bg="#48cae4", fg="black", font=("Arial", 16), bd=2, relief="ridge", command=on_closing, width=10)
    button_exit.place(x=center_x+100, y=y_button)
    

    button_cancel = Button(root, text='Cancelar',bg="#48cae4", fg="black", font=("Arial", 16), bd=2, relief="ridge", command=stop, width=10)
    button_cancel.place(x=center_x-50, y=y_button)

    for widg in (menu_button_archive, menu_button_media, menu_button_moni, loop_hour, loop_min, loop_seg, time_hr_im, time_min_im, time_seg_im):
        widg.bind("<Enter>", on_hover3)
        widg.bind("<Leave>", on_leave3)

    for wid in ( button, button_cancel):
        wid.bind("<Enter>", on_hover)
        wid.bind("<Leave>", on_leave)

    button_exit.bind("<Enter>", on_hover2)
    button_exit.bind("<Leave>", on_leave2)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    start_interface()