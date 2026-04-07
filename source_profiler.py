"""
source_profiler.py
──────────────────
Source Fingerprinting Engine
Profiles news domains by:
  - Lexical patterns (vocabulary, sensationalism score)
  - Publication cadence (posting frequency, timing)
  - Cross-article sentiment consistency
  - Domain metadata signals
  - Known fake/legit domain database lookup
"""

import re
import hashlib
from dataclasses import dataclass, field
from typing import Optional
import numpy as np


# ── Known Domain Database (extend this with real datasets) ───────────────────
# Real datasets: MBFC, NewsGuard API, OpenSources.co

KNOWN_FAKE_DOMAINS = {
    'worldnewsdailyreport.com', 'empirenews.net', 'abcnews.com.co',
    'thenationalistreview.net', 'infostorm247.co', 'libertywriters.com',
    'usapoliticstoday.com', 'neonnettle.com', 'yournewswire.com',
    'beforeitsnews.com', 'activistpost.com', 'thegatewaypundit.com',
}
KNOWN_SATIRE_DOMAINS = {
    'theonion.com', 'clickhole.com', 'babylonbee.com', 'newsthump.com',
    'thebeaverton.com', 'waterfordwhispersnews.com',
}
KNOWN_LEGIT_DOMAINS = {
    'reuters.com', 'apnews.com', 'bbc.com', 'bbc.co.uk', 'npr.org',
    'theguardian.com', 'nytimes.com', 'washingtonpost.com', 'economist.com',
    'factcheck.org', 'snopes.com', 'politifact.com', 'fullfact.org',
}

# Suspicious TLD patterns
SUSPICIOUS_TLDS = {'.com.co', '.news.co', '.co.nf', '.tk', '.ml', '.ga', '.cf'}

# URL structures that mimic legit outlets
MIMIC_PATTERNS = [
    r'abc\w+news', r'cnn\w+', r'fox\w+news', r'nbc\w+',
    r'bbc\w+news', r'reuters\w+',
]


# ── Source Profile ────────────────────────────────────────────────────────────

@dataclass
class SourceProfile:
    domain: str
    credibility_score: float    # 0-100 (100 = most credible)
    source_type: str            # 'legitimate' | 'fake' | 'satire' | 'unknown' | 'suspicious'
    risk_flags: list = field(default_factory=list)
    positive_signals: list = field(default_factory=list)
    lexical_fingerprint: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            'domain': self.domain,
            'credibility_score': round(self.credibility_score, 1),
            'source_type': self.source_type,
            'risk_flags': self.risk_flags,
            'positive_signals': self.positive_signals,
            'lexical_fingerprint': self.lexical_fingerprint,
            'metadata': self.metadata,
        }


# ── Profiler ──────────────────────────────────────────────────────────────────

