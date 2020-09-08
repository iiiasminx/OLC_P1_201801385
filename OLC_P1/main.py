import tkinter
import os
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk 
from tkinter import scrolledtext 
import Analizador_html
import Analizador_css
from collections import deque
from pathlib import Path

#
#   HACER LA MAGIA HTML
#

texto = None
final = ""
pathAbierto = ""

def hacerLaMagiaCSS():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando el analizador léxico - CSS")
    funcionaxfa = Analizador_css.AnalizadorCSS()
    funcionaxfa.comenzar()

    listaNueva = funcionaxfa.escanear(txtIngresado.get("1.0", END))
    txtDentro.delete('1.0', END)

    listaConsola = funcionaxfa.pasarListaAString()
    txtDentro.insert(INSERT, listaConsola)

    txtIngresado.delete('1.0', END)
    
    listaColores = funcionaxfa.getColores()

    for f in listaColores:
        txtIngresado.insert(END, f.token, f.color)

    funcionaxfa.crearHTMLReportes()

   #falta crear reportes!!
   
def hacerLaMagiaHTML():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Iniciando el analizador léxico - HTML")
    funcionaxfa = Analizador_html.AnalizadorHTML()
    funcionaxfa.comenzar()
    #listaNueva = funcionaxfa.escanear(txtIngresado.get("1.0", END))
    funcionaxfa.escanear(txtIngresado.get("1.0", END))
    txtDentro.delete('1.0', END)
    #listaNueva = funcionaxfa.escanear(final)
    #funcionaxfa.imprimirListaTokens(listaNueva)

    listaConsola = funcionaxfa.pasarListaAString()
    txtDentro.insert(INSERT, listaConsola)

    #ya solo faltan pintar palabras LISTANUEVA
    txtIngresado.delete('1.0', END)
    

    #txtIngresado.insert(END, "holaaa", 'rojo')
    listaColores = funcionaxfa.getColores()

    for f in listaColores:
        txtIngresado.insert(END, f.token, f.color)

    funcionaxfa.crearHTMLReportes()
    #messagebox.showinfo(message="REPORTE GENERADO CON ÉXITO", title=":D")

def guardarComo():
    f = filedialog.asksaveasfile(mode='w')
    if f is None: 
        return
    text2save = str(txtIngresado.get(1.0, END)) 
    f.write(text2save)
    f.close()

    pathAbierto = f.name
    print(pathAbierto)

def guardar():
    if pathAbierto == "":
        guardarComo()
        return
    
    print("Guardando")
    text2save = str(txtIngresado.get(1.0, END))
    with open(pathAbierto, "r+") as f:
       f.truncate(0)
       f.write(text2save)
       f.close()

def nuevoBoton():
    txtIngresado.delete('1.0', END)
    txtDentro.delete('1.0', END)

def aboutme():
    messagebox.showinfo(message="Yásmin Elisa Monterroso Escobedo\n\t201801385\n\t      :3", title="Sobre mi :D")

def abrirArchivo():
    nuevoBoton()
    #devuelve la location de la cosa
    ventana.filename = filedialog.askopenfilename(initialdir="/home", title="Selecciona tu archivo")
    f = open(ventana.filename, "r").read()
    final = f
    final = f.strip()
    #print("TEXTO QUE LEO: '", final, "'")

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
lNumber7 = tkinter.Label(frDerecha, text = "      ", bg ='plum4')
txtIngresado = scrolledtext.ScrolledText(frDerecha, height = "20", width ="50")

frIzquieda = tkinter.Frame(ventana, bg ='plum4')
lNumber2 = tkinter.Label(frIzquieda, text = "      ", bg ='plum4')
lNumber3 = tkinter.Label(frIzquieda, text = "      ", bg ='plum4')
lNumber5 = tkinter.Label(frIzquieda, text = "      ", bg ='plum4')
lNumber6 = tkinter.Label(frIzquieda, text = "      ", bg ='plum4')
txtDentro = scrolledtext.ScrolledText(frIzquieda, height = "20", width ="36", fg= "snow", bg ="gray25")
scrollbar = Scrollbar(txtDentro, orient='horizontal')


botonErrores = tkinter.Button(frIzquieda, text ="Reporte de Errores")
botonNormal = tkinter.Button(frDerecha, text ="Reporte de Tokens")


lTitulo.grid(row=0, column = 1)
lNumber.grid(row=1, column = 1)
txtIngresado.grid(row=2, column = 1)
lNumber4.grid(row=3, column = 1)
lNumber7.grid(row=2, column = 0)
botonNormal.grid(row=4, column=1)
frDerecha.grid(row=0, column=0)
#scrollbar.grid(row=4, column=1)


txtIngresado.tag_config('rojo', foreground="red")
txtIngresado.tag_config('verde', foreground="green4")
txtIngresado.tag_config('amarillo', foreground="goldenrod")
txtIngresado.tag_config('azul', foreground="blue")
txtIngresado.tag_config('gris', foreground="gray36")
txtIngresado.tag_config('naranja', foreground="orange3")
txtIngresado.tag_config('negro', foreground="gray2")
txtIngresado.tag_config('blanco', foreground="snow")

lNumber2.grid(row=0, column = 0)
lNumber3.grid(row=1, column = 0)
lNumber6.grid(row=1, column = 0)
txtDentro.grid(row=3, column=1)
lNumber5.grid(row=4, column=1)
botonErrores.grid(row=5, column=1)
frIzquieda.grid(row=0, column=1)

menu = Menu(ventana, tearoff=0)
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='Nuevo', command=nuevoBoton)
new_item.add_command(label='Abrir', command=abrirArchivo)
new_item.add_command(label='Guardar')
new_item.add_command(label='Guardar como', command=guardarComo)
menu.add_cascade(label='Archivo', menu=new_item)
nuevo = Menu(menu, tearoff=0)
nuevo.add_command(label='Ejecutar Análisis')
nuevo.add_command(label='Ejecutar HTML', command=hacerLaMagiaHTML)
nuevo.add_command(label='Ejecutar CSS', command=hacerLaMagiaCSS)
nuevo.add_command(label='Ejecutar JavaScript')
menu.add_cascade(label='Ejecutar', menu=nuevo)
bout = Menu(menu, tearoff=0)
bout.add_command(label='About', command=aboutme)
menu.add_cascade(label='About', menu=bout)
ventana.config(menu=menu)



ventana.mainloop()



    