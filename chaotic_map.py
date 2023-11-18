import math

def logistic(
    alpha: float, x: float
) -> float:

    y = alpha * x * (1 - x)
    return (y)

def iterative(
    alpha: float, x: float
) -> float:
    
    y = math.sin(alpha * math.pi / x)
    return(y)

def sine(
    alpha: float, x: float
) -> float:
    
    y = (alpha/4) * (math.sin(math.pi / x))
    return(y)

def tent(
    x: float
) -> float:
    
    if(x < 0.7):
        y = x / 0.7
    else:
        y = 10/3 * (1 - x)
    return(y)

def singer(
    mu: float, x: float
) -> float:
    
    y = mu * (7.86 * x - 23.31 * (x**2) + 28.75 * (x**3) - 13.30 * (x**4))
    return(y)