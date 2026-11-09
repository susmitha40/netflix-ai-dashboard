"""Score feedback_text with VADER and save to data/processed/.

Setup:  pip install pandas vaderSentiment
Run:    python scripts/sentiment_scoring.py
"""
from pathlib import Path
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "data" / "raw" / "netflix_customer_churn_synthetic.csv"
out = ROOT / "data" / "processed" / "customer_sentiment.csv"

df = pd.read_csv(src)
analyzer = SentimentIntensityAnalyzer()

def score(text):
    return analyzer.polarity_scores(text)["compound"] if isinstance(text, str) else None

def label(s):
    if s is None or pd.isna(s):
        return None
    return "Positive" if s >= 0.05 else "Negative" if s <= -0.05 else "Neutral"

df["sentiment_score"] = df["feedback_text"].apply(score)
df["sentiment_label"] = df["sentiment_score"].apply(label)

out.parent.mkdir(parents=True, exist_ok=True)
df[["customer_id", "sentiment_score", "sentiment_label"]].to_csv(out, index=False)
print(f"Saved {out}")
print(df["sentiment_label"].value_counts(dropna=False))
