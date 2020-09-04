import tkinter
import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk 
from tkinter import scrolledtext 
import Analizador_html
from collections import deque
from pathlib import Path

#
#   HACER LA MAGIA HTML
#

texto = None
final = ""

def hacerLaMagiaHTML():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando el analizador léxico - HTML")
    funcionaxfa = Analizador_html.AnalizadorHTML()
    listaNueva = funcionaxfa.escanear(txtIngresado.get("1.0", END))
    #listaNueva = funcionaxfa.escanear(final)
    funcionaxfa.imprimirListaTokens(listaNueva)


def aboutme():
    messagebox.showinfo(message="Yásmin Elisa Monterroso Escobedo\n\t201801385\n\t      :3", title="Sobre mi :D")

def abrirArchivo():
    #devuelve la location de la cosa
    ventana.filename = filedialog.askopenfilename(initialdir="/home", title="Selecciona tu archivo")
    f = open(ventana.filename, "r").read()
    final = f
    final = f.strip()
    print("TEXTO QUE LEO: '", final, "'")

    txtIngresado.insert(INSERT, final)
    

#
#   VENTANAS Y COMPLEMENTOS
#
ventana = tkinter.Tk()
ventana.option_add('*Dialog.msg.font', 'Helvetica 12')
ventana.resizable(False, False) 
ventana.config(bg ='plum4')
w = 800
h = 500
ws = ventana.winfo_screenwidth() 
hs = ventana.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
ventana.geometry('%dx%d+%d+%d' % (w, h, x, y))
ventana.title("ML WEB - COMPILADORES 1")

frDerecha = tkinter.Frame(ventana, bg ='plum4')
lTitulo = tkinter.Label(frDerecha, text = "ML WEB EDITOR", bg ='plum4')
lNumber = tkinter.Label(frDerecha, text = "[20.08]", bg ='plum4')
lNumber4 = tkinter.Label(frDerecha, text = "        ", bg ='plum4')
txtIngresado = scrolledtext.ScrolledText(frDerecha, height = "20", width ="50")

frIzquieda = tkinter.Frame(ventana, bg ='plum4')
lNumber2 = tkinter.Label(frIzquieda, text = "      ", bg ='plum4')
lNumber3 = tkinter.Label(frIzquieda, text = "      ", bg ='plum4')
txtDentro = scrolledtext.ScrolledText(frIzquieda, height = "20", width ="36", fg= "snow", bg ="gray25")

lTitulo.grid(row=0, column = 1)
lNumber.grid(row=1, column = 1)
txtIngresado.grid(row=2, column = 1)
lNumber4.grid(row=0, column = 0)
frDerecha.grid(row=0, column=0)

lNumber2.grid(row=0, column = 0)
lNumber3.grid(row=1, column = 0)
txtDentro.grid(row=3, column=1)
frIzquieda.grid(row=0, column=1)

menu = Menu(ventana, tearoff=0)
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='Nuevo')
new_item.add_command(label='Abrir', command=abrirArchivo)
new_item.add_command(label='Guardar')
new_item.add_command(label='Guardar como')
menu.add_cascade(label='Archivo', menu=new_item)
nuevo = Menu(menu, tearoff=0)
nuevo.add_command(label='Ejecutar Análisis')
nuevo.add_command(label='Ejecutar HTML', command=hacerLaMagiaHTML)
nuevo.add_command(label='Ejecutar CSS')
nuevo.add_command(label='Ejecutar JavaScript')
menu.add_cascade(label='Ejecutar', menu=nuevo)
bout = Menu(menu, tearoff=0)
bout.add_command(label='About', command=aboutme)
menu.add_cascade(label='About', menu=bout)
ventana.config(menu=menu)

ventana.mainloop()



    