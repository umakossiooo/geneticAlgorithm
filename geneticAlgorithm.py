import random

# Secuencia genética objetivo
SECUENCIA_OBJETIVO = "ATGCGTACGTCAGTGCATGCA"
TAMANO_POBLACION = 10
PROBABILIDAD_CRUCE = 0.7 # Probabilidad de cruce %70
PROBABILIDAD_MUTACION = 0.1 # Probabilidad de mutación del 10%
N_GENERACIONES = 5 

# Genes posibles en una secuencia de ADN
GENES = ['A', 'T', 'G', 'C']

# Inicializa una población de individuos aleatorios
def inicializar_poblacion(tamano_poblacion, longitud_secuencia):
    poblacion = []
    # Se genera 10 secuencias al azar 
    for _ in range(tamano_poblacion):
        individuo = []
        for _ in range(longitud_secuencia): # Aqui se genera una secuencia
            gen = random.choice(GENES) # Se toma un gen al azar para la secuencia
            individuo.append(gen) # Ese mismo se gen se agrega a la secuencia

        poblacion.append(individuo) # Cuando termina de agregar los genes se agrega la secuencia al arreglo donde van a estar las poblacions
    return poblacion

# Función para evaluar la similitud de un individuo (porcentaje de coincidencias con la secuencia objetivo)
def evaluar_individuo(individuo):
    coincidencias = 0
    for a, b in zip(individuo, SECUENCIA_OBJETIVO): # Se utiliza zip para combinar cada gen de cada lista(individuo, SECUENCIA_OBJETIVO) en su respectivo orden en una sola lista
        # Se compara cada gen del individuo contra el gen de secuencia objetivo
        if a == b:
            # Si coinciden, se aumenta el contador de coincidencias
            coincidencias += 1
    # Se calcula el porcentaje de coincidencias
    porcentaje_similitud = (coincidencias / len(SECUENCIA_OBJETIVO)) * 100
    return porcentaje_similitud


# Selección por torneo
# Aqui simplemente se tomas 2 secuencias al azar y se comparan con la que tenga mas probabilidad y se agrega a la lista de seleccionados, se repite cada combate dependiendo del tamaño de la poblacion
def seleccionar(poblacion, fitness):
    seleccionados = []
    for _ in range(len(poblacion)): # Se va a ejecutar una vez por cada individuo en la poblacion
        # range(len(poblacion)) genera una secuencia de numeros de 0 hasta 10-1 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # random.sample selecciona 2 numeros/individuos al azar de la lista de la población
        # i1 e i2 son los 2 numeros/secuencias/individuos elegidos
        i1, i2 = random.sample(range(len(poblacion)), 2)
        if fitness[i1] > fitness[i2]: # Gana la secuencia i1 porque tiene mejor probabilidad
            seleccionados.append(poblacion[i1])
        else: # Gana la secuencia i2 porque tiene mejor probabilidad
            seleccionados.append(poblacion[i2])
    # se regresa la lista con las secuencias ganadoras en el torneo
    return seleccionados

# Recombinar (cruce de dos puntos) entre dos individuos
def recombinar(individuo1, individuo2):
    # random.random() genera un numero entre 0.0 y 1.0
    # PROBABILIDAD_CRUCE es simplemente una variable para ver si se cruzan o no
    if random.random() < PROBABILIDAD_CRUCE: # Si el numero random es menor que la probabilidad se recombina 
        # len(individuo1) - 1 devuelve la longitud del individuo individuo1, es decir, el número de genes en la secuencia genética de este individuo.
        # random.randint(a, b) genera un número entero aleatorio entre a y b, ambos inclusive.
        # por lo tanto se genera un numero random entre 1 y la longitud de la secuencia del individuo y ese numero es el punto de cruce
        punto_cruce = random.randint(1, len(individuo1) - 1)
        # Ese punto de cruce por ejemplo si fuera 6 va tomar los primeros 6 genes del indiduo1 y va tomar 14 genes del individuo2 y los va juntar y va generar hijo1
        hijo1 = individuo1[:punto_cruce] + individuo2[punto_cruce:]
        #  Va ser lo mismo para hijo2 pero va tomar los primeros 6 genes del indiduo2 y va tomar 14 genes del individuo1 y los va juntar
        hijo2 = individuo2[:punto_cruce] + individuo1[punto_cruce:]
        return hijo1, hijo2
    return individuo1, individuo2

