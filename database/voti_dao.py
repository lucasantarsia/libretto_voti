import mysql.connector
from modello.voto_dto import VotoDto

class VotiDao:

    def get_voti(self):
        try:
            cnx = mysql.connector.connect(user='root',
                                          password='root',
                                          host='127.0.0.1',
                                          database='libretto')
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                FROM voti"""
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append(VotoDto(row["nome"],
                                      row["CFU"],
                                      row["punteggio"],
                                      bool(row["lode"]),
                                      row["data"]))
            cursor.close()
            cnx.close()
            return result
        except mysql.connector.Error as err:
            print(err)
            return None

if __name__ == '__main__':
    voti_dao = VotiDao()
    voti_dao.get_voti()