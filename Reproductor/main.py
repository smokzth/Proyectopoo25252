"""
main.py - Punto de entrada del Reproductor de Música
Ahora con opción de Interfaz Gráfica o Consola
Versión mejorada con verificación de archivos
"""

from cancion import Cancion
from biblioteca import Biblioteca
from reproductor import Reproductor
from interfaz import InterfazConsola
import sys
import os


def verificar_archivo_existe(ruta: str) -> bool:
    """Verifica si un archivo de audio existe"""
    return os.path.exists(ruta) and os.path.isfile(ruta)


def crear_datos_demo() -> Biblioteca:
    """Crea datos de demostración"""
    biblioteca = Biblioteca()

    print("📦 Cargando datos de demostración...")

    # IMPORTANTE: Asegúrate de que estos nombres coincidan EXACTAMENTE
    # con los archivos que tienes en tu carpeta music/
    canciones_demo = [
        # Formato: Cancion(titulo, artista, duracion_segundos, ruta, album, año, genero)
        Cancion("Love The Way You Lie", "Rihanna ft. Eminem", 263, "music/lovetheway.mp3",
                "Recovery", 2010, "Hip-Hop"),
        Cancion("Space Bound", "Eminem", 264, "music/spacebound.mp3",
                "Recovery", 2010, "Hip-Hop"),
        Cancion("Olvidala", "Binomio de Oro", 267, "music/olvidala.mp3",
                "Clásicos", 1990, "Vallenato"),
        Cancion("Hotel California", "Eagles", 391, "music/eagles_hc.mp3",
                "Hotel California", 1976, "Rock"),
        Cancion("La Avispa", "El Andariego", 232, "music/laavispa.mp3",
                "Clásicos", 1980, "Vallenato"),
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

    # Verificar qué archivos existen y cuáles no
    print("\n🔍 Verificando archivos de audio...")
    archivos_encontrados = 0
    archivos_faltantes = []

    for cancion in canciones_demo:
        if verificar_archivo_existe(cancion.ruta_archivo):
            biblioteca.agregar_cancion(cancion)
            archivos_encontrados += 1
            print(f"  ✓ {cancion.titulo} - {cancion.ruta_archivo}")
        else:
            archivos_faltantes.append((cancion.titulo, cancion.ruta_archivo))
            print(f"  ✗ {cancion.titulo} - NO ENCONTRADO: {cancion.ruta_archivo}")

    # Mostrar resumen
    print(f"\n📊 Resumen:")
    print(f"  ✓ {archivos_encontrados} archivos encontrados")
    print(f"  ✗ {len(archivos_faltantes)} archivos faltantes")

    if archivos_faltantes:
        print(f"\n⚠️  ARCHIVOS FALTANTES:")
        print(f"  Crea la carpeta 'music/' si no existe y agrega estos archivos:")
        for titulo, ruta in archivos_faltantes:
            print(f"    • {ruta}")
        print(f"\n  O edita main.py para usar las rutas correctas de tus archivos")

    # Verificar si hay al menos una canción
    if archivos_encontrados == 0:
        print("\n❌ ERROR: No se encontró ningún archivo de audio")
        print("   Por favor, agrega archivos .mp3 a la carpeta 'music/'")
        print("   y actualiza las rutas en main.py")
        return biblioteca

    # Crear listas solo con canciones que existen
    canciones_validas = biblioteca.canciones

    if len(canciones_validas) >= 4:
        # Lista Rock (canciones índices que sean rock si existen)
        lista_rock = biblioteca.crear_lista("Rock Clásico")
        if lista_rock:
            for cancion in canciones_validas:
                if cancion.genero in ["Rock", "Grunge", "Progressive Rock", "Metal"]:
                    lista_rock.agregar_cancion(cancion)

        # Lista Favoritos (primeras 4 canciones disponibles)
        lista_favoritos = biblioteca.crear_lista("Mis Favoritos")
        if lista_favoritos:
            for i, cancion in enumerate(canciones_validas[:4]):
                lista_favoritos.agregar_cancion(cancion)
                cancion.es_favorita = True

        # Lista Energéticas
        lista_energeticas = biblioteca.crear_lista("Para Entrenar")
        if lista_energeticas:
            for cancion in canciones_validas:
                if cancion.genero in ["Hip-Hop", "Metal", "Rock", "Grunge"]:
                    lista_energeticas.agregar_cancion(cancion)

        print(f"  ✓ 3 listas de reproducción creadas")

        # Simular reproducciones
        if len(canciones_validas) >= 1:
            canciones_validas[0].reproducciones = 15
        if len(canciones_validas) >= 2:
            canciones_validas[1].reproducciones = 12
        if len(canciones_validas) >= 3:
            canciones_validas[2].reproducciones = 20
        if len(canciones_validas) >= 4:
            canciones_validas[3].reproducciones = 8

    return biblioteca


def listar_archivos_music():
    """Lista todos los archivos en la carpeta music/ para ayudar al usuario"""
    print("\n📁 Archivos encontrados en la carpeta 'music/':")
    if os.path.exists("music"):
        archivos = [f for f in os.listdir("music") if f.endswith(('.mp3', '.wav', '.ogg', '.flac'))]
        if archivos:
            for archivo in sorted(archivos):
                print(f"  • {archivo}")
        else:
            print("  ⚠️  No hay archivos de audio en la carpeta")
    else:
        print("  ❌ La carpeta 'music/' no existe")
        print("  Crea la carpeta y agrega archivos .mp3")


def mostrar_menu_inicial():
    """Muestra menú para elegir tipo de interfaz"""
    print("\n" + "=" * 70)
    print("🎵 REPRODUCTOR DE MÚSICA - POO 🎵".center(70))
    print("=" * 70)
    print("\n¿Qué interfaz deseas usar?\n")
    print("  1. 🖥️  Interfaz Gráfica (GUI - Tkinter)")
    print("  2. 💻 Interfaz de Consola (Terminal)")
    print("  3. 📁 Listar archivos en carpeta music/")
    print("  0. ❌ Salir")
    print("\n" + "=" * 70)


def main():
    """Función principal"""
    print("\n⏳ Inicializando sistema...")

    # Crear carpeta music si no existe
    if not os.path.exists("music"):
        print("📁 Creando carpeta 'music/'...")
        try:
            os.makedirs("music")
            print("  ✓ Carpeta creada. Agrega archivos .mp3 aquí")
        except Exception as e:
            print(f"  ✗ Error al crear carpeta: {e}")

    # Crear biblioteca con datos
    biblioteca = crear_datos_demo()

    # Verificar si hay canciones
    if len(biblioteca.canciones) == 0:
        print("\n❌ No se puede continuar sin canciones")
        print("\nOpciones:")
        print("  1. Agrega archivos .mp3 a la carpeta 'music/'")
        print("  2. Edita main.py para usar las rutas correctas")
        print("  3. Usa la opción de 'Importar CSV' con tus propias canciones")
        input("\nPresiona Enter para salir...")
        return

    # Crear reproductor
    reproductor = Reproductor(biblioteca)

    # Cambiar a primera lista disponible
    if biblioteca.listas:
        primera_lista = list(biblioteca.listas.keys())[0]
        reproductor.cambiar_lista(primera_lista)

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
                import traceback
                traceback.print_exc()
                input("\nPresiona Enter para continuar...")

        elif opcion == "2":
            print("\n💻 Iniciando Interfaz de Consola...\n")
            interfaz = InterfazConsola(reproductor)
            try:
                interfaz.ejecutar()
                break
            except KeyboardInterrupt:
                print("\n\n⚠️  Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n\n❌ Error inesperado: {e}")
                import traceback
                traceback.print_exc()
                break

        elif opcion == "3":
            listar_archivos_music()
            input("\nPresiona Enter para continuar...")

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
        import traceback
        traceback.print_exc()
    finally:
        print("\n👋 Fin del programa\n")