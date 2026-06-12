import flet as ft
class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._genreId = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for n in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(key=n[1], data=n[0], on_click=self.getGenre)
            )
        self._view.update_page()

    def getGenre(self, e):
        selected_key = e.control.data
        self._genreId = int(selected_key)
        return

    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()
        if self._genreId is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere per continuare", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._genreId)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato! Ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi."))
        self._view.txt_result.controls.append(ft.Text(f"Artista con maggiore influenza -->  {self._model.grado_archi()[0]}: {self._model.grado_archi()[1]}"))
        for arco in self._model.archi_maggiori():
            self._view.txt_result.controls.append(ft.Text(f"{str(arco[0])}-->{arco[1]}: {arco[2]}"))
        self._view.update_page()
        return

    def handleCammino(self,e):
        pass