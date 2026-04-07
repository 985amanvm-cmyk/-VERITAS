"""
graph_analyzer.py
─────────────────
News Spread Network Analyzer
Builds a directed propagation graph and computes graph-theoretic metrics:
- Betweenness centrality (who amplifies most?)
- Connected components (echo chambers)
- Cascade depth and viral coefficient
- Community detection (Louvain algorithm)
"""

import networkx as nx
import numpy as np
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


# ── Data Structures ──────────────────────────────────────────────────────────

@dataclass
class NewsNode:
    id: str
    label: str
    node_type: str          # 'origin' | 'amplifier' | 'mainstream' | 'debunker' | 'recipient'
    platform: str           # 'twitter' | 'facebook' | 'telegram' | 'website' | etc.
    timestamp: float        # Unix timestamp of first share
    followers: int = 0
    is_bot: bool = False
    country: str = 'Unknown'
    metadata: dict = field(default_factory=dict)


@dataclass
class ShareEdge:
    source: str
    target: str
    timestamp: float
    share_type: str = 'share'   # 'share' | 'quote' | 'reply' | 'embed'


# ── Main Analyzer ────────────────────────────────────────────────────────────

class SpreadGraphAnalyzer:
    def __init__(self):
        self.G = nx.DiGraph()   # directed graph: edges = share events

    def add_node(self, node: NewsNode):
        self.G.add_node(node.id, **{
            'label': node.label,
            'type': node.node_type,
            'platform': node.platform,
            'timestamp': node.timestamp,
            'followers': node.followers,
            'is_bot': node.is_bot,
            'country': node.country,
        })

    def add_edge(self, edge: ShareEdge):
        self.G.add_edge(edge.source, edge.target,
                        timestamp=edge.timestamp,
                        share_type=edge.share_type)

    def build_from_dict(self, data: dict):
        """
        Build graph from frontend-style dict with nodes + edges lists.
        data = {
          'nodes': [{'id': 'n1', 'label': '...', 'type': '...', ...}],
          'edges': [{'source': 'n1', 'target': 'n2', 'timestamp': 0}]
        }
        """
        self.G.clear()
        for n in data['nodes']:
            self.G.add_node(n['id'], **n)
        for e in data['edges']:
            self.G.add_edge(e['source'], e['target'],
                            timestamp=e.get('timestamp', 0),
                            share_type=e.get('share_type', 'share'))

    # ── Core Metrics ─────────────────────────────────────────────────────────

    def find_origin(self) -> Optional[str]:
        """Origin = node with in-degree 0 (no one shared to it)."""
        origins = [n for n, d in self.G.in_degree() if d == 0]
        if not origins:
            return None
        # If multiple, pick the one with earliest timestamp
        return min(origins, key=lambda n: self.G.nodes[n].get('timestamp', float('inf')))

    def cascade_depth(self) -> int:
        """Longest shortest path from origin."""
        origin = self.find_origin()
        if not origin:
            return 0
        lengths = nx.single_source_shortest_path_length(self.G, origin)
        return max(lengths.values()) if lengths else 0

    def betweenness_centrality(self) -> dict:
        """
        Betweenness centrality: fraction of shortest paths passing through a node.
        High value = key amplifier / bridge node.
        """
        bc = nx.betweenness_centrality(self.G, normalized=True)
        return dict(sorted(bc.items(), key=lambda x: x[1], reverse=True))

    def viral_coefficient(self) -> float:
        """
        Average number of new shares each node generates.
        K > 1.0 means viral growth.
        """
        out_degrees = [d for _, d in self.G.out_degree()]
        return round(np.mean(out_degrees), 2) if out_degrees else 0.0

    def reach(self) -> int:
        """Total unique nodes reached."""
        return self.G.number_of_nodes()

    def bot_ratio(self) -> float:
        """Fraction of nodes marked as bots."""
        total = self.G.number_of_nodes()
        if total == 0:
            return 0.0
        bots = sum(1 for _, d in self.G.nodes(data=True) if d.get('is_bot', False))
        return round(bots / total, 2)

    def spread_speed(self) -> dict:
        """
        Time from origin share to each hop depth.
        Returns {depth: min_time_seconds}.
        """
        origin = self.find_origin()
        if not origin:
            return {}
        origin_time = self.G.nodes[origin].get('timestamp', 0)
        paths = nx.single_source_shortest_path(self.G, origin)
        depth_times = defaultdict(list)
        for node, path in paths.items():
            depth = len(path) - 1
            node_time = self.G.nodes[node].get('timestamp', origin_time)
            depth_times[depth].append(node_time - origin_time)
        return {d: round(min(times), 1) for d, times in depth_times.items()}

    def detect_communities(self) -> dict:
        """
        Community detection using greedy modularity (works on directed→undirected).
        Returns {node_id: community_id}.
        """
        undirected = self.G.to_undirected()
        if undirected.number_of_edges() == 0:
            return {n: 0 for n in self.G.nodes()}
        communities = nx.community.greedy_modularity_communities(undirected)
        node_community = {}
        for i, community in enumerate(communities):
            for node in community:
                node_community[node] = i
        return node_community

    def top_amplifiers(self, n: int = 5) -> list:
        """Top N nodes by out-degree (most shares sent)."""
        ranked = sorted(self.G.nodes(), key=lambda x: self.G.out_degree(x), reverse=True)
        return [
            {
                'id': node,
                'label': self.G.nodes[node].get('label', node),
                'out_degree': self.G.out_degree(node),
                'type': self.G.nodes[node].get('type', 'unknown'),
                'is_bot': self.G.nodes[node].get('is_bot', False),
            }
            for node in ranked[:n]
        ]

    def cross_border_spread(self) -> list:
        """List of unique countries reached."""
        countries = set()
        for _, data in self.G.nodes(data=True):
            c = data.get('country', 'Unknown')
            if c and c != 'Unknown':
                countries.add(c)
        return sorted(countries)

    def full_report(self) -> dict:
        """Generate complete graph analysis report."""
        bc = self.betweenness_centrality()
        top_bc = list(bc.items())[:5]

        return {
            'summary': {
                'total_nodes': self.G.number_of_nodes(),
                'total_edges': self.G.number_of_edges(),
                'origin': self.find_origin(),
                'cascade_depth': self.cascade_depth(),
                'viral_coefficient': self.viral_coefficient(),
                'bot_ratio': self.bot_ratio(),
                'countries_reached': len(self.cross_border_spread()),
            },
            'top_amplifiers': self.top_amplifiers(),
            'top_betweenness': [{'node': n, 'score': round(s, 3)} for n, s in top_bc],
            'spread_speed_seconds': self.spread_speed(),
            'communities': self.detect_communities(),
            'graph': {
                'nodes': [
                    {'id': n, **self.G.nodes[n]}
                    for n in self.G.nodes()
                ],
                'edges': [
                    {'source': u, 'target': v, **self.G.edges[u, v]}
                    for u, v in self.G.edges()
                ]
            }
        }


