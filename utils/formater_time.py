from tkinter import *


def validate_min(new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 60))

def validate_sg(new_value):
    return (new_value == '' or (new_value.isdigit() and 0 <= int(new_value) <= 59))

def command_min(root):
    return (root.register(validate_min), '%P')    

def command_sg(root):
    return (root.register(validate_sg), '%P')

def format_time_label(root, string_time, font_label):
    time_label = Label(root, text=string_time, bg="#caf0f8", fg="black", font=font_label, justify='left')
    return time_label 

def format_minute(root, font_body):
    time_min = Entry(root, bg="#48cae4", fg="black", font=font_body, width=2, validate="key", validatecommand=command_min(root))
    time_min.insert(0, '00')
    return time_min

def format_second(root, font_body):
    time_seg = Entry(root, bg="#48cae4", fg="black", font=font_body, width=2, validate="key", validatecommand=command_sg(root))
    time_seg.insert(0, '00')
    return time_seg

def separate(root, font_body):
    separate = Label(root, text=":", bg="#caf0f8", fg="black", font=font_body)
    return separate

def focus_time(event):
    if event.widget.get() == "00":
        event.widget.delete(0, END)

def lost_focus_time(event):
    if event.widget.get() == "":
        event.widget.insert(0, "00")

def convert_seconds(minutes, seconds):
    total = int(minutes) * 60 + int(seconds)
    return total


