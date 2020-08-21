import enum
from enum import Enum, auto
from collections import deque


#
#
#       TOKEN
#
#
class TokenHTML:
    def __init__(self, tipo, valor):
        self.valor = valor
        self.tipo = Token
        #hola = tokenhtml(token.html_abrir)

    def getValorToken(self):
        return self.valor

    def getTipo(self):
        return self.tipo

    def getTipoString(self):
        tipoo = self.tipo
      #  def switchdemo(tipoo):
       #     switcher = {
        #        1: ""
         #   }

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
    comillas = auto()
    link = auto()
    a_abrir = auto()
    a_cerrar = auto()
    href = auto()
    ul_abrir = auto()
    ul_cerrar = auto()
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
    tfoot_abri = auto()
    tfoot_cerrar = auto()

class ErrorHtml:
    def __init__(self, linea, columna, caracter_error):
        self.linea = linea
        self.columna = columna
        self.caracter_error = caracter_error
        self.descripcion = "El caracter " + self.caracter_error + " no pertenece al lenguaje" 

#
#
#       ANALIZADOR
#
#

class AnalizadorHTML:

   listaSalida = deque()

   estado = None
   auxlex, comentario = None, None

   contador = None

   contaerror, contafila, contacolumna = None, None, None
   descerror = "caracter desconocido"

   contatoken = 1

   listaErrores = deque()
   listaTokens = deque()

   arreglotokens = []

   def escanear(self, entrada):
       entrada = entrada + '%'
       estado = 0
       auxlex = ""

       # BANDERAS
       etiqueta_abierta = False
       comillas_abiertas = False

       c = None
       y = len(entrada)-1

       for i in range(y):
           c = entrada[i]

           # acá mando todo a todos lados
           if estado == 0:
                if c.isalnum():
                   #si es alpha puede ser texto o un link.
                   #si es link siempre va en comillas
                   estado = 1
                   auxlex += c
                   contacolumna +=1
                elif c == '<':
                    etiqueta_abierta = True
                    
                    
















