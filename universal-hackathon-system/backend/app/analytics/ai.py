from typing import List

# Lazy import heavy libs
_sentiment_pipeline = None
_isolation_forest = None


def sentiment_analysis(text: str) -> tuple[str, float]:
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        from transformers import pipeline

        _sentiment_pipeline = pipeline("sentiment-analysis")
    result = _sentiment_pipeline(text)[0]
    return result["label"], float(result["score"])  # type: ignore


def anomaly_detection(values: List[float]) -> tuple[List[bool], List[float]]:
    global _isolation_forest
    if _isolation_forest is None:
        from sklearn.ensemble import IsolationForest

        _isolation_forest = IsolationForest(contamination=0.1, random_state=42)
    # Fit on the data (demo). In production, fit on baseline/reference
    arr = [[v] for v in values]
    _isolation_forest.fit(arr)
    preds = _isolation_forest.predict(arr)
    scores = _isolation_forest.decision_function(arr)
    is_anomaly = [p == -1 for p in preds]
    return is_anomaly, list(map(float, scores))


def generic_score(features: dict) -> float:
    # Simple demo: score in [0,1] based on weighted heuristics
    base = 0.5
    if features.get("sentiment") == "POSITIVE":
        base += 0.2
    if features.get("risk", 0) > 0.7:
        base -= 0.3
    activity = float(features.get("activity", 0.0))
    base += min(activity / 100.0, 0.2)
    return max(0.0, min(1.0, base))