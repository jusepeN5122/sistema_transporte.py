import heapq
import math

# ==========================================
# 1. BASE DE CONOCIMIENTO (Hechos y Reglas)
# ==========================================

# Ubicación de las estaciones
ESTACIONES = {
    "Portal Norte": (10, 20),
    "Calle 170": (10, 18),
    "Calle 100": (10, 12),
    "Héroes": (10, 8),
    "Calle 72": (10, 6),
    "Calle 26": (10, 2),
    "Marly": (12, 5),
    "Suba Calle 100": (5, 12),
    "Portal Suba": (2, 16)
}

# Reglas de conexión
CONEXIONES = [
    ("Portal Norte", "Calle 170", 3, "Línea A"),
    ("Calle 170", "Calle 100", 6, "Línea A"),
    ("Calle 100", "Héroes", 5, "Línea A"),
    ("Héroes", "Calle 72", 3, "Línea A"),
    ("Calle 72", "Calle 26", 5, "Línea A"),
    ("Portal Suba", "Suba Calle 100", 8, "Línea B"),
    ("Suba Calle 100", "Calle 100", 4, "Línea B"),
    ("Calle 100", "Marly", 7, "Línea B"),
    ("Marly", "Calle 26", 4, "Línea B")
]

PENALIZACION_TRANSBORDO = 3  

# ==========================================
# 2. MOTOR DE INFERENCIA Y BÚSQUEDA HEURÍSTICA (A*)
# ==========================================

def construir_grafo():
    """Convierte la base de conocimiento en un grafo bidireccional."""
    grafo = {estacion: [] for estacion in ESTACIONES}
    for origen, destino, tiempo, linea in CONEXIONES:
        grafo[origen].append((destino, tiempo, linea))
        grafo[destino].append((origen, tiempo, linea))
    return grafo

def heuristica(estacion_actual, estacion_destino):
    """Estima la distancia restante usando la distancia Euclídea."""
    x1, y1 = ESTACIONES[estacion_actual]
    x2, y2 = ESTACIONES[estacion_destino]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def buscar_mejor_ruta(origen, destino):
    """Implementa el algoritmo A* para encontrar la ruta con menor tiempo."""
    if origen not in ESTACIONES or destino not in ESTACIONES:
        return None, "Una o ambas estaciones no existen en el sistema."

    grafo = construir_grafo()
    
    # Cola de prioridad: (f_score, g_score, estacion_actual, linea_actual, camino)
    cola_prioridad = [(0 + heuristica(origen, destino), 0, origen, None, [(origen, None)])]
    visitados = {}

    while cola_prioridad:
        f, g, actual, linea_actual, camino = heapq.heappop(cola_prioridad)

        if actual == destino:
            return camino, g

        estado = (actual, linea_actual)
        if estado in visitados and visitados[estado] <= g:
            continue
        visitados[estado] = g

        for vecino, tiempo_tramo, nueva_linea in grafo[actual]:
            costo_adicional = tiempo_tramo
            # Aplica regla de inferencia: si cambia de línea, añade penalización por transbordo
            if linea_actual is not None and linea_actual != nueva_linea:
                costo_adicional += PENALIZACION_TRANSBORDO

            nuevo_g = g + costo_adicional
            nuevo_h = heuristica(vecino, destino)
            nuevo_f = nuevo_g + nuevo_h
            nuevo_camino = camino + [(vecino, nueva_linea)]

            heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, vecino, nueva_linea, nuevo_camino))

    return None, "No se encontró una ruta disponible."

# ==========================================
# 3. INTERFAZ DE CONSOLA
# ==========================================

def ejecutar():
    print("==================================================")
    print("   SISTEMA INTELIGENTE DE RUTAS DE TRANSPORTE     ")
    print("==================================================")
    print("Estaciones disponibles:")
    for est in ESTACIONES.keys():
        print(f" - {est}")
    print("--------------------------------------------------")

    origen = input("\nIngrese la estación de ORIGEN: ").strip()
    destino = input("Ingrese la estación de DESTINO: ").strip()

    camino, tiempo_total = buscar_mejor_ruta(origen, destino)

    if isinstance(camino, list):
        print("\n--------------------------------------------------")
        print(f"¡Ruta Óptima Encontrada! (Tiempo total: {tiempo_total} min)")
        print("--------------------------------------------------")
        
        linea_anterior = None
        for i, (estacion, linea) in enumerate(camino):
            if i == 0:
                print(f"1. Iniciar en [{estacion}]")
            else:
                if linea != linea_anterior and linea_anterior is not None:
                    print(f"   * HACER TRANSBORDO a {linea} (+{PENALIZACION_TRANSBORDO} min)")
                print(f"{i+1}. Tomar {linea} hasta [{estacion}]")
            linea_anterior = linea
        print("--------------------------------------------------")
    else:
        print(f"\nError: {tiempo_total}")

if __name__ == "__main__":
    ejecutar()