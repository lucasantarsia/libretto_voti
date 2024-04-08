import flet as ft

from controller import Controller
from view import View

def main(page: ft.Page): # --> il mio main istanzia un view e un controllore
    v = View(page)  # --> il view è l'unico che conosce la pagina e che può modificarla
    c = Controller(v)  # --> il controllore è l'unico che può parlare sia con il view che con il modello
    v.setController(c)  # --> dico al view che il suo controllore si chiama c
    v.caricaInterfaccia()

ft.app(target=main)