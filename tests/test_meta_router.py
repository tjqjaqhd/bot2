from libs.common.types import AgentResult
from router.meta_router import MetaRouter


def test_meta_router_cap():
    router = MetaRouter()
    res1 = AgentResult(name="a", mu_hat=1.0, sigma2=1.0, cost_est=0.0)
    res2 = AgentResult(name="b", mu_hat=0.1, sigma2=1.0, cost_est=0.0)
    decision = router.decide([res1, res2])
    assert len(decision.contributors) == 2
    max_edge = res1.mu_hat - (router.fee + res1.cost_est)
    assert decision.edge_hat < max_edge * 0.6
