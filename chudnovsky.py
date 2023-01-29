# implementación del algoritmo de Chudnovsky para calcular pi.
# Autor de esta version: J. Martinez @jomdh (github)
# basado en el código de Mark Becwar @thebecwar en github.
# url: original https://gist.github.com/thebecwar/b53f3a9b6e0428a40b27d99745c794a8

# importamos las librerías necesarias
import time
import decimal
import functools


# a modo de referencia,  estos son los primeros 100 dígitos de pi
pi = decimal.Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')


# función factorial, con cache para mejorar el rendimiento.
@functools.lru_cache(maxsize=None)
def fact(n):
    res = 1
    for i in range(1, n+1):
        res *= i
    return res


# Denominador- calcula la suma de 0 a k.
@functools.lru_cache(maxsize=None)
def den(k):
    # implementación de la fórmula de Chudnovsky
    a = decimal.Decimal(fact(6*k)*(545140134*k+13591409))
    b = decimal.Decimal(fact(3*k)*(fact(k)**3)*((-262537412640768000)**k))
    res = a / b
    if k > 0:
        return res + den(k - 1)
    else:
        return res



# Numerador- root_precision es el número de dígitos significativos a usar al calcular la raíz.
@functools.lru_cache(maxsize=None)
def num(root_precision):
    p = decimal.getcontext().prec
    decimal.getcontext().prec = root_precision
    d = decimal.Decimal(10005).sqrt()
    decimal.getcontext().prec = p
    # print(d)
    return 426880 * d
    

# Calcula el algoritmo de Chudnovsky para un k y precisión dados.
def chudnovsky(k, root_precision):
    return num(root_precision)/den(k)

#############################################################################
# función principal, que calcula pi con n dígitos de precisión.
# parámeteros: n: número de dígitos de precisión
# devuelve: pi_estimate: valor de pi con n dígitos de precisión
# imprime: el valor de pi con n dígitos de precisión, y el tiempo que ha tardado en calcularlo.

def get_pi(n):
    # establecer la precisión decimal.
    decimal.getcontext().prec = n
    root_precision = n
    time_start = time.time()
    pi_estimate = chudnovsky(n, root_precision)
    time_end = time.time()

    # imprimir información sobre la ejecución del algoritmo.
    if decimal.getcontext().prec < 100:
        print(pi_estimate)
    else:
        # print pi_estimate decimals length
        print("decimals length: {}".format(decimal.getcontext().prec))
    print('Time taken: {} seconds'.format(time_end - time_start))

    # devolver el valor de pi.
    return pi_estimate


# prueba de la función principal
if __name__ == '__main__':
    get_pi(100)
    get_pi(110)
    get_pi(111)