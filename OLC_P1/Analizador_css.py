import enum
from enum import Enum, auto
from collections import deque
from pathlib import Path
import os
import errno
import subprocess
import webbrowser
import time



#
#
#       TOKEN
#
#

class TokenC:
    def __init__(self, tipo, valor):
        # Token.html_cerrar, "hdsih"
        self.valor = valor
        self.tipo = tipo
    def __str__(self):
        return '{} {} {}'.format(self.tipo, "->", self.valor)
        #return self.tipo, " -> ", self.valor
    
class TokenColor:
    def __init__(self, token, color):
        # Token.html_cerrar, "hdsih"
        self.token = token
        self.color = color

class TokenCSS:
    def __init__(self, tipo, valor, contafila, contacolumna, estado):
        self.valor = valor
        self.tipo = tipo
        self.contafilaa = contafila
        self.contacolumnaa = contacolumna
        self.estado = estado
        # hola = tokenhtml(token.html_abrir)

    def getValorToken(self):
        return self.valor

    def getTipo(self):
        return self.tipo

    def __str__(self):
        cadena = self.tipo +  " -> '" + self.valor + "' [" + str(self.contafilaa) + "," + str(self.contacolumnaa)+"]"
        return cadena

    def toString(self):
        cadena = self.tipo +  " -> '" + self.valor + "' [" + str(self.contafilaa) + "," + str(self.contacolumnaa)+"]" + " || ESTADO: " + str(self.estado) + "\n"
        return cadena

class Token(enum.Enum):
    ruta_abrir = auto()
    comentario_abrir = auto()
    comentario_cerrar = auto()
    comentario = auto()
    llave_abrir = auto()
    llave_cerrar = auto()
    dos_puntos = auto()
    dos_puntos_dobles = auto()
    punto_y_coma = auto()
    coma = auto()
    pr_color = auto()
    pr_bg_color = auto()
    pr_bg_image = auto()
    pr_border = auto()
    pr_opacity = auto()
    pr_background = auto()
    pr_text_align = auto()
    pr_font_family = auto()
    pr_font_style = auto()
    pr_font_weight = auto()
    pr_font_size = auto()
    pr_font = auto()
    pr_padding_left = auto()
    pr_padding_right = auto()
    pr_padding_bottom = auto()
    pr_padding_top = auto()
    pr_padding = auto()
    pr_display = auto()
    pr_line_height = auto()
    pr_width = auto()
    pr_height = auto()
    pr_margin_top = auto()
    pr_margin_right = auto()
    pr_margin_bottom = auto()
    pr_margin_left = auto()
    pr_margin = auto()
    pr_border_style = auto()
    pr_position = auto()
    pr_bottom = auto()
    pr_top = auto()
    pr_right = auto()
    pr_left = auto()
    pr_float = auto()
    pr_clear = auto()
    pr_max_width = auto()
    pr_min_width = auto()
    pr_max_height = auto()
    pr_min_height = auto()
    numero = auto()
    u_px = auto()
    u_em = auto()
    u_vh = auto()
    u_vw = auto()
    u_in = auto()
    u_cm = auto()
    u_mm = auto()
    u_pt = auto()
    u_pc = auto()
    porcentaje = auto()
    selector = auto()
    asterisco = auto()
    selector_universal = auto()
    numeral = auto()
    guion = auto()
    parentesis_abrir = auto()
    parentesis_cerrar = auto()
    comillas_dobles = auto()
    punto = auto()
    identificador = auto()
    pr_rgba = auto()
    pr_url = auto()
    cadena = auto()

class ErrorCSS:
    def __init__(self, linea, columna, caracter_error, estado):
        self.linea = linea
        self.columna = columna
        self.caracter_error = caracter_error
        self.estado = estado
        self.descripcion = "El caracter " + \
            self.caracter_error + " no pertenece al lenguaje"

