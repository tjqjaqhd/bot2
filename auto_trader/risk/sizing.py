"""켈리 및 인벤토리 패널티"""

def kelly(mu: float, var: float, fmin: float, fmax: float, eta: float, inventory: float, lam: float) -> float:
    if var == 0:
        return 0.0
    f = mu / var
    f = max(fmin, min(fmax, f))
    f *= eta
    f -= lam * inventory
    return f
