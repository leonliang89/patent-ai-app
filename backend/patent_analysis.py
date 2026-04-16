import os
import json
import httpx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

PATENTSVIEW_URL = "https://search.patentsview.org/api/v1/patent/"

TECH_TERMS = [
    "AI", "machine learning", "neural network", "IoT", "sensor",
    "robot", "cloud", "blockchain", "autonomous", "wireless",
    "semiconductor", "battery", "medical", "imaging", "5G",
    "detection", "vehicle", "communication", "control", "system"
]

def fetch_patents_from_uspto(query: str, limit: int = 50) -> list:
    try:
        params = {
            "q": json.dumps({"_text_any": {"patent_title": query}}),
            "f": json.dumps([
                "patent_id", "patent_title", "patent_abstract",
                "patent_date", "assignee_organization"
            ]),
            "o": json.dumps({"per_page": limit})
        }
        with httpx.Client(timeout=20) as client:
            r = client.get(PATENTSVIEW_URL, params=params)
            r.raise_for_status()
            return r.json().get("patents") or []
    except Exception as e:
        print(f"[USPTO ERROR] {e}")
        return []

def extract_keyword_distribution(patents: list) -> dict:
    counter = Counter()
    for p in patents:
        title = (p.get("patent_title") or "").lower()
        abstract = (p.get("patent_abstract") or "").lower()
        combined = title + " " + abstract
        for term in TECH_TERMS:
            if term.lower() in combined:
                counter[term] += 1
    return dict(counter.most_common(8))

def analyze_patents(query: str) -> dict:
    os.makedirs("output", exist_ok=True)

    patents = fetch_patents_from_uspto(query, limit=50)

    if not patents:
        return {
            "total_patents": 0,
            "top_keywords": [],
            "distribution": {},
            "source": "USPTO PatentsView",
            "note": f"No patents found for '{query}', or USPTO API temporarily unavailable."
        }

    distribution = extract_keyword_distribution(patents)
    top_keywords = list(distribution.keys())[:5]

    if distribution:
        labels = list(distribution.keys())
        values = list(distribution.values())
        plt.figure(figsize=(8, 4))
        bars = plt.bar(labels, values, color="#4A90D9")
        plt.title(f'Patent Technology Distribution: "{query}" (USPTO)', fontsize=12)
        plt.ylabel("Patent Count")
        plt.xticks(rotation=30, ha="right")
        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.3,
                     str(val), ha="center", va="bottom", fontsize=9)
        plt.tight_layout()
        plt.savefig("output/chart.png")
        plt.close()

    recent_patents = []
    for p in patents[:5]:
        assignee = p.get("assignee_organization", "N/A")
        if isinstance(assignee, list) and len(assignee) > 0:
            assignee = assignee[0].get("assignee_organization", "N/A")
        recent_patents.append({
            "id": p.get("patent_id"),
            "title": p.get("patent_title"),
            "date": p.get("patent_date"),
            "assignee": assignee
        })

    return {
        "total_patents": len(patents),
        "top_keywords": top_keywords,
        "distribution": distribution,
        "recent_patents": recent_patents,
        "source": "USPTO PatentsView (real data)"
    }