# ── Demo / Test ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    analyzer = SpreadGraphAnalyzer()

    # Build a sample propagation graph
    sample = {
        'nodes': [
            {'id': 'n0', 'label': 'GossipBlog.com', 'type': 'origin', 'platform': 'website', 'timestamp': 0,    'is_bot': False, 'country': 'US'},
            {'id': 'n1', 'label': 'TelegramGroup',   'type': 'amplifier', 'platform': 'telegram', 'timestamp': 1800, 'is_bot': False, 'country': 'RU'},
            {'id': 'n2', 'label': '@BotAccount99',   'type': 'amplifier', 'platform': 'twitter',  'timestamp': 3600, 'is_bot': True,  'country': 'Unknown'},
            {'id': 'n3', 'label': 'LocalNews.tv',    'type': 'mainstream','platform': 'website',  'timestamp': 7200, 'is_bot': False, 'country': 'US'},
            {'id': 'n4', 'label': 'FactCheck.org',   'type': 'debunker',  'platform': 'website',  'timestamp': 14400,'is_bot': False, 'country': 'US'},
            {'id': 'n5', 'label': 'User A',           'type': 'recipient', 'platform': 'facebook', 'timestamp': 9000, 'is_bot': False, 'country': 'IN'},
        ],
        'edges': [
            {'source': 'n0', 'target': 'n1', 'timestamp': 1800},
            {'source': 'n0', 'target': 'n2', 'timestamp': 3600},
            {'source': 'n1', 'target': 'n3', 'timestamp': 7200},
            {'source': 'n2', 'target': 'n5', 'timestamp': 9000},
            {'source': 'n3', 'target': 'n4', 'timestamp': 14400},
        ]
    }

    analyzer.build_from_dict(sample)
    report = analyzer.full_report()

    print("=== Spread Graph Report ===")
    print(f"Nodes:            {report['summary']['total_nodes']}")
    print(f"Edges:            {report['summary']['total_edges']}")
    print(f"Origin:           {report['summary']['origin']}")
    print(f"Cascade depth:    {report['summary']['cascade_depth']}")
    print(f"Viral coefficient:{report['summary']['viral_coefficient']}")
    print(f"Bot ratio:        {report['summary']['bot_ratio']}")
    print(f"Countries:        {report['summary']['countries_reached']}")
    print(f"Top amplifiers:   {[a['label'] for a in report['top_amplifiers']]}")
