import requests

def web_search(query: str = None, search_query: str = None) -> dict:
    # Accept both 'query' and 'search_query' to prevent parameter mismatch
    search_term = query or search_query
    if not search_term:
        return {"status": "error", "message": "No query term provided"}
        
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": search_term, "format": "json", "no_html": 1, "skip_disambig": 1}
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        answer  = data.get("AbstractText", "")
        source  = data.get("AbstractSource", "")
        related = [r.get("Text","") for r in data.get("RelatedTopics",[])[:3] if r.get("Text")]
        if not answer and related:
            answer = " | ".join(related[:2])
        if not answer:
            answer = f"Searched for '{search_term}'. Please refer to training knowledge for this topic."
        return {
            "status": "success",
            "query": search_term,
            "answer": answer,
            "source": source,
            "related": related
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "query": search_term}