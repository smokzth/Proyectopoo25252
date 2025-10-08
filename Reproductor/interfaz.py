from biblioteca import Biblioteca
from lista_reproduccion import ListaReproduccion
from reproductor import Reproductor
from cancion import Cancion

class Interfaz:
    def __init__(self):
        self.biblioteca = Biblioteca()
        self.listas = {}
        self.reproductor = Reproductor()

    def ejecutar(self):
        while True:
            print("\n--- Menú Principal ---")
            print("1. Biblioteca")
            print("2. Listas de Reproducción")
            print("3. Reproductor")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.menu_biblioteca()
            elif opcion == "2":
                self.menu_listas()
            elif opcion == "3":
                self.menu_reproductor()
            elif opcion == "4":
                print("👋 Saliendo del programa...")
                break
            else:
                print("Opción inválida.")

    # ----------- Biblioteca -------------
    def menu_biblioteca(self):
        while True:
            print("\n--- Biblioteca ---")
            print("1. Agregar canción")
            print("2. Eliminar canción")
            print("3. Mostrar canciones")
            print("4. Volver")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                titulo = input("Título: ")
                artista = input("Artista: ")
                duracion = input("Duración: ")
                album = input("Álbum: ")
                anio = input("Año: ")
                genero = input("Género: ")
                cancion = Cancion(titulo, artista, duracion, album, anio, genero)
                self.biblioteca.agregar_cancion(cancion)
                print("✅ Canción agregada exitosamente.")

            elif opcion == "2":
                titulo = input("Título de la canción a eliminar: ")
                if self.biblioteca.eliminar_cancion(titulo):
                    print("🗑️ Canción eliminada.")
                else:
                    print("❌ No se encontró la canción.")

            elif opcion == "3":
                self.biblioteca.listar_canciones()

            elif opcion == "4":
                break
            else:
                print("Opción inválida.")

    # ----------- Listas de reproducción -------------
    def menu_listas(self):
        while True:
            print("\n--- Listas de Reproducción ---")
            print("1. Crear lista")
            print("2. Agregar canción a lista")
            print("3. Eliminar canción de lista")
            print("4. Mostrar listas")
            print("5. Seleccionar lista para reproducir")
            print("6. Volver")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Nombre de la lista: ")
                self.listas[nombre] = ListaReproduccion(nombre)
                print(f"✅ Lista '{nombre}' creada.")

            elif opcion == "2":
                nombre = input("Nombre de la lista: ")
                if nombre not in self.listas:
                    print("❌ No existe esa lista.")
                    continue
                self.biblioteca.listar_canciones()
                titulo = input("Título de la canción a agregar: ")
                cancion = next((c for c in self.biblioteca.canciones if c.titulo.lower() == titulo.lower()), None)
                if cancion:
                    self.listas[nombre].agregar_cancion(cancion)
                    print("🎵 Canción agregada a la lista.")
                else:
                    print("❌ No se encontró la canción.")

            elif opcion == "3":
                nombre = input("Nombre de la lista: ")
                if nombre in self.listas:
                    titulo = input("Título de la canción a eliminar: ")
                    if self.listas[nombre].eliminar_cancion(titulo):
                        print("🗑️ Canción eliminada de la lista.")
                    else:
                        print("❌ No se encontró en la lista.")
                else:
                    print("❌ No existe esa lista.")

            elif opcion == "4":
                if not self.listas:
                    print("No hay listas creadas.")
                else:
                    for nombre, lista in self.listas.items():
                        print(f"- {nombre} ({len(lista.canciones)} canciones)")

            elif opcion == "5":
                nombre = input("Nombre de la lista: ")
                if nombre in self.listas:
                    self.reproductor.seleccionar_lista(self.listas[nombre])
                else:
                    print("❌ No existe esa lista.")

            elif opcion == "6":
                break
            else:
                print("Opción inválida.")

    # ----------- Reproductor -------------
    def menu_reproductor(self):
        while True:
            print("\n--- Reproductor ---")
            print("1. Play")
            print("2. Stop")
            print("3. Siguiente")
            print("4. Anterior")
            print("5. Mostrar canción actual")
            print("6. Volver")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.reproductor.play()
            elif opcion == "2":
                self.reproductor.stop()
            elif opcion == "3":
                self.reproductor.siguiente()
            elif opcion == "4":
                self.reproductor.anterior()
            elif opcion == "5":
                if self.reproductor.cancion_actual:
                    self.reproductor.cancion_actual.mostrar_info()
                else:
                    print("No hay canción en reproducción.")
            elif opcion == "6":
                break
            else:
                print("Opción inválida.")

