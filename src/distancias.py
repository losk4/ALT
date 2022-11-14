"""
PROYECTO COORDINADO SAR-ALT (DISTANCIAS)
Autores:    Villanueva Tarazona, Jose
            Mengliev, Alexey
            Fernández Sutil, Diego
            Marcos Bravo, Pablo
Grupo:      L1-4CO11
"""

from re import S
import numpy as np

# [ALEXEY]
# Debajo utilizo esta misma versión que nos dan pero adaptada a mi gusto con el recorrido.
# He hecho que cuadre con el grafo de las transparencias (o eso creo), intercambiando ejes.

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
# Versión modificada.
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

# []
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

# []
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
        #if min>threshold
        if all(d > threshold for d in row1):
            return threshold + 1

    return min(row1[-1], threshold + 1)

# [JOSE]
def levenshtein_cota_optimista(x, y, threshold):
    dx = {}
    dy = {}
        
    for letra in x:
        if letra not in dx:
            dx[letra] = 1
    else:
        dx[letra] += 1
            
    for letra in y:
        if letra not in dy:
            dy[letra] = 1
    else:
        dy[letra] += 1
        
    for key,value in dx.items():
        if key in dy:
            dy[key] += dx[key]
        else:
            dy[key] = 1
        
    res = {
        'pos':0,
        'neg':0
     }
        
    for letra in dy:
        dif = x.count(letra) - y.count(letra)
            
        if dif > 0 :
            res['pos'] += dif
        else:
            res['neg'] += abs(dif)
        
    aux = max(res['pos'], res['neg'])

    if aux > threshold:
        return threshold + 1
    else:
        return levenshtein(x, y, threshold)

def damerau_restricted_matriz(x, y, threshold=None):
    # Versión Damerau-Levenstein restringida con matriz
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            op1 = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )
            #Regla para intercambio ab -> ba con coste 1
            if i > 1 and j > 1 and ((x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                op1 = min(op1, D[i - 2][j - 2] + 1)
            D[i][j] = op1

    return D[lenX, lenY]


def damerau_restricted_edicion(x, y, threshold=None):
    # 
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenY + 1, lenX + 1), dtype=np.int)

    for i in range(1, lenY + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenX + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenY + 1):
            op1 = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[j - 1] != y[i - 1]),
            )
            if i > 1 and j > 1 and ((x[j - 2] == y[i - 1]) and (x[j - 1] == y[i - 2])):
                op1 = min(op1, D[i - 2][j - 2] + 1)
            D[i][j] = op1

    # Lista de tuplas de edición.
    B = []

    # Empezamos desde la "esquina" superior derecha de la matriz de Levenshtein.
    i = lenY
    j = lenX

    while i>0 and j>0:
        # Si viene por la izquierda:
        if D[i-1][j] + 1 == D[i][j]:
            B.append(('', y[i - 1]))
            i = i - 1

        # Si viene por debajo
        elif D[i][j-1] + 1 == D[i][j]:
            B.append((x[j - 1], ''))
            j = j - 1
        
	# si está en la diagonal, y las letras son iguales
        elif (D[i-1][j-1] + (x[j - 1] != y[i - 1]) == D[i][j]):
            B.append((x[j - 1], y[i - 1]))
            i = i - 1
            j = j - 1

        # Si no ocurre nada de lo anterior, aplica Damerau-Restricted
        else:
            #cogería las dos letras
            B.append((x[j-2] + x[j-1], y[i-2] + y[i-1]))
            i = i - 2
            j = j - 2

    # Limites de contorno de la matriz
    while j>0:
        B.append((x[j - 1], ''))
        j = j - 1

    while i>0:
        B.append(('', y[i - 1]))
        i = i - 1

    # Revertimos la secuencia y retornamos la tupla (distancia, secuencia)
    B.reverse()
    return D[lenY, lenX], B




def damerau_restricted(x, y, threshold=None):
    #Versión del damerau-restricted con vectores en vez de la matriz
    #Ahorro coste espacial. Uso de tres vetores para poder aplicar la regla del Damerau-Restricted
    lenX, lenY = len(x) + 1, len(y) + 1
    row1 = list(range(lenX))
    row2 = [None] * lenX
    row3 = [None] * lenX

    for i in range(1, lenY):
        row1,row2,row3=row3,row1,row2
        row1[0] = i
        for j in range(1, lenX):
            row1[j] = min(
                row1[j - 1] + 1,
                row2[j] + 1,
                row2[j - 1] + (x[j - 1] != y[i - 1])
            )
            if i>1 and j>1 and (x[j - 1] == y[i - 2]) and (x[j - 2] == y[i - 1]):
                row1[j] = min(
                    row1[j],
                    row3[j - 2] + 1
                )

        # Parada por threshold
        if all(d > threshold for d in row1):
            return threshold + 1

    return min(row1[-1], threshold + 1)


