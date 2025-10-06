from cancion import Cancion

class ListaDeReproduccion:

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.canciones: list[Cancion] = []
        self.indice_actual = 0

    def agregar_cancion(self, cancion: Cancion) -> None:
        self.canciones.append(cancion)
        print(f"✓ '{cancion.titulo}' agregada a '{self.nombre}'")

    def eliminar_cancion(self, indice: int) -> None:
        if 0 <= indice < len(self.canciones):
            cancion = self.canciones.pop(indice)
            print(f"✓ '{cancion.titulo}' eliminada de '{self.nombre}'")
            if self.indice_actual >= len(self.canciones) and len(self.canciones) > 0:
                self.indice_actual = len(self.canciones) - 1
        else:
            print("✗ Índice inválido")

    def obtener_cancion_actual(self) -> Cancion | None:
        if self.canciones:
            return self.canciones[self.indice_actual]
        return None

    def siguiente(self) -> Cancion | None:
        if self.canciones:
            self.indice_actual = (self.indice_actual + 1) % len(self.canciones)
            return self.canciones[self.indice_actual]
        return None

    def anterior(self) -> Cancion | None:
        if self.canciones:
            self.indice_actual = (self.indice_actual - 1) % len(self.canciones)
            return self.canciones[self.indice_actual]
        return None

    def listar_canciones(self) -> str:
        if not self.canciones:
            return f"\n=== {self.nombre.upper()} ===\nLista vacía\n"

        lista_str = f"\n=== {self.nombre.upper()} ===\n"
        lista_str += f"Total: {len(self.canciones)} canciones | "
        lista_str += f"Duración: {self._get_duracion_total_formateada()}\n\n"

        for i, cancion in enumerate(self.canciones):
            marcador = "▶ " if i == self.indice_actual else "  "
            lista_str += f"{marcador}{i + 1}. {cancion}\n"

        return lista_str

    def obtener_total_canciones(self) -> int:
        return len(self.canciones)

    def _obtener_duracion_total(self) -> int:
        return sum(cancion.duracion_segundos for cancion in self.canciones)

    def _get_duracion_total_formateada(self) -> str:
        total = self._obtener_duracion_total()
        horas = total // 3600
        minutos = (total % 3600) // 60
        segundos = total % 60

        if horas > 0:
            return f"{horas}:{minutos:02d}:{segundos:02d}"
        return f"{minutos}:{segundos:02d}"

    def __str__(self) -> str:
        return f"{self.nombre} ({len(self.canciones)} canciones)"
