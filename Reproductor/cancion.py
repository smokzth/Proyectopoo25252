class Cancion:

    def __init__(self, titulo: str, artista: str, duracion_segundos: int,
                 ruta_archivo: str, album: str = "", año: int = 0, genero: str = ""):
        self.titulo = titulo
        self.artista = artista
        self.duracion_segundos = duracion_segundos
        self.ruta_archivo = ruta_archivo
        self.album = album
        self.año = año
        self.genero = genero
        self.reproducciones = 0
        self.es_favorita = False  # RF7: Sistema de favoritos

    def info(self) -> str:
        """Retorna información detallada de la canción"""
        info_str = f"\n{'=' * 50}\n"
        info_str += f"♪ {self.titulo}\n"
        info_str += f"{'=' * 50}\n"
        info_str += f"Artista: {self.artista}\n"
        info_str += f"Duración: {self.get_duracion_formateada()}\n"

        if self.album:
            info_str += f"Álbum: {self.album}\n"
        if self.año:
            info_str += f"Año: {self.año}\n"
        if self.genero:
            info_str += f"Género: {self.genero}\n"

        info_str += f"Reproducciones: {self.reproducciones}\n"
        info_str += f"Favorita: {'★ Sí' if self.es_favorita else '☆ No'}\n"
        info_str += f"Archivo: {self.ruta_archivo}\n"
        info_str += f"{'=' * 50}\n"

        return info_str

    def incrementar_reproducciones(self) -> None:
        """Incrementa el contador de reproducciones"""
        self.reproducciones += 1

    def marcar_favorita(self) -> None:
        """RF7: Marca o desmarca la canción como favorita"""
        self.es_favorita = not self.es_favorita
        estado = "agregada a" if self.es_favorita else "eliminada de"
        print(f"✓ '{self.titulo}' {estado} favoritos")

    def get_duracion_formateada(self) -> str:
        """Convierte duración a formato MM:SS"""
        minutos = self.duracion_segundos // 60
        segundos = self.duracion_segundos % 60
        return f"{minutos}:{segundos:02d}"

    def to_dict(self) -> dict:
        """RF9: Convierte la canción a diccionario para JSON"""
        return {
            "titulo": self.titulo,
            "artista": self.artista,
            "duracion": self.duracion_segundos,
            "ruta": self.ruta_archivo,
            "album": self.album,
            "año": self.año,
            "genero": self.genero
        }

    def __str__(self) -> str:
        """Representación en string"""
        fav = "★ " if self.es_favorita else ""
        return f"{fav}{self.titulo} - {self.artista} ({self.get_duracion_formateada()})"