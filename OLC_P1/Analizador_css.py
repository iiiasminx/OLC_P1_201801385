import enum
from enum import Enum, auto
from collections import deque
from pathlib import Path
import os
import errno



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
    def __init__(self, tipo, valor, contafila, contacolumna):
        self.valor = valor
        self.tipo = tipo
        self.contafilaa = contafila
        self.contacolumnaa = contacolumna
        # hola = tokenhtml(token.html_abrir)

    def getValorToken(self):
        return self.valor

    def getTipo(self):
        return self.tipo

    def __str__(self):
        cadena = self.tipo +  " -> '" + self.valor + "' [" + str(self.contafilaa) + "," + str(self.contacolumnaa)+"]"
        return cadena

    def toString(self):
        cadena = self.tipo +  " -> '" + self.valor + "' [" + str(self.contafilaa) + "," + str(self.contacolumnaa)+"]"
        return cadena

class Token(enum.Enum):
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
    pr_padd_left = auto()
    pr_padd_right = auto()
    pr_padd_bottom = auto()
    pr_padd_top = auto()
    pr_padding = auto()
    pr_display = auto()
    pr_line_height = auto()
    pr_width = auto()
    pr_height = auto()
    pr_mar_top = auto()
    pr_mar_right = auto()
    pr_mar_bottom = auto()
    pr_mar_left = auto()
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
    numeral = auto()
    menos = auto()
    parentesis_abrir = auto()
    parentesis_cerrar = auto()
    comillas_dobles = auto()
    punto = auto()
    identificador = auto()

class ErrorCSS:
    def __init__(self, linea, columna, caracter_error):
        self.linea = linea
        self.columna = columna
        self.caracter_error = caracter_error
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

   listaErrores = deque()
   listaTokens = deque()
   listaColores = deque()

   arreglotokens = []

   stringListaSalida = ""
   mihtml = ""

   def comenzar(self):
       self.stringListaSalida = ""
       self.listaColores.clear()
       self.listaErrores.clear()
       self.listaSalida.clear()
       self.listaTokens.clear()

   def escanear(self, entrada):
       entrada = entrada + '%'
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
                   self.estado = 4
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
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Llaves abrir", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.llave_abrir)
                   self.contacolumna += 1
                   self.yaNumeral = False
               elif c == '#':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Numeral", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.numeral)
                   self.contacolumna += 1
                   self.yaNumeral = True
               elif c == '.':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Punto", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.punto)
                   self.contacolumna += 1
               elif c == ',':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Coma", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.coma)
                   self.contacolumna += 1
               else:
                   if c == '%':
                       print("El análisis Ha terminado")
                   else:
                       if c == ' ':
                           self.contacolumna += 1
                           w = TokenColor(c, 'blanco')
                           self.listaColores.append(w)
                       else:
                           print("NO SE RECONOCE LA PALABRA0:  -> '", self.auxlex, "'")
                           n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex)
                           self.listaErrores.append(n)
                           self.auxlex = ""
                           self.estado = 0    
           elif self.estado == 1:
               if c == '*':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenCSS("Inicio Comentario", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_abrir)
                   self.contacolumna += 1

                   self.estado = 2
               else:
                   print("NO SE RECONOCE LA PALABRA1:  -> '", self.auxlex, "'")
                   n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0

                   i -=1
           elif self.estado == 2:
               if c == '*':
                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenCSS("Cuerpo Comentario", self.auxlex, self.contafila, self.contacolumna)
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
                   n = TokenCSS("Final Comentario", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_cerrar)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Asterisco", self.auxlex, self.contafila, self.contacolumna)
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
                       n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.identificador)
                       w = TokenColor(c, 'blanco')
                       self.listaColores.append(w)
                   else:
                       self.estado = 5
                   #pongo iwal todo lo que va de acá para abajo
               elif c == '{' or c == ':' or c == '#' or c == ',':
                   w = TokenColor(self.auxlex, 'verde')
                   self.listaColores.append(w)
                   n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.identificador)
                   i -=1
               else:
                       print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                       n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex)
                       self.listaErrores.append(n)
                       self.auxlex = ""
                       self.estado = 0
           elif self.estado == 5:
               if c == '{' or c == ':' or c == '#' or c == ',':
                   w = TokenColor(self.auxlex, 'verde')
                   self.listaColores.append(w)
                   n = TokenCSS("Identificador", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.identificador)
                   w = TokenColor(" ", 'verde')
                   self.listaColores.append(w)
                   i -=1
               else:
                       print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                       n = ErrorCSS(self.contafila, self.contacolumna, self.auxlex)
                       self.listaErrores.append(n)
                       self.auxlex = ""
                       self.estado = 0
           elif self.estado == 6:
               #dos puntos, dos puntos dobles
               if c == ':':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Dos puntos dobles", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.dos_puntos_dobles)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenCSS("Dos puntos", self.auxlex, self.contafila, self.contacolumna)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.dos_puntos)
                   self.contacolumna += 1
                   i -= 1

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
