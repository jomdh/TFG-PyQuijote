"""
# implementación del algoritmo de Chudnovsky para calcular pi.
# Autor de esta version: J. Martinez @jomdh (github)
# basado en el código de Nick Craig-Wood <nick@craig-wood.com>.
# url: original http://www.craig-wood.com/nick/articles/pi-chudnovsky/ 
"""

# importamos las librerías necesarias
import math
from time import time
import decimal

# a modo de referencia,  estos son los primeros 100 dígitos de pi
pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"


def sqrt(n, one):
    """
    # Devuelve la raíz cuadrada de n como un número en coma flotante.
    # Utiliza una convergencia de Newton-Raphson de segundo orden. 
    # duplicando el número de cifras significativas en cada iteración.
    """

    # uso de aritmética de punto flotante para hacer una estimación inicial
    floating_point_precision = 10**16

    # convertir n a un número de punto flotante
    n_float = float((n * floating_point_precision) // one) / floating_point_precision

    # calcular la raíz cuadrada de n_float
    x = (int(floating_point_precision * math.sqrt(n_float)) * one) // floating_point_precision

    # calcular n * one. 
    n_one = n * one

    # iterar hasta que converja a la raíz cuadrada con la precisión deseada.
    # mediante la convergencia de Newton-Raphson de segundo orden.
    while 1:
        x_old = x
        # 
        x = (x + n_one // x) // 2
        # si x == x_old, entonces la raíz cuadrada ha convergido
        if x == x_old:
            break
    return x

def pi_chudnovsky_bs(digits):
    """
    Traduccion al español: bs significa división binaria, 
    En matemáticas, la división binaria es una técnica para acelerar la evaluación numérica de muchos tipos de series con términos racionales. 
    En particular, se puede usar para evaluar series hipergeométricas en puntos racionales.
    Las series de Chudnovsky son una precisamente este tipo de series hipergeométricas.
    
    Compute int(pi * 10**digits)
    This is done using Chudnovsky's series with binary splitting
    """
    C = 640320
    C3_OVER_24 = C**3 // 24

    def bs(a, b):
        """
        Computes the terms for binary splitting the Chudnovsky infinite series

        a(a) = +/- (13591409 + 545140134*a)
        p(a) = (6*a-5)*(2*a-1)*(6*a-1)
        b(a) = 1
        q(a) = a*a*a*C3_OVER_24

        returns P(a,b), Q(a,b) and T(a,b)
        """
        if b - a == 1:
            # Directly compute P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = 1
            else:
                Pab = (6*a-5)*(2*a-1)*(6*a-1)
                Qab = a*a*a*C3_OVER_24
            Tab = Pab * (13591409 + 545140134*a) # a(a) * p(a)
            if a & 1:
                Tab = -Tab
        else:
            # Recursively compute P(a,b), Q(a,b) and T(a,b)
            # m is the midpoint of a and b
            m = (a + b) // 2
            # Recursively calculate P(a,m), Q(a,m) and T(a,m)
            Pam, Qam, Tam = bs(a, m)
            # Recursively calculate P(m,b), Q(m,b) and T(m,b)
            Pmb, Qmb, Tmb = bs(m, b)
            # Now combine
            Pab = Pam * Pmb
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
        return Pab, Qab, Tab
    # how many terms to compute
    DIGITS_PER_TERM = math.log10(C3_OVER_24/6/2/6)
    # print (DIGITS_PER_TERM)
    N = int(digits/DIGITS_PER_TERM + 1)
    # print (N)

    # Calclate P(0,N) and Q(0,N)
    P, Q, T = bs(0, N)
    one = 10**digits
    sqrtC = sqrt(10005*one, one)
    return (Q*426880*sqrtC) // T


if __name__ == "__main__":
    digits = 5000000
    # time start
    start = time()
    pi = pi_chudnovsky_bs(digits)
    # time end
    end = time()
    print("Tiempo de ejecucion: ", end - start)

    # convertir a un número decimal con la precisión deseada
    decimal.getcontext().prec = 10000 + 10
    pi = decimal.Decimal(pi) / 10**digits

    print_file = True
    if print_file:
        with open("5Mpi.txt", "w") as f:
           f.write(str(pi))
           f.close()