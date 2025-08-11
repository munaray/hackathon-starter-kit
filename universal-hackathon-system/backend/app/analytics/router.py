from fastapi import APIRouter
from ..schemas import SentimentRequest, SentimentResponse, AnomalyRequest, AnomalyResponse, ScoreRequest, ScoreResponse
from .ai import sentiment_analysis, anomaly_detection, generic_score

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/sentiment", response_model=SentimentResponse)
def analyze_sentiment(req: SentimentRequest):
    label, score = sentiment_analysis(req.text)
    return SentimentResponse(label=label, score=score)


@router.post("/anomaly", response_model=AnomalyResponse)
def analyze_anomaly(req: AnomalyRequest):
    flags, scores = anomaly_detection(req.values)
    return AnomalyResponse(is_anomaly=flags, scores=scores)


@router.post("/score", response_model=ScoreResponse)
def compute_score(req: ScoreRequest):
    score = generic_score(req.features)
    return ScoreResponse(score=score)