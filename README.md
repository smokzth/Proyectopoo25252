# 🎵 Reproductor de Música - POO

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Diagrama de Clases](#-diagrama-de-clases)
- [Requisitos Funcionales](#-requisitos-funcionales)

---

## 📖 Descripción

Reproductor de música interactivo que permite a los usuarios gestionar sus gustos musicales, crear listas de reproducción personalizadas, y controlar la reproducción con una interfaz de consola.

### Problemática

Los usuarios necesitan una herramienta que les permita:
- 📚 Organizar colecciones de música
- 🎵 Crear listas de reproducción 
- ⚡ Acceder rápidamente a sus canciones
- 🔍 Buscar canciones por título o artista
- 📊 Obtener estadísticas de reproducción

### Solución

Sistema de gestión musical con arquitectura orientada a objetos:
- ✅ Gestión de la biblioteca
- ✅ Listas de reproducción ilimitadas
- ✅ Navegación entre canciones
- ✅ Controles de reproducción completos

---

## ✨ Características

### Implementadas en MVP 

#### 📚 Gestión de Biblioteca
- Agregar canciones con (título, artista, álbum, año, género)
- Eliminar canciones del catálogo
- Listar todas las canciones con formato legible
#### 🎵 Listas de Reproducción
- Crear múltiples listas personalizadas
- Agregar/eliminar canciones de listas
- Ver contenido detallado de cada lista
- Cálculo automático de duración total

#### ▶ Controles de Reproducción
- *Play*: Inicia o reanuda reproducción
- *Pause*: Pausa la canción actual
- *Siguiente*: Avanza (navegación circular)
- *Anterior*: Retrocede (navegación circular)

#### 🔍 Búsqueda Inteligente
- Búsqueda por título 
- Búsqueda por artista 

#### 📊 Estadísticas
- Total de canciones en biblioteca
- Total de listas creadas
- Duración acumulada de toda la música
- Información detallada por canción

---

## 🎵 Diagrama de Clases

```mermaid
classDiagram
    class Cancion {
        -titulo: str
        -artista: str
        -duracion_segundos: int
        -ruta_archivo: str
        -album: str
        -año: int
        -genero: str
        -reproducciones: int
        -es_favorita: bool
        +__init__(titulo: str, artista: str, duracion: int, ruta: str)
        +info() str
        +incrementar_reproducciones() None
        +marcar_favorita() None
        +get_duracion_formateada() str
        +to_dict() dict
    }

    class ListaDeReproduccion {
        -nombre: str
        -canciones: list[Cancion]
        -indice_actual: int
        -orden_original: list[Cancion]
        -shuffle_activo: bool
        +__init__(nombre: str)
        +agregar_cancion(cancion: Cancion) None
        +eliminar_cancion(indice: int) None
        +obtener_cancion_actual() Cancion | None
        +siguiente() Cancion | None
        +anterior() Cancion | None
        +listar_canciones() str
        +shuffle() None
        +restaurar_orden() None
        +to_dict() dict
    }

    class Biblioteca {
        -canciones: list[Cancion]
        -listas: dict[str, ListaDeReproduccion]
        +__init__()
        +agregar_cancion(cancion: Cancion) None
        +eliminar_cancion(indice: int) None
        +buscar_por_titulo(titulo: str) list[Cancion]
        +buscar_por_artista(artista: str) list[Cancion]
        +crear_lista(nombre: str) ListaDeReproduccion | None
        +obtener_favoritas() list[Cancion]
        +obtener_top_canciones(n: int) list[Cancion]
        +mostrar_estadisticas() None
        +importar_desde_csv(ruta: str) None
        +exportar_listas_json(ruta: str) None
        +importar_listas_json(ruta: str) None
    }

    class Reproductor {
        -biblioteca: Biblioteca
        -lista_actual: ListaDeReproduccion | None
        -cancion_actual: Cancion | None
        -reproduciendo: bool
        -volumen: float
        -modo_audio_real: bool
        +__init__(biblioteca: Biblioteca)
        +play() None
        +pause() None
        +unpause() None
        +stop() None
        +siguiente() None
        +anterior() None
        +cambiar_lista(nombre_lista: str) None
        +activar_shuffle() None
        +desactivar_shuffle() None
        +ajustar_volumen(nivel: float) None
        +seek(posicion_segundos: float) None
        +get_posicion_actual() float
    }

    class InterfazConsola {
        -reproductor: Reproductor
        +__init__(reproductor: Reproductor)
        +mostrar_menu_principal() None
        +mostrar_biblioteca() None
        +gestionar_listas() None
        +controles_reproductor() None
        +buscar_canciones() None
        +menu_favoritos() None
        +menu_importar_exportar() None
        +ejecutar() None
    }

    class ReproductorGUI {
        -reproductor: Reproductor
        -root: tk.Tk
        -colors: dict
        -lista_canciones: tk.Listbox
        -lista_listas: tk.Listbox
        -lista_actual: tk.Listbox
        -btn_play: tk.Button
        -progress_slider: tk.Scale
        -volume_slider: tk.Scale
        +__init__(reproductor: Reproductor)
        +_crear_interfaz() None
        +_crear_panel_izquierdo() None
        +_crear_panel_central() None
        +_crear_panel_derecho() None
        +_toggle_play() None
        +_siguiente() None
        +_anterior() None
        +_toggle_shuffle() None
        +_toggle_favorita() None
        +_actualizar_progreso() None
        +_seek_musica(valor) None
        +_importar_csv() None
        +_exportar_json() None
        +ejecutar() None
    }

    class GestorArchivos {
        +leer_csv(ruta: str) list
        +guardar_json(ruta: str, datos: dict) None
        +leer_json(ruta: str) dict
    }

    class ControlVolumen {
        -nivel: float
        +__init__(nivel_inicial: float)
        +aumentar(delta: float) float
        +disminuir(delta: float) float
        +establecer(nivel: float) float
    }

    class ExcepcionReproductor {
        +__init__(mensaje: str)
        +__str__() str
    }

    Biblioteca "1" *-- "*" Cancion : contiene
    Biblioteca "1" *-- "*" ListaDeReproduccion : gestiona
    ListaDeReproduccion "1" o-- "*" Cancion : referencia
    Reproductor "1" --> "1" Biblioteca : usa
    Reproductor "1" --> "0..1" ListaDeReproduccion : reproduce
    Reproductor "1" --> "0..1" Cancion : actual
    Reproductor "1" *-- "1" ControlVolumen : controla
    InterfazConsola "1" --> "1" Reproductor : controla
    ReproductorGUI "1" --> "1" Reproductor : controla
    Biblioteca "1" --> "1" GestorArchivos : usa
    Reproductor "1" --> "0..*" ExcepcionReproductor : lanza

```

### Descripción de Clases

#### 🎼 Cancion
Representa una canción individual con todos sus metadatos.
- *Responsabilidad*: Almacenar y gestionar información de una canción
- *Métodos principales*: info(), incrementar_reproducciones(), get_duracion_formateada()

#### 📋 ListaDeReproduccion
Gestiona una colección ordenada de canciones.
- *Responsabilidad*: Mantener lista de canciones y controlar navegación
- *Métodos principales*: siguiente(), anterior(), agregar_cancion(), eliminar_cancion()

#### 📚 Biblioteca
Catálogo central de toda la música y listas.
- *Responsabilidad*: Gestionar todas las canciones y listas de reproducción
- *Métodos principales*: crear_lista(), buscar_por_titulo(), buscar_por_artista()

#### 🎮 Reproductor
Controlador principal de reproducción.
- *Responsabilidad*: Gestionar estado de reproducción y controles
- *Métodos principales*: play(), pause(), stop(), siguiente(), anterior()

#### 💻 InterfazConsola
Interfaz de usuario en modo consola.
- *Responsabilidad*: Interacción con el usuario mediante menús
- *Métodos principales*: ejecutar(), mostrar_menu_principal(), gestionar_listas()

---




## 📋 Requisitos Funcionales

### ✅ Implementados (Primera entrega)

#### RF1: Gestionar Biblioteca Musical
- *Descripción*: Agregar, eliminar y listar canciones
- *Archivos*: biblioteca.py, cancion.py
- *Estado*: ✅ Completado

#### RF2: Reproducir Canción Actual
- *Descripción*: Simular reproducción con controles play/pause/stop
- *Archivos*: reproductor.py, cancion.py
- *Estado*: ✅ Completado

#### RF3: Navegar entre Canciones
- *Descripción*: Siguiente/Anterior con navegación circular
- *Archivos*: reproductor.py, lista_reproduccion.py
- *Estado*: ✅ Completado

#### RF4: Gestionar Listas de Reproducción
- *Descripción*: Crear, eliminar y modificar listas
- *Archivos*: biblioteca.py, lista_reproduccion.py
- *Estado*: ✅ Completado

#### RF5: Mostrar Información Detallada
- *Descripción*: Información completa de canciones
- *Archivos*: cancion.py, interfaz.py
- *Estado*: ✅ Completado

### 🔜 Planificados (Entrega final)

#### RF6: Modo Aleatorio
- Reproducción aleatoria de canciones
- Librería: random

#### RF7: Sistema de Favoritos y Estadísticas
- Marcar canciones favoritas

#### RF8: Importar desde CSV
- Carga masiva de canciones
- Librería: csv

#### RF9: Exportar a JSON
- Persistencia de listas
- Librería: json

#### RF10: Reproducción Real de Audio
- Reproducción de archivos MP3/WAV
- Librería: pygame