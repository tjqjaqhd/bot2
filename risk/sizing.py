from libs.common.types import AgentResult


def kelly_size(agent: AgentResult, eta: float, fmax: float, inventory: float, lam: float) -> float:
    if agent.sigma2 == 0:
        return 0.0
    f_star = agent.mu_hat / agent.sigma2
    f_star = max(min(f_star, fmax), -fmax)
    f_star *= eta
    f_star -= lam * inventory
    return f_star