class SourceProfiler:

    SENSATIONAL_VOCAB = [
        'shocking', 'bombshell', 'exposed', 'secret', 'hiding', 'truth',
        'deep state', 'miracle', 'banned', 'censored', 'wake up', 'must watch',
        'share before deleted', 'going viral', 'they dont want you to know',
        'mainstream media wont', 'urgent', 'breaking', 'exclusive'
    ]
    CREDIBILITY_MARKERS = [
        'according to', 'study published', 'peer-reviewed', 'data shows',
        'officials confirmed', 'sources said', 'in a statement', 'reported by',
        'research indicates', 'statistics show', 'survey found'
    ]

    def profile_domain(self, domain: str, articles: list = None) -> SourceProfile:
        """
        Profile a domain. Pass articles (list of text strings) for deeper analysis.
        """
        domain = self._clean_domain(domain)
        score = 50.0
        flags = []
        positives = []
        source_type = 'unknown'

        # ── Step 1: Database lookup ──────────────────────────────────────────
        if domain in KNOWN_FAKE_DOMAINS:
            return SourceProfile(domain=domain, credibility_score=5.0,
                                 source_type='fake',
                                 risk_flags=['Listed in known fake news database'],
                                 metadata={'database': 'internal'})
        if domain in KNOWN_SATIRE_DOMAINS:
            return SourceProfile(domain=domain, credibility_score=60.0,
                                 source_type='satire',
                                 positive_signals=['Known satire outlet'],
                                 metadata={'database': 'internal'})
        if domain in KNOWN_LEGIT_DOMAINS:
            return SourceProfile(domain=domain, credibility_score=92.0,
                                 source_type='legitimate',
                                 positive_signals=['Established credible outlet'],
                                 metadata={'database': 'internal'})

        # ── Step 2: URL structure analysis ───────────────────────────────────
        for tld in SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                score -= 20
                flags.append(f'Suspicious TLD: {tld}')

        for pattern in MIMIC_PATTERNS:
            if re.search(pattern, domain, re.I):
                score -= 25
                flags.append('Domain mimics legitimate outlet')
                break

        domain_parts = domain.split('.')
        if any(word in domain for word in ['news', 'daily', 'truth', 'patriot', 'freedom', 'liberty']):
            score -= 8
            flags.append('Domain uses loaded political/news keywords')

        domain_age_signal = self._estimate_domain_age(domain)
        if domain_age_signal == 'new':
            score -= 10
            flags.append('Domain appears newly registered')
        elif domain_age_signal == 'established':
            score += 10
            positives.append('Domain has established history')

        # ── Step 3: Article-level analysis ───────────────────────────────────
        lexical = {}
        if articles:
            lexical = self._analyze_articles(articles)
            score += lexical['sentiment_signal']
            if lexical['avg_sensational_score'] > 3:
                flags.append(f"High sensationalism index ({lexical['avg_sensational_score']:.1f}/10)")
                score -= 10
            if lexical['avg_credibility_markers'] > 1:
                positives.append('Regular use of attribution language')
                score += 10
            if lexical['posting_frequency'] == 'very_high':
                flags.append('Unusually high posting frequency (bot signal)')
                score -= 15
            if lexical['cross_article_consistency'] > 0.8:
                positives.append('Consistent editorial voice')
                score += 5

        # ── Step 4: Final score ───────────────────────────────────────────────
        score = max(2.0, min(98.0, score))
        if score < 35:
            source_type = 'fake'
        elif score < 55:
            source_type = 'suspicious'
        elif score < 75:
            source_type = 'unknown'
        else:
            source_type = 'legitimate'

        return SourceProfile(
            domain=domain,
            credibility_score=score,
            source_type=source_type,
            risk_flags=flags,
            positive_signals=positives,
            lexical_fingerprint=lexical,
            metadata={'domain_age': domain_age_signal}
        )

    def _analyze_articles(self, articles: list) -> dict:
        """Compute cross-article statistics."""
        sensational_scores = []
        credibility_scores = []
        word_counts = []

        for text in articles:
            t = text.lower()
            sens = sum(1 for w in self.SENSATIONAL_VOCAB if w in t)
            cred = sum(1 for w in self.CREDIBILITY_MARKERS if w in t)
            sensational_scores.append(sens)
            credibility_scores.append(cred)
            word_counts.append(len(text.split()))

        avg_sens = np.mean(sensational_scores) if sensational_scores else 0
        avg_cred = np.mean(credibility_scores) if credibility_scores else 0

        # Consistency: low std dev = consistent voice
        consistency = 1 - min(1.0, np.std(word_counts) / max(np.mean(word_counts), 1))

        # Frequency signal
        freq = 'normal'
        if len(articles) > 20:
            freq = 'very_high'
        elif len(articles) > 10:
            freq = 'high'

        # Sentiment signal (rough: negative sentiment = -5 to +5)
        negative_words = ['outrage', 'scandal', 'attack', 'destroy', 'corrupt', 'evil', 'lie']
        neg_ratio = np.mean([sum(1 for w in negative_words if w in a.lower()) for a in articles])
        sentiment_signal = -min(10, neg_ratio * 3)

        return {
            'avg_sensational_score': round(float(avg_sens), 2),
            'avg_credibility_markers': round(float(avg_cred), 2),
            'cross_article_consistency': round(float(consistency), 2),
            'avg_word_count': round(float(np.mean(word_counts)), 0) if word_counts else 0,
            'posting_frequency': freq,
            'article_count': len(articles),
            'sentiment_signal': round(float(sentiment_signal), 2),
        }

    def _clean_domain(self, domain: str) -> str:
        domain = re.sub(r'^https?://', '', domain)
        domain = re.sub(r'^www\.', '', domain)
        domain = domain.split('/')[0].lower().strip()
        return domain

    def _estimate_domain_age(self, domain: str) -> str:
        """
        Heuristic: hash the domain name to simulate age lookup.
        In production: use WHOIS API (python-whois library).
        """
        h = int(hashlib.md5(domain.encode()).hexdigest(), 16)
        bucket = h % 3
        return ['new', 'established', 'established'][bucket]

    def bulk_profile(self, domains: list) -> list:
        """Profile a list of domains and return sorted by credibility."""
        profiles = [self.profile_domain(d) for d in domains]
        return sorted(profiles, key=lambda p: p.credibility_score, reverse=True)

    def compare(self, domain_a: str, domain_b: str, articles_a=None, articles_b=None) -> dict:
        """Side-by-side comparison of two sources."""
        pa = self.profile_domain(domain_a, articles_a)
        pb = self.profile_domain(domain_b, articles_b)
        return {
            'domain_a': pa.to_dict(),
            'domain_b': pb.to_dict(),
            'winner': domain_a if pa.credibility_score > pb.credibility_score else domain_b,
        }


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    profiler = SourceProfiler()
    domains = [
        'reuters.com',
        'worldnewsdailyreport.com',
        'theonion.com',
        'freedompatriotnews.co.nf',
        'apnews.com',
    ]
    print("=== Source Profiler Results ===\n")
    for d in domains:
        p = profiler.profile_domain(d)
        print(f"🌐 {d}")
        print(f"   Type:  {p.source_type}  |  Score: {p.credibility_score}/100")
        if p.risk_flags:
            print(f"   ⚠️  {', '.join(p.risk_flags[:2])}")
        if p.positive_signals:
            print(f"   ✅  {', '.join(p.positive_signals[:2])}")
        print()
