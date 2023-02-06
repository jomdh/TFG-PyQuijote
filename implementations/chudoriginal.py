import decimal

# for reference, the first 100 digits of pi
pi = decimal.Decimal('3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679')


# Basic recursive factorial calculation. For large n switch to iterative.
def fact(n):
    if n == 0:
        return 1
    else:
        return n * fact(n - 1)


# Denominator- Calculates the sum from 0 to k.
def den(k):
    a = decimal.Decimal(fact(6*k)*(545140134*k+13591409))
    b = decimal.Decimal(fact(3*k)*(fact(k)**3)*((-262537412640768000)**k))
    res = a / b
    if k > 0:
        return res + den(k - 1)
    else:
        return res


# Numerator- root_precision is the number of significant digits to use when calculating the root.
def num(root_precision):
    p = decimal.getcontext().prec
    decimal.getcontext().prec = root_precision
    d = decimal.Decimal(10005).sqrt()
    decimal.getcontext().prec = p
    print(d)
    return 426880 * decimal.Decimal(10005).sqrt()
    

# Calculates the Chudnovsky Algorithm for a given k, and precision.
def chudnovsky(k, root_precision):
    return num(root_precision)/den(k)
  
# Example usage
decimal.getcontext().prec = 50 # set 100 significant figures for decimal numbers
pi_estimate = chudnovsky(50, 50)
error = pi_estimate - pi
print('Error: {}'.format(error))
print(pi_estimate)
print(pi)

