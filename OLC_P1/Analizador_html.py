import enum
from enum import Enum, auto
from collections import deque
from pathlib import Path
import os
import errno
import time
import subprocess
import webbrowser



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

class TokenHTML:
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
        cadena = self.tipo +  " -> '" + self.valor + "' [" + str(self.contafilaa) + "," + str(self.contacolumnaa)+"]"
        return cadena


class Token(enum.Enum):
    html_abrir = auto()
    html_cerrar = auto()
    head_abrir = auto()
    head_cerrar = auto()
    title_abrir = auto()
    title_cerrar = auto()
    body_abrir = auto()
    body_cerrar = auto()
    h1_abrir = auto()
    h1_cerrar = auto()
    h2_abrir = auto()
    h2_cerrar = auto()
    h3_abrir = auto()
    h3_cerrar = auto()
    h4_abrir = auto()
    h4_cerrar = auto()
    h5_abrir = auto()
    h5_cerrar = auto()
    h6_abrir = auto()
    h6_cerrar = auto()
    p_abrir = auto()
    p_cerrar = auto()
    br = auto()
    texto = auto()
    img = auto()
    src = auto()
    igual = auto()
    comillas_dobles = auto()
    comillas_simples = auto()
    cadena = auto()
    link = auto()
    a_abrir = auto()
    a_cerrar = auto()
    href = auto()
    ul_abrir = auto()
    ul_cerrar = auto()
    ol_abrir = auto()
    ol_cerrar = auto()
    li_abrir = auto()
    li_cerrar = auto()
    style = auto()
    table_abrir = auto()
    table_cerrar = auto()
    border = auto()
    caption_abrir = auto()
    caption_cerrar = auto()
    tr_abrir = auto()
    tr_cerrar = auto()
    th_abrir = auto()
    th_cerrar = auto()
    td_abrir = auto()
    td_cerrar = auto()
    col = auto()
    colgroup_abrir = auto()
    colgroup_cerrar = auto()
    thead_abrir = auto()
    thead_cerrar = auto()
    tbody_abrir = auto()
    tbody_cerrar = auto()
    tfoot_abrir = auto()
    tfoot_cerrar = auto()
    pr_cerrar = auto()
    ruta_abrir = auto()
    ruta_cerrar = auto()
    path_windows = auto()
    path_linux = auto()


class ErrorHtml:
    def __init__(self, linea, columna, caracter_error):
        self.linea = linea
        self.columna = columna
        self.caracter_error = caracter_error
        self.descripcion = "El caracter " + \
            self.caracter_error + " no pertenece al lenguaje"

#
#
#       ANALIZADOR
#
#



