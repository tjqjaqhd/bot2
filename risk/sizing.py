from __future__ import annotations


def kelly(mu_hat: float, sigma2: float, eta: float, fmin: float, fmax: float, inventory: float, lam: float = 0.1) -> float:
    if sigma2 <= 0:
        return 0.0
    f = mu_hat / sigma2
    f = max(fmin, min(fmax, f))
    f *= eta
    f -= lam * inventory
    return f
