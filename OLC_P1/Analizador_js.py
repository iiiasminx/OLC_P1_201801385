import enum
from enum import Enum, auto
from collections import deque
from pathlib import Path
import os
import errno
import subprocess
import webbrowser
import time
from subprocess import check_call
from PIL import Image


#
#
#       TOKEN
#
#

class TkOperacion:
    def __init__(self, operacion, analisis, linea):
        # Token.html_cerrar, "hdsih"
        self.operacion = operacion
        self.analisis = analisis
        self.linea = linea
    def __str__(self):
        return '{} {} {}'.format(self.operacion, "->", self.analisis)
        #return self.tipo, " -> ", self.valor

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

class TokenJS:
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
        cadena = self.tipo +  " -> '" + self.valor + "' [" + str(self.contafilaa) + "," + str(self.contacolumnaa)+"]\n"
        return cadena

class ErrorJS:
    def __init__(self, linea, columna, caracter_error, estado):
        self.linea = linea
        self.columna = columna
        self.caracter_error = caracter_error
        self.estado = estado
        self.descripcion = "El caracter " + \
            self.caracter_error + " no pertenece al lenguaje"

class Token(enum.Enum):
    comentario_unalinea = auto()
    comentario_multilinea_abrir  = auto()
    comentario_multilinea_cerrar = auto()
    cuerpo_comentario = auto()
    pr_var  = auto()
    identificador = auto()
    igual = auto()
    numero = auto()
    comillas_dobles = auto()
    comillas_simples = auto()
    cadena = auto()
    pr_true = auto()
    pr_false = auto()
    asignacion = auto() #asterisco iwal
    punto_y_coma = auto()
    pr_if = auto()
    parentesis_abrir = auto()
    parentesis_cerrar = auto()
    mayor = auto()
    menor = auto()
    mayor_igual = auto()
    menor_igual = auto()
    igual_igual = auto()
    igual_igual_igual = auto()
    pr_console_log = auto()
    llave_abrir = auto()
    llave_cerrar = auto()
    pr_else = auto()
    pr_else_if = auto()
    pr_for = auto()
    mas_mas = auto()
    menos_menos = auto()
    mas_igual = auto()
    menos_igual = auto()
    pr_while = auto()
    pr_do = auto()
    mas = auto()
    menos = auto()
    asterisco = auto()
    dividido = auto()
    pr_continue = auto()
    pr_break = auto()
    pr_return = auto()
    pr_function = auto()
    nombre_funcion = auto()
    pr_this = auto()
    pr_constructor = auto()
    pr_class = auto()
    parametro = auto()
    pr_Math_pow = auto()
    distinto = auto()
    l_and = auto()
    l_or = auto()
    l_not = auto()
    ruta_abrir = auto()
    ruta_cerrar = auto()
    punto = auto()
    coma = auto()
    negacion = auto()
    dos_puntos = auto()
    guion_bajo = auto()
    pr_null = auto()
    salto_de_linea = auto()

