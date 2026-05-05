import numpy as np
import pandas as pd


SEEDS = {"NOVA": 11, "AURA": 23, "ORBT": 37, "KRYN": 51}


def get_price_frame(ticker: str) -> pd.DataFrame:
    ticker = ticker.upper()
    rng = np.random.default_rng(SEEDS.get(ticker, 99))
    drift = {"NOVA": 0.0018, "AURA": 0.0013, "ORBT": 0.0004, "KRYN": -0.0002}.get(ticker, 0.0005)
    volatility = {"NOVA": 0.018, "AURA": 0.016, "ORBT": 0.021, "KRYN": 0.026}.get(ticker, 0.02)
    returns = rng.normal(drift, volatility, 180)
    close = 100 * np.cumprod(1 + returns)
    frame = pd.DataFrame({"day": np.arange(1, 181), "close": close})
    frame["return"] = frame["close"].pct_change().fillna(0)
    frame["sma_20"] = frame["close"].rolling(20, min_periods=1).mean()
    frame["sma_50"] = frame["close"].rolling(50, min_periods=1).mean()
    return frame


def rsi(values: pd.Series, window: int = 14) -> float:
    delta = values.diff().fillna(0)
    gain = delta.clip(lower=0).rolling(window, min_periods=1).mean()
    loss = -delta.clip(upper=0).rolling(window, min_periods=1).mean()
    rs = gain / loss.replace(0, np.nan)
    score = 100 - (100 / (1 + rs))
    return float(score.fillna(50).iloc[-1])


def quant_agent(ticker: str) -> dict:
    frame = get_price_frame(ticker)
    latest = frame.iloc[-1]
    first = frame.iloc[0]
    momentum = ((latest["close"] / first["close"]) - 1) * 100
    realized_vol = frame["return"].std() * np.sqrt(252) * 100
    current_rsi = rsi(frame["close"])
    trend_positive = latest["sma_20"] > latest["sma_50"]
    drawdown = ((frame["close"] / frame["close"].cummax()) - 1).min() * 100

    score = 50
    score += min(max(momentum, -25), 25) * 0.7
    score += 12 if trend_positive else -8
    score += 8 if 40 <= current_rsi <= 70 else -6
    score -= max(realized_vol - 25, 0) * 0.4
    score += max(drawdown, -35) * 0.2
    score = int(round(min(max(score, 0), 100)))

    return {
        "score": score,
        "momentum": round(momentum, 2),
        "volatility": round(realized_vol, 2),
        "rsi": round(current_rsi, 2),
        "trend": "positive" if trend_positive else "negative",
        "max_drawdown": round(drawdown, 2),
    }
