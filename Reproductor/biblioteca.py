from cancion import Cancion

class Biblioteca:
    def __init__(self):
        self.canciones = []

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    def eliminar_cancion(self, titulo):
        for c in self.canciones:
            if c.titulo.lower() == titulo.lower():
                self.canciones.remove(c)
                return True
        return False

    def listar_canciones(self):
        if not self.canciones:
            print("No hay canciones en la biblioteca.")
        else:
            print("\n--- Canciones en la Biblioteca ---")
            for i, c in enumerate(self.canciones, start=1):
                print(f"{i}. {c.titulo} - {c.artista}")