class AnalizadorCSS:

   listaSalida = deque()

   estado = None
   auxlex = ""

   contador = None

   contaerror = 0
   contafila = 1
   contacolumna = 0
   descerror = "caracter desconocido"

   contatoken = 1
   escadena = False
   yaNumeral = False
   yaPR = False
   yapunto = False
   vueltaEspacio11 = False

   listaErrores = deque()
   listaTokens = deque()
   listaColores = deque()

   arreglotokens = []

   linklinux = ""
   stringListaSalida = ""
   mihtml = ""

   def comenzar(self):
       self.stringListaSalida = ""
       self.listaColores.clear()
       self.listaErrores.clear()
       self.listaSalida.clear()
       self.listaTokens.clear()

   def escanear(self, entrada):
       entrada = entrada + '$'
       self.estado = 0
      # print("'",entrada1,"'")

       #BANDERAS

       c = ''
       y = len(entrada)

       i = 0

       while (i < y):
           c = entrada[i]

           #acá comiendo a mandar todo a todos lados
           if self.estado == 0:
               if c.isalpha():
                   if self.yaPR == False:
                       self.estado = 4
                   else:
                       self.estado = 13
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '/':
                   #podría ser comentario
                   self.estado = 1
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ' ':
                   self.contacolumna += 1
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
               elif c == '\n':
                   self.contafila += 1
                   self.contacolumna = 0
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
                   self.yaNumeral = False
                   self.yaPR = False
               elif c == '\r':
                   self.contacolumna += 1
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
               elif c == '*':
                   #fin de comentario o asterisco
                   self.estado = 3
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ':':
                   #dos puntos o dobles dos puntos
                   self.estado = 6
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '{':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Llaves abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.llave_abrir)
                   self.contacolumna += 1
                   self.yaNumeral = False
               elif c == '}':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Llaves cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.llave_cerrar)
                   self.contacolumna += 1
                   self.yaNumeral = False
                   self.yaPR = False
               elif c == '#':
                   self.auxlex += c
                   if self.yaPR == False:
                       w = TokenColor(self.auxlex, 'negro')
                       self.listaColores.append(w)
                       n = TokenCSS("Numeral", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.numeral)
                       self.contacolumna += 1
                       self.yaNumeral = True
                   else:
                       self.estado = 12
                       self.contacolumna += 1
               elif c == '.':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Punto", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.punto)
                   self.contacolumna += 1
               elif c == ',':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Coma", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.coma)
                   self.contacolumna += 1
               elif c == '%':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Porcentaje", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.porcentaje)
                   self.contacolumna += 1
               elif c == '-':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Guión", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.guion)
                   self.contacolumna += 1
               elif c == '(':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Paréntesis abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.parentesis_abrir)
                   self.contacolumna += 1
               elif c == ')':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Paréntesis cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.parentesis_cerrar)
                   self.contacolumna += 1
               elif c == ';':
                   self.yaPR = False
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Punto y coma", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.punto_y_coma)
                   self.contacolumna += 1
               elif c == '\"':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenCSS("Comillas dobles", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comillas_dobles)
                   self.contacolumna += 1

                   if self.escadena == False:
                       self.escadena = True
                       self.estado = 14
                   else:
                       self.escadena = False
               elif c.isnumeric():
                   self.estado = 9
                   self.auxlex += c
                   self.contacolumna += 1
               else:
                   if c == '$':
                       print("El análisis Ha terminado")
                   else:
                       if c == ' ' or c == '\t':
                           self.contacolumna += 1
                           w = TokenColor(c, 'blanco')
                           self.listaColores.append(w)
                       else:
                           self.auxlex += c
                           print("NO SE RECONOCE LA PALABRA0:  -> '", self.auxlex, "'")
                           n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                           self.listaErrores.append(n)
                           self.auxlex = ""
                           self.estado = 0    
           elif self.estado == 1:
               if c == '*':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenCSS("Inicio Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_abrir)
                   self.contacolumna += 1

                   self.estado = 2
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA1:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0

                   i -=1
           elif self.estado == 2:
               if c == '*':
                   
                   z = self.auxlex.lower()
                   if z.startswith("pathw"):
                       w = TokenColor(self.auxlex, 'gris')
                       self.listaColores.append(w)
                       n = TokenCSS("PR - ruta windows abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.ruta_abrir)
                   elif z.startswith("pathl"):
                       w = TokenColor(self.auxlex, 'gris')
                       self.listaColores.append(w)
                       x = self.auxlex
                       self.linklinux = x.replace('PATHL: ', '')
                       print("LINK ENCONTRADO:", self.linklinux)
                       n = TokenCSS("PR - ruta linux abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.ruta_abrir)
                   else:
                       w = TokenColor(self.auxlex, 'gris')
                       self.listaColores.append(w)
                       n = TokenCSS("Cuerpo Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.comentario)
                       self.contacolumna += 1                   
                   i -= 1
               else:
                   self.estado = 2
                   self.auxlex += c
                   if c == '\n':
                       self.contafila += 1
                       self.contacolumna = 0
                   else:
                      self.contacolumna += 1
           elif self.estado == 3:
               if c == '/':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenCSS("Final Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_cerrar)
                   self.contacolumna += 1
               elif c == '{':
                   w = TokenColor(self.auxlex, 'rojo')
                   self.listaColores.append(w)
                   n = TokenCSS("Selector Universal", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.selector_universal)
                   self.contacolumna += 1
                   i -= 1
               elif c == ' ':
                   self.estado = 7
                   self.contacolumna +=1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Asterisco", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.asterisco)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 4:
               #algo pasa
               if c.isalpha() or c.isnumeric() or c == '-':
                   #acá junto todo lo que permite el id
                   self.estado = 4
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ' ':
                   if self.yaNumeral == True:
                       w = TokenColor(self.auxlex, 'verde')
                       self.listaColores.append(w)
                       n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.identificador)
                       w = TokenColor(c, 'blanco')
                       self.listaColores.append(w)
                   else:
                       self.estado = 5
                   #pongo iwal todo lo que va de acá para abajo
               elif c == '{' or c == '#' or c == ',':
                   w = TokenColor(self.auxlex, 'verde')
                   self.listaColores.append(w)
                   n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.identificador)
                   i -=1
               elif c == ':':
                   #solo lo mando para ver si es palabra reservada
                   #else, es identificador
                   self.contacolumna += 1
                   self.estado = 8
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0
           elif self.estado == 5:
               if c == '{' or c == ':' or c == '#' or c == ',':
                   w = TokenColor(self.auxlex, 'verde')
                   self.listaColores.append(w)
                   n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.identificador)
                   w = TokenColor(" ", 'verde')
                   self.listaColores.append(w)
                   i -=1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0
           elif self.estado == 6:
               #dos puntos, dos puntos dobles
               if c == ':':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Dos puntos dobles", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.dos_puntos_dobles)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenCSS("Dos puntos", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.dos_puntos)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 7:
               if c == '{':
                   w = TokenColor(self.auxlex, 'rojo')
                   self.listaColores.append(w)
                   n = TokenCSS("Selector Universal", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.selector_universal)
                   self.contacolumna += 1
                   i -= 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Asterisco", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.asterisco)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 8:
               w = TokenColor(self.auxlex, 'rojo')
               self.listaColores.append(w)
               self.yaPR = True
               if self.auxlex.lower() == "color":
                   n = TokenCSS("PR - color", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_color)
                   i -=1
               elif self.auxlex.lower() == "background-color":
                   n = TokenCSS("PR - background-color", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_bg_color)
                   i -=1
               elif self.auxlex.lower() == "background-image":
                   n = TokenCSS("PR - background-image", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_bg_image)
                   i -=1
               elif self.auxlex.lower() == "border":
                   n = TokenCSS("PR - border", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_border)
                   i -=1
               elif self.auxlex.lower() == "opacity":
                   n = TokenCSS("PR - opacity", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_opacity )
                   i -=1
               elif self.auxlex.lower() == "background":
                   n = TokenCSS("PR - background", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_background )
                   i -=1
               elif self.auxlex.lower() == "text-align":
                   n = TokenCSS("PR - text-align", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_text_align )
                   i -=1
               elif self.auxlex.lower() == "font-family":
                   n = TokenCSS("PR - font-family", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_font_family )
                   i -=1
               elif self.auxlex.lower() == "font-style":
                   n = TokenCSS("PR - font-style", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_font_style )
                   i -=1
               elif self.auxlex.lower() == "font-weight":
                   n = TokenCSS("PR - font-weight", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_font_weight )
                   i -=1
               elif self.auxlex.lower() == "font-size":
                   n = TokenCSS("PR - font-size", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_font_size )
                   i -=1
               elif self.auxlex.lower() == "font":
                   n = TokenCSS("PR - font", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_font )
                   i -=1
               elif self.auxlex.lower() == "padding-left":
                   n = TokenCSS("PR - padding-left", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_padding_left )
                   i -=1
               elif self.auxlex.lower() == "padding-right":
                   n = TokenCSS("PR - padding-right", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_padding_right )
                   i -=1     
               elif self.auxlex.lower() == "padding-bottom":
                   n = TokenCSS("PR - padding-bottom", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_padding_bottom )
                   i -=1
               elif self.auxlex.lower() == "padding-top":
                   n = TokenCSS("PR - padding-top", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_padding_top )
                   i -=1  
               elif self.auxlex.lower() == "padding":
                   n = TokenCSS("PR - padding", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_padding )
                   i -=1   
               elif self.auxlex.lower() == "display":
                   n = TokenCSS("PR - display", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_display )
                   i -=1
               elif self.auxlex.lower() == "line-height":
                   n = TokenCSS("PR - line-height", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_line_height )
                   i -=1
               elif self.auxlex.lower() == "height":
                   n = TokenCSS("PR - height", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_height )
                   i -=1
               elif self.auxlex.lower() == "width":
                   n = TokenCSS("PR - width", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_width )
                   i -=1
               elif self.auxlex.lower() == "margin-top":
                   n = TokenCSS("PR - margin-top", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_margin_top )
                   i -=1
               elif self.auxlex.lower() == "margin-right":
                   n = TokenCSS("PR - margin-right", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_margin_right )
                   i -=1
               elif self.auxlex.lower() == "margin-bottom":
                   n = TokenCSS("PR - margin-bottom", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_margin_bottom )
                   i -=1
               elif self.auxlex.lower() == "margin-left":
                   n = TokenCSS("PR - margin-left", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_margin_left )
                   i -=1
               elif self.auxlex.lower() == "margin":
                   n = TokenCSS("PR - margin", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_margin )
                   i -=1
               elif self.auxlex.lower() == "border-style":
                   n = TokenCSS("PR - border-style", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_border_style )
                   i -=1
               elif self.auxlex.lower() == "position":
                   n = TokenCSS("PR - position", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_position )
                   i -=1
               elif self.auxlex.lower() == "bottom":
                   n = TokenCSS("PR - bottom", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_bottom )
                   i -=1
               elif self.auxlex.lower() == "top":
                   n = TokenCSS("PR - top", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_top )
                   i -=1
               elif self.auxlex.lower() == "right":
                   n = TokenCSS("PR - right", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_right )
                   i -=1
               elif self.auxlex.lower() == "left":
                   n = TokenCSS("PR - left", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_left )
                   i -=1
               elif self.auxlex.lower() == "float":
                   n = TokenCSS("PR - float", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_float )
                   i -=1
               elif self.auxlex.lower() == "clear":
                   n = TokenCSS("PR - clear", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_clear )
                   i -=1
               elif self.auxlex.lower() == "max-width":
                   n = TokenCSS("PR - max-width", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_max_width )
                   i -=1
               elif self.auxlex.lower() == "min-width":
                   n = TokenCSS("PR - min-width", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_min_width )
                   i -=1
               elif self.auxlex.lower() == "min-height":
                   n = TokenCSS("PR - min-height", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_min_height )
                   i -=1
               elif self.auxlex.lower() == "max-height":
                   n = TokenCSS("PR - max-height", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_max_height )
                   i -=1
               else:
                   self.yaPR = False
                   self.listaColores.pop()
                   w = TokenColor(self.auxlex, 'verde')
                   self.listaColores.append(w)
                   n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.identificador)
                   i -= 1
               i -= 1
           elif self.estado == 9:
               if c.isnumeric():
                   self.estado = 9
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '.':
                   if self.yapunto == False:
                       self.yapunto = True
                       self.estado = 9
                       self.auxlex += c
                       self.contacolumna += 1
                   else:
                       self.auxlex += c
                       print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                       n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                       self.listaErrores.append(n)
                       self.auxlex = ""
                       self.estado = 0
               else:
                   self.yapunto = False
                   w = TokenColor(self.auxlex, 'azul')
                   self.listaColores.append(w)
                   n = TokenCSS("Número", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.numero)

                   if c.isalpha() or c == ' ':
                       self.estado = 10
                   
                   i -=1
           elif self.estado == 10:
               if c.isalpha():
                   self.estado = 10
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ' ':
                   self.contacolumna += 1
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
                   self.estado = 10
               else:
                   self.contacolumna += 1
                   self.estado = 11
           elif self.estado == 11:
               w = TokenColor(self.auxlex, 'rojo')
               self.listaColores.append(w)
               if self.auxlex.lower() == "px":
                   n = TokenCSS("U - px", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_px)
                   i -=1
               elif self.auxlex.lower() == "em":
                   n = TokenCSS("U - em", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_em)
                   i -=1
               elif self.auxlex.lower() == "vh":
                   n = TokenCSS("U - vh", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_vh)
                   i -=1
               elif self.auxlex.lower() == "vw":
                   n = TokenCSS("U - vw", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_vw)
                   i -=1
               elif self.auxlex.lower() == "in":
                   n = TokenCSS("U - in", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_in)
                   i -=1
               elif self.auxlex.lower() == "cm":
                   n = TokenCSS("U - cm", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_cm)
                   i -=1
               elif self.auxlex.lower() == "mm":
                   n = TokenCSS("U - mm", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_mm)
                   i -=1
               elif self.auxlex.lower() == "pt":
                   n = TokenCSS("U - pt", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_pt)
                   i -=1
               elif self.auxlex.lower() == "pc":
                   n = TokenCSS("U - pc", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.u_pc)
                   i -=1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA UNIDAD DE MEDIDA:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0
               i -= 1
           elif self.estado == 12:
               if c.isalnum() or c == '-':
                   self.estado = 12
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ' ' or c == ',' or c == ';' or c == '\n'or c == '}':
                    w = TokenColor(self.auxlex, 'verde')
                    self.listaColores.append(w)
                    n = TokenCSS("Variable", self.auxlex, self.contafila, self.contacolumna, self.estado)
                    self.listaTokens.append(n)
                    self.agregarToken(Token.numeral)
                    i -= 1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA12:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0 
           elif self.estado == 13:
               if c.isalpha() or c == '-':
                   self.estado = 13
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ' ' or c == ',' or c == ';' or c == '\n':
                    w = TokenColor(self.auxlex, 'verde')
                    self.listaColores.append(w)
                    n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                    self.listaTokens.append(n)
                    self.agregarToken(Token.numeral)
                    i -= 1
               elif c == '(':
                   if self.auxlex.lower() == "rgba":
                       w = TokenColor(self.auxlex, 'rojo')
                       self.listaColores.append(w)
                       n = TokenCSS("PR - rgba", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.pr_rgba)
                   elif self.auxlex.lower() == "url":
                       w = TokenColor(self.auxlex, 'rojo')
                       self.listaColores.append(w)
                       n = TokenCSS("PR - url", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.pr_url)
                   else:
                       self.auxlex += c
                       print("NO SE RECONOCE LA PALABRA13:  -> '", self.auxlex, "'")
                       n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                       self.listaErrores.append(n)
                       self.auxlex = ""
                       self.estado = 0   
                   i -= 1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA13:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0 
           elif self.estado == 14:
               if c == "\"":
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenCSS("Cadena", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.cadena)
                   i -=1
                   self.contacolumna += 1
                   #self.estado = 8
               else:
                   self.estado = 14
                   self.auxlex += c

           i += 1

       return self.listaSalida

   def imprimirListaTokens(self, lista: deque):
       for f in lista:
           print(f)

   def pasarListaAString(self):
       for f in self.listaTokens:
           hola = f.toString() + "\n"
           self.stringListaSalida += hola
       return self.stringListaSalida

   def getColores(self):
       return self.listaColores

   def agregarToken(self, tipoToken):
       n = TokenC(tipoToken, self.auxlex)
       self.listaSalida.append(n)
       self.auxlex = ""
       self.estado = 0

   def crearHTMLReportes(self):
       contenido = self.reporteCompleto()
       #print(contenido)
       path = self.linklinux

       if path == "":
           print("ERROR: no hay ruta :C")
           return

        #  if os.path.exists(os.path.dirname(path)):
        #  os.remove(path)
        #   time.sleep(1)

       path = path.replace('.', '')
       path2 = path + "ReporteCSS.html"

       if not os.path.exists(os.path.dirname(path2)):
           try:
               os.makedirs(os.path.dirname(path2))
           except OSError as exc: # Guard against race condition
              if exc.errno != errno.EEXIST:
                  raise
            
       with open(path2, "w") as f:
            f.write(contenido) 

       print("Reporte generado con éxito :D")
       time.sleep(1)
       webbrowser.open('file://' + os.path.realpath(path2))
   
   def reporteCompleto(self):
        frase_actual = ("<!DOCTYPE HTML>" +
                "<html>" +
                    "<head>" +
                        "<title>Mis Tokens CSS</title>" +
                        "<meta charset=\"utf8\">" +
                "</head>" +
                "<body><h1>Reporte de Análisis</h1>" +
                "<h2>Lista de Tokens Aprobados</h2>")
        self.mihtml = frase_actual
       
       #acá van mis tokens geniales

        frase_actual = ("<table border=\"1\">"
            + "<thead>"
            + "<tr><th><strong>#</strong></th>"
            + "<th><strong>Tipo</strong></th>"
            + "<th><strong>Valor de Token</strong></th>"+
            "<th><strong>Fila</strong></th>" +
            "<th><strong>Columna</strong></th>"+
            "<th><strong>Estado</strong></th></tr></thead>"
            + "<tbody>")
        self.mihtml = self.mihtml + frase_actual

        contador = 0

        for f in self.listaTokens:
            holi = str(contador)
            scontafila = str(f.contafilaa)
            scontacolumna = str(f.contacolumnaa)
            token_valor = f.valor.replace("<", "&lt;")
            tokenvalor = token_valor.replace(">", "&gt;")
            stringEstado =str(f.estado)

            frase_actual = ("<tr><td>" + holi + "</td>"
                    + "<td>" + f.tipo + "</td>"
                    + "<td>" + tokenvalor + "</td>"
                    + "<td>" + scontafila+ "</td>"
                    + "<td>" + scontacolumna + "</td>"
                    + "<td>" + stringEstado + "</td>"
                    + " </tr>")

            self.mihtml = self.mihtml + frase_actual
            contador += 1
       
        #try:
           
        #except:
        #   print("Algo pasó a la hora del for en los reportes aprobados :c")

        frase_actual = "</tbody></table></div><br><br><br>"
        self.mihtml = self.mihtml + frase_actual

        #aquí empiezan los errores léxicos

        contador2 = 0

        frase_actual = "<h2>Lista de Errores Léxicos</h2>"
        self.mihtml = self.mihtml + frase_actual

        frase_actual = ("<table border=\"1\">"
             + "<thead>"
             + "<tr><th><strong>#</strong></th>"
             + "<th><strong>Fila</strong></th>"
             + "<th><strong>Columna</strong></th>"
             + "<th><strong>Caracter</strong></th>"
             + "<th><strong>Estado</strong></th>"
             + "<th><strong>Descripción</strong></th></tr></thead>"
             + "<tbody>")

        self.mihtml = self.mihtml + frase_actual

        #try:
        for f in self.listaErrores:
            hello = str(contador2)
            slinea = str(f.linea)
            scol = str(f.columna)
            token_valor = f.descripcion.replace("<", "&lt;")
            tokenvalor = token_valor.replace(">", "&gt;")
            stringEstado =str(f.estado)

            frase_actual = ("<tr><td>" + hello + "</td>"
                + "<td>" + slinea + "</td>"
                + "<td>" + scol + "</td>"
                + "<td>" + f.caracter_error+ "</td>"
                + "<td>" + stringEstado+ "</td>"
                + "<td>" + tokenvalor + "</td>"
                + " </tr>")
            self.mihtml = self.mihtml + frase_actual
            contador2 += 1
        #except:
        # print("Algo pasó a la hora del for en los reportes de error :c")
    
        frase_actual = "</tbody></table></div><br><br><br>"
        self.mihtml = self.mihtml + frase_actual
        frase_actual = "</body></html>"
        self.mihtml = self.mihtml + frase_actual

        return self.mihtml
