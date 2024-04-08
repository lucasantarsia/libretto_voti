# from dataclasses import dataclass

import dataclasses  # con dataclass di default viene definito il metodo equal
                    # mentre non viene definito il metodo __lt__, devo farlo io
                    # con order=True
import operator


@dataclasses.dataclass()
class Voto:
    esame: str
    cfu: int
    punteggio: int
    lode: bool
    data: str  # = dataclasses.field(compare=False) per non comparare il campo data

    def str_punteggio(self):
        """
        Costruisce la stringa che rappresenta in forma leggibile il punteggio,
        tenendo conto della possibilità di lode
        :return: "30 e lode" oppure il punteggio (senza lode), sotto forma di stringa
        """
        if self.punteggio == 30 and self.lode:
            return "30 e lode"
        else:
            return f"{self.punteggio}"
            # return self.punteggio  NOOO

    def copy(self):
        return Voto(self.esame, self.cfu, self.punteggio, self.lode, self.data)

    def __str__(self):
        return f"{self.esame} ({self.cfu} CFU): voto {self.str_punteggio()} il {self.data}"


class Libretto:
    def __init__(self):
        self._voti = []

    def append(self, voto):
        if self.has_voto(voto) == False and self.has_conflitto(voto)==False:
            self._voti.append(voto)
        else:
            raise ValueError("Voto non valido")

    def media(self):
        if len(self._voti)==0:
            raise ValueError("Elenco voti vuoto")
        punteggi = [v.punteggio for v in self._voti]
        return sum(punteggi)/len(punteggi)

    def findByPunteggio(self, punteggio, lode):
        """
        Seleziona tutti e soli i soli voti che hanno un punteggio definito.
        :param punteggio: numero intero che rappresenta il punteggio
        :param lode: booleano che indica la presenza della lode
        :return: lista di oggetti di tipo Voto che hanno il punteggio specificato (può anche essere vuota)
        """
        corsi = []
        for v in self._voti:
            if v.punteggio == punteggio and v.lode == lode:
                corsi.append(v)
        return corsi

    def findByEsame(self, esame):
        """
        Cerca il voto a partire dal nome dell'esame.
        :param esame: Nome dall'esame da ricercare
        :return: l'oggetto Voto corrispondente al nome trovato, oppure None se non viene trovato
        """
        for v in self._voti:
            if v.esame == esame:
                return v
        return None

    def findByEsame2(self, esame):
        """
        Cerca il voto a partire dal nome dell'esame.
        :param esame: Nome dall'esame da ricercare
        :return: l'oggetto Voto corrispondente al nome trovato, oppure un'eccezione ValueError se
        l'elemento non viene trovato
        """
        for v in self._voti:
            if v.esame == esame:
                return v
        raise ValueError(f"Esame '{esame}' non presente nel libretto")


    def has_voto(self, voto):
        """
        Ricerca se nel libretto esiste già un esame con lo stesso nome e lo stesso punteggio
        :param voto: oggetto Voto da confrontare
        :return: True se esiste, False se non esiste
        """
        for v in self._voti:
            if v.esame == voto.esame and v.punteggio == voto.punteggio and v.lode == voto.lode:
                return True
        return False

    def has_conflitto(self, voto):
        """
        Ricerca se nel libretto esiste già un esame con lo stesso nome ma punteggio diverso
        :param voto: oggetto Voto da confrontare
        :return: True se esiste, False se non esiste
        """
        for v in self._voti:
            if v.esame == voto.esame and not(v.punteggio == voto.punteggio and v.lode == voto.lode):
            # if v.esame == voto.esame and (v.punteggio != voto.punteggio or v.lode != voto.lode):
                    return True
        return False

    def copy(self):
        nuovo = Libretto()
        #nuovo._voti = self._voti.copy() --> #copy è un metodo della lista che copia tutti i dati della lista
                                             #si puo anche scrivere: nuovo._voti = self._voti[:]

                                             #con il copy le operazioni che posso fare senza modificare gli oggetti
                                             #della lista sono quelle operazioni vhe modificano SOLO la lista (es. append,..)

                                             #nuovo._voti[0] = self._voti[0] --> copiando la lista ho gli stessi oggetti
                                                                                 #in due liste, quindi se modifico
                                                                                 #gli oggetti in una lista si modificano anche nell'altra lista

        #Devo fare in un altro modo (quello di sopra non conviene):

        for v in self._voti:
            #nuovo._voti.append(Voto(v.esame, v.cfu, v.punteggio, v.lode, v.data)) --> in questo caso aggiungo alla lista nuova
                                                                                       #un nuovo oggetto Voto ma con gli stessi attributi
                                                                                       #degli oggetti precedenti, cioè con gli stessi riferimenti,
                                                                                       #ma essenso variabili immutabili (str, int, bool) va bene così,
                                                                                       #non serve fare una copia anche degli attributi
            #OPPURE

            nuovo._voti.append(v.copy()) #--> #creando cosi la nuova lista, aggiungo alla lista nuova una copia
                                              # degli oggetti della lista vecchia possiamo modificare
                                              # gli oggetti della nuova lista senza modificare quelli della vecchia lista
        return nuovo


    def crea_migliorato(self):
        """
        Crea una copia del libretto e "migliora" i voti presenti
        :return:
        """
        nuovo = self.copy()

        for v in nuovo._voti:
            if 18 <= v.punteggio <= 23:
                v.punteggio += 1
            elif 24 <= v.punteggio <= 28:
                v.punteggio += 2
            elif v.punteggio == 29:
                v.punteggio = 30

        return nuovo

    """
    Opzione 1: (meglio non usare)
        metodo stampa_per_nome e metodo stampa_per_punteggio, che semplicemente stampano e non modificano nulla

    Opzione 2: (creo un nuovo oggetto)
        metodo crea_libretto_ordinato_per_nome ed un metodo crea_libretto_ordinato_per_punteggio, che creano delle copie
        separate, sulle quali potrò chiamare il metodo stampa()

    Opzione 3: (lavora sugli effetti collaterali) --> MIGLIORE
        metodo ordina_per_nome, che modifica il libretto stesso riordinando i Voti, e ordina_per_punteggio, poi userò
        stampa()
        + aggiungiamo gratis un metodo copy()

    Opzione 2bis:
        crea una copia shallow del Libretto: faccio una copia della lista, tanto non
        devo modificare gli oggetti
    """

    def crea_ordinato_per_esame(self):
        nuovo = self.copy()
        # ordina i nuovi voti
        nuovo.ordina_per_esame()
        return nuovo

    def ordina_per_esame(self):
        # ordina self._voti per nome esame:
        # self._voti.sort() --> se faccio solo questo non funziona: come devo confrontare gli oggetti?
        self._voti.sort(key=operator.attrgetter('esame'))  # --> ordina self._voti per esame
        # self._voti.sort(key=lambda v: v.esame) --> altro modo equivalente a quello sopra

    def crea_ordinato_per_punteggio(self):
        nuovo = self.copy()
        self._voti.sort(key=lambda v: (v.punteggio, v.lode), reverse=True)  # --> prima confronto i punteggi, se sono uguali confronto la lode
                                                                            #     ricordando che True > False
        return nuovo

    def stampa(self):
        print(f"Hai {len(self._voti)} voti")
        for v in self._voti:
            print(v)
        print(f"La media vale {self.media():.2f}")

    def stampaGUI(self):
        outList = []
        outList.append(f"Hai {len(self._voti)} voti")
        for v in self._voti:
            outList.append(v)
        outList.append(f"La media vale {self.media():.2f}")
        return outList

    def cancella_inferiori(self, punteggio):
        # for v in self._voti:
            # if v.punteggio < punteggio:
                # self._voti.remove(v)
        # --> SBAGLIATO: 1)il metodo remove() itera a sua volta quindi è complesso e poco efficiente
        #                2)meglio non modificare la lista mentre itero sulla stessa

        # for i in range(len(self._voti)):
            # if self._voti[i] < punteggio:
                # self._voti.pop(i) --> remove richiede il valore, pop richiede l'indice
        # --> SBAGLIATO: meglio non modificare la lista mentre itero sulla stessa

        # Quello che conviene fare è costruire una lista nuova che contiene quello vhe non deve essere cancellato
        voti_nuovi = []
        for v in self._voti:
            if v.punteggio >= punteggio:
                voti_nuovi.append(v)
        # adesso modifico anche la lista self._voti
        self._voti = voti_nuovi

        # Potrei anche fare piu semplicemente così:
        # self._voti = [v for v in self._voti if v.punteggio >= punteggio]


def _test_voto():
    print(__name__)
    v1 = Voto("nome esame", 8, 28, False, '2024-03-11')
    l1 = Libretto()
    l1.append(v1)
    print(l1.media())

if __name__ == "__main__":
    _test_voto()
