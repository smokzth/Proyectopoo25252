class ListaReproduccion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []
        self.indice_actual = 0

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    def eliminar_cancion(self, titulo):
        for c in self.canciones:
            if c.titulo.lower() == titulo.lower():
                self.canciones.remove(c)
                return True
        return False

    def obtener_actual(self):
        if not self.canciones:
            return None
        return self.canciones[self.indice_actual]

    def siguiente(self):
        if not self.canciones:
            return None
        self.indice_actual = (self.indice_actual + 1) % len(self.canciones)
        return self.obtener_actual()

    def anterior(self):
        if not self.canciones:
            return None
        self.indice_actual = (self.indice_actual - 1) % len(self.canciones)
        return self.obtener_actual()




