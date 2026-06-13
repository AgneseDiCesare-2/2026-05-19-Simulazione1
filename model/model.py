import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._max = None
        self._bestSolution = None
        self._grafo=nx.DiGraph()
        self._idMap={}

    def getAllGenres(self):
        return DAO.getGenres()

    def buildGraph(self, genreId):
        self._grafo.clear()
        self._idMap = {}
        popolarità={}

        nodi=DAO.getNodi(genreId)
        for nodo in nodi:
            self._idMap[nodo.ArtistId]=nodo
        self._grafo.add_nodes_from(nodi)
        p=DAO.getPopolarità(genreId) #(artistId, popolarità)

        for artist in p:
            if artist[0] in self._idMap.keys():
                popolarità[artist[0]]=artist[1] #{artistId: popolarità}

        archi=DAO.getArchi(genreId) #(nodo1, nodo2)

        for arco in archi:
            if arco[0] in self._idMap.keys() and arco[1] in self._idMap.keys():
                nodo1=self._idMap[arco[0]]
                nodo2=self._idMap[arco[1]]

                if popolarità[arco[0]]>popolarità[arco[1]]:
                    self._grafo.add_edge(nodo1, nodo2, weight=popolarità[arco[0]]+popolarità[arco[1]])

                elif popolarità[arco[0]]<popolarità[arco[1]]:
                    self._grafo.add_edge(nodo2, nodo1, weight=popolarità[arco[0]]+popolarità[arco[1]])

                else:
                    self._grafo.add_edge(nodo1, nodo2, weight=popolarità[arco[0]] + popolarità[arco[1]])
                    self._grafo.add_edge(nodo2, nodo1, weight=popolarità[arco[0]] + popolarità[arco[1]])
        print(f"archi aggiunti: {self.num_archi()}, nodi: {self.num_nodi()}")
        return


    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)

    def grado_archi(self):
        p=[]
        for nodo in self._grafo.nodes():
            diff=self._grafo.out_degree(nodo, weight="weight")-self._grafo.in_degree(nodo, weight="weight")
            p.append((nodo, diff))
        p.sort(key=lambda x: x[1], reverse=True)
        return p[0]

    def archi_maggiori(self):
        archi_ordinati = sorted(self._grafo.edges.data("weight"), key=lambda x: x[2], reverse=True)
        return archi_ordinati[:5]

    def getArtists(self, genreId):
        return DAO.getNodi(genreId)

    def handleCammino(self, artist):
        self._bestSolution=[]
        self._max=0

        self._ricorsione([artist])

        return self._bestSolution, self._max

    def _ricorsione(self, parziale: list):
        #condizione terminale --> non c'è
        #verifica best condizione
        if len(parziale)>self._max:
            self._max=len(parziale)
            self._bestSolution=copy.deepcopy(parziale)

        for n in self._grafo.neighbors(parziale[-1]):
            if n not in parziale:
                if len(parziale)==1:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

                #controllo peso archi strett. crescente
                else:
                    if self._grafo[parziale[-1]][n]["weight"]>self._grafo[parziale[-2]][parziale[-1]]["weight"]:
                        parziale.append(n)
                        self._ricorsione(parziale)
                        parziale.pop()


