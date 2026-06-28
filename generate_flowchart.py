def generate_flowchart(diagram_type: str = "er",
                        entities: list = None,
                        relationships: list = None,
                        title: str = "Diagram") -> dict:
    try:
        if diagram_type == "er":
            lines = ["erDiagram"]
            if relationships:
                for r in relationships:
                    lines.append(
                        f'  {r["from"]} ||--o{{ {r["to"]} : "{r.get("label","has")}"'
                    )
            if entities:
                for e in entities:
                    lines.append(f'  {e["name"]} {{')
                    for field in e.get("fields", []):
                        lines.append(f'    {field["type"]} {field["name"]}')
                    lines.append("  }")
        else:
            lines = ["flowchart TD"]
            if entities:
                for i, e in enumerate(entities):
                    lines.append(f'  N{i}["{e}"]')
                    if i > 0:
                        lines.append(f'  N{i-1} --> N{i}')
        mermaid_code = "\n".join(lines)
        return {"status": "success", "mermaid_code": mermaid_code, "diagram_type": diagram_type}
    except Exception as e:
        return {"status": "error", "message": str(e)}