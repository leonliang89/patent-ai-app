import json
import httpx

PATENTSVIEW_URL = "https://search.patentsview.org/api/v1/patent/"

def run_agent(text: str) -> str:
    """從 USPTO 取得真實專利，回傳最相關的一筆摘要"""
    try:
        params = {
            "q": json.dumps({"_text_any": {"patent_title": text}}),
            "f": json.dumps([
                "patent_id", "patent_title", "patent_abstract",
                "patent_date", "assignee_organization"
            ]),
            "o": json.dumps({"per_page": 3})
        }
        with httpx.Client(timeout=20) as client:
            r = client.get(PATENTSVIEW_URL, params=params)
            r.raise_for_status()
            patents = r.json().get("patents") or []

        if not patents:
            return f"No real patents found for '{text}' in USPTO database."

        top = patents[0]
        patent_id = top.get("patent_id", "N/A")
        title = top.get("patent_title", "N/A")
        abstract = top.get("patent_abstract") or "No abstract available."
        date = top.get("patent_date", "N/A")

        assignee = top.get("assignee_organization", "N/A")
        if isinstance(assignee, list) and len(assignee) > 0:
            assignee = assignee[0].get("assignee_organization", "N/A")

        result = (
            f"[USPTO Real Patent]\n\n"
            f"Patent ID : {patent_id}\n"
            f"Title     : {title}\n"
            f"Assignee  : {assignee}\n"
            f"Date      : {date}\n\n"
            f"Abstract  :\n{abstract}\n\n"
            f"────────────────────────────────\n"
            f"Also found {len(patents)-1} more patent(s) related to '{text}'."
        )

        if len(patents) > 1:
            result += "\n\nOther relevant patents:\n"
            for p in patents[1:]:
                result += f"  • [{p.get('patent_date','?')}] {p.get('patent_title','N/A')}\n"

        return result

    except Exception as e:
        return f"[USPTO API Error] Could not fetch patents: {str(e)}"