# Mutación de un individuo
def mutar(individuo):
    for i in range(len(individuo)): # Itera sobre la longitud de la secuencia del individuo
        # random.random() genera un numero entre 0.0 y 1.0
        if random.random() < PROBABILIDAD_MUTACION: # Si el numero random es menor que la probabilidad de mutacion
            individuo[i] = random.choice(GENES) # Aqui basicamente se toma un letra de GENES y lo que va hacer es remplazar ese gen localizado en individuo[i] con la letra tomada al azar

# Evaluar una población completa
def evaluar_poblacion(poblacion):
    resultados = []
    for individuo in poblacion:
        fitness = evaluar_individuo(individuo)
        resultados.append(fitness)
    return resultados


# Algoritmo Genético siguiendo el esquema proporcionado
def algoritmo_genetico():
    t = 0  # Inicialización del tiempo o generaciones
    parada = False  # Criterio de parada
    historial_mejores = []  # Almacenar el mejor individuo de cada generación
    
    # Paso: Inicializar P(0) (población inicial)
    print("SE INICIALIZA LA POBLACION")
    P_t = inicializar_poblacion(TAMANO_POBLACION, len(SECUENCIA_OBJETIVO))
    print("Poblacion:" + str(P_t) + "\n")

    print("SE EVALUAN LOS PADRES")
    fitness_P_t = evaluar_poblacion(P_t)
    print("Fitness:" + str(fitness_P_t) + "\n")

    # Comenzamos el bucle del algoritmo genético
    while not parada and t < N_GENERACIONES:
        t += 1
        print(f"Generación {t}:")
        
        # Paso: Seleccionar P(t) desde P(t-1)
        P_t_seleccionada = seleccionar(P_t, fitness_P_t)
        print("Secuencias que ganaron en el torneo:" + str(P_t_seleccionada) + "\n")
        
        # Paso: Recombinar P(t)
        nueva_poblacion = []
        for i in range(0, len(P_t_seleccionada), 2): # Se itera a traves de las secuencias ganadoras pero con un paso de 2, osea va con cada par 
            padre1 = P_t_seleccionada[i] 
            # Aqui basicamente se maneja el caso en el que el la longitud de la lista de los seleccionados sea impar, ya que ahi no habra un padre 2 entonces se maneja ese tipo de situaciones
            if i + 1 < len(P_t_seleccionada): 
                padre2 = P_t_seleccionada[i + 1]
            else:
                padre2 = padre1
            # Se recombina el padre1 y el padre2 para 
            hijo1, hijo2 = recombinar(padre1, padre2)
            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)

        # Paso: Mutación en P(t)
        print("SE HACE MUTACIONES EN LA NUEVA POBLACION QUE SERIA LA DE LOS HIJOS")
        for individuo in nueva_poblacion:
            mutar(individuo)

        # Paso: Evaluar P(t)
        P_t = nueva_poblacion

        fitness_P_t = evaluar_poblacion(P_t)
        print("SE EVALUAN LOS HIJOS") 
        print("Fitness:" + str(fitness_P_t) + "\n")

        # Guardar el mejor individuo de la generación actual
        mejor_individuo = P_t[fitness_P_t.index(max(fitness_P_t))]
        historial_mejores.append((t, mejor_individuo, max(fitness_P_t)))

        # Verificar criterio de parada (si encontramos la secuencia objetivo con 100% de similitud)
        # max(fitness_P_t) devuelve el mayor valor de la lista fitness_P_t
        if max(fitness_P_t) == 100.0: # si el mayor valor de la lista fitness_P_t es igual a 100
            parada = True # se para porque ya se encontró la secuencia objetivo
            print(f"Secuencia objetivo encontrada en la generación {t}.")
        
        # Imprimir porcentaje de similitud para cada individuo
        print("Porcentaje de similitud de cada hijo:")
        for i, individuo in enumerate(P_t):
            print(f"Individuo {i+1}: {''.join(individuo)}, Similitud: {fitness_P_t[i]:.2f}%")
        print("-" * 40)

    # Imprimir los resultados finales de todas las generaciones
    print("RESULTADOS FINALES DE TODAS LAS GENERACIONES")
    for generacion, mejor_individuo, mejor_fitness in historial_mejores:
        print(f"Generación {generacion}: Mejor secuencia: {''.join(mejor_individuo)}, Similitud: {mejor_fitness:.2f}%")

# Ejecutar el algoritmo genético
if __name__ == "__main__":
    algoritmo_genetico()