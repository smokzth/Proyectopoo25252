from biblioteca import Biblioteca
from lista_reproduccion import ListaDeReproduccion
from cancion import Cancion


class Reproductor:
    def __init__(self, biblioteca: Biblioteca) -> None:
        self.biblioteca = biblioteca
        self.lista_actual: ListaDeReproduccion | None = None
        self.cancion_actual: Cancion | None = None
        self.reproduciendo = False

    def play(self) -> None:
        if self.cancion_actual:
            self.reproduciendo = True
            self.cancion_actual.incrementar_reproducciones()
            print(f"\n▶ REPRODUCIENDO: {self.cancion_actual}")
        else:
            print("✗ No hay canción seleccionada")

    def pause(self) -> None:
        if self.reproduciendo:
            self.reproduciendo = False
            print("⏸ Pausado")
        else:
            print("✗ No hay reproducción activa")

    def stop(self) -> None:
        self.reproduciendo = False
        print("⏹ Detenido")

    def siguiente(self) -> None:
        if self.lista_actual:
            self.cancion_actual = self.lista_actual.siguiente()
            if self.reproduciendo and self.cancion_actual:
                self.play()
            elif self.cancion_actual:
                print(f"⏭ Siguiente: {self.cancion_actual}")
        else:
            print("✗ No hay lista de reproducción activa")

    def anterior(self) -> None:
        if self.lista_actual:
            self.cancion_actual = self.lista_actual.anterior()
            if self.reproduciendo and self.cancion_actual:
                self.play()
            elif self.cancion_actual:
                print(f"⏮ Anterior: {self.cancion_actual}")
        else:
            print("✗ No hay lista de reproducción activa")

    def cambiar_lista(self, nombre_lista: str) -> None:
        lista = self.biblioteca.obtener_lista(nombre_lista)
        if lista and lista.obtener_total_canciones() > 0:
            self.lista_actual = lista
            self.cancion_actual = lista.obtener_cancion_actual()
            print(f"✓ Lista activa: {nombre_lista}")
            print(f"  Canción actual: {self.cancion_actual}")
        else:
            print(f"✗ Lista '{nombre_lista}' no existe o está vacía")

    def obtener_estado(self) -> dict[str, str | bool]:
        return {
            "cancion": str(self.cancion_actual) if self.cancion_actual else "Ninguna",
            "lista": self.lista_actual.nombre if self.lista_actual else "Ninguna",
            "reproduciendo": self.reproduciendo
        }

    def __str__(self) -> str:
        estado = "reproduciendo" if self.reproduciendo else "pausado"
        return f"Reproductor ({estado})"