def damerau_intermediate_matriz(x, y, threshold=None):
    # Versión Damerau-Levenstein intermedia con matriz
    # Se utiliza mismo procedimiento anterior, y se le añaden las dos reglas que conforman Damerau-Intermediate
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            op1 = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )
            if i > 1 and j > 1 and ((x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                op1 = min(op1, D[i - 2][j - 2] + 1)

            # Intercambio acb -> ba con coste 2
            if i > 2 and j > 1 and (x[i - 3] == y[j - 1]) and  x[i - 1] == y[j - 2]:
                op1 = min(op1, D[i - 3][j - 2] + 2)
            # Intercambio ab -> bca con coste 2
            if i > 1 and j > 2 and (x[i - 1] == y[j - 3]) and x[i - 2] == y[j - 1]:
                op1 = min(op1, D[i - 2][j - 3] + 2)

            D[i][j] = op1

    return D[lenX, lenY]


def damerau_intermediate_edicion(x, y, threshold=None):
    # partiendo de matrix_intermediate_damerau añadir recuperar
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            op1 = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )
            if i > 1 and j > 1 and ((x[i - 2] == y[j - 1]) and (x[i - 1] == y[j - 2])):
                op1 = min(op1, D[i - 2][j - 2] + 1)
            if i > 2 and j > 1 and (x[i - 3] == y[j - 1]) and  x[i - 1] == y[j - 2]:
                op1 = min(op1, D[i - 3][j - 2] + 2)
            if i > 1 and j > 2 and (x[i - 1] == y[j - 3]) and x[i - 2] == y[j - 1]:
                op1 = min(op1, D[i - 2][j - 3] + 2)

            D[i][j] = op1

    # Lista de tuplas de edición.
    B = []

    # Empezamos desde la "esquina" superior derecha de la matriz de Levenshtein.
    i = lenY
    j = lenX

    while i>0 and j>0:

        # Si viene por la izquierda:
        if D[i-1][j] + 1 == D[i][j]:
            B.append(('', y[i - 1]))
            i = i - 1

        # Si viene por debajo
        elif D[i][j-1] + 1 == D[i][j]:
            B.append((x[j - 1], ''))
            j = j - 1

        # Si está en la diagonal, y las letras son iguales
        elif (D[i-1][j-1] + (x[j - 1] != y[i - 1]) == D[i][j]):
            B.append((x[j - 1], y[i - 1]))
            i = i - 1
            j = j - 1

        # Si se cumple Damerau-intermediate (regla acb->ba)
        elif i > 2 and j > 1 and (x[j - 3] == y[i - 1]) and  x[j - 1] == y[i - 2]:
            B.append((x[j-3] + x[j-2] + x[j-1], y[i-2] + y[i-1]))
            j = j - 3
            i = i - 2

        # Si se cumple Damerau-intermediate (regla ab->bca)
        elif i > 1 and j > 2 and (x[j - 1] == y[i - 3]) and x[j - 2] == y[i - 1]:
            B.append((x[j-2] + x[j-1], y[i-3] + y[i-2] + y[i-1]))
            j = j - 2
            i = i - 3            

        else:
            #cogería las dos letras
            B.append((x[j-2] + x[j-1], y[i-2] + y[i-1]))
            i = i - 2
            j = j - 2

    # Límites de contorno de la matriz
    while j>0:
        B.append((x[j - 1], ''))
        j = j - 1

    while i>0:
        B.append(('', y[i - 1]))
        i = i - 1

    # Revertimos la secuencia y retornamos la tupla (distancia, secuencia)
    B.reverse()
    return D[lenY, lenX], B




def damerau_intermediate(x, y, threshold=None):
    # Versión damerau intermedia con vectores
    # Se encesitan 4 vectores para aplicar la última regla del DI: (ab -> bca)
    lenX, lenY = len(x) + 1, len(y) + 1
    row1 = list(range(lenX))
    row2 = [None] * lenX
    row3 = [None] * lenX
    row4 = [None] * lenX

    for i in range(1, lenY):
        row1,row2,row3,row4=row4,row1,row2,row3
        row1[0] = i
        for j in range(1, lenX):
            row1[j] = min(
                row1[j - 1] + 1,
                row2[j] + 1,
                row2[j - 1] + (x[j - 1] != y[i - 1])
            )
            if i > 1 and j > 1 and (x[j - 1] == y[i - 2]) and (x[j - 2] == y[i - 1]):
                row1[j] = min(
                    row1[j],
                    row3[j - 2] + 1
                )
            if i > 1 and j > 2 and (x[j - 3] == y[i - 1]) and  (x[j - 1] == y[i - 2]):
                row1[j]= min(
                    row1[j],
                    row3[j - 3] + 2
                )
            if i > 2 and j > 1 and (x[j - 1] == y[i - 3]) and (x[j - 2] == y[i - 1]):
                row1[j]= min(
                    row1[j],
                    row4[j - 2] + 2
                )

        # Parada por threshold
        if all(d > threshold for d in row1):
            return threshold + 1

    return min(row1[-1], threshold + 1)


opcionesSpell = {
    'levenshtein_m': levenshtein_matriz,
    'levenshtein_r': levenshtein_reduccion,
    'levenshtein':   levenshtein,
    'levenshtein_o': levenshtein_cota_optimista,
    'damerau_rm':    damerau_restricted_matriz,
    'damerau_r':     damerau_restricted,
    'damerau_im':    damerau_intermediate_matriz,
    'damerau_i':     damerau_intermediate
}

opcionesEdicion = {
    'levenshtein': levenshtein_edicion,
    'damerau_r':   damerau_restricted_edicion
    #'damerau_i':   damerau_intermediate_edicion
}
