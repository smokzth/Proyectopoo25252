"""
Módulo interfaz.py
Define la clase InterfazConsola para interacción con el usuario
VERSIÓN ACTUALIZADA - Sincronizada con cambios del reproductor
"""

from reproductor import Reproductor


class InterfazConsola:
    """Interfaz de usuario en consola con todos los RF implementados"""

    def __init__(self, reproductor: Reproductor):
        self.reproductor = reproductor

    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 60)
        print("🎵 --- REPRODUCTOR DE MÚSICA --- 🎵".center(60))
        print("=" * 60)
        print("1. Ver biblioteca")
        print("2. Gestionar listas")
        print("3. Controles de reproducción")
        print("4. Buscar canciones")
        print("5. Estadísticas")  # RF7
        print("6. Favoritos")  # RF7
        print("7. Importar/Exportar")  # RF8 y RF9
        print("0. Salir")
        print("=" * 60)

    def mostrar_biblioteca(self):
        """Muestra todas las canciones de la biblioteca"""
        print("\n" + "=" * 60)
        print("📚 BIBLIOTECA MUSICAL".center(60))
        print("=" * 60)
        canciones = self.reproductor.biblioteca.canciones
        if not canciones:
            print("✗ La biblioteca está vacía")
        else:
            for i, cancion in enumerate(canciones):
                print(f"{i + 1}. {cancion}")
            print("=" * 60)
            print(f"Total: {len(canciones)} canciones")

    def gestionar_listas(self):
        """Gestiona las listas de reproducción"""
        while True:
            print("\n" + "=" * 60)
            print("🎶 GESTIÓN DE LISTAS".center(60))
            print("=" * 60)

            # Mostrar listas existentes
            listas = self.reproductor.biblioteca.listas
            if listas:
                print("\nListas disponibles:")
                for nombre, lista in listas.items():
                    shuffle_icon = "🔀 " if lista.shuffle_activo else ""
                    total = lista.obtener_total_canciones()
                    estado = "VACÍA" if total == 0 else f"{total} canciones"
                    print(f"  ▸ {shuffle_icon}{nombre} ({estado})")
            else:
                print("\n✗ No hay listas creadas")

            print("\n1. Crear nueva lista")
            print("2. Trabajar con lista existente")
            print("3. Eliminar lista")
            print("4. Ver todas las listas")
            print("0. Volver")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                nombre_lista = input("Nombre de la nueva lista: ").strip()
                if nombre_lista:
                    self.reproductor.biblioteca.crear_lista(nombre_lista)

            elif opcion == "2":
                nombre_lista = input("Nombre de la lista: ").strip()
                lista = self.reproductor.biblioteca.obtener_lista(nombre_lista)
                if lista:
                    self._menu_lista_especifica(lista, nombre_lista)
                else:
                    print(f"✗ La lista '{nombre_lista}' no existe")

            elif opcion == "3":
                nombre_lista = input("Nombre de la lista a eliminar: ").strip()
                self.reproductor.biblioteca.eliminar_lista(nombre_lista)

            elif opcion == "4":
                self._ver_todas_las_listas()

            elif opcion == "0":
                break

    def _ver_todas_las_listas(self):
        """Muestra información detallada de todas las listas"""
        listas = self.reproductor.biblioteca.listas
        if not listas:
            print("\n✗ No hay listas creadas")
            return

        print("\n" + "=" * 60)
        print("📋 TODAS LAS LISTAS".center(60))
        print("=" * 60)

        for nombre, lista in listas.items():
            shuffle_texto = " (🔀 ALEATORIO)" if lista.shuffle_activo else ""
            print(f"\n▸ {nombre}{shuffle_texto}")
            print(f"  Total: {lista.obtener_total_canciones()} canciones")
            if lista.obtener_total_canciones() > 0:
                print(f"  Duración: {lista._get_duracion_total_formateada()}")
            else:
                print("  (Lista vacía)")
        print("=" * 60)

    def _menu_lista_especifica(self, lista, nombre_lista):
        """Submenú para gestionar una lista específica"""
        while True:
            print(f"\n{'=' * 60}")
            shuffle_texto = " (🔀 ALEATORIO)" if lista.shuffle_activo else ""
            total = lista.obtener_total_canciones()
            estado = "VACÍA" if total == 0 else f"{total} canciones"
            print(f"📀 Lista: {nombre_lista}{shuffle_texto} ({estado})".center(60))
            print(f"{'=' * 60}")
            print("1. Ver canciones")
            print("2. Agregar canción de la biblioteca")
            print("3. Eliminar canción")
            print("4. Activar/Desactivar shuffle")  # RF6
            print("5. Cargar esta lista en el reproductor")
            print("0. Volver")

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                if lista.obtener_total_canciones() > 0:
                    print(lista.listar_canciones())
                else:
                    print("\n✗ La lista está vacía")
                    print("💡 Usa la opción 2 para agregar canciones desde la biblioteca")

            elif opcion == "2":
                self.mostrar_biblioteca()
                if len(self.reproductor.biblioteca.canciones) == 0:
                    print("\n✗ No hay canciones en la biblioteca")
                    continue

                try:
                    indice = int(input("\nNúmero de canción a agregar: ")) - 1
                    canciones = self.reproductor.biblioteca.canciones
                    if 0 <= indice < len(canciones):
                        lista.agregar_cancion(canciones[indice])
                    else:
                        print("✗ Número inválido")
                except ValueError:
                    print("✗ Entrada inválida. Ingrese un número.")

            elif opcion == "3":
                if lista.obtener_total_canciones() == 0:
                    print("\n✗ La lista está vacía, no hay nada que eliminar")
                    continue

                print(lista.listar_canciones())
                try:
                    indice = int(input("\nNúmero de canción a eliminar: ")) - 1
                    lista.eliminar_cancion(indice)
                except ValueError:
                    print("✗ Entrada inválida. Ingrese un número.")

            elif opcion == "4":  # RF6: Shuffle
                if lista.obtener_total_canciones() == 0:
                    print("\n✗ No se puede activar shuffle en una lista vacía")
                    continue

                if lista.shuffle_activo:
                    lista.restaurar_orden()
                else:
                    lista.shuffle()

            elif opcion == "5":
                if lista.obtener_total_canciones() > 0:
                    self.reproductor.cambiar_lista(nombre_lista)
                else:
                    print("\n✗ No puedes cargar una lista vacía en el reproductor")
                    print("💡 Agrega canciones primero")

            elif opcion == "0":
                break

    def controles_reproductor(self):
        """Controles del reproductor"""
        while True:
            print("\n" + "=" * 60)
            print("🎧 CONTROLES DEL REPRODUCTOR".center(60))
            print("=" * 60)

            # Mostrar estado actual
            estado = self.reproductor.obtener_estado()
            print(f"\n🎵 Canción: {estado['cancion']}")
            print(f"📋 Lista: {estado['lista']}")
            shuffle_estado = "🔀 Activado" if estado['shuffle'] else "Desactivado"
            print(f"🔀 Shuffle: {shuffle_estado}")

            # Estado mejorado
            if estado['pausado']:
                print(f"⏸ Estado: Pausado")
            elif estado['reproduciendo']:
                print(f"▶ Estado: Reproduciendo")
            else:
                print(f"⏹ Estado: Detenido")

            print(f"🔊 Volumen: {estado['volumen']}%")
            if estado['audio_real']:
                print("🎼 Modo: Audio Real (pygame)")
            else:
                print("🎼 Modo: Simulado")

            print("\n1. Play / Resume")
            print("2. Pause")
            print("3. Stop")
            print("4. Siguiente")
            print("5. Anterior")
            print("6. Cambiar lista activa")
            print("7. Activar/Desactivar shuffle")  # RF6
            print("8. Ajustar volumen")
            print("9. Info de canción actual")
            print("10. Marcar/Desmarcar favorita")  # RF7
            print("11. Reproducir canción específica")
            print("0. Volver")

            opcion = input("\nSeleccione: ").strip()

            if opcion == "1":
                if self.reproductor.cancion_actual:
                    self.reproductor.play()
                else:
                    print("\n✗ No hay canción seleccionada")
                    print("💡 Carga una lista primero (opción 6)")

            elif opcion == "2":
                self.reproductor.pause()

            elif opcion == "3":
                self.reproductor.stop()

            elif opcion == "4":
                if self.reproductor.lista_actual:
                    self.reproductor.siguiente()
                else:
                    print("✗ No hay lista activa")

            elif opcion == "5":
                if self.reproductor.lista_actual:
                    self.reproductor.anterior()
                else:
                    print("✗ No hay lista activa")

            elif opcion == "6":
                self._cambiar_lista_activa()

            elif opcion == "7":  # RF6: Shuffle
                if self.reproductor.lista_actual:
                    if self.reproductor.lista_actual.obtener_total_canciones() == 0:
                        print("✗ La lista activa está vacía")
                    elif self.reproductor.lista_actual.shuffle_activo:
                        self.reproductor.desactivar_shuffle()
                    else:
                        self.reproductor.activar_shuffle()
                else:
                    print("✗ No hay lista activa")

            elif opcion == "8":
                try:
                    vol = float(input("Volumen (0-1): "))
                    self.reproductor.ajustar_volumen(vol)
                except ValueError:
                    print("✗ Entrada inválida")

            elif opcion == "9":
                if self.reproductor.cancion_actual:
                    print(self.reproductor.cancion_actual.info())
                else:
                    print("✗ No hay canción seleccionada")

            elif opcion == "10":  # RF7: Favoritos
                if self.reproductor.cancion_actual:
                    self.reproductor.cancion_actual.marcar_favorita()
                else:
                    print("✗ No hay canción seleccionada")

            elif opcion == "11":
                self._reproducir_cancion_especifica()

            elif opcion == "0":
                break

    def _reproducir_cancion_especifica(self):
        """Permite seleccionar y reproducir una canción específica de la lista actual"""
        if not self.reproductor.lista_actual:
            print("\n✗ No hay lista activa")
            print("💡 Carga una lista primero")
            return

        if self.reproductor.lista_actual.obtener_total_canciones() == 0:
            print("\n✗ La lista activa está vacía")
            return

        print(self.reproductor.lista_actual.listar_canciones())
        try:
            indice = int(input("\nNúmero de canción a reproducir: ")) - 1
            self.reproductor.reproducir_cancion_especifica(indice)
        except ValueError:
            print("✗ Entrada inválida. Ingrese un número.")

    def _cambiar_lista_activa(self):
        """Auxiliar para cambiar la lista activa"""
        listas = self.reproductor.biblioteca.listas
        if listas:
            print("\nListas disponibles:")
            for nombre, lista in listas.items():
                total = lista.obtener_total_canciones()
                estado = "VACÍA" if total == 0 else f"{total} canciones"
                print(f"  ▸ {nombre} ({estado})")
            nombre = input("\nNombre de la lista: ").strip()

            lista = self.reproductor.biblioteca.obtener_lista(nombre)
            if lista:
                if lista.obtener_total_canciones() > 0:
                    self.reproductor.cambiar_lista(nombre)
                else:
                    print(f"\n⚠ La lista '{nombre}' está vacía")
                    respuesta = input("¿Deseas cargarla de todas formas? (s/n): ").strip().lower()
                    if respuesta == 's':
                        self.reproductor.cambiar_lista(nombre)
                    else:
                        print("✗ Operación cancelada")
            else:
                print(f"✗ La lista '{nombre}' no existe")
        else:
            print("✗ No hay listas creadas")
            print("💡 Crea una lista desde el menú principal (opción 2)")

    def buscar_canciones(self):
        """Busca canciones por título o artista"""
        print("\n" + "=" * 60)
        print("🔍 BUSCAR CANCIONES".center(60))
        print("=" * 60)
        print("1. Buscar por título")
        print("2. Buscar por artista")

        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            valor = input("Título: ").strip()
            resultados = self.reproductor.biblioteca.buscar_por_titulo(valor)
        elif opcion == "2":
            valor = input("Artista: ").strip()
            resultados = self.reproductor.biblioteca.buscar_por_artista(valor)
        else:
            print("✗ Opción inválida")
            return

        if resultados:
            print(f"\n{'=' * 60}")
            print(f"Encontradas {len(resultados)} canciones".center(60))
            print(f"{'=' * 60}")
            for i, cancion in enumerate(resultados, 1):
                print(f"{i}. {cancion}")
            print(f"{'=' * 60}")
        else:
            print("\n✗ No se encontraron resultados")

    def menu_favoritos(self):
        """RF7: Menú de gestión de favoritos"""
        while True:
            print("\n" + "=" * 60)
            print("⭐ CANCIONES FAVORITAS".center(60))
            print("=" * 60)

            favoritas = self.reproductor.biblioteca.obtener_favoritas()

            if favoritas:
                print(f"\nTotal: {len(favoritas)} canciones favoritas\n")
                for i, cancion in enumerate(favoritas, 1):
                    print(f"{i}. {cancion}")
                print("=" * 60)
            else:
                print("\n✗ No tienes canciones favoritas")
                print("  Marca canciones como favoritas desde el reproductor")

            print("\n1. Ver información detallada")
            print("2. Crear lista con favoritas")
            print("0. Volver")

            opcion = input("\nSeleccione: ").strip()

            if opcion == "1" and favoritas:
                try:
                    indice = int(input("Número de canción: ")) - 1
                    if 0 <= indice < len(favoritas):
                        print(favoritas[indice].info())
                    else:
                        print("✗ Número inválido")
                except ValueError:
                    print("✗ Entrada inválida")

            elif opcion == "2" and favoritas:
                nombre = input("Nombre para la nueva lista: ").strip()
                if nombre:
                    lista = self.reproductor.biblioteca.crear_lista(nombre)
                    if lista:
                        for cancion in favoritas:
                            lista.agregar_cancion(cancion)
                        print(f"✓ Lista '{nombre}' creada con {len(favoritas)} favoritas")

            elif opcion == "0":
                break

    def menu_importar_exportar(self):
        """RF8 y RF9: Menú de importación/exportación"""
        while True:
            print("\n" + "=" * 60)
            print("📥📤 IMPORTAR/EXPORTAR".center(60))
            print("=" * 60)
            print("1. Importar canciones desde CSV")  # RF8
            print("2. Exportar listas a JSON")  # RF9
            print("3. Importar listas desde JSON")  # RF9
            print("0. Volver")

            opcion = input("\nSeleccione: ").strip()

            if opcion == "1":  # RF8
                print("\nFormato esperado del CSV:")
                print("titulo,artista,duracion,ruta,album,año,genero")
                print("\nEjemplo:")
                print("Canción,Artista,180,music/song.mp3,Album,2020,Rock")
                ruta = input("\nRuta del archivo CSV: ").strip()
                if ruta:
                    self.reproductor.biblioteca.importar_desde_csv(ruta)

            elif opcion == "2":  # RF9: Exportar
                if len(self.reproductor.biblioteca.listas) == 0:
                    print("\n✗ No hay listas para exportar")
                    print("💡 Crea listas primero desde el menú principal")
                    continue

                ruta = input("Ruta para guardar JSON (ej: listas.json): ").strip()
                if ruta:
                    if not ruta.endswith('.json'):
                        ruta += '.json'
                    self.reproductor.biblioteca.exportar_listas_json(ruta)

            elif opcion == "3":  # RF9: Importar
                ruta = input("Ruta del archivo JSON: ").strip()
                if ruta:
                    self.reproductor.biblioteca.importar_listas_json(ruta)

            elif opcion == "0":
                break

    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación"""
        while True:
            self.mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self.mostrar_biblioteca()

            elif opcion == "2":
                self.gestionar_listas()

            elif opcion == "3":
                self.controles_reproductor()

            elif opcion == "4":
                self.buscar_canciones()

            elif opcion == "5":  # RF7: Estadísticas
                self.reproductor.biblioteca.mostrar_estadisticas()

            elif opcion == "6":  # RF7: Favoritos
                self.menu_favoritos()

            elif opcion == "7":  # RF8 y RF9: Importar/Exportar
                self.menu_importar_exportar()

            elif opcion == "0":
                print("\n" + "=" * 60)
                print("👋 Gracias por usar el reproductor".center(60))
                print("=" * 60 + "\n")
                break

            else:
                print("✗ Opción inválida. Intente de nuevo.")