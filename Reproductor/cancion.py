class Cancion:
    def __init__(self, titulo, artista, duracion, album, anio, genero):
        self.titulo = titulo
        self.artista = artista
        self.duracion = duracion
        self.album = album
        self.anio = anio
        self.genero = genero
        self.veces_reproducida = 0

    def reproducir(self):
        self.veces_reproducida += 1
        print(f"▶ Reproduciendo: {self.titulo} - {self.artista}")
        print(f"Veces reproducida: {self.veces_reproducida}")

    def mostrar_info(self):
        print(f"Título: {self.titulo}")
        print(f"Artista: {self.artista}")
        print(f"Duración: {self.duracion}")
        print(f"Álbum: {self.album}")
        print(f"Año: {self.anio}")
        print(f"Género: {self.genero}")
        print(f"Reproducciones: {self.veces_reproducida}")



