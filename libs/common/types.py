from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class MarketState(BaseModel):
    ts: float
    symbol: str
    best_bid: float
    best_ask: float
    spread: float
    bids: List[List[float]]  # [[price, size], ...]
    asks: List[List[float]]
    trades_1s: Dict[str, float] = {}
    funding: Optional[float] = None
    oi: Optional[float] = None


class AgentResult(BaseModel):
    name: str
    mu_hat: float
    sigma2: float
    cost_est: float
    exec_profile: Dict[str, float] = {}
    meta: Dict[str, float] = {}


class RouterDecision(BaseModel):
    edge_hat: float
    contributors: List[AgentResult]
    regime: str


class OrderIntent(BaseModel):
    side: str
    qty: float
    price: Optional[float] = None
    mode: str
    pov_cap: Optional[float] = None
    tif: str = "GTC"


class TradeFill(BaseModel):
    ts: float
    filled_qty: float
    avg_px: float
    fees: float
    slip: float


class PnlBreakdown(BaseModel):
    signal_pnl: float
    slippage_pnl: float
    fee_pnl: float
    hedge_cost_pnl: float
    net_pnl: float
