import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from PIL import Image, ImageTk

window = tk.Tk()
btn_cargar = tk.Button(window,text="Cargar datos",bg="white")
btn_entrenar = tk.Button(window,text="Entrenar",bg="white")
btn_recuperar = tk.Button(window,text="Recuperar",bg="white")
style = ttk.Style()
style.theme_use('default')
style.configure("blue.Horizontal.TProgressbar", background='#3981BF')
progreso = Progressbar(window,length="200",style="blue.Horizontal.TProgressbar")
imagen = Image.open("verde.jpg")
render = ImageTk.PhotoImage(imagen)
img = Label(image=render)
combo = Combobox(window)
combo['values']= (1, 2, 3, 4, 5, "Text")
combo.current(1) #set the selected item
chk_ruido = tk.BooleanVar()
chk_ruido.set(True)

def main():
    window.title("Memoria morfológica heteroasociativa")
    window.geometry('750x450')
    btn_cargar.place(x="500",y="30",width="100",height="30")
    btn_entrenar.place(x="500",y="60",width="100",height="30")
    btn_recuperar.place(x="500",y="90",width="100",height="30")
    progreso.place(x="400",y="200")
    combo.place(x="300",y="30")
    chk = Checkbutton(window,text="Ruido",var=chk_ruido).place(x="300",y="50")
    #img.image = render
    #img.place(x=0, y=0)
    window.mainloop()

main()
