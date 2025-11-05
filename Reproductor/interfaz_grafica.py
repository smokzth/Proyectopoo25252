
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from reproductor import Reproductor
from cancion import Cancion
from typing import Optional


class ReproductorGUI:

    def __init__(self, reproductor: Reproductor):
        self.reproductor = reproductor
        self.root = tk.Tk()
        self.root.title("🎵 Reproductor de Música")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1a1a2e')

        # Colores del tema
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text': '#ffffff',
            'text_secondary': '#b8b8b8',
            'success': '#00d9ff',
            'warning': '#f39c12'
        }

        self._crear_interfaz()
        self._actualizar_info()


    def _crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        main_frame = tk.Frame(self.root, bg=self.colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self._crear_panel_izquierdo(main_frame)
        self._crear_panel_central(main_frame)
        self._crear_panel_derecho(main_frame)

    def _crear_panel_izquierdo(self, parent):
        """Panel con biblioteca y listas"""
        left_panel = tk.Frame(parent, bg=self.colors['bg_medium'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))

        # Título
        titulo = tk.Label(left_panel, text="📚 BIBLIOTECA",
                          font=('Arial', 14, 'bold'),
                          bg=self.colors['bg_medium'], fg=self.colors['text'])
        titulo.pack(pady=10)

        # Pestañas
        notebook = ttk.Notebook(left_panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Pestaña Canciones
        tab_canciones = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(tab_canciones, text="Canciones")

        self.lista_canciones = tk.Listbox(tab_canciones,
                                          bg=self.colors['bg_light'],
                                          fg=self.colors['text'],
                                          font=('Courier', 9),
                                          selectmode=tk.SINGLE,
                                          borderwidth=0,
                                          highlightthickness=0,
                                          selectbackground=self.colors['accent'])
        self.lista_canciones.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lista_canciones.bind('<Double-Button-1>', self._reproducir_desde_biblioteca)

        # Pestaña Listas
        tab_listas = tk.Frame(notebook, bg=self.colors['bg_light'])
        notebook.add(tab_listas, text="Listas")

        self.lista_listas = tk.Listbox(tab_listas,
                                       bg=self.colors['bg_light'],
                                       fg=self.colors['text'],
                                       font=('Arial', 10),
                                       selectmode=tk.SINGLE,
                                       borderwidth=0,
                                       highlightthickness=0,
                                       selectbackground=self.colors['accent'])
        self.lista_listas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lista_listas.bind('<Double-Button-1>', self._cargar_lista)

        # Botones de gestión
        btn_frame = tk.Frame(tab_listas, bg=self.colors['bg_light'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(btn_frame, text="Nueva Lista",
                  command=self._crear_lista,
                  bg=self.colors['success'], fg='white',
                  font=('Arial', 9, 'bold'),
                  relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, padx=2)

        tk.Button(btn_frame, text="Eliminar",
                  command=self._eliminar_lista,
                  bg=self.colors['accent'], fg='white',
                  font=('Arial', 9, 'bold'),
                  relief=tk.FLAT, cursor='hand2').pack(side=tk.LEFT, padx=2)

        self._actualizar_listas()

    def _crear_panel_central(self, parent):
        """Panel central con reproductor"""
        center_panel = tk.Frame(parent, bg=self.colors['bg_medium'])
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Info de canción actual
        info_frame = tk.Frame(center_panel, bg=self.colors['bg_dark'],
                              height=200, relief=tk.RIDGE, borderwidth=2)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        info_frame.pack_propagate(False)

        self.lbl_cancion = tk.Label(info_frame, text="♪ Sin canción",
                                    font=('Arial', 20, 'bold'),
                                    bg=self.colors['bg_dark'],
                                    fg=self.colors['accent'])
        self.lbl_cancion.pack(pady=(20, 5))

        self.lbl_artista = tk.Label(info_frame, text="Selecciona una canción",
                                    font=('Arial', 14),
                                    bg=self.colors['bg_dark'],
                                    fg=self.colors['text_secondary'])
        self.lbl_artista.pack()

        self.lbl_duracion = tk.Label(info_frame, text="--:--",
                                     font=('Arial', 12),
                                     bg=self.colors['bg_dark'],
                                     fg=self.colors['success'])
        self.lbl_duracion.pack(pady=5)

        self.lbl_estado = tk.Label(info_frame, text="⏸ Pausado",
                                   font=('Arial', 11),
                                   bg=self.colors['bg_dark'],
                                   fg=self.colors['warning'])
        self.lbl_estado.pack()

        # Controles
        controles_frame = tk.Frame(center_panel, bg=self.colors['bg_medium'])
        controles_frame.pack(pady=20)

        btn_style = {
            'font': ('Arial', 16),
            'width': 4,
            'height': 2,
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'borderwidth': 0
        }

        self.btn_anterior = tk.Button(controles_frame, text="⏮",
                                      command=self._anterior,
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['text'],
                                      **btn_style)
        self.btn_anterior.pack(side=tk.LEFT, padx=5)

        self.btn_play = tk.Button(controles_frame, text="▶",
                                  command=self._toggle_play,
                                  bg=self.colors['accent'],
                                  fg='white',
                                  font=('Arial', 20),
                                  width=4, height=2,
                                  relief=tk.FLAT, cursor='hand2')
        self.btn_play.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(controles_frame, text="⏹",
                                  command=self._stop,
                                  bg=self.colors['bg_light'],
                                  fg=self.colors['text'],
                                  **btn_style)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_siguiente = tk.Button(controles_frame, text="⏭",
                                       command=self._siguiente,
                                       bg=self.colors['bg_light'],
                                       fg=self.colors['text'],
                                       **btn_style)
        self.btn_siguiente.pack(side=tk.LEFT, padx=5)

        # Volumen
        vol_frame = tk.Frame(center_panel, bg=self.colors['bg_medium'])
        vol_frame.pack(pady=10)

        tk.Label(vol_frame, text="🔊 Volumen:",
                 font=('Arial', 10),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text']).pack(side=tk.LEFT, padx=5)

        self.volume_slider = tk.Scale(vol_frame, from_=0, to=100,
                                      orient=tk.HORIZONTAL,
                                      command=self._cambiar_volumen,
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['text'],
                                      troughcolor=self.colors['bg_dark'],
                                      highlightthickness=0,
                                      length=200)
        self.volume_slider.set(70)
        self.volume_slider.pack(side=tk.LEFT)

        # Botones extras
        extras_frame = tk.Frame(center_panel, bg=self.colors['bg_medium'])
        extras_frame.pack(pady=10)

        self.btn_shuffle = tk.Button(extras_frame, text="🔀 Shuffle",
                                     command=self._toggle_shuffle,
                                     bg=self.colors['bg_light'],
                                     fg=self.colors['text'],
                                     font=('Arial', 10, 'bold'),
                                     relief=tk.FLAT,
                                     cursor='hand2',
                                     padx=15, pady=8)
        self.btn_shuffle.pack(side=tk.LEFT, padx=5)

        self.btn_favorita = tk.Button(extras_frame, text="☆ Favorita",
                                      command=self._toggle_favorita,
                                      bg=self.colors['bg_light'],
                                      fg=self.colors['text'],
                                      font=('Arial', 10, 'bold'),
                                      relief=tk.FLAT,
                                      cursor='hand2',
                                      padx=15, pady=8)
        self.btn_favorita.pack(side=tk.LEFT, padx=5)

        # ➕ Agregar a lista (AHORA en extras_frame, junto a Favorita y Shuffle)
        btn_agregar_lista = tk.Button(extras_frame,
                                      text="➕ Agregar a Lista",
                                      font=("Segoe UI", 10, "bold"),
                                      bg="#394b61",
                                      fg="white",
                                      activebackground="#4f688f",
                                      relief="flat",
                                      command=self._agregar_a_lista)
        btn_agregar_lista.pack(side=tk.LEFT, padx=5)

        # Cola de reproducción
        tk.Label(center_panel, text="📋 Cola de Reproducción",
                 font=('Arial', 12, 'bold'),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text']).pack(pady=(10, 5))

        self.lista_actual = tk.Listbox(center_panel,
                                       bg=self.colors['bg_dark'],
                                       fg=self.colors['text'],
                                       font=('Courier', 9),
                                       selectmode=tk.SINGLE,
                                       borderwidth=0,
                                       highlightthickness=0,
                                       selectbackground=self.colors['accent'],
                                       height=8)
        self.lista_actual.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.lista_actual.bind('<Double-Button-1>', self._reproducir_desde_cola)

    def _crear_panel_derecho(self, parent):
        """Panel derecho con opciones"""
        right_panel = tk.Frame(parent, bg=self.colors['bg_medium'], width=250)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(5, 0))

        tk.Label(right_panel, text="⚙️ OPCIONES",
                 font=('Arial', 14, 'bold'),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text']).pack(pady=10)

        btn_style = {
            'font': ('Arial', 10, 'bold'),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'width': 20,
            'pady': 10
        }

        tk.Button(right_panel, text="🔍 Buscar Canciones",
                  command=self._buscar,
                  bg=self.colors['success'], fg='white',
                  **btn_style).pack(pady=5, padx=10)

        tk.Button(right_panel, text="📊 Ver Estadísticas",
                  command=self._mostrar_estadisticas,
                  bg=self.colors['accent'], fg='white',
                  **btn_style).pack(pady=5, padx=10)

        tk.Button(right_panel, text="⭐ Ver Favoritas",
                  command=self._ver_favoritas,
                  bg=self.colors['warning'], fg='white',
                  **btn_style).pack(pady=5, padx=10)

        tk.Button(right_panel, text="📥 Importar CSV",
                  command=self._importar_csv,
                  bg=self.colors['bg_light'], fg='white',
                  **btn_style).pack(pady=5, padx=10)

        tk.Button(right_panel, text="💾 Exportar JSON",
                  command=self._exportar_json,
                  bg=self.colors['bg_light'], fg='white',
                  **btn_style).pack(pady=5, padx=10)

        tk.Button(right_panel, text="📂 Importar JSON",
                  command=self._importar_json,
                  bg=self.colors['bg_light'], fg='white',
                  **btn_style).pack(pady=5, padx=10)

        # Info lista actual
        tk.Label(right_panel, text="📋 Lista Actual",
                 font=('Arial', 11, 'bold'),
                 bg=self.colors['bg_medium'],
                 fg=self.colors['text']).pack(pady=(20, 5))

        self.lbl_lista_actual = tk.Label(right_panel, text="Ninguna",
                                         font=('Arial', 10),
                                         bg=self.colors['bg_dark'],
                                         fg=self.colors['success'],
                                         wraplength=200)
        self.lbl_lista_actual.pack(pady=5, padx=10, fill=tk.X)

        self.lbl_shuffle = tk.Label(right_panel, text="🔀 Shuffle: OFF",
                                    font=('Arial', 9),
                                    bg=self.colors['bg_medium'],
                                    fg=self.colors['text_secondary'])
        self.lbl_shuffle.pack(pady=2)

        # Info adicional
        info_text = scrolledtext.ScrolledText(right_panel,
                                              height=8,
                                              bg=self.colors['bg_dark'],
                                              fg=self.colors['text'],
                                              font=('Courier', 8),
                                              borderwidth=0,
                                              wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        biblioteca = self.reproductor.biblioteca
        total_repr = sum(c.reproducciones for c in biblioteca.canciones)
        info = f"""
🎵 Biblioteca:
   • {len(biblioteca.canciones)} canciones
   • {len(biblioteca.listas)} listas

⭐ Favoritas: {len(biblioteca.obtener_favoritas())}

📊 Total reproducciones: {total_repr}

💡 Tip: Haz doble clic en una 
   canción para reproducirla
        """
        info_text.insert('1.0', info)
        info_text.config(state=tk.DISABLED)

    # ==================== MÉTODOS DE CONTROL ====================

    def _toggle_play(self):
        """Play/Pause - CORREGIDO"""
        # Si está reproduciendo, pausar
        if self.reproductor.reproduciendo:
            self.reproductor.pause()
            self.btn_play.config(text="▶")
            self.lbl_estado.config(text="⏸ Pausado", fg=self.colors['warning'])
        # Si está pausado o detenido, reproducir/reanudar
        else:
            # Si hay canción seleccionada, reproducir
            if self.reproductor.cancion_actual:
                self.reproductor.play()
                self.btn_play.config(text="⏸")
                self.lbl_estado.config(text="▶ Reproduciendo", fg=self.colors['success'])
            else:
                messagebox.showwarning("Advertencia", "Selecciona una canción primero")
        self._actualizar_info()

    def _stop(self):
        """Stop"""
        self.reproductor.stop()
        self.btn_play.config(text="▶")
        self.lbl_estado.config(text="⏹ Detenido", fg=self.colors['accent'])
        self._actualizar_info()

    def _siguiente(self):
        """Siguiente"""
        self.reproductor.siguiente()
        self._actualizar_info()
        self._actualizar_lista_actual()

    def _anterior(self):
        """Anterior"""
        self.reproductor.anterior()
        self._actualizar_info()
        self._actualizar_lista_actual()

    def _cambiar_volumen(self, valor):
        """Cambiar volumen"""
        self.reproductor.ajustar_volumen(int(valor) / 100)

    def _toggle_shuffle(self):
        """Toggle shuffle"""
        if self.reproductor.lista_actual:
            if self.reproductor.lista_actual.shuffle_activo:
                self.reproductor.desactivar_shuffle()
                self.btn_shuffle.config(bg=self.colors['bg_light'])
                self.lbl_shuffle.config(text="🔀 Shuffle: OFF")
            else:
                self.reproductor.activar_shuffle()
                self.btn_shuffle.config(bg=self.colors['success'])
                self.lbl_shuffle.config(text="🔀 Shuffle: ON", fg=self.colors['success'])
            self._actualizar_lista_actual()
        else:
            messagebox.showwarning("Advertencia", "No hay lista activa")

    def _toggle_favorita(self):
        """Toggle favorita"""
        if self.reproductor.cancion_actual:
            self.reproductor.cancion_actual.marcar_favorita()
            self._actualizar_info()
            self._actualizar_canciones()
            if self.reproductor.cancion_actual.es_favorita:
                self.btn_favorita.config(text="★ Favorita", bg=self.colors['warning'])
            else:
                self.btn_favorita.config(text="☆ Favorita", bg=self.colors['bg_light'])
        else:
            messagebox.showwarning("Advertencia", "No hay canción seleccionada")

    # ==================== ACTUALIZACIÓN ====================

    def _actualizar_info(self):
        """Actualiza info mostrada"""
        if self.reproductor.cancion_actual:
            cancion = self.reproductor.cancion_actual
            self.lbl_cancion.config(text=f"♪ {cancion.titulo}")
            self.lbl_artista.config(text=cancion.artista)
            self.lbl_duracion.config(text=cancion.get_duracion_formateada())

            if cancion.es_favorita:
                self.btn_favorita.config(text="★ Favorita", bg=self.colors['warning'])
            else:
                self.btn_favorita.config(text="☆ Favorita", bg=self.colors['bg_light'])

        if self.reproductor.lista_actual:
            nombre = self.reproductor.lista_actual.nombre
            total = self.reproductor.lista_actual.obtener_total_canciones()
            self.lbl_lista_actual.config(text=f"{nombre}\n({total} canciones)")

            if self.reproductor.lista_actual.shuffle_activo:
                self.lbl_shuffle.config(text="🔀 Shuffle: ON", fg=self.colors['success'])
                self.btn_shuffle.config(bg=self.colors['success'])
            else:
                self.lbl_shuffle.config(text="🔀 Shuffle: OFF", fg=self.colors['text_secondary'])
                self.btn_shuffle.config(bg=self.colors['bg_light'])
        else:
            self.lbl_lista_actual.config(text="Ninguna\n(0 canciones)")
            self.lbl_shuffle.config(text="🔀 Shuffle: OFF", fg=self.colors['text_secondary'])

    def _actualizar_canciones(self):
        """Actualiza lista de canciones"""
        self.lista_canciones.delete(0, tk.END)
        for i, cancion in enumerate(self.reproductor.biblioteca.canciones, 1):
            fav = "★ " if cancion.es_favorita else ""
            texto = f"{i}. {fav}{cancion.titulo} - {cancion.artista}"
            self.lista_canciones.insert(tk.END, texto)

    def _actualizar_listas(self):
        """Actualiza lista de listas"""
        self.lista_listas.delete(0, tk.END)
        for nombre, lista in self.reproductor.biblioteca.listas.items():
            shuffle = "🔀 " if lista.shuffle_activo else ""
            texto = f"{shuffle}{nombre} ({lista.obtener_total_canciones()})"
            self.lista_listas.insert(tk.END, texto)

    def _actualizar_lista_actual(self):
        """Actualiza cola"""
        self.lista_actual.delete(0, tk.END)
        if self.reproductor.lista_actual and len(self.reproductor.lista_actual.canciones) > 0:
            for i, cancion in enumerate(self.reproductor.lista_actual.canciones):
                marcador = "▶ " if i == self.reproductor.lista_actual.indice_actual else "  "
                fav = "★ " if cancion.es_favorita else ""
                texto = f"{marcador}{fav}{cancion.titulo} - {cancion.artista}"
                self.lista_actual.insert(tk.END, texto)

                if i == self.reproductor.lista_actual.indice_actual:
                    self.lista_actual.itemconfig(i, bg=self.colors['accent'])
        else:
            self.lista_actual.insert(tk.END, "  [Lista vacía]")
            self.lista_actual.insert(tk.END, "  ")
            self.lista_actual.insert(tk.END, "  💡 Carga una lista con canciones")
            self.lista_actual.insert(tk.END, "     o reproduce desde la biblioteca")

    # ==================== EVENTOS ====================

    def _reproducir_desde_biblioteca(self, event):
        """Reproduce desde biblioteca - VERSIÓN CORREGIDA"""
        seleccion = self.lista_canciones.curselection()
        if not seleccion:
            return

        indice = seleccion[0]

        # Si no hay lista actual o está vacía, crear una temporal con todas las canciones
        if not self.reproductor.lista_actual or self.reproductor.lista_actual.obtener_total_canciones() == 0:
            # Buscar si existe lista temporal
            temp_lista = self.reproductor.biblioteca.obtener_lista("🎵 Reproducción Rápida")

            # Si no existe, crearla
            if not temp_lista:
                temp_lista = self.reproductor.biblioteca.crear_lista("🎵 Reproducción Rápida")
            else:
                # Limpiar la lista existente
                temp_lista.canciones.clear()

            # Agregar todas las canciones de la biblioteca
            if temp_lista:
                for cancion in self.reproductor.biblioteca.canciones:
                    temp_lista.agregar_cancion(cancion)

                # Cambiar a esta lista
                self.reproductor.cambiar_lista("🎵 Reproducción Rápida")
                self._actualizar_listas()

        # Ahora reproducir la canción seleccionada
        if self.reproductor.lista_actual and self.reproductor.lista_actual.obtener_total_canciones() > 0:
            # índice corresponde a la posición en la biblioteca; si la lista actual fue creada
            # con todas las canciones en el mismo orden, el índice es válido.
            self.reproductor.lista_actual.indice_actual = indice
            self.reproductor.cancion_actual = self.reproductor.lista_actual.obtener_cancion_actual()
            self.reproductor.play()
            self.btn_play.config(text="⏸")
            self.lbl_estado.config(text="▶ Reproduciendo", fg=self.colors['success'])
            self._actualizar_info()
            self._actualizar_lista_actual()

    def _cargar_lista(self, event):
        """Carga lista"""
        seleccion = self.lista_listas.curselection()
        if seleccion:
            indice = seleccion[0]
            nombres = list(self.reproductor.biblioteca.listas.keys())
            if indice < len(nombres):
                nombre = nombres[indice]
                lista = self.reproductor.biblioteca.obtener_lista(nombre)

                # Verificar si la lista tiene canciones
                if lista and lista.obtener_total_canciones() > 0:
                    self.reproductor.cambiar_lista(nombre)
                    self._actualizar_info()
                    self._actualizar_lista_actual()
                    messagebox.showinfo("Éxito",
                                        f"Lista '{nombre}' cargada con {lista.obtener_total_canciones()} canciones")
                else:
                    respuesta = messagebox.askyesno(
                        "Lista Vacía",
                        f"La lista '{nombre}' está vacía.\n\n¿Deseas cargarla de todas formas?\n\n" +
                        "Puedes agregar canciones haciendo doble clic en una canción de la biblioteca " +
                        "y seleccionando 'Agregar a lista'."
                    )
                    if respuesta:
                        self.reproductor.cambiar_lista(nombre)
                        self._actualizar_info()
                        self._actualizar_lista_actual()

    def _reproducir_desde_cola(self, event):
        """Reproduce desde cola"""
        seleccion = self.lista_actual.curselection()
        if seleccion and self.reproductor.lista_actual:
            if self.reproductor.lista_actual.obtener_total_canciones() > 0:
                indice = seleccion[0]
                if indice < self.reproductor.lista_actual.obtener_total_canciones():
                    self.reproductor.reproducir_cancion_especifica(indice)
                    self.btn_play.config(text="⏸")
                    self.lbl_estado.config(text="▶ Reproduciendo", fg=self.colors['success'])
                    self._actualizar_info()
                    self._actualizar_lista_actual()

    # ==================== DIÁLOGOS ====================

    def _crear_lista(self):
        """Crea lista"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Nueva Lista")
        ventana.geometry("400x150")
        ventana.configure(bg=self.colors['bg_dark'])
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text="Nombre de la lista:",
                 font=('Arial', 11),
                 bg=self.colors['bg_dark'],
                 fg=self.colors['text']).pack(pady=10)

        entrada = tk.Entry(ventana, font=('Arial', 11), width=30)
        entrada.pack(pady=5)
        entrada.focus()

        def crear():
            nombre = entrada.get().strip()
            if nombre:
                self.reproductor.biblioteca.crear_lista(nombre)
                self._actualizar_listas()
                ventana.destroy()
                messagebox.showinfo("Éxito",
                                    f"Lista '{nombre}' creada.\n\nAgrega canciones haciendo doble clic en ellas desde la biblioteca.")

        tk.Button(ventana, text="Crear",
                  command=crear,
                  bg=self.colors['success'], fg='white',
                  font=('Arial', 10, 'bold'),
                  relief=tk.FLAT, cursor='hand2',
                  padx=20, pady=8).pack(pady=10)

        entrada.bind('<Return>', lambda e: crear())

    def _eliminar_lista(self):
        """Elimina lista"""
        seleccion = self.lista_listas.curselection()
        if seleccion:
            indice = seleccion[0]
            nombres = list(self.reproductor.biblioteca.listas.keys())
            if indice < len(nombres):
                nombre = nombres[indice]
                if messagebox.askyesno("Confirmar", f"¿Eliminar lista '{nombre}'?"):
                    self.reproductor.biblioteca.eliminar_lista(nombre)
                    self._actualizar_listas()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una lista")

    def _agregar_a_lista(self):
        """Agrega una canción seleccionada a una lista existente"""
        # Verificar si hay una canción seleccionada en la biblioteca
        seleccion = self.lista_canciones.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una canción de la biblioteca primero.")
            return

        indice_cancion = seleccion[0]

        # Asegurarse de que el índice esté en rango
        if indice_cancion < 0 or indice_cancion >= len(self.reproductor.biblioteca.canciones):
            messagebox.showerror("Error", "Índice de canción inválido.")
            return

        cancion = self.reproductor.biblioteca.canciones[indice_cancion]

        # Verificar si hay listas disponibles
        listas = list(self.reproductor.biblioteca.listas.keys())
        if not listas:
            messagebox.showwarning("Sin Listas", "Primero crea una lista antes de agregar canciones.")
            return

        # Crear ventana para seleccionar a qué lista agregar
        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar a Lista")
        ventana.geometry("350x250")
        ventana.configure(bg=self.colors['bg_dark'])
        ventana.transient(self.root)
        ventana.grab_set()

        tk.Label(ventana, text=f"Agregar '{cancion.titulo}' a:",
                 font=('Arial', 11, 'bold'),
                 bg=self.colors['bg_dark'], fg=self.colors['text']).pack(pady=10)

        lista_box = tk.Listbox(ventana,
                               bg=self.colors['bg_light'],
                               fg=self.colors['text'],
                               font=('Arial', 10),
                               selectmode=tk.SINGLE,
                               borderwidth=0,
                               highlightthickness=0,
                               selectbackground=self.colors['accent'])
        lista_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for nombre in listas:
            lista_box.insert(tk.END, nombre)

        def agregar():
            seleccion_lista = lista_box.curselection()
            if not seleccion_lista:
                messagebox.showwarning("Advertencia", "Selecciona una lista.")
                return

            nombre_lista = listas[seleccion_lista[0]]
            lista = self.reproductor.biblioteca.obtener_lista(nombre_lista)

            if lista:
                lista.agregar_cancion(cancion)
                ventana.destroy()
                self._actualizar_listas()
                messagebox.showinfo("Éxito",
                                    f"La canción '{cancion.titulo}' fue agregada a la lista '{nombre_lista}'.")
            else:
                messagebox.showerror("Error", f"No se encontró la lista '{nombre_lista}'.")

        tk.Button(ventana, text="Agregar",
                  command=agregar,
                  bg=self.colors['success'], fg='white',
                  font=('Arial', 10, 'bold'),
                  relief=tk.FLAT, cursor='hand2',
                  padx=20, pady=8).pack(pady=5)

        tk.Button(ventana, text="Cancelar",
                  command=ventana.destroy,
                  bg=self.colors['accent'], fg='white',
                  font=('Arial', 10, 'bold'),
                  relief=tk.FLAT, cursor='hand2',
                  padx=20, pady=8).pack(pady=5)

    def _buscar(self):
        """Buscar"""
        ventana = tk.Toplevel(self.root)
        ventana.title("🔍 Buscar Canciones")
        ventana.geometry("500x400")
        ventana.configure(bg=self.colors['bg_dark'])

        frame = tk.Frame(ventana, bg=self.colors['bg_dark'])
        frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Label(frame, text="Buscar por:",
                 font=('Arial', 10),
                 bg=self.colors['bg_dark'],
                 fg=self.colors['text']).pack(side=tk.LEFT, padx=5)

        tipo = tk.StringVar(value="titulo")
        tk.Radiobutton(frame, text="Título", variable=tipo,
                       value="titulo", bg=self.colors['bg_dark'],
                       fg=self.colors['text'], selectcolor=self.colors['bg_light']).pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Artista", variable=tipo,
                       value="artista", bg=self.colors['bg_dark'],
                       fg=self.colors['text'], selectcolor=self.colors['bg_light']).pack(side=tk.LEFT)

        entrada = tk.Entry(frame, font=('Arial', 10), width=25)
        entrada.pack(side=tk.LEFT, padx=5)

        resultados = tk.Listbox(ventana, bg=self.colors['bg_light'],
                                fg=self.colors['text'],
                                font=('Courier', 9))
        resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        def buscar():
            resultados.delete(0, tk.END)
            valor = entrada.get().strip()
            if valor:
                if tipo.get() == "titulo":
                    encontradas = self.reproductor.biblioteca.buscar_por_titulo(valor)
                else:
                    encontradas = self.reproductor.biblioteca.buscar_por_artista(valor)

                for cancion in encontradas:
                    resultados.insert(tk.END, str(cancion))

                if not encontradas:
                    resultados.insert(tk.END, "No se encontraron resultados")

        tk.Button(frame, text="Buscar",
                  command=buscar,
                  bg=self.colors['success'], fg='white',
                  font=('Arial', 9, 'bold'),
                  relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        entrada.bind('<Return>', lambda e: buscar())

    def _mostrar_estadisticas(self):
        """Estadísticas"""
        ventana = tk.Toplevel(self.root)
        ventana.title("📊 Estadísticas")
        ventana.geometry("600x500")
        ventana.configure(bg=self.colors['bg_dark'])

        texto = scrolledtext.ScrolledText(ventana,
                                          bg=self.colors['bg_light'],
                                          fg=self.colors['text'],
                                          font=('Courier', 10),
                                          borderwidth=0,
                                          wrap=tk.WORD)
        texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        biblioteca = self.reproductor.biblioteca

        stats = "=" * 60 + "\n"
        stats += "   📊 ESTADÍSTICAS DE LA BIBLIOTECA\n"
        stats += "=" * 60 + "\n\n"
        stats += f"📚 Total de canciones: {len(biblioteca.canciones)}\n"
        stats += f"📋 Total de listas: {len(biblioteca.listas)}\n"
        stats += f"⭐ Canciones favoritas: {len(biblioteca.obtener_favoritas())}\n\n"

        duracion_total = sum(c.duracion_segundos for c in biblioteca.canciones)
        horas = duracion_total // 3600
        minutos = (duracion_total % 3600) // 60
        stats += f"⏱️ Duración total: {horas}h {minutos}m\n\n"

        total_repr = sum(c.reproducciones for c in biblioteca.canciones)
        stats += f"🎵 Total reproducciones: {total_repr}\n\n"

        stats += "-" * 60 + "\n"
        stats += "🏆 Top 10 Canciones Más Reproducidas\n"
        stats += "-" * 60 + "\n"

        top = biblioteca.obtener_top_canciones(10)
        if top and top[0].reproducciones > 0:
            for i, cancion in enumerate(top, 1):
                if cancion.reproducciones > 0:
                    fav = "★ " if cancion.es_favorita else ""
                    stats += f"{i:2d}. {fav}{cancion.titulo} - {cancion.artista}\n"
                    stats += f"    ({cancion.reproducciones} repr.)\n"
        else:
            stats += "No hay canciones reproducidas aún\n"

        stats += "\n" + "=" * 60 + "\n"

        texto.insert('1.0', stats)
        texto.config(state=tk.DISABLED)

    def _ver_favoritas(self):
        """Ver favoritas"""
        ventana = tk.Toplevel(self.root)
        ventana.title("⭐ Canciones Favoritas")
        ventana.geometry("500x400")
        ventana.configure(bg=self.colors['bg_dark'])

        tk.Label(ventana, text="⭐ MIS FAVORITAS",
                 font=('Arial', 14, 'bold'),
                 bg=self.colors['bg_dark'],
                 fg=self.colors['warning']).pack(pady=10)

        favoritas = self.reproductor.biblioteca.obtener_favoritas()

        lista = tk.Listbox(ventana, bg=self.colors['bg_light'],
                           fg=self.colors['text'],
                           font=('Courier', 10))
        lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        if favoritas:
            for cancion in favoritas:
                lista.insert(tk.END, f"★ {cancion}")
        else:
            lista.insert(tk.END, "No tienes canciones favoritas")
            lista.insert(tk.END, "Marca canciones como favoritas desde el reproductor")

        if favoritas:
            btn_frame = tk.Frame(ventana, bg=self.colors['bg_dark'])
            btn_frame.pack(pady=10)

            def crear_lista_favoritas():
                nombre = f"Favoritas {len(self.reproductor.biblioteca.listas) + 1}"
                nueva_lista = self.reproductor.biblioteca.crear_lista(nombre)
                if nueva_lista:
                    for cancion in favoritas:
                        nueva_lista.agregar_cancion(cancion)
                    self._actualizar_listas()
                    ventana.destroy()
                    messagebox.showinfo("Éxito", f"Lista '{nombre}' creada con {len(favoritas)} favoritas")

            tk.Button(btn_frame, text="Crear Lista con Favoritas",
                      command=crear_lista_favoritas,
                      bg=self.colors['success'], fg='white',
                      font=('Arial', 10, 'bold'),
                      relief=tk.FLAT, cursor='hand2',
                      padx=20, pady=8).pack()

    def _importar_csv(self):
        """Importar CSV"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )

        if archivo:
            self.reproductor.biblioteca.importar_desde_csv(archivo)
            self._actualizar_canciones()
            self._actualizar_listas()
            messagebox.showinfo("Éxito", "Canciones importadas correctamente")

    def _exportar_json(self):
        """Exportar JSON"""
        archivo = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if archivo:
            self.reproductor.biblioteca.exportar_listas_json(archivo)
            messagebox.showinfo("Éxito", f"Listas exportadas a:\n{archivo}")

    def _importar_json(self):
        """Importar JSON"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo JSON",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )

        if archivo:
            self.reproductor.biblioteca.importar_listas_json(archivo)
            self._actualizar_canciones()
            self._actualizar_listas()
            messagebox.showinfo("Éxito", "Listas importadas correctamente")

    def ejecutar(self):
        """Ejecutar GUI"""
        self._actualizar_canciones()
        self._actualizar_listas()
        self._actualizar_lista_actual()

        # Centrar ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.root.mainloop()


def iniciar_gui(reproductor: Reproductor):
    """Inicia la interfaz gráfica"""
    app = ReproductorGUI(reproductor)
    app.ejecutar()


if __name__ == "__main__":
    from biblioteca import Biblioteca
    from cancion import Cancion

    biblioteca = Biblioteca()

    canciones = [
        Cancion("Bohemian Rhapsody", "Queen", 355, "music/lovetheway.mp3",
                "A Night at the Opera", 1975, "Rock"),
        Cancion("Imagine", "John Lennon", 183, "music/lennon.mp3",
                "Imagine", 1971, "Rock"),
        Cancion("Billie Jean", "Michael Jackson", 294, "music/mj.mp3",
                "Thriller", 1982, "Pop"),
    ]

    for cancion in canciones:
        biblioteca.agregar_cancion(cancion)

    lista = biblioteca.crear_lista("Test")
    for cancion in canciones:
        lista.agregar_cancion(cancion)

    reproductor = Reproductor(biblioteca)
    reproductor.cambiar_lista("Test")

    iniciar_gui(reproductor)
