from auto_trader.libs.common.types import AgentResult
from auto_trader.router.meta_router import MetaRouter


def test_meta_router():
    router = MetaRouter(fee=0.0001)
    agents = [
        AgentResult(name="a", mu_hat=0.02, sigma2=1, cost_est=0.0),
        AgentResult(name="b", mu_hat=0.01, sigma2=1, cost_est=0.0),
    ]
    decision = router.route(agents)
    assert decision.edge_hat > 0
    assert len(decision.contributors) == 2
