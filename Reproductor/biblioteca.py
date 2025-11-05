

from cancion import Cancion
from lista_reproduccion import ListaDeReproduccion
from typing import Optional
import csv
import json


class Biblioteca:


    def __init__(self):
        self.canciones: list[Cancion] = []
        self.listas: dict[str, ListaDeReproduccion] = {}

    def agregar_cancion(self, cancion: Cancion) -> None:
        """Agrega una canción a la biblioteca"""
        self.canciones.append(cancion)
        print(f"✓ '{cancion.titulo}' agregada a la biblioteca")

    def eliminar_cancion(self, indice: int) -> None:
        """Elimina una canción de la biblioteca"""
        if 0 <= indice < len(self.canciones):
            cancion = self.canciones.pop(indice)
            print(f"✓ '{cancion.titulo}' eliminada de la biblioteca")
        else:
            print("✗ Índice inválido")

    def buscar_por_titulo(self, titulo: str) -> list[Cancion]:
        """Busca canciones por título"""
        resultados = [c for c in self.canciones if titulo.lower() in c.titulo.lower()]
        return resultados

    def buscar_por_artista(self, artista: str) -> list[Cancion]:
        """Busca canciones por artista"""
        resultados = [c for c in self.canciones if artista.lower() in c.artista.lower()]
        return resultados

    def crear_lista(self, nombre: str) -> Optional[ListaDeReproduccion]:
        """Crea una nueva lista de reproducción"""
        if nombre not in self.listas:
            self.listas[nombre] = ListaDeReproduccion(nombre)
            print(f"✓ Lista '{nombre}' creada")
            return self.listas[nombre]
        else:
            print(f"✗ La lista '{nombre}' ya existe")
            return None

    def eliminar_lista(self, nombre: str) -> None:
        """Elimina una lista de reproducción"""
        if nombre in self.listas:
            del self.listas[nombre]
            print(f"✓ Lista '{nombre}' eliminada")
        else:
            print(f"✗ Lista '{nombre}' no existe")

    def obtener_lista(self, nombre: str) -> Optional[ListaDeReproduccion]:
        """Obtiene una lista de reproducción por nombre"""
        return self.listas.get(nombre)

    def obtener_todas_las_canciones(self) -> list[Cancion]:
        """Retorna todas las canciones de la biblioteca"""
        return self.canciones

    def obtener_top_canciones(self, n: int = 10) -> list[Cancion]:
        """RF7: Retorna las n canciones más reproducidas"""
        canciones_ordenadas = sorted(self.canciones,
                                     key=lambda c: c.reproducciones,
                                     reverse=True)
        return canciones_ordenadas[:n]

    def obtener_favoritas(self) -> list[Cancion]:
        """RF7: Retorna todas las canciones favoritas"""
        return [c for c in self.canciones if c.es_favorita]

    def mostrar_estadisticas(self) -> None:
        """RF7: Muestra estadísticas completas de la biblioteca"""
        print("\n" + "=" * 60)
        print("📊 ESTADÍSTICAS DE LA BIBLIOTECA".center(60))
        print("=" * 60)
        print(f"Total de canciones: {len(self.canciones)}")
        print(f"Total de listas: {len(self.listas)}")

        if self.canciones:
            duracion_total = sum(c.duracion_segundos for c in self.canciones)
            horas = duracion_total // 3600
            minutos = (duracion_total % 3600) // 60
            print(f"Duración total: {horas}h {minutos}m")

            total_reproducciones = sum(c.reproducciones for c in self.canciones)
            print(f"Reproducciones totales: {total_reproducciones}")

            favoritas = self.obtener_favoritas()
            print(f"Canciones favoritas: {len(favoritas)}")

            # Top 5 más reproducidas
            print(f"\n{'─' * 60}")
            print("🏆 Top 5 Canciones Más Reproducidas".center(60))
            print(f"{'─' * 60}")
            top = self.obtener_top_canciones(5)
            if top and top[0].reproducciones > 0:
                for i, cancion in enumerate(top, 1):
                    if cancion.reproducciones > 0:
                        print(f"{i}. {cancion.titulo} - {cancion.artista} ({cancion.reproducciones} repr.)")
            else:
                print("No hay canciones reproducidas aún")

            print("=" * 60)

    def importar_desde_csv(self, ruta: str) -> None:
        """RF8: Importa canciones desde un archivo CSV"""
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                contador = 0
                for fila in lector:
                    try:
                        cancion = Cancion(
                            titulo=fila['titulo'],
                            artista=fila['artista'],
                            duracion_segundos=int(fila['duracion']),
                            ruta_archivo=fila['ruta'],
                            album=fila.get('album', ''),
                            año=int(fila.get('año', 0)) if fila.get('año') else 0,
                            genero=fila.get('genero', '')
                        )
                        self.agregar_cancion(cancion)
                        contador += 1
                    except (KeyError, ValueError) as e:
                        print(f"⚠ Error en fila: {e}")
                        continue

                print(f"\n✓ Total importado: {contador} canciones desde '{ruta}'")
        except FileNotFoundError:
            print(f"✗ Archivo '{ruta}' no encontrado")
        except Exception as e:
            print(f"✗ Error al importar: {e}")

    def exportar_listas_json(self, ruta: str) -> None:
        """RF9: Exporta todas las listas a JSON"""
        try:
            datos = {
                "listas": [lista.to_dict() for lista in self.listas.values()],
                "total_listas": len(self.listas),
                "fecha_exportacion": self._obtener_fecha_actual()
            }
            with open(ruta, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            print(f"✓ {len(self.listas)} listas exportadas a '{ruta}'")
        except Exception as e:
            print(f"✗ Error al exportar: {e}")

    def importar_listas_json(self, ruta: str) -> None:
        """RF9: Importa listas desde un archivo JSON"""
        try:
            with open(ruta, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)

                for lista_data in datos.get('listas', []):
                    nombre = lista_data['nombre']
                    if nombre in self.listas:
                        print(f"⚠ Lista '{nombre}' ya existe, omitiendo...")
                        continue

                    nueva_lista = self.crear_lista(nombre)
                    if nueva_lista:
                        for cancion_data in lista_data['canciones']:
                            # Buscar si la canción ya existe en la biblioteca
                            cancion_existente = None
                            for c in self.canciones:
                                if c.titulo == cancion_data['titulo'] and c.artista == cancion_data['artista']:
                                    cancion_existente = c
                                    break

                            # Si no existe, crearla
                            if not cancion_existente:
                                cancion_existente = Cancion(
                                    titulo=cancion_data['titulo'],
                                    artista=cancion_data['artista'],
                                    duracion_segundos=cancion_data['duracion'],
                                    ruta_archivo=cancion_data['ruta'],
                                    album=cancion_data.get('album', ''),
                                    año=cancion_data.get('año', 0),
                                    genero=cancion_data.get('genero', '')
                                )
                                self.agregar_cancion(cancion_existente)

                            nueva_lista.agregar_cancion(cancion_existente)

                print(f"✓ Listas importadas desde '{ruta}'")
        except FileNotFoundError:
            print(f"✗ Archivo '{ruta}' no encontrado")
        except json.JSONDecodeError:
            print(f"✗ Error: El archivo no tiene un formato JSON válido")
        except Exception as e:
            print(f"✗ Error al importar: {e}")

    def _obtener_fecha_actual(self) -> str:
        """Obtiene la fecha actual en formato string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self) -> str:
        return f"Biblioteca ({len(self.canciones)} canciones, {len(self.listas)} listas)"