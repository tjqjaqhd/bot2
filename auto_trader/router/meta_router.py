"""간단한 EXP3 가중합 라우터"""
from typing import List

from ..libs.common.types import AgentResult, RouterDecision


class MetaRouter:
    def __init__(self, fee: float = 0.0004, gamma: float = 1.8):
        self.weights: dict[str, float] = {}
        self.fee = fee
        self.gamma = gamma

    def route(self, agents: List[AgentResult]) -> RouterDecision:
        edges = []
        for ar in agents:
            edge = ar.mu_hat - (self.fee + ar.cost_est)
            edges.append((edge, ar))
        edges.sort(key=lambda x: x[0], reverse=True)
        top = [ar for _, ar in edges[:2]]
        edge_hat = sum(e for e, _ in edges[:2]) / max(1, len(top))
        return RouterDecision(edge_hat=edge_hat, contributors=top, regime="trend")
