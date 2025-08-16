from libs.common.types import AgentResult
from router.meta_router import MetaRouter


def test_router_weight_cap():
    router = MetaRouter(fee=0.0)
    ar1 = AgentResult(name="a1", mu_hat=1.0, sigma2=1, cost_est=0.0)
    ar2 = AgentResult(name="a2", mu_hat=0.1, sigma2=1, cost_est=0.0)
    decision = router.route([ar1, ar2])
    weights = [ar.meta["weight"] for ar in decision.contributors]
    assert max(weights) <= 0.5
