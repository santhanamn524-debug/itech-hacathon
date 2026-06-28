def explain_data(data: list, context: str = "") -> dict:
    try:
        if not data:
            return {"status": "success", "explanation": "No data found for that query."}
        row_count = len(data)
        cols = list(data[0].keys()) if data else []
        numeric_cols = {}
        for col in cols:
            vals = [r[col] for r in data if isinstance(r.get(col), (int, float))]
            if vals:
                numeric_cols[col] = {
                    "min": min(vals),
                    "max": max(vals),
                    "avg": round(sum(vals)/len(vals), 2)
                }
        explanation = f"Found {row_count} records with columns: {', '.join(cols)}."
        if numeric_cols:
            for col, stats in numeric_cols.items():
                explanation += f" {col}: avg={stats['avg']}, min={stats['min']}, max={stats['max']}."
        return {"status": "success", "explanation": explanation, "row_count": row_count}
    except Exception as e:
        return {"status": "error", "message": str(e)}