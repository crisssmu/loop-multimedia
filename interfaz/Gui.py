import ctypes
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import *
import sys
import os
from pathlib import Path

# Agrega el path a la raíz del proyecto (donde está la carpeta utils/)
sys.path.append(str(Path(__file__).resolve().parent.parent))
import utils.Loop_media as loop
from utils.monitor_utils import Monitor
from utils.EmptyArgs import EmptyArgs as exceptions
import threading as th
import utils.formater_time as ft
from utils.extension_media import ExtensionMedia as ext

video_thread = None
def start_interface(file_video, file_image, moni):
    def resource_path(relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
# events
    def click_file(event):
        try:
            value_media = select_media.get()
            if value_media == 0:
                if file_video == []:
                    exceptions.empty_file(file_video)
                    return
            elif value_media == 1:
                if file_image == []:
                    exceptions.empty_file(file_image)
                    return
            else: 
                select_file()
        except exceptions as ep:
            root.after(0, lambda e=ep:messagebox.showerror("Error", str(e)))
            print(ep)
            
        except Exception as e:
            root.after(0, lambda e=e:messagebox.showerror("Error", str(e)))
            print(e)
    
    def on_hover_button(event):
        event.widget.config(cursor="hand2")
        event.widget.config(fg="white",bg="#0077b6")
    
    def on_leave_button(event):
        event.widget.config(cursor="arrow")
        event.widget.config(fg="black",bg="#48cae4")
    
    def on_hover_exit(event):
        event.widget.config(cursor="hand2")
        event.widget.config(fg="white",bg="#e5383b")
    def on_leave_exit(event):
        event.widget.config(cursor="arrow")
        event.widget.config(fg="black",bg="#48cae4")

    def on_leave_widgets(event):
        event.widget.config(cursor="arrow")
        event.widget.config(fg="black",bg="#48cae4")
    
    def on_hover_widgets(event):
        event.widget.config(cursor="hand2")
        event.widget.config(fg="white",bg="#0077b6")
    
    def out_entry(event):
        root.focus_set()
    
    def block_entry():
        menu_button_moni.config(state=DISABLED)
        menu_button_archive.config(state=DISABLED)
        loop_min.config(state=DISABLED)
        loop_seg.config(state=DISABLED)
        time_min_im.config(state=DISABLED)
        time_seg_im.config(state=DISABLED)
        menu_button_media.config(state=DISABLED)
    
    def unblock_entry():
        menu_button_moni.config(state=NORMAL)
        menu_button_archive.config(state=NORMAL)
        loop_min.config(state=NORMAL)
        loop_seg.config(state=NORMAL)
        time_min_im.config(state=NORMAL)
        time_seg_im.config(state=NORMAL)
        menu_button_media.config(state=NORMAL)
    
    def button_play(event=None):
            global video_thread
            try:
                if video_thread and video_thread.is_alive():
                    print("Video is already playing")
                    return
                out_entry(event)
                video_thread = th.Thread(target=play)
                video_thread.daemon = True
                video_thread.start()
            except Exception as e:
                print(e)
    
    def remove_focus(event):
        widget = event.widget
        if not isinstance(event.widget, tk.Entry):
            root.focus()
    
    def see_widgets():
        time_img_label.place(x=x_windget, y=center_y-20)
        time_min_im.place(x=x_min, y=y_time_img)
        separate.place(x=x_separate, y=y_time_img)
        time_seg_im.place(x=x_seg, y=y_time_img)

    def hide_widgets():
        time_img_label.place_forget()
        separate.place_forget()
        time_min_im.place_forget()
        time_seg_im.place_forget()
    
    def set_menu_button_text(text):
        max_chars = 18
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
        menu_button_archive.config(text=text)

# Select 
    def select_type_media():
        value_media = select_media.get()
        if value_media == 0:
            menu_button_archive.config(text="Selecciona el archivo")
            menu_button_media.config(text="Video")
            file = file_video
            hide_widgets()
            y_new_moni = y_moni
            select_archive.set(-1)
        
        elif value_media == 1:
            
            menu_button_archive.config(text="Selecciona el archivo")
            menu_button_media.config(text="Imagen")
            file = file_image
            see_widgets()
            y_new_moni = center_y+50
            select_archive.set(-1)
        else:
            return
        
        choose_moni.place(x=x_windget, y=y_new_moni)
        menu_button_moni.place(x=center_x-130, y=y_new_moni)
        menu_archive.delete(0, 'end')
        for i, file in enumerate(file):
            menu_archive.add_radiobutton(label=file, value=i, variable=select_archive, command=select_file)
        return file
    
    def select_file():
        try:
            media = select_media.get()
            if(media == 0):
                for i, file in enumerate(file_video):
                    if(select_archive.get() == i):
                        menu_button_archive.config(text=set_menu_button_text(file))
                        print(f"Archivo: {file}")
                        return file
            elif media == 1:
                for i, file in enumerate(file_image):
                    if(select_archive.get() == i):
                        menu_button_archive.config(text=set_menu_button_text(file))
                        print(f"Archivo: {file}")
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
                print(f"Moni: {monitor.name} indice: {i}")
                return i

#Actions
    def play():
        try:    
            loop.stop_event.clear()
            path = select_file()
            tiempo_intermedio = ft.convert_seconds(loop_min.get(), loop_seg.get())
            index_moni = select_monitor()
            duration_time = ft.convert_seconds(time_min_im.get(), time_seg_im.get())
            type_media = select_media.get()
            exceptions.empty_selection(path, index_moni, type_media)
            if type_media == 0:
                exceptions.empty_file(path)
                exceptions.empty_time(tiempo_intermedio)
            else:
                exceptions.empty_file(path)
                exceptions.empty_time(tiempo_intermedio)
                exceptions.empty_time(duration_time)
                
            block_entry()
            loop.loop_video(path, tiempo_intermedio, index_moni, duration_time, type_media)
            
        except exceptions as ep:
            root.after(0, lambda e=ep:messagebox.showerror("Error", str(e)))
            print(ep)
            
        except Exception as e:
            root.after(0, lambda e=e:messagebox.showerror("Error", str(e)))
            print(e)
        
    
    def on_closing():
        global video_thread
        loop.stop_event.set()
        if video_thread and video_thread.is_alive():
            video_thread.join()
            stop()
        root.destroy()
    
    def stop():
        loop.stop_event.set()
        unblock_entry()
    
# Interface root
    root = Tk()

# window size
    window_width = 650
    window_height = 450

# Program window settings
    root.title("Loop Media")
    root.iconbitmap(resource_path("loopMedia_logo.ico"))
    root.resizable(False, False)
    root.attributes('-topmost',1)
    root.config(bg = "#caf0f8")  
    root.winfo_screenwidth()
    root.winfo_screenheight()
    center_x = int(window_width // 2)
    center_y = int(window_height // 2)
    root.geometry(f"{window_width}x{window_height}")


# global variables
    #print(tkFont.families())

    #font
    fonts = ["fonts_custom/Roboto-Regular.ttf", "fonts_custom/Roboto-Light.ttf", "fonts_custom/Roboto-Bold.ttf"]
    
    for font in fonts:
        rute = resource_path(font)
        ctypes.windll.gdi32.AddFontResourceExW(rute, 0, 0)

    font_label = tkFont.Font(family="Roboto", size=16, weight="bold")

    font_body = tkFont.Font(family="Roboto Lt", size=14, weight="normal")

    font_button = tkFont.Font(family="Roboto", size=14, weight="normal")

    # x,y position
    y_moni = center_y-10
    y_loop = center_y-80
    y_loop_time = center_y-60
    y_media = center_y-150
    y_time_img = center_y
    x_windget = center_x-260
    x_min = center_x-120
    x_separate = center_x-90
    x_seg = center_x-75

# Type of media archive
    select_media = IntVar(value=-1)
    menu_media_label = Label(root, text='Tipo:', bg="#caf0f8", fg="black", font=font_label)
    menu_button_media = Menubutton(root,text="Media",bg="#48cae4", fg="black", font=font_body, bd=2, relief="ridge")
    
    menu_media_label.place(x=center_x+100, y=y_media)
    menu_button_media.place(x=center_x+160, y=y_media)
    
    menu_media = tk.Menu(menu_button_media, tearoff=False)
    menu_button_media["menu"] = menu_media
    
    menu_media.add_radiobutton(label="Video", value=0, variable=select_media, command=select_type_media)
    menu_media.add_radiobutton(label="Imagen", value=1, variable=select_media, command=select_type_media)

# time duration to image
    
    time_img_label = ft.format_time_label(root, 'Tiempo ' + '\nde la imagen:', font_label)

    time_min_im = ft.format_minute(root, font_body)
    separate = ft.separate(root, font_button)
    time_seg_im = ft.format_second(root, font_body)

# Drop-down menu to choose archive
    archive_label = Label(root, text='Archivo:', bg="#caf0f8", fg="black", font=font_label)
    archive_label.place(x=x_windget, y=center_y-150)
    
    select_archive = IntVar(value=-1)
    
    menu_button_archive = Menubutton(root, text='Selecciona el archivo',bg="#48cae4", fg="black", anchor='w', font=font_body, justify='left',bd=2, relief="ridge", width=18)
    menu_button_archive.pack()
    menu_button_archive.place(x=center_x-130, y=center_y-150)
    menu_button_archive.bind("<Button-1>", click_file)
    menu_archive = tk.Menu(menu_button_archive, tearoff=False)
    menu_button_archive["menu"] = menu_archive

#Time duration to loop

    loop_time_label = ft.format_time_label(root, 'Tiempo' + '\nde loop: ', font_label)
    loop_time_label.place(x=x_windget, y=y_loop)

    loop_min = ft.format_minute(root, font_body)
    loop_separate = ft.separate(root, font_button)
    loop_seg = ft.format_second(root, font_body)

    loop_min.place(x=x_min, y=y_loop_time)
    loop_min.bind("<Return>", out_entry)
    loop_separate.place(x=x_separate, y=y_loop_time)
    loop_seg.place(x=x_seg, y=y_loop_time)
    loop_seg.bind("<Return>", out_entry)

# drop-down menu to choose monitor
    choose_moni = Label(root, text='Monitor:', bg="#caf0f8", fg="black", font=font_label)
    choose_moni.place(x=x_windget, y=y_moni)
    

# drop-down menu
    select_moni = tk.IntVar(value=-1)
    menu_button_moni = Menubutton(root, text='Selecciona el monitor' ,bg="#48cae4", fg="black", font=font_body, bd=2, relief="ridge", width=18)
    menu_moni  = tk.Menu(menu_button_moni , tearoff=False)
    menu_button_moni ["menu"] = menu_moni
    
    for i, monitor in enumerate(moni):
        menu_moni.add_radiobutton(label=monitor.name, value=i, variable = select_moni, command=select_monitor)
    
    menu_button_moni.pack()
    menu_button_moni.place(x=center_x-130, y=y_moni)

#Select the file type and add a drop-down list
    select_type_media() 

# Boton para reproducir
    y_button = center_y+110
    button = Button(root, text='Reproducir', bg="#48cae4", fg="black", font=font_button, bd=2, relief="ridge", width=10)
    button.place(x=center_x-200, y=y_button)
    button.bind("<Button-1>", button_play)

# Exit Button
    button_exit = Button(root, text='Salir',bg="#48cae4", fg="black", font=font_button, bd=2, relief="ridge", command=on_closing, width=10)
    button_exit.place(x=center_x+100, y=y_button)
    
# cancel Button
    button_cancel = Button(root, text='Cancelar',bg="#48cae4", fg="black", font=font_button, bd=2, relief="ridge", command=stop, width=10)
    button_cancel.place(x=center_x-50, y=y_button)

# Events widgets 
    for widg in (loop_min, loop_seg, time_min_im, time_seg_im):
        widg.bind("<Return>", out_entry)
        widg.bind_all("<Button-1>", remove_focus)
    
    for widget in (loop_min, loop_seg, time_min_im, time_seg_im):
        widget.bind("<FocusIn>", ft.focus_time)
        widget.bind("<FocusOut>", ft.lost_focus_time)
    
    for widg in (menu_button_archive, menu_button_media, menu_button_moni, loop_min, loop_seg, time_min_im, time_seg_im):
        widg.bind("<Enter>", on_hover_widgets)
        widg.bind("<Leave>", on_leave_widgets)
    
    for wid in ( button, button_cancel):
        wid.bind("<Enter>", on_hover_button)
        wid.bind("<Leave>", on_leave_button)
    
    button_exit.bind("<Enter>", on_hover_exit)
    button_exit.bind("<Leave>", on_leave_exit)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    start_interface()