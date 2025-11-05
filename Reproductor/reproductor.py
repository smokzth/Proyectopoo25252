

from biblioteca import Biblioteca
from lista_reproduccion import ListaDeReproduccion
from cancion import Cancion
from typing import Optional

# RF10: Reproducción real de audio con pygame
try:
    import pygame

    PYGAME_DISPONIBLE = True
except ImportError:
    PYGAME_DISPONIBLE = False
    print("⚠ pygame no está instalado. Reproducción de audio no disponible.")
    print("  Instala con: pip install pygame")


class Reproductor:



    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
        self.lista_actual: Optional[ListaDeReproduccion] = None
        self.cancion_actual: Optional[Cancion] = None
        self.reproduciendo = False
        self.pausado = False  # NUEVO: para distinguir entre pausado y detenido
        self.volumen = 0.7
        self.modo_audio_real = PYGAME_DISPONIBLE

        # RF10: Inicializar pygame si está disponible
        if self.modo_audio_real:
            try:
                pygame.mixer.init()
                pygame.mixer.music.set_volume(self.volumen)
                print("✓ Sistema de audio inicializado (pygame)")
            except:
                self.modo_audio_real = False
                print("⚠ Error al inicializar pygame, usando modo simulado")

    def play(self) -> None:
        """Inicia o reanuda la reproducción"""
        if self.cancion_actual:
            # Si estaba pausado, solo reanudar
            if self.pausado and self.modo_audio_real:
                try:
                    pygame.mixer.music.unpause()
                    self.reproduciendo = True
                    self.pausado = False
                    print(f"\n▶ REANUDANDO: {self.cancion_actual}")
                    return
                except Exception as e:
                    print(f"⚠ Error al reanudar: {e}")

            # Si no estaba pausado, iniciar desde el principio
            self.reproduciendo = True
            self.pausado = False
            self.cancion_actual.incrementar_reproducciones()

            # RF10: Reproducción real con pygame
            if self.modo_audio_real:
                try:
                    import os
                    if os.path.exists(self.cancion_actual.ruta_archivo):
                        pygame.mixer.music.load(self.cancion_actual.ruta_archivo)
                        pygame.mixer.music.play()
                        print(f"\n▶ REPRODUCIENDO (AUDIO REAL): {self.cancion_actual}")
                    else:
                        print(f"\n▶ REPRODUCIENDO (Simulado - archivo no encontrado): {self.cancion_actual}")
                except Exception as e:
                    print(f"\n▶ REPRODUCIENDO (Simulado - error: {e}): {self.cancion_actual}")
            else:
                print(f"\n▶ REPRODUCIENDO (Modo simulado): {self.cancion_actual}")
        else:
            print("✗ No hay canción seleccionada")

    def pause(self) -> None:
        """Pausa la reproducción"""
        if self.reproduciendo and not self.pausado:
            self.reproduciendo = False
            self.pausado = True

            # RF10: Pausar audio real
            if self.modo_audio_real:
                try:
                    pygame.mixer.music.pause()
                except:
                    pass

            print("⏸ Pausado")
        else:
            print("✗ No hay reproducción activa")

    def stop(self) -> None:
        """Detiene la reproducción completamente"""
        self.reproduciendo = False
        self.pausado = False

        # RF10: Detener audio real
        if self.modo_audio_real:
            try:
                pygame.mixer.music.stop()
            except:
                pass

        print("⏹ Detenido")

    def siguiente(self) -> None:
        """Avanza a la siguiente canción"""
        if self.lista_actual:
            was_playing = self.reproduciendo
            self.stop()  # Detener la canción actual
            self.cancion_actual = self.lista_actual.siguiente()
            if was_playing and self.cancion_actual:
                self.play()
            elif self.cancion_actual:
                print(f"⏭ Siguiente: {self.cancion_actual}")
        else:
            print("✗ No hay lista de reproducción activa")

    def anterior(self) -> None:
        """Retrocede a la canción anterior"""
        if self.lista_actual:
            was_playing = self.reproduciendo
            self.stop()  # Detener la canción actual
            self.cancion_actual = self.lista_actual.anterior()
            if was_playing and self.cancion_actual:
                self.play()
            elif self.cancion_actual:
                print(f"⏮ Anterior: {self.cancion_actual}")
        else:
            print("✗ No hay lista de reproducción activa")

    def cambiar_lista(self, nombre_lista: str) -> None:
        """Cambia la lista de reproducción actual"""
        lista = self.biblioteca.obtener_lista(nombre_lista)
        if lista and lista.obtener_total_canciones() > 0:
            self.stop()  # Detener lo que esté sonando
            self.lista_actual = lista
            self.cancion_actual = lista.obtener_cancion_actual()
            print(f"✓ Lista activa: {nombre_lista}")
            print(f"  Canción actual: {self.cancion_actual}")
        else:
            print(f"✗ Lista '{nombre_lista}' no existe o está vacía")

    def activar_shuffle(self) -> None:
        """RF6: Activa el modo aleatorio"""
        if self.lista_actual:
            self.lista_actual.shuffle()
            self.cancion_actual = self.lista_actual.obtener_cancion_actual()
        else:
            print("✗ No hay lista activa")

    def desactivar_shuffle(self) -> None:
        """RF6: Desactiva el modo aleatorio"""
        if self.lista_actual:
            self.lista_actual.restaurar_orden()
            self.cancion_actual = self.lista_actual.obtener_cancion_actual()
        else:
            print("✗ No hay lista activa")

    def ajustar_volumen(self, nivel: float) -> None:
        """Ajusta el volumen (0.0 - 1.0)"""
        if 0.0 <= nivel <= 1.0:
            self.volumen = nivel

            # RF10: Ajustar volumen real
            if self.modo_audio_real:
                try:
                    pygame.mixer.music.set_volume(nivel)
                except:
                    pass

            print(f"🔊 Volumen: {int(nivel * 100)}%")
        else:
            print("✗ El volumen debe estar entre 0 y 1")

    def obtener_estado(self) -> dict:
        """Retorna el estado actual del reproductor"""
        return {
            "cancion": str(self.cancion_actual) if self.cancion_actual else "Ninguna",
            "lista": self.lista_actual.nombre if self.lista_actual else "Ninguna",
            "reproduciendo": self.reproduciendo,
            "pausado": self.pausado,
            "shuffle": self.lista_actual.shuffle_activo if self.lista_actual else False,
            "volumen": int(self.volumen * 100),
            "audio_real": self.modo_audio_real
        }

    def reproducir_cancion_especifica(self, indice: int) -> None:
        """Reproduce una canción específica de la lista actual"""
        if self.lista_actual and 0 <= indice < self.lista_actual.obtener_total_canciones():
            self.stop()  # Detener primero
            self.lista_actual.indice_actual = indice
            self.cancion_actual = self.lista_actual.obtener_cancion_actual()
            self.play()
        else:
            print("✗ Índice inválido")

    def __str__(self) -> str:
        if self.pausado:
            estado = "pausado"
        elif self.reproduciendo:
            estado = "reproduciendo"
        else:
            estado = "detenido"
        return f"Reproductor ({estado})"

    def __del__(self):
        """Limpia recursos al destruir el objeto"""
        if self.modo_audio_real:
            try:
                pygame.mixer.quit()
            except:
                pass