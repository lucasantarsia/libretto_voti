import flet as ft

from UI.controller import Controller
from UI.view import View
from modello.voto import Libretto

def main(page: ft.Page): # --> il mio main istanzia un view e un controllore
    v = View(page)  # --> il view è l'unico che conosce la pagina e che può modificarla
    l = Libretto()
    c = Controller(v, l)  # --> il controllore è l'unico che può parlare sia con il view che con il modello
    v.setController(c)  # --> dico al view che il suo controllore si chiama c
    v.caricaInterfaccia()

ft.app(target=main)