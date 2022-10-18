""" 
PROYECTO COORDINADO SAR-ALT (DISTANCIAS)
Autores:    Villanueva Tarazona, Jose
            Mengliev, Alexey
            Apellido/s, Nombre
            Apellido/s, Nombre
Grupo:      L1-4CO11             
"""

from re import S
import numpy as np

# [ALEXEY]
# Debajo utilizo esta misma versión que nos dan pero adaptada a mi gusto con el recorrido.
# He hecho que cuadre con el grafo de las transparencias (o eso creo), intercambiando ejes.
# Elegid solo UNA versión para realizar los demás algoritmos y me lo comentáis para que cambie la edición más adelante.

# Versión base.
def levenshtein_matriz(x, y, threshold=None):
    # esta versión no utiliza threshold, se pone porque se puede
    # invocar con él, en cuyo caso se ignora
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )
    return D[lenX, lenY]

# [ALEXEY]
# Versión modificada. SIN OPTIMIZAR, la he hecho del tirón.
# Recuperación de operaciones de edición. 
def levenshtein_edicion(x, y, threshold=None):
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenY + 1, lenX + 1), dtype=np.int)

    for i in range(1, lenY + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenX + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenY + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[j - 1] != y[i - 1]),
            )

    # Diapo. 25: ... Importante: tras finalizar el cálculo de la distancia.
    # Esto significa que hay que reconstruir.

    # Lista de tuplas de edición.
    B = []

    '''
    EJEMPLO
    
    x = ejemplo (eje J)
    y = campos  (eje I)

            s   6   6   6   6   6   5   5   5                          
            o   5   5   5   5   5   4   4   4
    I       p   4   4   4   4   4   3   4   5
            m   3   3   3   3   3   4   5   6
            a   2   2   2   3   4   5   6   7
            c   1   1   2   3   4   5   6   7
                0   1   2   3   4   5   6   7
                    e   j   e   m   p   l   o

                                J

    '''
    
    # Empezamos desde la "esquina" superior derecha de la matriz de Levenshtein.
    i = lenY
    j = lenX

    while True:
        # Final del camino, estamos en la "esquina" inferior izquierda.
        if i == 0 and j == 0:
            break
        # Estamos en la "pared" inferior, hay que eliminar.
        elif i == 0:
            B.append((x[j - 1], ''))
            j = j - 1
        # Estamos en la "pared" izquierda, hay que insertar.
        elif j == 0:
            B.append(('', y[i - 1]))
            i = i - 1

        # Elegimos la operación de edicion óptima. Si hay mas de una, la que sea.
        # En este caso, se prioriza SUB > BOR > INS en caso de empate.
        # Si quereis cambiar el orden, tendriais que checkear los SUBs de coste 0 antes de esto.
        else:
            op = [D[i - 1][j - 1], D[i][j - 1], D[i - 1][j]]
            
            minval = min(op)
            minindex = op.index(minval)

            if minindex == 0:
                B.append((x[j - 1], y[i - 1]))
                i = i - 1
                j = j - 1
            elif minindex == 1:
                B.append((x[j - 1], ''))
                j = j - 1
            else:
                B.append(('', y[i - 1]))
                i = i - 1
    
    # Revertimos la secuencia y retornamos la tupla (distancia, secuencia)
    B.reverse()
    return D[lenY, lenX], B

# [ALEXEY]
def levenshtein_reduccion(x, y, threshold=None):
    # Nos basta con utilizar dos vectores en vez de toda la matriz.
    lenX, lenY = len(x) + 1, len(y) + 1
    row1 = list(range(lenX))
    row2 = [None] * lenX

    for i in range(1, lenY):
        row1, row2 = row2, row1
        row1[0] = i
        for j in range(1, lenX):
            row1[j] = min(
                row1[j - 1] + 1,
                row2[j] + 1,
                row2[j - 1] + (x[j - 1] != y[i - 1])
            )
    
    return row1[-1]

# [ALEXEY]
def levenshtein(x, y, threshold):
    lenX, lenY = len(x) + 1, len(y) + 1
    row1 = list(range(lenX))
    row2 = [None] * lenX

    for i in range(1, lenY):
        row1, row2 = row2, row1
        row1[0] = i
        for j in range(1, lenX):
            row1[j] = min(
                row1[j - 1] + 1,
                row2[j] + 1,
                row2[j - 1] + (x[j - 1] != y[i - 1])
            )
        # Os hago la version pocha de parada por threshold, que tengo prisa. Usad esto si no teneis nada mejor.
        if all(d > threshold for d in row1):
            return threshold + 1
    
    return min(row1[-1], threshold + 1)

def levenshtein_cota_optimista(x, y, threshold):
    return 0 # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_restricted_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein restringida con matriz
    lenX, lenY = len(x), len(y)
    # COMPLETAR
    return D[lenX, lenY]

def damerau_restricted_edicion(x, y, threshold=None):
    # partiendo de damerau_restricted_matriz añadir recuperar
    # secuencia de operaciones de edición
    return 0,[] # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_restricted(x, y, threshold=None):
    # versión con reducción coste espacial y parada por threshold
    return min(0,threshold+1) # COMPLETAR Y REEMPLAZAR ESTA PARTE

def damerau_intermediate_matriz(x, y, threshold=None):
    # completar versión Damerau-Levenstein intermedia con matriz
    return D[lenX, lenY]

def damerau_intermediate_edicion(x, y, threshold=None):
    # partiendo de matrix_intermediate_damerau añadir recuperar
    # secuencia de operaciones de edición
    # completar versión Damerau-Levenstein intermedia con matriz
    return 0,[] # COMPLETAR Y REEMPLAZAR ESTA PARTE
    
def damerau_intermediate(x, y, threshold=None):
    # versión con reducción coste espacial y parada por threshold
    return min(0,threshold+1) # COMPLETAR Y REEMPLAZAR ESTA PARTE

opcionesSpellBase = {
    'levenshtein_m': levenshtein_matriz,
    'levenshtein_r': levenshtein_reduccion,
    'levenshtein':   levenshtein,
    'levenshtein_o': levenshtein_cota_optimista,
    'damerau_rm':    damerau_restricted_matriz,
    'damerau_r':     damerau_restricted,
    'damerau_im':    damerau_intermediate_matriz,
    'damerau_i':     damerau_intermediate
}

opcionesEdicionBase = {
    'levenshtein': levenshtein_edicion,
    'damerau_r':   damerau_restricted_edicion,
    'damerau_i':   damerau_intermediate_edicion
}

# Para no pillar TODOS los tests de momento, id modificando esto mejor.
opcionesSpell = {
    'levenshtein_m': levenshtein_matriz,
    'levenshtein_r': levenshtein_reduccion,
    'levenshtein':   levenshtein,
}

opcionesEdicion = {
    'levenshtein': levenshtein_edicion
}
#