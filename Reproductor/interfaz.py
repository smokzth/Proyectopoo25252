class InterfazConsola:
    def __init__(self, reproductor):
        self.reproductor = reproductor

    def mostrar_menu_principal(self):
        print("\n🎵 --- REPRODUCTOR DE MÚSICA --- 🎵")
        print("1. Ver biblioteca")
        print("2. Gestionar listas")
        print("3. Controles de reproducción")
        print("4. Buscar canciones")
        print("5. Estadísticas")
        print("0. Salir")

    def mostrar_biblioteca(self):
        print("\n📚 Biblioteca musical:")
        for i, cancion in enumerate(self.reproductor.biblioteca.canciones):
            print(f"{i+1}. {cancion.info()}")

    def gestionar_listas(self):
        print("\n🎶 Listas disponibles:")
        for nombre in self.reproductor.biblioteca.listas:
            print(f"- {nombre}")
        nombre_lista = input("Nombre de la lista para crear/usar: ")
        lista = self.reproductor.biblioteca.obtener_lista(nombre_lista)
        if not lista:
            lista = self.reproductor.biblioteca.crear_lista(nombre_lista)
            print(f"Lista '{nombre_lista}' creada.")
        while True:
            print(f"\n📀 Lista '{nombre_lista}'")
            print("1. Ver canciones")
            print("2. Agregar canción de la biblioteca")
            print("3. Eliminar canción")
            print("0. Volver")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print(lista.listar_canciones())
            elif opcion == "2":
                self.mostrar_biblioteca()
                indice = int(input("Número de canción a agregar: ")) - 1
                if 0 <= indice < len(self.reproductor.biblioteca.canciones):
                    lista.agregar_cancion(self.reproductor.biblioteca.canciones[indice])
                    print("Canción agregada.")
            elif opcion == "3":
                print(lista.listar_canciones())
                indice = int(input("Número de canción a eliminar: ")) - 1
                lista.eliminar_cancion(indice)
            elif opcion == "0":
                break

    def controles_reproductor(self):
        while True:
            print("\n🎧 Controles:")
            print("1. Play")
            print("2. Pause")
            print("3. Stop")
            print("4. Siguiente")
            print("5. Anterior")
            print("6. Cambiar lista")
            print("0. Volver")
            opcion = input("Seleccione: ")
            if opcion == "1":
                self.reproductor.play()
            elif opcion == "2":
                self.reproductor.pause()
            elif opcion == "3":
                self.reproductor.stop()
            elif opcion == "4":
                self.reproductor.siguiente()
            elif opcion == "5":
                self.reproductor.anterior()
            elif opcion == "6":
                nombre = input("Nombre de la lista: ")
                self.reproductor.cambiar_lista(nombre)
            elif opcion == "0":
                break

    def buscar_canciones(self):
        criterio = input("Buscar por (titulo/artista): ").lower()
        valor = input("Ingrese el texto de búsqueda: ")
        if criterio == "titulo":
            resultados = self.reproductor.biblioteca.buscar_por_titulo(valor)
        else:
            resultados = self.reproductor.biblioteca.buscar_por_artista(valor)
        print("\n🔍 Resultados:")
        for c in resultados:
            print(c.info())

    def ejecutar(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.mostrar_biblioteca()
            elif opcion == "2":
                self.gestionar_listas()
            elif opcion == "3":
                self.controles_reproductor()
            elif opcion == "4":
                self.buscar_canciones()
            elif opcion == "5":
                self.reproductor.biblioteca.mostrar_estadisticas()
            elif opcion == "0":
                print("👋 Saliendo del reproductor.")
                break
