from database.DB_connect import DBConnect
from model.Artist import Artist


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getGenres():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.*
                            from genre g
                            order by g.Name """

        cursor.execute(query)

        for row in cursor:
            result.append((row["GenreId"], row["Name"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(genreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.*
                    from artist a, album al, track t 
                    where a.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId 
                            and t.GenreId = %s """

        cursor.execute(query, (genreId, ))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(genreId):
        #nb: ho interpretato che i clienti devono aver comprato da entrambi gli artisti per lo stesso genere!
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct tab1.ArtistId as a, tab2.ArtistId as b
                    from 
                    (select a.ArtistId, i.CustomerId 
                    from invoice i, invoiceline il, track t, album a
                    where i.InvoiceId = il.InvoiceId and il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and t.GenreId = %s) as tab1, 
                    (select a.ArtistId, i.CustomerId 
                    from invoice i, invoiceline il, track t, album a
                    where i.InvoiceId = il.InvoiceId and il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and t.GenreId = %s) as tab2 
                    where tab1.CustomerId = tab2.CustomerId and tab1.ArtistId < tab2.ArtistId  """

        cursor.execute(query, (genreId, genreId))

        for row in cursor:
            result.append((row["a"], row["b"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopolarità(GenreId):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ArtistId, sum(il.Quantity) as p
                        from invoiceline il, track t, album a
                        where il.TrackId = t.TrackId and t.AlbumId = a.AlbumId and t.GenreId=%s
                        group by a.ArtistId"""

        cursor.execute(query, (GenreId, ))

        for row in cursor:
            result.append((row["ArtistId"], row["p"]))

        cursor.close()
        conn.close()
        return result