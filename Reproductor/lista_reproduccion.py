"""
Módulo lista_reproduccion.py
Define la clase ListaDeReproduccion para gestionar colecciones de canciones
"""

from cancion import Cancion
from typing import Optional
import random


class ListaDeReproduccion:
    """
    Representa una lista de reproducción personalizada.

    Attributes:
        nombre (str): Nombre de la lista
        canciones (list): Lista de canciones
        indice_actual (int): Índice de la canción actual
        orden_original (list): Backup del orden para shuffle
        shuffle_activo (bool): Estado del modo aleatorio
    """

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.canciones: list[Cancion] = []
        self.indice_actual = 0
        self.orden_original: list[Cancion] = []  # RF6: Para shuffle
        self.shuffle_activo = False

    def agregar_cancion(self, cancion: Cancion) -> None:
        """Agrega una canción a la lista"""
        self.canciones.append(cancion)
        print(f"✓ '{cancion.titulo}' agregada a '{self.nombre}'")

    def eliminar_cancion(self, indice: int) -> None:
        """Elimina una canción por su índice"""
        if 0 <= indice < len(self.canciones):
            cancion = self.canciones.pop(indice)
            print(f"✓ '{cancion.titulo}' eliminada de '{self.nombre}'")

            # Ajustar índice actual si es necesario
            if self.indice_actual >= len(self.canciones) and len(self.canciones) > 0:
                self.indice_actual = len(self.canciones) - 1
        else:
            print("✗ Índice inválido")

    def obtener_cancion_actual(self) -> Optional[Cancion]:
        """Retorna la canción en la posición actual"""
        if self.canciones:
            return self.canciones[self.indice_actual]
        return None

    def siguiente(self) -> Optional[Cancion]:
        """Avanza a la siguiente canción (navegación circular)"""
        if self.canciones:
            self.indice_actual = (self.indice_actual + 1) % len(self.canciones)
            return self.canciones[self.indice_actual]
        return None

    def anterior(self) -> Optional[Cancion]:
        """Retrocede a la canción anterior (navegación circular)"""
        if self.canciones:
            self.indice_actual = (self.indice_actual - 1) % len(self.canciones)
            return self.canciones[self.indice_actual]
        return None

    def shuffle(self) -> None:
        """RF6: Activa modo aleatorio guardando el orden original"""
        if self.canciones and not self.shuffle_activo:
            self.orden_original = self.canciones.copy()
            cancion_actual = self.canciones[self.indice_actual] if self.canciones else None
            random.shuffle(self.canciones)

            # Mantener la canción actual después del shuffle
            if cancion_actual:
                self.indice_actual = self.canciones.index(cancion_actual)

            self.shuffle_activo = True
            print(f"✓ Modo aleatorio activado en '{self.nombre}'")
        elif self.shuffle_activo:
            print(f"⚠ El modo aleatorio ya está activado")
        else:
            print("✗ Lista vacía")

    def restaurar_orden(self) -> None:
        """RF6: Restaura el orden original"""
        if self.orden_original and self.shuffle_activo:
            cancion_actual = self.canciones[self.indice_actual] if self.canciones else None
            self.canciones = self.orden_original.copy()

            # Restaurar posición de la canción actual
            if cancion_actual and cancion_actual in self.canciones:
                self.indice_actual = self.canciones.index(cancion_actual)

            self.orden_original = []
            self.shuffle_activo = False
            print(f"✓ Orden original restaurado en '{self.nombre}'")
        else:
            print("⚠ No hay orden aleatorio activo")

    def listar_canciones(self) -> str:
        """Genera una representación visual de todas las canciones"""
        if not self.canciones:
            return f"\n=== {self.nombre.upper()} ===\nLista vacía\n"

        shuffle_texto = " (🔀 ALEATORIO)" if self.shuffle_activo else ""
        lista_str = f"\n=== {self.nombre.upper()}{shuffle_texto} ===\n"
        lista_str += f"Total: {len(self.canciones)} canciones | "
        lista_str += f"Duración: {self._get_duracion_total_formateada()}\n\n"

        for i, cancion in enumerate(self.canciones):
            marcador = "▶ " if i == self.indice_actual else "  "
            lista_str += f"{marcador}{i + 1}. {cancion}\n"

        return lista_str

    def obtener_total_canciones(self) -> int:
        """Retorna la cantidad de canciones"""
        return len(self.canciones)

    def _obtener_duracion_total(self) -> int:
        """Calcula la duración total en segundos"""
        return sum(cancion.duracion_segundos for cancion in self.canciones)

    def _get_duracion_total_formateada(self) -> str:
        """Retorna la duración total en formato legible"""
        total = self._obtener_duracion_total()
        horas = total // 3600
        minutos = (total % 3600) // 60
        segundos = total % 60

        if horas > 0:
            return f"{horas}:{minutos:02d}:{segundos:02d}"
        return f"{minutos}:{segundos:02d}"

    def to_dict(self) -> dict:
        """RF9: Convierte la lista a diccionario para JSON"""
        return {
            "nombre": self.nombre,
            "canciones": [cancion.to_dict() for cancion in self.canciones]
        }

    def __str__(self) -> str:
        shuffle = " 🔀" if self.shuffle_activo else ""
        return f"{self.nombre}{shuffle} ({len(self.canciones)} canciones)"