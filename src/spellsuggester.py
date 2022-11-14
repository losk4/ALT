# -*- coding: utf-8 -*-
import re
import numpy as np

import distancias
import time

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self,
                 dist_functions = [],
                 vocab = [],
                 default_distance = None,
                 default_threshold = None):
        
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),

        Args:
           dist_functions es un diccionario nombre->funcion_distancia
           vocab es una lista de palabras o la ruta de un fichero
           default_distance debe ser una clave de dist_functions
           default_threshold un entero positivo

        """
        self.distance_functions = dist_functions
        self.vocabulary = None
        self.set_vocabulary(vocab)
        if default_distance is None:
            default_distance = 'levenshtein'
        if default_threshold is None:
            default_threshold = 3
        self.default_distance = default_distance
        self.default_threshold = default_threshold

    def build_vocabulary(self, vocab_file_path):
        """Método auxiliar para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        tokenizer=re.compile("\W+")
        with open(vocab_file_path, "r", encoding="utf-8") as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard("")  # por si acaso
            return sorted(vocab)

    def set_vocabulary(self, vocabulary):
        if isinstance(vocabulary,list):
            self.vocabulary = vocabulary # atención! nos quedamos una referencia, a tener en cuenta
        elif isinstance(vocabulary,str):
            self.vocabulary = self.build_vocabulary(vocabulary)
        else:
            raise Exception("SpellSuggester incorrect vocabulary value")
    
    def cota_optimista(self, x, y):
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
        
        return max(res['pos'], res['neg'])

    def suggest(self, term, distance=None, threshold=None, flatten=True):
        """

        Args:
            term (str): término de búsqueda.
            distance (str): nombre del algoritmo de búsqueda a utilizar
            threshold (int): threshold para limitar la búsqueda
        """ 
        # [JOSE]
        ########################################
        # COMPLETAR
        ########################################
        
        if threshold == None:
            threshold = self.default_threshold
        if distance == None:
            distance = self.default_distance
        
        resul = [[] for _ in range(threshold+1)]
        for i in range(threshold+1):
            if distance == "levenshtein_m":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                            d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.levenshtein_matriz(x, term, i)
                    if d == i:
                        resul[i].append(x)
            if distance == "levenshtein_r":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                        d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.levenshtein_reduccion(x, term, i)
                    if d == i:
                        resul[i].append(x)
            if distance == "levenshtein":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                        d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.levenshtein(x, term, i)
                    if d == i:
                        resul[i].append(x)
            if distance == "damerau_r":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                        d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.damerau_restricted(x, term, i)
                    if d == i:
                        resul[i].append(x)
            if distance == "damerau_rm":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                        d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.damerau_restricted_matriz(x, term, i)
                    if d == i:
                        resul[i].append(x)
            if distance == "damerau_im":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                        d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.damerau_intermediate_matriz(x, term, i)
                    if d == i:
                        resul[i].append(x)
            if distance == "damerau_i":
                for x in self.vocabulary:
                    if abs(len(x)-len(term)) > i:
                        d = i + 1
                    elif self.cota_optimista(term, x) > threshold:
                        d = threshold + 1
                    else:
                        d = distancias.damerau_intermediate(x, term, i)
                    if d == i:
                        resul[i].append(x)

        if flatten:
            resul = [word for wlist in resul for word in wlist]
            
        return resul

