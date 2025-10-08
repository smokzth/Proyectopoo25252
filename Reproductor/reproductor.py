class Reproductor:
    def __init__(self):
        self.lista_actual = None
        self.cancion_actual = None
        self.reproduciendo = False

    def seleccionar_lista(self, lista):
        self.lista_actual = lista
        self.cancion_actual = lista.obtener_actual()
        print(f"Lista '{lista.nombre}' seleccionada para reproducción.")

    def play(self):
        if not self.lista_actual:
            print("No hay lista seleccionada.")
            return
        if not self.cancion_actual:
            self.cancion_actual = self.lista_actual.obtener_actual()
        if self.cancion_actual:
            self.cancion_actual.reproducir()
            self.reproduciendo = True
        else:
            print("No hay canciones en la lista.")

    def stop(self):
        if self.reproduciendo:
            print("⏹ Reproducción detenida.")
            self.reproduciendo = False
        else:
            print("No hay ninguna canción reproduciéndose.")

    def siguiente(self):
        if self.lista_actual:
            self.cancion_actual = self.lista_actual.siguiente()
            if self.cancion_actual:
                self.cancion_actual.reproducir()
            else:
                print("No hay más canciones.")
        else:
            print("No hay lista seleccionada.")

    def anterior(self):
        if self.lista_actual:
            self.cancion_actual = self.lista_actual.anterior()
            if self.cancion_actual:
                self.cancion_actual.reproducir()
            else:
                print("No hay canciones anteriores.")
        else:
            print("No hay lista seleccionada.")




