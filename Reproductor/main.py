"""
main.py - Punto de entrada del Reproductor de Música
Ahora con opción de Interfaz Gráfica o Consola
"""

from cancion import Cancion
from biblioteca import Biblioteca
from reproductor import Reproductor
from interfaz import InterfazConsola
import sys


def crear_datos_demo() -> Biblioteca:
    """Crea datos de demostración"""
    biblioteca = Biblioteca()

    print("📦 Cargando datos de demostración...")

    canciones_demo = [
        Cancion("Love The Way You Lie", "Rihanna", 263, "music/lovetheway.mp3",
                "A Night at the Opera", 1975, "Rock"),
        Cancion("Space bound", "Eminem", 264, "music/spacebound.mp3",
                "Imagine", 1971, "Rock"),
        Cancion("Stairway to Heaven", "Led Zeppelin", 482, "music/lz_stairway.mp3",
                "Led Zeppelin IV", 1971, "Rock"),
        Cancion("Hotel California", "Eagles", 391, "music/eagles_hc.mp3",
                "Hotel California", 1976, "Rock"),
        Cancion("Billie Jean", "Michael Jackson", 294, "music/mj_bj.mp3",
                "Thriller", 1982, "Pop"),
        Cancion("Smells Like Teen Spirit", "Nirvana", 301, "music/nirvana_slts.mp3",
                "Nevermind", 1991, "Grunge"),
        Cancion("One", "Metallica", 447, "music/metallica_one.mp3",
                "...And Justice for All", 1988, "Metal"),
        Cancion("November Rain", "Guns N' Roses", 537, "music/gnr_nr.mp3",
                "Use Your Illusion I", 1991, "Rock"),
        Cancion("Comfortably Numb", "Pink Floyd", 382, "music/pf_cn.mp3",
                "The Wall", 1979, "Progressive Rock"),
        Cancion("Sweet Child O' Mine", "Guns N' Roses", 356, "music/gnr_scom.mp3",
                "Appetite for Destruction", 1987, "Rock"),
    ]

    for cancion in canciones_demo:
        biblioteca.agregar_cancion(cancion)

    # Crear listas
    lista_rock = biblioteca.crear_lista("Rock Clásico")
    if lista_rock:
        for i in [0, 1, 2, 3, 7, 8, 9]:
            lista_rock.agregar_cancion(canciones_demo[i])

    lista_favoritos = biblioteca.crear_lista("Mis Favoritos")
    if lista_favoritos:
        for i in [0, 2, 4, 6]:
            lista_favoritos.agregar_cancion(canciones_demo[i])
            canciones_demo[i].es_favorita = True

    lista_energeticas = biblioteca.crear_lista("Para Entrenar")
    if lista_energeticas:
        for i in [4, 5, 6, 9]:
            lista_energeticas.agregar_cancion(canciones_demo[i])

    # Simular reproducciones
    canciones_demo[0].reproducciones = 15
    canciones_demo[2].reproducciones = 12
    canciones_demo[4].reproducciones = 20
    canciones_demo[6].reproducciones = 8
    canciones_demo[1].reproducciones = 5

    print(f"  ✓ {len(canciones_demo)} canciones cargadas")
    print(f"  ✓ 3 listas de reproducción creadas")

    return biblioteca


def mostrar_menu_inicial():
    """Muestra menú para elegir tipo de interfaz"""
    print("\n" + "=" * 70)
    print("🎵 REPRODUCTOR DE MÚSICA - POO 🎵".center(70))
    print("=" * 70)
    print("\n¿Qué interfaz deseas usar?\n")
    print("  1. 🖥️  Interfaz Gráfica (GUI - Tkinter)")
    print("  2. 💻 Interfaz de Consola (Terminal)")
    print("  0. ❌ Salir")
    print("\n" + "=" * 70)


def main():
    """Función principal"""
    print("\n⏳ Inicializando sistema...")

    # Crear biblioteca con datos
    biblioteca = crear_datos_demo()

    # Crear reproductor
    reproductor = Reproductor(biblioteca)
    reproductor.cambiar_lista("Rock Clásico")

    print("\n✓ Sistema listo\n")

    # Menú de selección
    while True:
        mostrar_menu_inicial()
        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "1":
            print("\n🎨 Iniciando Interfaz Gráfica...")
            print("⏳ Cargando componentes visuales...\n")
            try:
                from interfaz_grafica import iniciar_gui
                iniciar_gui(reproductor)
                break
            except ImportError as e:
                print(f"❌ Error al cargar la interfaz gráfica: {e}")
                print("Asegúrate de que el archivo 'interfaz_grafica.py' existe")
                input("\nPresiona Enter para continuar...")
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                input("\nPresiona Enter para continuar...")

        elif opcion == "2":
            print("\n💻 Iniciando Interfaz de Consola...\n")
            interfaz = InterfazConsola(reproductor)
            try:
                interfaz.ejecutar()
                break
            except KeyboardInterrupt:
                print("\n\n⚠ Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n\n❌ Error inesperado: {e}")
                break

        elif opcion == "0":
            print("\n👋 ¡Hasta pronto!\n")
            break

        else:
            print("\n❌ Opción inválida. Intenta de nuevo.")
            input("Presiona Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("Por favor, reporta este error al equipo de desarrollo")
    finally:
        print("\n👋 Fin del programa\n")