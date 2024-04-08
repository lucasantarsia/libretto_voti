import datetime

import flet as ft

class View(object):
    def __init__(self, page):
        self._page = page
        self._page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self._titolo = None
        self._datePicker = None

    def caricaInterfaccia(self):
        self._titolo = ft.Text("Il mio Libretto Voti ++",
                               color="blue", size=24)

        # Row 1
        """
        Row 1: ci mettiamo i controlli che ci permettono di dare informazioni riguardo l'esame
        Quello di cui ho bisogno:
            esame: str
            cfu: int
            punteggio: int
            lode: bool
            data: str
        """

        self._txtIn = ft.TextField(label="Nome", width=200)
        self._txtCFU = ft.TextField(label="CFU", width=100)
        self._ddVoto = ft.Dropdown(label="Voto", width=100)  # --> dropdown: menu a tendina
        self._fillDdVoto()

        self._datePicker = ft.DatePicker(
            first_date=datetime.datetime(2022, 11, 1),
            last_date=datetime.datetime(2025, 10, 31)
        )

        self._page.overlay.append(self._datePicker)  # --> aggiungo il calendario
        self._btnCalendar = ft.ElevatedButton("Pick date",
                                              icon=ft.icons.CALENDAR_MONTH,
                                              on_click=lambda _: self._datePicker.pick_date())

        row1 = ft.Row([self._txtIn, self._txtCFU, self._ddVoto, self._btnCalendar], alignment=ft.MainAxisAlignment.CENTER)

        # Row 2: mettiamo i tasti
        self._btnAdd = ft.ElevatedButton(text="Add", on_click=self._controller.handleAdd)
        self._btnPrint = ft.ElevatedButton(text="Print", on_click=self._controller.handlePrint)

        row2 = ft.Row([self._btnAdd, self._btnPrint], alignment=ft.MainAxisAlignment.CENTER)

        # Row 3: riga per stampare
        self._lvOut = ft.ListView()

        self._page.add(self._titolo, row1, row2, self._lvOut)

    def setController(self, controller):
        """
        Metodo di appoggio che uso per assegnare il controller locale
        :param controller:
        :return:
        """
        self._controller = controller

    def update(self):
        self._page.update()

    def _fillDdVoto(self):
        for i in range(18, 31):
            self._ddVoto.options.append(ft.dropdown.Option(str(i)))
        self._ddVoto.options.append(ft.dropdown.Option("30L"))