"""
app.py
──────
Flask REST API — Fake News Origin Tracker Backend
Endpoints:
  POST /api/classify        → NLP classification
  POST /api/graph/analyze   → Spread graph metrics
  POST /api/source/profile  → Source fingerprinting
  GET  /api/source/list     → Ranked source database
  GET  /api/health          → Health check
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback

from classifier import FakeNewsClassifier
from graph_analyzer import SpreadGraphAnalyzer
from source_profiler import SourceProfiler

app = Flask(__name__)
CORS(app)   # Allow cross-origin requests from the frontend

# ── Initialize modules (loaded once at startup) ───────────────────────────────
clf      = FakeNewsClassifier()   # tries to load saved model; falls back to heuristic
analyzer = SpreadGraphAnalyzer()
profiler = SourceProfiler()

print("✅ All modules initialized")


# ── Helper ─────────────────────────────────────────────────────────────────────

def error(msg: str, code: int = 400):
    return jsonify({'error': msg}), code


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get('/api/health')
def health():
    return jsonify({'status': 'ok', 'model_trained': clf.is_trained})


@app.post('/api/classify')
def classify():
    """
    Request body: { "text": "news article text here" }
    Returns: verdict, confidence, features, top_signals
    """
    data = request.get_json(silent=True)
    if not data or 'text' not in data:
        return error('Missing "text" field')
    text = data['text'].strip()
    if len(text) < 10:
        return error('Text too short (minimum 10 characters)')
    if len(text) > 10_000:
        return error('Text too long (maximum 10,000 characters)')

    try:
        result = clf.predict(text)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        traceback.print_exc()
        return error(f'Classification failed: {str(e)}', 500)


@app.post('/api/graph/analyze')
def graph_analyze():
    """
    Request body:
    {
      "nodes": [{"id":"n0","label":"Blog","type":"origin","platform":"web","timestamp":0,...}],
      "edges": [{"source":"n0","target":"n1","timestamp":1800}]
    }
    Returns: full spread graph report
    """
    data = request.get_json(silent=True)
    if not data or 'nodes' not in data or 'edges' not in data:
        return error('Missing "nodes" or "edges" fields')

    try:
        analyzer.build_from_dict(data)
        report = analyzer.full_report()
        return jsonify({'success': True, 'report': report})
    except Exception as e:
        traceback.print_exc()
        return error(f'Graph analysis failed: {str(e)}', 500)


@app.post('/api/source/profile')
def source_profile():
    """
    Request body: { "domain": "example.com", "articles": ["text1", "text2"] }
    The "articles" field is optional.
    """
    data = request.get_json(silent=True)
    if not data or 'domain' not in data:
        return error('Missing "domain" field')

    domain = data['domain'].strip()
    articles = data.get('articles', [])

    try:
        profile = profiler.profile_domain(domain, articles if articles else None)
        return jsonify({'success': True, 'profile': profile.to_dict()})
    except Exception as e:
        traceback.print_exc()
        return error(f'Profiling failed: {str(e)}', 500)


@app.get('/api/source/list')
def source_list():
    """
    Returns ranked list of profiled sources.
    Query param: ?type=fake|legitimate|satire|all  (default: all)
    """
    filter_type = request.args.get('type', 'all')

    domains_to_profile = [
        'reuters.com', 'apnews.com', 'bbc.com', 'factcheck.org', 'snopes.com',
        'worldnewsdailyreport.com', 'thenationalistreview.net', 'infostorm247.co',
        'theonion.com', 'babylonbee.com',
    ]

    profiles = profiler.bulk_profile(domains_to_profile)
    result = [p.to_dict() for p in profiles]

    if filter_type != 'all':
        result = [p for p in result if p['source_type'] == filter_type]

    return jsonify({'success': True, 'sources': result, 'count': len(result)})


@app.post('/api/train')
def train_model():
    """
    Train the classifier with provided data.
    Request body: { "texts": [...], "labels": [0, 1, ...] }
    0 = real news, 1 = fake news
    """
    data = request.get_json(silent=True)
    if not data or 'texts' not in data or 'labels' not in data:
        return error('Missing "texts" or "labels"')

    texts = data['texts']
    labels = data['labels']

    if len(texts) != len(labels):
        return error('texts and labels must have the same length')
    if len(texts) < 10:
        return error('Need at least 10 samples to train')

    try:
        clf.train(texts, labels)
        clf.save('model.joblib')
        return jsonify({'success': True, 'message': f'Trained on {len(texts)} samples'})
    except Exception as e:
        traceback.print_exc()
        return error(f'Training failed: {str(e)}', 500)


# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, port=5000)
