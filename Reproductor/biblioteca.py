from cancion import Cancion
from lista_reproduccion import ListaDeReproduccion


class Biblioteca:
    def __init__(self) -> None:
        self.canciones: list[Cancion] = []
        self.listas: dict[str, ListaDeReproduccion] = {}

    def agregar_cancion(self, cancion: Cancion) -> None:
        self.canciones.append(cancion)
        print(f"✓ '{cancion.titulo}' agregada a la biblioteca")

    def eliminar_cancion(self, indice: int) -> None:
        if 0 <= indice < len(self.canciones):
            cancion = self.canciones.pop(indice)
            print(f"✓ '{cancion.titulo}' eliminada de la biblioteca")
        else:
            print("✗ Índice inválido")

    def buscar_por_titulo(self, titulo: str) -> list[Cancion]:
        return [c for c in self.canciones if titulo.lower() in c.titulo.lower()]

    def buscar_por_artista(self, artista: str) -> list[Cancion]:
        return [c for c in self.canciones if artista.lower() in c.artista.lower()]

    def crear_lista(self, nombre: str) -> ListaDeReproduccion | None:
        if nombre not in self.listas:
            self.listas[nombre] = ListaDeReproduccion(nombre)
            print(f"✓ Lista '{nombre}' creada")
            return self.listas[nombre]
        else:
            print(f"✗ La lista '{nombre}' ya existe")
            return None

    def eliminar_lista(self, nombre: str) -> None:
        if nombre in self.listas:
            del self.listas[nombre]
            print(f"✓ Lista '{nombre}' eliminada")
        else:
            print(f"✗ Lista '{nombre}' no existe")

    def obtener_lista(self, nombre: str) -> ListaDeReproduccion | None:
        return self.listas.get(nombre)

    def obtener_todas_las_canciones(self) -> list[Cancion]:
        return self.canciones

    def mostrar_estadisticas(self) -> None:
        print("\n=== ESTADÍSTICAS DE LA BIBLIOTECA ===")
        print(f"Total de canciones: {len(self.canciones)}")
        print(f"Total de listas: {len(self.listas)}")

        if self.canciones:
            duracion_total = sum(c.duracion_segundos for c in self.canciones)
            horas = duracion_total // 3600
            minutos = (duracion_total % 3600) // 60
            print(f"Duración total: {horas}h {minutos}m")
            total_reproducciones = sum(c.reproducciones for c in self.canciones)
            print(f"Reproducciones totales: {total_reproducciones}")

    def __str__(self) -> str:
        return f"Biblioteca ({len(self.canciones)} canciones, {len(self.listas)} listas)"
