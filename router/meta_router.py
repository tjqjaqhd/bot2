from __future__ import annotations
from typing import List
from libs.common.types import AgentResult, RouterDecision


class MetaRouter:
    def __init__(self, fee: float = 0.0004, k: int = 2):
        self.fee = fee
        self.k = k

    def decide(self, results: List[AgentResult], regime: str = "neutral") -> RouterDecision:
        edges = [r.mu_hat - (self.fee + r.cost_est) for r in results]
        ranked = sorted(zip(results, edges), key=lambda x: x[1], reverse=True)[: self.k]
        if not ranked:
            return RouterDecision(edge_hat=0.0, contributors=[], regime=regime)
        total = sum(max(e, 0) for _, e in ranked)
        contribs = []
        weights = []
        for res, edge in ranked:
            w = max(edge, 0) / total if total > 0 else 1 / len(ranked)
            w = min(w, 0.5)
            weights.append(w)
            contribs.append(res)
        edge_hat = sum(w * (res.mu_hat - (self.fee + res.cost_est)) for w, res in zip(weights, contribs))
        return RouterDecision(edge_hat=edge_hat, contributors=contribs, regime=regime)
