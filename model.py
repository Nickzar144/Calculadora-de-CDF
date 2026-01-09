import math

class CDFModel:
    def __init__(self):
        self.datos = []

    def limpiar_datos(self):
        self.datos = []

    def agregar_datos(self, lista):
        self.datos.extend(lista)

    def calcular_cdf(self):
        datos = self.datos
        n = len(datos)
        Xmin = min(datos)
        Xmax = max(datos)
        R = Xmax - Xmin

        # Número de clases 
        k = round(1 + 3.322 * math.log10(n)) 
        A = math.ceil(R / k) # Anchura de clases

        # Limites de clase
        limites = []
        inicio = Xmin
        for i in range(k):
            fin = inicio + A
            limites.append((inicio, fin))
            inicio = fin

        tabla = []
        Ni = 0
        hi_list = []

        # Calculo de las  frecuencias y acumuladas menor que
        for i, (li, ls) in enumerate(limites):
            ni = sum(1 for x in datos if li <= x < ls or (i == k-1 and x == ls))
            Ni += ni
            hi = ni / n
            hi_list.append(hi)
            Hi = Ni / n

            fila = {
                "Límite Inferior": li,
                "Límite Superior": ls,
                "Marca de Clase": (li + ls)/2,
                "Frecuencia": ni,
                "Ni": Ni,
                "Frecuencia Relativa": round(hi,3),
                "Hi": round(Hi,3),
                "hi_preciso": hi,
                "Hi_preciso": Hi
            }
            tabla.append(fila)

        # Calculo de las frecuencia relativa acumulada mayor que (Hi*) y absoluta mayor que (Ni*)
        Hi_mayor_list = []
        Ni_mayor_list = []
        for i in range(k):
            suma_restante = sum(hi_list[i:])  # acumulado mayor que la clase i
            Hi_mayor_list.append(suma_restante)
            Ni_mayor_list.append(round(suma_restante * n))

        # Guardar Hi* y Ni* en la tabla
        for i in range(k):
            tabla[i]["Hi*"] = round(Hi_mayor_list[i],3)
            tabla[i]["Hi*_preciso"] = Hi_mayor_list[i]
            tabla[i]["Ni*"] = Ni_mayor_list[i]

        # Para gráficas
        clases = [li for li,_ in limites] + [limites[-1][1]]

        resumen = {
            "n": n,
            "Xmin": Xmin,
            "Xmax": Xmax,
            "R": R,
            "k": k,
            "A": A
        }

        return tabla, resumen, clases, hi_list, [fila["Hi_preciso"] for fila in tabla], Hi_mayor_list