class AnalizadorHTML:

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
   espathwindows = False
   espathlinux = False
   rutalinux = ""

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
       #entrada1 = entrada.strip()
       entrada = entrada + '%'
       self.estado = 0
      # print("'",entrada1,"'")

       #BANDERAS

       c = ''
       y = len(entrada)

       i = 0
        #for i in range(y):
       while (i < y):
           c = entrada[i]

           #acá comiendo a mandar todo a todos lados

           if self.estado == 0:
               if c == '<':
                   #etiqueta abierta
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
               elif c == '\r':
                   self.contacolumna += 1
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
               elif c == '=':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenHTML("Igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.igual)
                   self.contacolumna += 1
               elif c == '\"':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenHTML("Comillas dobles", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comillas_dobles)
                   self.contacolumna += 1

                   if self.escadena == False:
                       self.escadena = True
                       self.estado = 6
                   else:
                       self.escadena = False
                       self.estado = 8
               elif c == '\'':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenHTML("Comillas simples", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comillas_simples)
                   self.contacolumna += 1

                   if self.escadena == False:
                       self.escadena = True
                       self.estado = 7
                   else:
                       self.escadena = False
                       self.estado = 8
                   
               else:
                   if c == '%':
                       print("El análisis Ha terminado")
                   else:
                       #print("Error Léxico con: " + c)
                       #acepto todo hasta que venga un '<'
                       self.contacolumna += 1
                       self.auxlex += c
                       self.estado = 9         
           elif self.estado == 1:
               #acá junto las palabras reservadas
               if c == '>':
                   self.contacolumna += 1
                   self.estado = 2
                   self.auxlex += c
                  # print("mandando")
               elif c == ' ':
                   self.contacolumna += 1
                   self.estado = 3
               else:
                   self.contacolumna += 1
                   self.auxlex += c
                   self.estado = 1
                   #print(self.auxlex)
           elif self.estado == 2:
               w = TokenColor(self.auxlex, 'rojo')
               self.listaColores.append(w)
               if self.auxlex.lower() == "<html>":
                   n = TokenHTML("PR - html abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.html_abrir)
                   i -=1
               elif self.auxlex.lower() == "</html>":
                   n = TokenHTML("PR - html cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.html_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<head>":
                   n = TokenHTML("PR - head abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.head_abrir)
                   i -=1
               elif self.auxlex.lower() == "</head>":
                   n = TokenHTML("PR - head cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.head_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<title>":
                   n = TokenHTML("PR - title abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.title_abrir)
                   i -=1
               elif self.auxlex.lower() == "</title>":
                   n = TokenHTML("PR - title cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.title_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<body>":
                   n = TokenHTML("PR - body abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.body_abrir)
                   i -=1
               elif self.auxlex.lower() == "</body>":
                   n = TokenHTML("PR - body cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.body_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<h1>":
                   n = TokenHTML("PR - h1 abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h1_abrir)
                   i -=1
               elif self.auxlex.lower() == "</h1>":
                   n = TokenHTML("PR - h1 cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h1_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<h2>":
                   n = TokenHTML("PR - h2 abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h2_abrir)
                   i -=1
               elif self.auxlex.lower() == "</h2>":
                   n = TokenHTML("PR - h2 cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h2_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<h3>":
                   n = TokenHTML("PR - h3 abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h3_abrir)
                   i -=1
               elif self.auxlex.lower() == "</h3>":
                   n = TokenHTML("PR - h3 cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h3_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<h4>":
                   n = TokenHTML("PR - h4 abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h4_abrir)
                   i -=1
               elif self.auxlex.lower() == "</h4>":
                   n = TokenHTML("PR - h4 cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h4_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<h5>":
                   n = TokenHTML("PR - h5 abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h5_abrir)
                   i -=1
               elif self.auxlex.lower() == "</h5>":
                   n = TokenHTML("PR - h5 cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h5_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<h6>":
                   n = TokenHTML("PR - h6 abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h6_abrir)
                   i -=1
               elif self.auxlex.lower() == "</h6>":
                   n = TokenHTML("PR - h6 cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h6_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<p>":
                   n = TokenHTML("PR - p abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.p_abrir)
                   i -=1
               elif self.auxlex.lower() == "</p>":
                   n = TokenHTML("PR - p cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.p_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<br>":
                   n = TokenHTML("PR - br", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.br)
                   i -=1
               elif self.auxlex.lower() == "<ul>":
                   n = TokenHTML("PR - ul abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ul_abrir)
                   i -=1
               elif self.auxlex.lower() == "</ul>":
                   n = TokenHTML("PR - ul cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ul_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<li>":
                   n = TokenHTML("PR - li abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.li_abrir)
                   i -=1
               elif self.auxlex.lower() == "</li>":
                   n = TokenHTML("PR - li cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.li_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<table>":
                   n = TokenHTML("PR - table abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.table_abrir)
                   i -=1
               elif self.auxlex.lower() == "</table>":
                   n = TokenHTML("PR - table cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.table_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<img>":
                   n = TokenHTML("PR - img", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.img)
                   i -=1 
               elif self.auxlex.lower() == "<caption>":
                   n = TokenHTML("PR - caption abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.caption_abrir)
                   i -=1
               elif self.auxlex.lower() == "</caption>":
                   n = TokenHTML("PR - caption cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.caption_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<tr>":
                   n = TokenHTML("PR - tr abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tr_abrir)
                   i -=1
               elif self.auxlex.lower() == "</tr>":
                   n = TokenHTML("PR - tr cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tr_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<th>":
                   n = TokenHTML("PR - th abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.th_abrir)
                   i -=1
               elif self.auxlex.lower() == "</th>":
                   n = TokenHTML("PR - th cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.th_cerrar)
                   i -=1 
               elif self.auxlex.lower() == "<td>":
                   n = TokenHTML("PR - td abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.td_abrir)
                   i -=1
               elif self.auxlex.lower() == "</td>":
                   n = TokenHTML("PR - td cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.td_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<a>":
                   n = TokenHTML("PR - a abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.a_abrir)
                   i -=1
               elif self.auxlex.lower() == "</a>":
                   n = TokenHTML("PR - a cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.a_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<colgroup>":
                   n = TokenHTML("PR - colgroup abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.colgroup_abrir)
                   i -=1
               elif self.auxlex.lower() == "</colgroup>":
                   n = TokenHTML("PR - colgroup cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.colgroup_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<thead>":
                   n = TokenHTML("PR - thead abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.thead_abrir)
                   i -=1
               elif self.auxlex.lower() == "</thead>":
                   n = TokenHTML("PR - thead cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.thead_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<tbody>":
                   n = TokenHTML("PR - tbody abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tbody_abrir)
                   i -=1
               elif self.auxlex.lower() == "</tbody>":
                   n = TokenHTML("PR - tbody cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tbody_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<tfoot>":
                   n = TokenHTML("PR - tfoot abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tfoot_abrir)
                   i -=1
               elif self.auxlex.lower() == "</tfoot>":
                   n = TokenHTML("PR - tfoot cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tfoot_cerrar)
                   i -=1
               elif self.auxlex.lower() == "<col>":
                   n = TokenHTML("PR - col", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.col)
                   i -=1
               elif self.auxlex.lower() == "<ol>":
                   n = TokenHTML("PR - ol abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ol_abrir)
                   i -=1
               elif self.auxlex.lower() == "</ol>":
                   n = TokenHTML("PR - ol cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ol_cerrar)
                   i -=1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA2:  -> '", self.auxlex, "'")
                   self.listaColores.pop()
                   n = ErrorHtml(self.contafila, self.contacolumna, self.auxlex)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0

                   i -=1
           elif self.estado == 3:
               w = TokenColor(self.auxlex, 'rojo')
               self.listaColores.append(w)
               if self.auxlex.lower() == "<html":
                   n = TokenHTML("PR - html abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.html_abrir)
                   i -=1
               elif self.auxlex.lower() == "<head":
                   n = TokenHTML("PR - head abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.head_abrir)
                   i -=1
               elif self.auxlex.lower() == "<title":
                   n = TokenHTML("PR - title abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.title_abrir)
                   i -=1
               elif self.auxlex.lower() == "<body":
                   n = TokenHTML("PR - body abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.body_abrir)
                   i -=1
               elif self.auxlex.lower() == "<h1":
                   n = TokenHTML("PR - h1 abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h1_abrir)
                   i -=1
               elif self.auxlex.lower() == "<h2":
                   n = TokenHTML("PR - h2 abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h2_abrir)
                   i -=1
               elif self.auxlex.lower() == "<h3":
                   n = TokenHTML("PR - h3 abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h3_abrir)
                   i -=1
               elif self.auxlex.lower() == "<h4":
                   n = TokenHTML("PR - h4 abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h4_abrir)
                   i -=1
               elif self.auxlex.lower() == "<h5":
                   n = TokenHTML("PR - h5 abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h5_abrir)
                   i -=1
               elif self.auxlex.lower() == "<h6":
                   n = TokenHTML("PR - h6 abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.h6_abrir)
                   i -=1
               elif self.auxlex.lower() == "<p":
                   n = TokenHTML("PR - p abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.p_abrir)
                   i -=1
               elif self.auxlex.lower() == "<ul":
                   n = TokenHTML("PR - ul abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ul_abrir)
                   i -=1
               elif self.auxlex.lower() == "<li":
                   n = TokenHTML("PR - li abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.li_abrir)
                   i -=1
               elif self.auxlex.lower() == "<table":
                   n = TokenHTML("PR - table abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.table_abrir)
                   i -=1
               elif self.auxlex.lower() == "<img":
                   n = TokenHTML("PR - img2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.img)
                   i -=1 
               elif self.auxlex.lower() == "<caption":
                   n = TokenHTML("PR - caption abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.caption_abrir)
                   i -=1
               elif self.auxlex.lower() == "<tr":
                   n = TokenHTML("PR - tr abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tr_abrir)
                   i -=1
               elif self.auxlex.lower() == "<th":
                   n = TokenHTML("PR - th abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.th_abrir)
                   i -=1
               elif self.auxlex.lower() == "<td":
                   n = TokenHTML("PR - td abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.td_abrir)
                   i -=1
               elif self.auxlex.lower() == "<a":
                   n = TokenHTML("PR - a abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.a_abrir)
                   i -=1
               elif self.auxlex.lower() == "<colgroup":
                   n = TokenHTML("PR - colgroup abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.colgroup_abrir)
                   i -=1
               elif self.auxlex.lower() == "<thead":
                   n = TokenHTML("PR - thead abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.thead_abrir)
                   i -=1
               elif self.auxlex.lower() == "<tbody":
                   n = TokenHTML("PR - tbody abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tbody_abrir)
                   i -=1
               elif self.auxlex.lower() == "<tfoot":
                   n = TokenHTML("PR - tfoot abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.tfoot_abrir)
                   i -=1
               elif self.auxlex.lower() == "<col":
                   n = TokenHTML("PR - col2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.col)
                   i -=1
               elif self.auxlex.lower() == "<ol":
                   n = TokenHTML("PR - ol abrir2", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ol_abrir)
                   i -=1
               elif self.auxlex.lower() == "<!--pathw:":
                   n = TokenHTML("PR - ruta windows abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ruta_abrir)
                   self.espathwindows = True
                   i -=1
               elif self.auxlex.lower() == "<!--pathl:":
                   n = TokenHTML("PR - ruta linux abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.ruta_abrir)
                   self.espathlinux = True
                   i -=1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA3:  -> '", self.auxlex, "'")
                   self.listaColores.pop()
                   n = ErrorHtml(self.contafila, self.contacolumna, self.auxlex)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0

                   i -=1
               w = TokenColor(" ", 'rojo')
               self.listaColores.append(w)
               self.estado = 4
           elif self.estado == 4:
               #de aquí vienen los que están abiertos
               if (self.espathlinux == True) or (self.espathwindows == True):
                   if c == '>':                       
                       self.auxlex += c
                       if self.espathlinux == True:
                           self.rutalinux = self.auxlex.replace('-->', '')
                           print("PATH ENCONTRADO: ", self.rutalinux)
                        # tengo rutaaa-->   

                       self.espathwindows = False
                       self.espathlinux = False                    

                       w = TokenColor(self.auxlex, 'gris')
                       self.listaColores.append(w)
                       n = TokenHTML("Path", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.igual)
                       self.contacolumna += 1
                   else:
                       self.contacolumna += 1
                       self.auxlex += c
                       self.estado = 4
               elif c == '=':
                   self.contacolumna += 1
                   self.estado = 5
                   i -=1
                  # print("mandando")
               else:
                   self.contacolumna += 1
                   self.auxlex += c
                   self.estado = 4
                   #print(self.auxlex)
           elif self.estado == 5:
               w = TokenColor(self.auxlex, 'rojo')
               self.listaColores.append(w)
               if self.auxlex.lower() == "src":
                   n = TokenHTML("PR - src", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.src)
                   i -=1
               elif self.auxlex.lower() == "href":
                   n = TokenHTML("PR - href", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.href)
                   i -=1
               elif self.auxlex.lower() == "style":
                   n = TokenHTML("PR - style", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.style)
                   i -=1
               elif self.auxlex.lower() == "border":
                   n = TokenHTML("PR - border", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.border)
                   i -=1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA5:  -> '", self.auxlex, "'")
                   self.listaColores.pop()
                   n = ErrorHtml(self.contafila, self.contacolumna, self.auxlex)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0

                   i -=1
           elif self.estado == 6:
               if c == "\"":
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenHTML("Cadena", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.cadena)
                   i -=1
                   self.contacolumna += 1
                   #self.estado = 8
               else:
                   self.estado = 6
                   self.auxlex += c
           elif self.estado == 7:
               if c == "'":
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenHTML("Cadena", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.cadena)
                   i -=1
                   self.contacolumna += 1
                   self.estado = 8
               else:
                   self.estado = 7
                   self.auxlex += c
           elif self.estado == 8:
               if c == '>':
                   #acá es cuando estoy cerrando cadena
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'rojo')
                   self.listaColores.append(w)
                   n = TokenHTML("PR - cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_cerrar)
                   #todo
                   #i -=1
                   # i-=2
                   self.contacolumna += 1
               elif c == ' ':
                   w = TokenColor(" ", 'rojo')
                   self.listaColores.append(w)
                   self.estado = 8
           elif self.estado == 9:
               if c == '<':
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenHTML("Texto normal", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.texto)
                   #todo
                   i -=1
                   self.contacolumna += 1
               else:
                   self.estado = 9
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
      # print(contenido)
       path = self.rutalinux

       if path == "":
           print("ERROR: no hay ruta :C")
           return

        #  if os.path.exists(os.path.dirname(path)):
        #  os.remove(path)
        #   time.sleep(1)


       if not os.path.exists(os.path.dirname(path)):
           try:
               os.makedirs(os.path.dirname(path))
           except OSError as exc: # Guard against race condition
              if exc.errno != errno.EEXIST:
                  raise
            
       with open(path, "w") as f:
            f.write(contenido) 

       print("Reporte generado con éxito :D")
       time.sleep(1)
       webbrowser.open('file://' + os.path.realpath(path))
       
   def reporteCompleto(self):

        frase_actual = ("<!DOCTYPE HTML>" +
                "<html>" +
                    "<head>" +
                        "<title>Mis Tokens</title>" +
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
            "<th><strong>Columna</strong></th></tr></thead>"
            + "<tbody>")
        self.mihtml = self.mihtml + frase_actual

        contador = 0

        for f in self.listaTokens:
            holi = str(contador)
            scontafila = str(f.contafilaa)
            scontacolumna = str(f.contacolumnaa)
            token_valor = f.valor.replace("<", "&lt;")
            tokenvalor = token_valor.replace(">", "&gt;")

            frase_actual = ("<tr><td>" + holi + "</td>"
                    + "<td>" + f.tipo + "</td>"
                    + "<td>" + tokenvalor + "</td>"
                    + "<td>" + scontafila+ "</td>"
                    + "<td>" + scontacolumna + "</td>"
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

            frase_actual = ("<tr><td>" + hello + "</td>"
                + "<td>" + slinea + "</td>"
                + "<td>" + scol + "</td>"
                + "<td>" + f.caracter_error+ "</td>"
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





  




                


            


                

                    
















