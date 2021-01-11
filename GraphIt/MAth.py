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
