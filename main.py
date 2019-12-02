import tkinter as tk
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import imageio # Este modulo nos permite cargar los valores de una imagen en matriz
import numpy as np
from matplotlib.image import imread
import random

class Main:

    nombreImagen = "num.png"
    imagenActualDesplegada = ""
    tipoRuido = ""
    archivos = ()
    negro = 9
    blanco = 214
    vectoresImagen = []
    matricesImagen = []
    vectorPrueba = None
    clases = [np.array([1,0,0,0,0]),np.array([0,1,0,0,0]),np.array([0,0,1,0,0]),np.array([0,0,0,1,0]),np.array([0,0,0,0,1])]
    window = None
    btn_cargar = None
    btn_entrenar = None
    btn_recuperar = None
    btn_ruido = None
    progreso = None
    cant_ruido = None
    combo = None
    comboRuido = None
    chk_ruido = None

    def __init__(self):
        self.window = tk.Tk()
        self.btn_cargar = tk.Button(self.window,text="Cargar datos",bg="white",command=self.cargarImagenes)
        #btn_cargar_rec = tk.Button(window,text="Selecciona",bg="white",command=cargarImagen)
        self.btn_entrenar = tk.Button(self.window,text="Entrenar",bg="#3981BF",fg="white")
        self.btn_recuperar = tk.Button(self.window,text="Recuperar",bg="white")
        self.btn_ruido = tk.Button(self.window,text="Agregar",bg="gray",fg="white", command=self.desplegarRuido)
        style = ttk.Style()
        style.theme_use('default')
        style.configure("blue.Horizontal.TProgressbar", background='#3981BF')
        self.progreso = Progressbar(self.window,length="300",style="blue.Horizontal.TProgressbar")
        self.cant_ruido = Entry(self.window,width=10)
        self.combo = Combobox(self.window)
        self.combo['values']= ("-",0, 1, 2, 3, 4)
        self.combo.current(0)
        self.combo.bind("<<ComboboxSelected>>", self.cambiarImagenActiva)
        self.comboRuido = Combobox(self.window)
        self.comboRuido['values'] = ("Aditivo","Sustractivo","Mixto")
        self.comboRuido.current(0)
        self.chk_ruido = tk.BooleanVar()
        self.chk_ruido.set(False)

    def cargarImagenes(self):
        file = filedialog.askopenfilenames() # Esto nos devuelve una tupla con las direcciones de los archivos
        # Recorremos toda la tupla de direcciones y creamos una lista que contenga los archivos abiertos
        self.archivos = file
        avance = 100 / len(file)
        i = 0
        vector = []
        # Para cada imagen tomada obtenemos su valor en el vector de numpy
        for imagen in self.archivos:
            img = imread(imagen)
            self.matricesImagen.append(img)
            # Esta parte del codigo convierte la imagen en vector en lugar de matriz
            # Convertimos nuestra lista en un arreglo numpy
            v = self.convertirMatrizaVector(img)
            #a = self.normalizarVector(v)
            print(str(np.shape(v)))
            self.vectoresImagen.append(v)
            vector.clear()
            i += avance
            self.progreso['value'] = i
        messagebox.showinfo("Listo","Imágenes cargadas a la memoria")
        print(self.vectoresImagen)

    def cambiarImagenActiva(self,event):
        nombreImagen = self.combo.get() + ".bmp"
        imagen = Image.open(nombreImagen)
        render = ImageTk.PhotoImage(imagen)
        img = Label(image=render,borderwidth=2)
        img.image = render
        img.place(x=120, y=120)
        # Cuando cargamos un patrón colocamos que será el patrón de prueba para la memoria
        self.vectorPrueba = self.vectoresImagen[self.combo.current()]
        self.imagenActualDesplegada = nombreImagen

    def agregarRuido(self,indice,matriz,porcentaje,tipo):
        i = 0
        matrizRuido = matriz.copy()
        matrizRuido.setflags(write=1)
        # Obtenemos la cantidad de pixeles que se verán alterados con el ruido
        totalPixeles = len(self.vectoresImagen[indice])
        pixelesAfectados = int((porcentaje / 100) * totalPixeles)
        while i < pixelesAfectados:
            # Recorremos cada uno de los pixeles de forma aleatoria para afectarles con el ruido
            pixel = random.randint(0,len(self.vectoresImagen[indice])-1)
            fila = int(pixel / 28)
            columna = pixel % 28
            valor = matrizRuido.item(pixel)
            print(str(i))
            if tipo == "Aditivo":
                if valor == self.blanco:
                    matrizRuido[fila][columna] = self.negro
                    i += 1
            elif tipo == "Sustractivo":
                if valor == self.negro:
                    matrizRuido[fila][columna] = self.blanco
                    i += 1
            elif tipo == "Mixto":
                if valor == self.blanco:
                    matrizRuido[fila][columna] = self.negro
                    i += 1
                elif valor == self.negro:
                    matrizRuido[fila][columna] = self.blanco
                    i += 1
        return matrizRuido

    def desplegarRuido(self):
        # Si el checkbox de ruido se encuentra activo
        if self.chk_ruido.get():
            # Obtenemos el nombre de la imagen a la que se le quiere aplicar ruido
            nombre = self.imagenActualDesplegada
            nombreSeparado = nombre.split(".")
            nuevoNombre = nombreSeparado[0] + self.comboRuido.get() + "." + nombreSeparado[1]
            indice = int(self.combo.get())
            porcentaje = int(self.cant_ruido.get())
            tipo = self.comboRuido.get()
            # Tenemos que obtener la nueva matriz con ruido
            matrizRuido = self.agregarRuido(indice,self.matricesImagen[indice],porcentaje,tipo)
            v = self.convertirMatrizaVector(matrizRuido)
            self.vectorPrueba = v.copy()
            print(matrizRuido)
            # Creamos la imagen a partir de la correspondiente matriz de numpy
            img = Image.fromarray(matrizRuido,"RGB")
            img.save(nuevoNombre)
            # Desplegamos la nueva imagen
            imagen = Image.open(nuevoNombre)
            render = ImageTk.PhotoImage(imagen)
            img = Label(image=render,borderwidth=2)
            img.image = render
            img.place(x=120, y=120)
            self.imagenActualDesplegada = nuevoNombre
        else:
            # Lanzamos un mensaje de error
            messagebox.showerror("Error 101","No se puede aplicar ruido, seleccione primero el checkbox")

    def convertirMatrizaVector(self,matriz):
        vector = []
        for fila in matriz:
            for elemento in fila:
                vector.append(elemento)
        v = np.array(vector)
        return v

    def normalizarVector(self,vector):
        v = vector.copy()
        v[v == 9] = 0
        v[v == 214] = 1
        print(v)
        return v

    def main(self):
        self.window.title("Memoria morfológica heteroasociativa")
        self.window.geometry('750x450')
        self.btn_entrenar.place(x="500",y="60",width="100",height="30")
        self.btn_cargar.place(x="500",y="30",width="100",height="30")
        self.btn_recuperar.place(x="300",y="30",width="100",height="30")
    #    btn_cargar_rec.place(x="300",y="70",width="100",height="30")
        self.progreso.place(x="300",y="270")
        self.combo.place(x="300",y="100")
        self.chk = Checkbutton(self.window,text="Ruido",var=self.chk_ruido).place(x="300",y="130")
        self.cant_ruido.place(x="300",y="160")
        self.comboRuido.place(x="300",y="190")
        self.btn_ruido.place(x="300",y="220",width="100",height="30")
        #imagen = Image.open(nombreImagen)
        #render = ImageTk.PhotoImage(imagen)
        #img = Label(image=render,borderwidth=2)
        #img.image = render
        #img.place(x=0, y=0)
        self.window.mainloop()

m = Main()
m.main()
