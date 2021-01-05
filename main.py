from tkinter import *
import tkinter.simpledialog
import tkinter.messagebox
import os
import subprocess
import shutil


# Dialog window
def input_new_face_name():
    name = tkinter.simpledialog.askstring("New face", "What's face's name: ")
    # tkinter.messagebox.showinfo('OK', '{} added. Webcam starting...'.format(name))
    subprocess.call(["python", "capture_save_image.py", "-n", name])


def reset_database():
    folders = os.listdir("dataset")
    # print(folders)
    for folder_name in folders:
        if folder_name != "kim_thi_mai_huong":
            shutil.rmtree(f'dataset/{folder_name}')
    subprocess.call(["python", "encode_faces.py", "-i", "dataset", "-e", "encodings.pickle"])


# Recognize call
def recognize_face_call():
    # os.system("recognize_face_video_multi_thread.py -e encodings.pickle")
    subprocess.call(["python", "recognize_face_video_multi_thread.py", "-e", "encodings.pickle"])


root_window = Tk()
root_window.title("AGR face recognition")
root_window.config(padx=20, pady=20)
#
# canvas = Canvas(width=500, height=400)
# logo = PhotoImage(file="logo.png")
# image = canvas.create_image(250, 200, image=logo)
# canvas.grid(column=0, row=0, columnspan=2)

# button
recognize_button = Button(text="Start recognize faces", command=recognize_face_call)
recognize_button.grid(column=0, row=1, padx=10)

encoding_button = Button(text="Encoding new face", command=input_new_face_name)
encoding_button.grid(column=1, row=1, padx=10)

reset_button = Button(text="Reset database", command=reset_database)
reset_button.grid(column=0, row=2, pady=10, columnspan=2)


root_window.mainloop()
