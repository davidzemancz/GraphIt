import math

def lagrange(arr, x):
    """
    Lagrangeuv interpolacni polynom
    """
    n = len(arr)
    
    sum = 0
    for i in range(n):
        x_i = arr[i][0]
        y_i = arr[i][1]

        product = 1
        for j in range(n):
            if j == i: continue
            x_j = arr[j][0]
            y_j = arr[j][1]

            result = (x - x_j) / (x_i - x_j)
            product = product * result

        result = y_i * product
        sum = sum + result

    return sum

def bell_num(n):
    """
    Bellovo cislo - Pocet moznych rozkadu mnoziny (napr na ekvivalencni tridy)
    """
    if n == 0 or n == 1:
        return 1.0

    b = 0 
    for k in range(n):
        b += n_choose_k(n - 1, k) * bell_num(k)
    
    return b

def n_choose_k(n, k):
    """
    Kombinanci cislo
    """
    return factorial(n) / (factorial(k) * factorial(n - k))

def factorial(k):
    """
    Faktorial
    """
    if k == 0 or k == 1:
        return 1
    else:
        return k * factorial(k-1)

def is_prime(number):

    if number == 2:
        return True
    elif number % 2 == 0:
        return False
    else:
        sr = math.sqrt(number)
        for i in range(3, int(sr + 1), 2):
            if number % i == 0:
                print("Divisor:", i)
                return False
    return True

    pass

