import random

SECUENCIA_OBJETIVO = "ATGCGTACGTCAGTGCATGCA"
TAMAÑO_POBLACIÓN = 10
PROBABILIDAD_CRUCE = 0.7
PROBABILIDAD_MUTACION = 0.1
N_GENERACIONES = 5

GENES = ['A', 'T', 'G', 'C']

# Inicializa una población de individuos aleatorios
def inicializar_poblacion(tamaño_población, longitud_secuencia):
    return [[random.choice(GENES) for _ in range(longitud_secuencia)] for _ in range(tamaño_población)]

# Función para evaluar la similitud de un individuo (porcentaje de coincidencias con la secuencia objetivo)
def evaluar_individuo(individuo):
    coincidencias = sum(1 for a, b in zip(individuo, SECUENCIA_OBJETIVO) if a == b)
    porcentaje_similitud = (coincidencias / len(SECUENCIA_OBJETIVO)) * 100
    return porcentaje_similitud

# Selección por torneo
def seleccionar(población, fitness):
    seleccionados = []
    for _ in range(len(población)):
        i1, i2 = random.sample(range(len(población)), 2)
        if fitness[i1] > fitness[i2]:
            seleccionados.append(población[i1])
        else:
            seleccionados.append(población[i2])
    return seleccionados

# Recombinar (cruce de dos puntos) entre dos individuos
def recombinar(individuo1, individuo2):
    if random.random() < PROBABILIDAD_CRUCE:
        punto_cruce = random.randint(1, len(individuo1) - 1)
        hijo1 = individuo1[:punto_cruce] + individuo2[punto_cruce:]
        hijo2 = individuo2[:punto_cruce] + individuo1[punto_cruce:]
        return hijo1, hijo2
    return individuo1, individuo2

# Mutación de un individuo
def mutar(individuo):
    for i in range(len(individuo)):
        if random.random() < PROBABILIDAD_MUTACION:
            individuo[i] = random.choice(GENES)

# Evaluar una población completa
def evaluar_poblacion(población):
    return [evaluar_individuo(individuo) for individuo in población]

# Algoritmo Genético siguiendo el esquema proporcionado
def algoritmo_genetico():
    t = 0  # Inicialización del tiempo
    parada = False  # Criterio de parada
    
    # Paso: Inicializar P(0) (población inicial)
    P_t = inicializar_poblacion(TAMAÑO_POBLACIÓN, len(SECUENCIA_OBJETIVO))
    fitness_P_t = evaluar_poblacion(P_t)

    # Comenzamos el bucle del algoritmo genético
    while not parada and t < N_GENERACIONES:
        t += 1
        
        # Paso: Seleccionar P(t) desde P(t-1)
        P_t_seleccionada = seleccionar(P_t, fitness_P_t)
        
        # Paso: Recombinar P(t)
        nueva_poblacion = []
        for i in range(0, len(P_t_seleccionada), 2):
            padre1 = P_t_seleccionada[i]
            padre2 = P_t_seleccionada[i+1] if i+1 < len(P_t_seleccionada) else padre1
            hijo1, hijo2 = recombinar(padre1, padre2)
            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)

        # Paso: Mutación en P(t)
        for individuo in nueva_poblacion:
            mutar(individuo)

        # Paso: Evaluar P(t)
        P_t = nueva_poblacion
        fitness_P_t = evaluar_poblacion(P_t)

        # Verificar criterio de parada (si encontramos la secuencia objetivo con 100% de similitud)
        if max(fitness_P_t) == 100.0:
            parada = True
            print(f"Secuencia objetivo encontrada en la generación {t}.")
        
        # Imprimir porcentaje de similitud para cada individuo
        for i, individuo in enumerate(P_t):
            print(f"Individuo {i+1}: {''.join(individuo)}, Similitud: {fitness_P_t[i]:.2f}%")
        print("-" * 40)

    # Imprimir los resultados finales
    mejor_individuo = P_t[fitness_P_t.index(max(fitness_P_t))]
    print(f"Mejor secuencia encontrada: {''.join(mejor_individuo)}")
    print(f"Porcentaje de similitud: {max(fitness_P_t):.2f}%")

# Ejecutar el algoritmo genético
if __name__ == "__main__":
    algoritmo_genetico()