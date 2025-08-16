from auto_trader.exec.broker_paper import PaperBroker
from auto_trader.exec.execution_engine import ExecutionEngine
from auto_trader.libs.common.types import RouterDecision, AgentResult


def test_execution_engine():
    broker = PaperBroker()
    engine = ExecutionEngine(broker)
    rd = RouterDecision(edge_hat=0.1, contributors=[AgentResult(name="a", mu_hat=0.1, sigma2=1, cost_est=0)], regime="trend")
    fill = engine.execute(rd, "buy", 1.0, 100.0)
    assert fill.filled_qty == 1.0