class AnalizadorJS:

   #COSAS QUE USO PARA EL SINTÁCTITCO
   esSintáctico = False
   pilaSintactico = deque()
   todoBientodoCorrecto = True

   operacion = ""
   listaOperaciones = deque()
   htmlsintactico = ""

   #TODO LO DEMÁS
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
   eschar = False
   yapunto = False

   listaErrores = deque()
   listaTokens = deque()
   listaColores = deque()
   
   arreglotokens = []

   linklinux = ""
   stringListaSalida = ""
   mihtml = ""

   yaespacioinicio = False
   contaiwales = 0
   vienenNumeros = False

   grafito = ""
   yacomentariomulti = False
   yacomentariouna = False
   yacadena = False
   yacadenachikita  = False
   yanumeroo = False
   yaiwaliwal = False
   yaii = False

   stringArchivo = ""

   #
   #    BANDERAS DE CADA COSITO
   #

   ultimoAsterisco = False

   def setSintactico(self):
       self.esSintáctico = True
       

   def comenzar(self):
       self.stringListaSalida = ""
       self.listaColores.clear()
       self.listaErrores.clear()
       self.listaSalida.clear()
       self.listaTokens.clear()
       self.pilaSintactico.clear()
       self.todoBientodoCorrecto = True
       self.operacion = ""
       self.htmlsintactico = ""
       self.mihtml = ""
       self.grafito = ""

   def escanear(self, entrada):
       entrada = entrada + '$'
       self.estado = 0
      # print("'",entrada1,"'")

       print("Es Sintáctico? ", self.esSintáctico)

       #BANDERAS

       c = ''
       y = len(entrada)

       i = 0

       while (i < y):
           c = entrada[i]           

           #acá comiendo a mandar todo a todos lados
           if self.estado == 0 :
               #acá mando todo a todos lados               
               if c.isalpha():
                    #puede ser palabra reservada
                    self.estado = 5
                    self.auxlex += c
                    self.contacolumna += 1
               elif c == '/':
                   #podría ser comentario
                   self.estado = 1
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '*':
                   #puede ser multiplicador, cosito con iwal, o cierre comentario
                   self.estado = 4
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '=':
                   #puede ser iwal, iwaliwal o iwaliwaliwal
                   self.estado = 8
                   self.contaiwales = 1
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == ' ':
                   self.contacolumna += 1
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
               elif c.isnumeric():
                   self.estado = 9
                   self.auxlex += c
                   self.contacolumna += 1
                   if self.yanumeroo == False:
                       s0s9 = "S0 -> S9[ label=\"digito\" ];\n"                    
                       if s0s9 not in self.grafito:
                           self.grafito += s0s9
                           self.grafito += "S9 [style=filled, fillcolor=darkorchid3];\n"
               elif c == '\'':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenJS("Comillas simples", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comillas_simples)
                   self.contacolumna += 1

                   if self.eschar == False:
                       self.eschar = True
                       self.estado = 11

                       if self.yacadenachikita == False:
                            s0s12 = "S0 -> S12[ label=\"'\" ];\n"
                            if s0s12 not in self.grafito:
                                self.grafito += s0s12     
                   else:
                       self.eschar = False
                       if self.yacadenachikita == False:
                            self.yacadenachikita = True
                            s12s13 = "S12 -> S13[ label=\"'\" ];\n"
                            if s12s13 not in self.grafito:
                                self.grafito += s12s13
                                self.grafito += "S13 [style=filled, fillcolor=darkorchid3];\n"
               elif c == '\"':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'amarillo')
                   self.listaColores.append(w)
                   n = TokenJS("Comillas dobles", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comillas_dobles)
                   self.contacolumna += 1                   

                   if self.escadena == False:
                       self.escadena = True
                       self.estado = 10

                       if self.yacadena == False:
                            s0s10 = "S0 -> S10[ label=\"''\" ];\n"
                            if s0s10 not in self.grafito:
                                self.grafito += s0s10                           
                   else:
                       self.escadena = False
                       if self.yacadena == False:
                            self.yacadena = True
                            s10s11 = "S10 -> S11[ label=\"''\" ];\n"
                            if s10s11 not in self.grafito:
                                self.grafito += s10s11
                                self.grafito += "S11 [style=filled, fillcolor=darkorchid3];\n"
               elif c == '\n':
                   self.auxlex += c
                   self.contafila += 1
                   self.contacolumna = 0
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
                   self.agregarToken(Token.salto_de_linea)                   
               elif c == '\r':
                   self.contacolumna += 1
                   w = TokenColor(c, 'blanco')
                   self.listaColores.append(w)
               elif c == '{':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Llaves abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)

                   self.agregarToken(Token.llave_abrir)
                   self.contacolumna += 1  
               elif c == ':':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Dos puntos", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.dos_puntos)
                   self.contacolumna += 1          
               elif c == '}':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Llaves cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)

                   self.agregarToken(Token.llave_cerrar)
                   self.contacolumna += 1
               elif c == '.':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Punto", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)

                   self.agregarToken(Token.punto)
                   self.contacolumna += 1
               elif c == ',':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Coma", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.coma)
                   self.contacolumna += 1
               elif c == '(':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Paréntesis abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)

                   self.agregarToken(Token.parentesis_abrir)
                   self.contacolumna += 1                   
               elif c == ')':
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Paréntesis cerrar", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)

                   self.agregarToken(Token.parentesis_cerrar)
                   self.contacolumna += 1
               elif c == ';':
                   self.yaPR = False
                   self.auxlex += c
                   w = TokenColor(self.auxlex, 'negro')
                   self.listaColores.append(w)
                   n = TokenJS("Punto y coma", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)                   

                   self.agregarToken(Token.punto_y_coma)
                   self.contacolumna += 1
               elif c == '+':
                   #puede ser mas, mas iwal, mas mas
                   self.estado = 7
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '-':
                   #puede ser menos, menos iwal, menos menos
                   self.estado = 12
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '!':
                   #puede ser != o !exp
                   self.estado = 13
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '<':
                   self.estado = 15
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '>':
                   self.estado = 16
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '&':
                   self.estado = 17
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '|':
                   self.estado = 18
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
                           n = ErrorJS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                           self.listaErrores.append(n)
                           self.auxlex = ""
                           self.estado = 0 
           elif self.estado == 1: # /
               if c == '*':
                   self.auxlex += c

                   if self.yacomentariomulti == False:
                       s0s1 = "S0 -> S1[ label=\"/\" ];\n"
                       s1s2 = "S1 -> S2[ label=\"*\" ];\n"  

                       if s0s1 not in self.grafito:
                           self.grafito += s0s1
                    
                       if s1s2 not in self.grafito:
                           self.grafito += s1s2
                          

                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenJS("Inicio Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_multilinea_abrir)
                   self.contacolumna += 1

                   self.estado = 2
               elif c == '/':
                   self.auxlex += c

                   if self.yacomentariouna == False:
                       s0s1 = "S0 -> S1[ label=\"/\" ];\n"
                       s1s5 = "S1 -> S5[ label=\"/\" ];\n"  
                       if s0s1 not in self.grafito:
                           self.grafito += s0s1
                       if s1s5 not in self.grafito:
                           self.grafito += s1s5

                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenJS("Inicio Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_unalinea)
                   self.contacolumna += 1

                   self.estado = 3      
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Dividido", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.dividido)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 2: # comentario multilinea
               if c == '*':
                   #puede ser un asterisco salvaje
                   self.ultimoAsterisco = True
                   self.estado = 2
                   self.auxlex += c
               elif c == '/':
                   if self.ultimoAsterisco == True:                       
                        s2s3 = "S2 -> S3[ label=\"*\" ];\n" 
                        s2s2 = "S2 -> S2[ label=\"Comentario multilinea \" ];\n" 
                        if self.yacomentariomulti == False:                            
                            if "S2 -> S2[" not in self.grafito:
                                self.grafito += s2s2
                            if s2s3 not in self.grafito:
                                self.grafito += s2s3   


                        self.ultimoAsterisco = False
                        w = TokenColor(self.auxlex, 'gris')
                        self.listaColores.append(w)
                        n = TokenJS("Cuerpo Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                        self.listaTokens.append(n)
                        self.agregarToken(Token.cuerpo_comentario)
                        self.contacolumna += 1                   
                        i -= 2
                   else:
                      self.estado = 2
                      self.auxlex += c 
               else:
                   self.ultimoAsterisco = False
                   self.estado = 2
                   self.auxlex += c
                   if c == '\n':
                       self.contafila += 1
                       self.contacolumna = 0
                   else:
                      self.contacolumna += 1
           elif self.estado == 3: # commentario una linea
               if c == '\n':                   
                   z = self.auxlex.lower()
                   if z.startswith("pathw"):
                       w = TokenColor(self.auxlex, 'gris')
                       self.listaColores.append(w)
                       n = TokenJS("PR - ruta windows abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.ruta_abrir)
                   elif z.startswith("pathl"):
                       w = TokenColor(self.auxlex, 'gris')
                       self.listaColores.append(w)
                       x = self.auxlex
                       self.linklinux = x.replace('PATHL: ', '')
                       print("LINK ENCONTRADO:", self.linklinux)
                       n = TokenJS("PR - ruta linux abrir", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.ruta_abrir)
                   else:
                       w = TokenColor(self.auxlex, 'gris')

                       if self.yacomentariouna == False:
                            self.grafito += " S5 -> S5[ label=\""+ self.auxlex +"\" ];" 
                            self.grafito += " S5 -> S6[ label=\"/n\" ];" 
                            self.grafito += "S6 [style=filled, fillcolor=darkorchid3];\n" 
                            self.yacomentariouna = True

                       self.listaColores.append(w)
                       n = TokenJS("Cuerpo Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                       self.listaTokens.append(n)
                       self.agregarToken(Token.cuerpo_comentario)
                       self.contacolumna += 1                   
                   i -= 1
               else:
                   self.estado = 3
                   self.auxlex += c
           elif self.estado == 4: # *
               if c == '/':
                   self.auxlex += c

                   if self.yacomentariomulti == False:
                       s3s4 = "S3 -> S4[ label=\"/\" ];\n"
                       if s3s4 not in self.grafito:
                           self.grafito += s3s4
                           self.grafito += "S4 [style=filled, fillcolor=darkorchid3];\n"
                           self.yacomentariomulti = True 

                   w = TokenColor(self.auxlex, 'gris')
                   self.listaColores.append(w)
                   n = TokenJS("Final Comentario", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.comentario_multilinea_cerrar)
                   self.contacolumna += 1
               elif c == '=':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Asignacion", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.asignacion)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Asterisco", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.asterisco)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 5: # letras
               if c.isalpha():
                   #acá junto todo lo que pueda venir
                   self.estado = 5
                   self.auxlex += c
                   self.contacolumna += 1
               elif c.isdigit():
                   self.vienenNumeros = True
                   self.estado = 5
                   self.auxlex += c
                   self.contacolumna += 1
               elif c == '_':
                   self.vienenNumeros = True
                   self.estado = 5
                   self.auxlex += c
                   self.contacolumna += 1
               else:
                   self.contacolumna += 1
                   if self.vienenNumeros == True:
                        wangji = TokenColor(self.auxlex, 'verde')
                        self.listaColores.append(wangji)
                        n = TokenJS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                        self.listaTokens.append(n)
                        self.agregarToken(Token.identificador)
                        self.yaespacioinicio = False
                        self.vienenNumeros = False
                        i -=1 
                   else:
                       self.estado = 6                   
           elif self.estado == 6: #PR
               w = TokenColor(self.auxlex, 'rojo')
               self.listaColores.append(w)
               if self.auxlex == "var":
                   n = TokenJS("PR - var", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_var)
                   i -=1
                   self.esvar = True
               elif self.auxlex == "if":
                   n = TokenJS("PR - if", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_if)
                   i -=1    
               elif self.auxlex == "console":
                   #ACA ES CONSOLE.LOG, MANDAR A OTRO ESTADO Y VER QUE PEX
                   n = TokenJS("PR - console.log", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_console_log)
                   i -=1  
               elif self.auxlex == "else":
                   n = TokenJS("PR - else", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_else)
                   i -=1 
               elif self.auxlex == "for":
                   n = TokenJS("PR - for", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_for)
                   i -=1
               elif self.auxlex == "while":
                   n = TokenJS("PR - while", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_while)
                   i -=1
               elif self.auxlex == "do":
                   n = TokenJS("PR - do", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_do)
                   i -=1
               elif self.auxlex == "continue":
                   n = TokenJS("PR - continue", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_continue)
                   i -=1
               elif self.auxlex == "true":
                   self.listaColores.pop()
                   wangji = TokenColor(self.auxlex, 'azul')
                   self.listaColores.append(wangji)
                   n = TokenJS("PR - true", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_true)
                   i -=1
               elif self.auxlex == "false":
                   self.listaColores.pop()
                   wangji = TokenColor(self.auxlex, 'azul')
                   self.listaColores.append(wangji)
                   n = TokenJS("PR - false", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_false)
                   i -=1
               elif self.auxlex == "break":
                   n = TokenJS("PR - break", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_break)
                   i -=1
               elif self.auxlex == "return":
                   n = TokenJS("PR - return", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_return)
                   i -=1
               elif self.auxlex == "function":
                   n = TokenJS("PR - function", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_function)
                   i -=1
               elif self.auxlex == "null":
                   n = TokenJS("PR - null", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_null)
                   i -=1
               elif self.auxlex == "constructor":
                   n = TokenJS("PR - constructor", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_constructor)
                   i -=1
               elif self.auxlex == "class":
                   n = TokenJS("PR - class", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_class)
                   i -=1
               elif self.auxlex == "this":
                   n = TokenJS("PR - this", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.pr_this)
                   i -=1
               else:
                   self.listaColores.pop()
                   wangji = TokenColor(self.auxlex, 'verde')
                   self.listaColores.append(wangji)
                   n = TokenJS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.identificador)
                   self.yaespacioinicio = False
                   i -=1 
                   
               i -= 1
           elif self.estado == 7: # +
               if c == '+':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Mas Mas", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.mas_mas)
                   self.contacolumna += 1
               elif c == '=':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Mas igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.mas_igual)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Mas", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.mas)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 8: # =
              if c == '=':
                  self.estado = 8
                  self.auxlex += c
                  self.contacolumna += 1
                  self.contaiwales += 1
              else:
                   if self.contaiwales == 1:
                      w = TokenColor(self.auxlex, 'naranja')
                      self.listaColores.append(w)
                      n = TokenJS("Igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                      self.listaTokens.append(n)
                      self.agregarToken(Token.igual)
                      self.contacolumna += 1
                      if self.yaiwaliwal == False:
                            s0s8 = "S0 -> S8[ label=\"=\" ];\n" 
                            self.grafito += "S8 [style=filled, fillcolor=darkorchid3];\n" 
                            if s0s8 not in self.grafito:
                                self.grafito += s0s8
                   elif self.contaiwales == 2:
                      w = TokenColor(self.auxlex, 'naranja')
                      self.listaColores.append(w)
                      n = TokenJS("Igual doble", self.auxlex, self.contafila, self.contacolumna, self.estado)
                      self.listaTokens.append(n)
                      self.agregarToken(Token.igual_igual)
                      self.contacolumna += 1
                      if self.yaiwaliwal == False:
                            s0s8 = "S0 -> S8[ label=\"=\" ];\n" 
                            self.grafito += "S8 [style=filled, fillcolor=darkorchid3];\n" 
                            if s0s8 not in self.grafito:
                                self.grafito += s0s8

                            s8s9 = "S8 -> S15[ label=\"=\" ];\n"
                            self.grafito += "S15 [style=filled, fillcolor=darkorchid3];\n"
                            self.grafito += "S8 [style=filled, fillcolor=darkorchid3];\n" 
                            self.yaiwaliwal = True 
                            if s8s9 not in self.grafito:
                                self.grafito += s8s9
                   elif self.contaiwales == 3:
                      w = TokenColor(self.auxlex, 'naranja')
                      self.listaColores.append(w)
                      n = TokenJS("Igual triple", self.auxlex, self.contafila, self.contacolumna, self.estado)
                      self.listaTokens.append(n)
                      self.agregarToken(Token.igual_igual_igual)
                      self.contacolumna += 1
                      if self.yaiwaliwal == False:
                            s0s8 = "S0 -> S8[ label=\"=\" ];\n" 
                            self.grafito += "S8 [style=filled, fillcolor=darkorchid3];\n" 
                            if s0s8 not in self.grafito:
                                self.grafito += s0s8

                            s8s15 = "S8 -> S15[ label=\"=\" ];\n" 
                            s15s16 = "S15 -> S16[ label=\"=\" ];\n"
                            self.grafito += "S15 [style=filled, fillcolor=darkorchid3];\n" 
                            self.grafito += "S16 [style=filled, fillcolor=darkorchid3];\n" 
                            self.yaiwaliwal = True
                            if s8s15 not in self.grafito:
                                self.grafito += s8s15
                                self.grafito += s15s16
                   else:
                       self.auxlex += c
                       print("NO SE RECONOCE LA PALABRA8:  -> '", self.auxlex, "'")
                       n = ErrorJS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                       self.listaErrores.append(n)
                       self.auxlex = ""
                       self.estado = 0 

                   i -= 1
           elif self.estado == 9: # Numeros!
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
                       print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                       n = ErrorJS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                       self.listaErrores.append(n)
                       self.auxlex = ""
                       self.estado = 0
               else:
                   if self.yanumeroo == False:
                       s9s9 = "S9 -> S9[ label=\"digito\" ];\n"                    
                       if s9s9 not in self.grafito:
                            self.grafito += s9s9
                       s9s14 = "S9 -> S14[ label=\".\" ];\n"                    
                       if s9s14 not in self.grafito:
                            self.grafito += s9s14
                            self.grafito += "S14 [style=filled, fillcolor=darkorchid3];\n"
                       s14s14 = "S14 -> S14[ label=\"digito\" ];\n"                    
                       if s14s14 not in self.grafito:
                            self.grafito += s14s14
                       self.yanumeroo = True

                   self.yapunto = False
                   w = TokenColor(self.auxlex, 'azul')
                   self.listaColores.append(w)
                   n = TokenJS("Número", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.numero)
                   i -=1
           elif self.estado == 10: # cadena ""
               #aceptando cadenas
               if c == "\"":
                   w = TokenColor(self.auxlex, 'amarillo')

                   s10s10 = " S10 -> S10[ label=\""+ self.auxlex +"\" ];\n"
                   if self.yacadena == False:                            
                       if "S10 -> S10[" not in self.grafito:
                           self.grafito += s10s10

                   self.listaColores.append(w)
                   n = TokenJS("Cadena", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.cadena)
                   i -=1
                   self.contacolumna += 1
               else:
                   self.estado = 10
                   self.auxlex += c
           elif self.estado == 11: # cadena '
               #aceptando cadenas
               if c == "\'":
                   w = TokenColor(self.auxlex, 'amarillo')
                   
                   if self.yacadenachikita == False:     
                       s12s12 = " S12 -> S12[ label=\""+ self.auxlex +"\" ];\n" 
                       if s12s12 not in self.grafito:
                           self.grafito += s12s12  

                   self.listaColores.append(w)
                   n = TokenJS("Char", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.cadena)
                   i -=1
                   self.contacolumna += 1
               else:
                   self.estado = 11
                   self.auxlex += c
           elif self.estado == 12: # -
               if c == '-':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Menos Menos", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.menos_menos)
                   self.contacolumna += 1
               elif c == '=':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Menos igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.menos_igual)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Menos", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.menos)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 13: # !
               # != o !exp
               if c == '=':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Distinto", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.distinto)
                   self.contacolumna += 1
               elif c.isalpha():
                   #meto negación y mando al 14 para ver la exp
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("No igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.negacion)
                   self.contacolumna += 1
                   self.estado = 14
                   i -= 1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                   n = ErrorJS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0 
           elif self.estado == 14: #identificador del not
              if c.isalnum() or c == '_':
                  self.estado = 14
                  self.auxlex += c
                  self.contacolumna += 1
              else:
                  wangji = TokenColor(self.auxlex, 'verde')
                  self.listaColores.append(wangji)
                  n = TokenJS("Identificador", self.auxlex, self.contafila, self.contacolumna, self.estado)
                  self.listaTokens.append(n)
                  self.agregarToken(Token.identificador)
                  self.yaespacioinicio = False
                  self.vienenNumeros = False
                  i -=1 
           elif self.estado == 15: #<
               if c == '=':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Menor o igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.menor_igual)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Menor que", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.menor)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 16: # >
               if c == '=':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Mayor o igual", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.mayor_igual)
                   self.contacolumna += 1
               else:
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("Mayor que", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.mayor)
                   self.contacolumna += 1
                   i -= 1
           elif self.estado == 17: # &&
               if c == '&':
                   if self.yaii == False:
                            s0s17 = "S0 -> S17[ label=\"&\" ];\n" 
                            s17s18 = "S17 -> S18[ label=\"&\" ];\n" 
                            self.grafito += "S18 [style=filled, fillcolor=darkorchid3];\n" 
                            if s0s17 not in self.grafito:
                                self.grafito += s0s17
                                self.grafito += s17s18


                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("AND", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.l_and)
                   self.contacolumna += 1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                   n = ErrorJS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0 
           elif self.estado == 18: # ||
               if c == '|':
                   w = TokenColor(self.auxlex, 'naranja')
                   self.listaColores.append(w)
                   n = TokenJS("OR", self.auxlex, self.contafila, self.contacolumna, self.estado)
                   self.listaTokens.append(n)
                   self.agregarToken(Token.l_or)
                   self.contacolumna += 1
               else:
                   self.auxlex += c
                   print("NO SE RECONOCE LA PALABRA:  -> '", self.auxlex, "'")
                   n = ErrorJS(self.contafila, self.contacolumna, self.auxlex, self.estado)
                   self.listaErrores.append(n)
                   self.auxlex = ""
                   self.estado = 0 
           elif self.estado == 19:
              pass
           elif self.estado == 20:
              pass           
           
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


   def imprimirPilaSintactico(self):
        for f in self.pilaSintactico:
            print(f)

   def compararSintáctico(self, tipo):
       if len(self.pilaSintactico) >= 1:
            sizhui = self.pilaSintactico[-1]
            if tipo == sizhui.tipo:
                print("Match!")
                self.pilaSintactico.pop()
            else:
                print("Nop")
                self.todoBientodoCorrecto = False
       else:
           print("Nop")
           self.todoBientodoCorrecto = False

   def todoSintáctico(self):
       contasaltos = 1
       for tokenc in self.listaSalida:
           #Todo lo que no sea ; o \n lo meto a la cadena operacion
           #si es ( o { los meto a la pila
           if tokenc.tipo == Token.parentesis_abrir or tokenc.tipo == Token.llave_abrir:
               self.pilaSintactico.append(tokenc)
           
           #Miro si tengo que sacar de la pila algo
           if tokenc.tipo == Token.parentesis_cerrar:
               self.compararSintáctico(Token.parentesis_abrir)
           elif tokenc.tipo == Token.llave_cerrar:
               self.compararSintáctico(Token.llave_abrir)

           #acá es cuando termina la cosa
           
           if tokenc.tipo == Token.salto_de_linea:

               if self.operacion != "":
                   if len(self.pilaSintactico) > 0:
                        self.todoBientodoCorrecto = False

                   wei = TkOperacion(self.operacion, self.todoBientodoCorrecto, contasaltos)
                   self.listaOperaciones.append(wei)

                   print("Operacion: ", contasaltos, " es ", self.todoBientodoCorrecto)
               
               self.operacion = ""
               self.pilaSintactico.clear()
               self.todoBientodoCorrecto = True
               contasaltos += 1
           else:
               self.operacion += tokenc.valor              


   def generarStringGraphviz(self):
       holiwi = "digraph G {\n"
       holiwi += self.grafito
       holiwi += "\n}"
       return holiwi

   def generarGrafo(self):
       wuxian = self.generarStringGraphviz()
       path1 = self.linklinux        

       if path1 == "":
           print("ERROR: no hay ruta :C")
           return
       
       path1 = path1.replace('.', '')
       path2 = path1 + "GrafoJS.png"
       path1 = path1 + "GrafoJS.dot"

       if not os.path.exists(os.path.dirname(path1)):
           try:
               os.makedirs(os.path.dirname(path1))
           except OSError as exc: # Guard against race condition
              if exc.errno != errno.EEXIST:
                  raise
            
       with open(path1, "w") as f:
            f.write(wuxian) 

       time.sleep(1)
       check_call(['dot','-Tpng',path1,'-o',path2])
       time.sleep(1)
       f = Image.open(path2)
       f.show()

       #print("ya :D")

   # Estos dos son los que puedo tocar, los demás noooo 
   def generarHTMLSintactico(self):
       contenido = self.sintacticoCompleto()
       #print(contenido)
       path = self.linklinux

       if path == "":
           print("ERROR: no hay ruta :C")
           return

        #  if os.path.exists(os.path.dirname(path)):
        #  os.remove(path)
        #   time.sleep(1)

       path = path.replace('.', '')
       path2 = path + "ReporteSintácticoJS.html"


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

   def sintacticoCompleto(self):
       frase_actual = ("<!DOCTYPE HTML>" +
                "<html>" +
                    "<head>" +
                        "<title>Analizador Sintáctico JS</title>" +
                        "<meta charset=\"utf8\">" +
                "</head>" +
                "<body><h1>Reporte de Análisis</h1>" +
                "<h2>Lista de Tokens Aprobados</h2>")
       self.htmlsintactico = frase_actual

       #acá van mis tokens geniales

       frase_actual = ("<table border=\"1\">"
            + "<thead>"
            + "<tr><th><strong>#</strong></th>"
            "<th><strong>Fila</strong></th>" +
            "<th><strong>Operacion</strong></th>"+
            "<th><strong>Análisis</strong></th></tr></thead>"
            + "<tbody>")
       self.htmlsintactico = self.htmlsintactico + frase_actual


       # aca es donde meto lo importante (una lista(?))
       contador = 0
       for f in self.listaOperaciones:
           holi = str(contador) 
           scontafila = str(f.linea)
           
           analisis = "Correcto"
           
           if f.analisis == False:
                analisis = "Incorrecto"


           frase_actual = ("<tr><td>" + holi + "</td>"
                    + "<td>" + scontafila + "</td>"
                    + "<td>" + f.operacion + "</td>"
                    + "<td>" + analisis + "</td>"
                    + " </tr>")

           self.htmlsintactico = self.htmlsintactico + frase_actual
           contador += 1


       frase_actual = "</tbody></table></div><br><br><br>"
       self.htmlsintactico = self.htmlsintactico + frase_actual

       frase_actual = "</tbody></table></div><br><br><br>"
       self.htmlsintactico = self.htmlsintactico + frase_actual
       frase_actual = "</body></html>"
       self.htmlsintactico = self.htmlsintactico + frase_actual

       return self.htmlsintactico

   def pasarArchivo(self):
       for f in self.listaColores:
           self.stringArchivo += f.token
       return self.stringArchivo

   def generarArchivoCorregido(self):
       contenido = self.pasarArchivo()
       #print(contenido)
       path = self.linklinux

       if path == "":
           print("ERROR: no hay ruta :C")
           return

        #  if os.path.exists(os.path.dirname(path)):
        #  os.remove(path)
        #   time.sleep(1)

       path = path.replace('.', '')
       path2 = path + "ArchivoJS.js"


       if not os.path.exists(os.path.dirname(path2)):
           try:
               os.makedirs(os.path.dirname(path2))
           except OSError as exc: # Guard against race condition
              if exc.errno != errno.EEXIST:
                  raise
            
       with open(path2, "w") as f:
            f.write(contenido) 

       print("Archivo corregido generado con éxito :D")
       time.sleep(1)
       webbrowser.open('file://' + os.path.realpath(path2))


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
       path2 = path + "ReporteJS.html"


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
                        "<title>Mis Tokens JS</title>" +
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





    