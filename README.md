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
- ✅ Búsqueda 
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
        +__init__(titulo: str, artista: str, duracion: int, ruta: str)
        +info() str
        +incrementar_reproducciones() None
        +get_duracion_formateada() str
    }

    class ListaDeReproduccion {
        -nombre: str
        -canciones: list[Cancion]
        -indice_actual: int
        -orden_original: list[Cancion]
        +__init__(nombre: str)
        +agregar_cancion(cancion: Cancion) None
        +eliminar_cancion(indice: int) None
        +obtener_cancion_actual() Cancion | None
        +siguiente() Cancion | None
        +anterior() Cancion | None
        +listar_canciones() str
        +obtener_total_canciones() int
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
        +eliminar_lista(nombre: str) None
        +obtener_lista(nombre: str) ListaDeReproduccion | None
        +mostrar_estadisticas() None
    }

    class Reproductor {
        -biblioteca: Biblioteca
        -lista_actual: ListaDeReproduccion | None
        -cancion_actual: Cancion | None
        -reproduciendo: bool
        -volumen: float
        +__init__(biblioteca: Biblioteca)
        +play() None
        +pause() None
        +stop() None
        +siguiente() None
        +anterior() None
        +cambiar_lista(nombre_lista: str) None
        +ajustar_volumen(nivel: float) None
        +obtener_estado() dict
    }

    class InterfazConsola {
        -reproductor: Reproductor
        +__init__(reproductor: Reproductor)
        +mostrar_menu_principal() None
        +mostrar_biblioteca() None
        +gestionar_listas() None
        +controles_reproductor() None
        +buscar_canciones() None
        +ejecutar() None
    }

    Biblioteca "1" *-- "*" Cancion : contiene
    Biblioteca "1" *-- "*" ListaDeReproduccion : gestiona
    ListaDeReproduccion "1" o-- "*" Cancion : referencia
    Reproductor "1" --> "1" Biblioteca : usa
    Reproductor "1" --> "0..1" ListaDeReproduccion : reproduce
    Reproductor "1" --> "0..1" Cancion : actual
    InterfazConsola "1" --> "1" Reproductor : controla



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