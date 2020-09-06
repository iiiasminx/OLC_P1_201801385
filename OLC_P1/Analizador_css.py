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
    llave_abrir = auto()
    llave_cerrar = auto()
    dos_puntos = auto()
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
    selector_universal = auto()
    numeral = auto()
    dos_puntos = auto()
    menos = auto()
    parentesis_abrir = auto()
    parentesis_cerrar = auto()
    comillas_dobles = auto()
    punto = auto()


