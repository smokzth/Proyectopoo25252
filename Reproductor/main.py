"""
main.py - Punto de entrada del Reproductor de Música
Proyecto de Programación Orientada a Objetos
"""

from cancion import Cancion
from biblioteca import Biblioteca
from reproductor import Reproductor
from interfaz import InterfazConsola


def crear_datos_demo() -> Biblioteca:
    """
    Crea datos de demostración para probar el sistema.

    Returns:
        Biblioteca: Biblioteca con canciones y listas de ejemplo
    """
    biblioteca = Biblioteca()

    # Crear canciones de ejemplo (sin ruta de archivo)
    canciones_demo = [
        Cancion("Bohemian Rhapsody", "Queen", 355, "A Night at the Opera", 1975, "Rock"),
        Cancion("Imagine", "John Lennon", 183, "Imagine", 1971, "Rock"),
        Cancion("Stairway to Heaven", "Led Zeppelin", 482, "Led Zeppelin IV", 1971, "Rock"),
        Cancion("Hotel California", "Eagles", 391, "Hotel California", 1976, "Rock"),
        Cancion("Billie Jean", "Michael Jackson", 294, "Thriller", 1982, "Pop"),
        Cancion("Smells Like Teen Spirit", "Nirvana", 301, "Nevermind", 1991, "Grunge"),
    ]

    # Agregar canciones a la biblioteca
    for cancion in canciones_demo:
        biblioteca.agregar_cancion(cancion)

    # Crear listas de reproducción de ejemplo
    lista_rock = biblioteca.crear_lista("Rock Clásico")
    if lista_rock:
        for i in [0, 1, 2, 3]:
            lista_rock.agregar_cancion(canciones_demo[i])

    lista_favoritos = biblioteca.crear_lista("Mis Favoritos")
    if lista_favoritos:
        for i in [0, 2, 4]:
            lista_favoritos.agregar_cancion(canciones_demo[i])

    # Simular algunas reproducciones
    canciones_demo[0].reproducciones = 15
    canciones_demo[2].reproducciones = 12
    canciones_demo[4].reproducciones = 8

    return biblioteca


def main():
    """Función principal del programa"""
    print("\n" + "=" * 60)
    print(" " * 15 + "REPRODUCTOR DE MÚSICA - POO")
    print(" " * 18 + "Inicializando sistema...")
    print("=" * 60)

    # Crear biblioteca con datos de demo
    biblioteca = crear_datos_demo()

    # Crear reproductor
    reproductor = Reproductor(biblioteca)

    # Configurar lista inicial
    reproductor.cambiar_lista("Rock Clásico")

    # Crear interfaz
    interfaz = InterfazConsola(reproductor)

    print("\n✓ Sistema listo")
    print("✓ Biblioteca cargada con 6 canciones")
    print("✓ 2 listas de reproducción creadas")

    # Ejecutar aplicación
    interfaz.ejecutar()

if __name__ == "__main__":
    main()


