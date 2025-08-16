from __future__ import annotations
from typing import List
from libs.common.types import AgentResult, RouterDecision


class MetaRouter:
    """단순 가중합 라우터 (EXP3 대체)."""

    def __init__(self, fee: float = 0.0004):
        self.fee = fee

    def route(self, agents: List[AgentResult]) -> RouterDecision:
        edges = []
        for ar in agents:
            edge = ar.mu_hat - (self.fee + ar.cost_est)
            edges.append((edge, ar))
        edges = [e for e in edges if e[0] > 0]
        edges.sort(key=lambda x: x[0], reverse=True)
        top = edges[:3]
        if not top:
            return RouterDecision(edge_hat=0.0, contributors=[], regime="flat")
        total = sum(e for e, _ in top)
        weights = []
        for edge, ar in top:
            w = min(0.5, edge / total)
            ar.meta["weight"] = w
            weights.append((w, ar))
        edge_hat = sum(w * ar.mu_hat for w, ar in weights)
        contribs = [ar for _, ar in weights]
        return RouterDecision(edge_hat=edge_hat, contributors=contribs, regime="trend")
