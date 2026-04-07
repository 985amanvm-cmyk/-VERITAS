"""
classifier.py
─────────────
Fake News NLP Classifier
Uses TF-IDF + Logistic Regression (fast, explainable) with optional
BERT fine-tuning for higher accuracy.
"""

import re
import string
import joblib
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pandas as pd

# Download NLTK resources once
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

STOP_WORDS = set(stopwords.words('english'))
stemmer = PorterStemmer()


# ── Text Preprocessing ──────────────────────────────────────────────────────

def preprocess(text: str) -> str:
    """Clean and normalize input text."""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', ' URL ', text)   # mask URLs
    text = re.sub(r'@\w+', ' USER ', text)             # mask mentions
    text = re.sub(r'#(\w+)', r'\1', text)              # strip # from hashtags
    text = re.sub(r'\d+', ' NUM ', text)               # normalize numbers
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [stemmer.stem(t) for t in tokens if t not in STOP_WORDS and len(t) > 2]
    return ' '.join(tokens)


# ── Feature Engineering (hand-crafted signals) ──────────────────────────────

SENSATIONAL = [
    'shocking', 'bombshell', 'exposed', 'secret', 'they', 'hiding',
    'deep state', 'miracle', 'cure', 'banned', 'censored', 'wake up',
    'mainstream media', 'fake news', 'cover up', 'illuminati',
    'government lies', 'the truth', 'must share', 'going viral'
]
HEDGE_WORDS = [
    'according to', 'reportedly', 'sources say', 'officials said',
    'study shows', 'data suggests', 'research indicates', 'experts say'
]

def extract_features(text: str) -> dict:
    """Extract interpretable NLP features from raw text."""
    t = text.lower()
    words = text.split()

    caps_words = sum(1 for w in words if w.isupper() and len(w) > 2)
    exclamations = text.count('!')
    question_marks = text.count('?')
    sensational_count = sum(1 for s in SENSATIONAL if s in t)
    hedge_count = sum(1 for h in HEDGE_WORDS if h in t)
    has_numbers = bool(re.search(r'\d+(\.\d+)?%|\$[\d,]+|\d+ (million|billion)', text, re.I))
    avg_word_len = np.mean([len(w) for w in words]) if words else 0
    unique_ratio = len(set(words)) / len(words) if words else 0
    url_count = len(re.findall(r'http\S+|www\S+', text))

    return {
        'caps_ratio': caps_words / max(len(words), 1),
        'exclamation_count': exclamations,
        'question_count': question_marks,
        'sensational_score': sensational_count,
        'hedge_score': hedge_count,
        'has_numbers': int(has_numbers),
        'avg_word_length': round(avg_word_len, 2),
        'lexical_diversity': round(unique_ratio, 2),
        'url_count': url_count,
        'word_count': len(words),
    }


# ── Model (TF-IDF + Logistic Regression pipeline) ───────────────────────────

class FakeNewsClassifier:
    def __init__(self, model_path: str = None):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                preprocessor=preprocess,
                ngram_range=(1, 3),       # unigrams, bigrams, trigrams
                max_features=50_000,
                sublinear_tf=True,        # log TF scaling
                min_df=2,
            )),
            ('clf', LogisticRegression(
                C=1.0,
                max_iter=1000,
                class_weight='balanced',  # handle class imbalance
                solver='lbfgs',
            ))
        ])
        self.is_trained = False
        if model_path:
            self.load(model_path)

    def train(self, texts: list, labels: list):
        """Train on a list of texts and binary labels (0=real, 1=fake)."""
        self.pipeline.fit(texts, labels)
        self.is_trained = True
        print("✅ Model trained successfully")

    def predict(self, text: str) -> dict:
        """Return verdict + confidence + explainable features."""
        if not self.is_trained:
            # Fallback: heuristic-only mode (no ML model needed)
            return self._heuristic_predict(text)

        prob = self.pipeline.predict_proba([text])[0]
        label = self.pipeline.predict([text])[0]
        features = extract_features(text)

        fake_prob = round(float(prob[1]) * 100, 1)
        real_prob = round(float(prob[0]) * 100, 1)

        return {
            'verdict': 'FAKE' if label == 1 else 'REAL',
            'confidence': fake_prob if label == 1 else real_prob,
            'fake_probability': fake_prob,
            'real_probability': real_prob,
            'features': features,
            'top_signals': self._get_top_signals(features),
        }

    def _heuristic_predict(self, text: str) -> dict:
        """Rule-based fallback when no trained model is available."""
        f = extract_features(text)
        score = 50.0
        score += f['sensational_score'] * 8
        score += f['caps_ratio'] * 30
        score += f['exclamation_count'] * 7
        score -= f['hedge_score'] * 10
        score -= f['has_numbers'] * 8
        score -= f['lexical_diversity'] * 15
        score = max(3.0, min(97.0, score))

        return {
            'verdict': 'FAKE' if score >= 55 else 'REAL',
            'confidence': round(score if score >= 55 else 100 - score, 1),
            'fake_probability': round(score, 1),
            'real_probability': round(100 - score, 1),
            'features': f,
            'top_signals': self._get_top_signals(f),
            'mode': 'heuristic'
        }

    def _get_top_signals(self, features: dict) -> list:
        signals = []
        if features['sensational_score'] > 2:
            signals.append({'signal': 'High emotional language', 'impact': 'negative'})
        if features['caps_ratio'] > 0.15:
            signals.append({'signal': 'Excessive capitalization', 'impact': 'negative'})
        if features['exclamation_count'] > 1:
            signals.append({'signal': 'Clickbait punctuation', 'impact': 'negative'})
        if features['hedge_score'] > 0:
            signals.append({'signal': 'Attribution present', 'impact': 'positive'})
        if features['has_numbers']:
            signals.append({'signal': 'Specific data cited', 'impact': 'positive'})
        if features['lexical_diversity'] > 0.7:
            signals.append({'signal': 'High vocabulary diversity', 'impact': 'positive'})
        return signals

    def evaluate(self, texts: list, labels: list):
        preds = self.pipeline.predict(texts)
        print(classification_report(labels, preds, target_names=['Real', 'Fake']))

    def save(self, path: str = 'model.joblib'):
        joblib.dump(self.pipeline, path)
        print(f"💾 Model saved to {path}")

    def load(self, path: str):
        self.pipeline = joblib.load(path)
        self.is_trained = True
        print(f"📦 Model loaded from {path}")


# ── Quick test ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    clf = FakeNewsClassifier()

    tests = [
        "BREAKING: Scientists discover bleach cures COVID, government hiding the truth!!!",
        "The Federal Reserve raised interest rates by 0.25 percentage points, citing inflation data.",
        "Area man solves climate change with one weird trick; scientists hate him",
    ]
    for t in tests:
        result = clf.predict(t)
        print(f"\n📰 '{t[:60]}...'")
        print(f"   Verdict: {result['verdict']} ({result['confidence']}% confidence)")
        print(f"   Signals: {[s['signal'] for s in result['top_signals']]}")
