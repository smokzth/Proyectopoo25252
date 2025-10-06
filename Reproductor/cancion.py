class Cancion:

    def __init__(self, titulo: str, artista: str, duracion_segundos: int,
                 album: str = "", año: int = 0, genero: str = "") -> None:
        self.titulo = titulo
        self.artista = artista
        self.duracion_segundos = duracion_segundos
        self.album = album
        self.año = año
        self.genero = genero
        self.reproducciones = 0

    def info(self) -> str:
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
        info_str += f"{'=' * 50}\n"

        return info_str

    def incrementar_reproducciones(self) -> None:
        self.reproducciones += 1

    def get_duracion_formateada(self) -> str:
        minutos = self.duracion_segundos // 60
        segundos = self.duracion_segundos % 60
        return f"{minutos}:{segundos:02d}"

    def __str__(self) -> str:
        return f"{self.titulo} - {self.artista} ({self.get_duracion_formateada()})"

