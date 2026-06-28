import plotly.express as px
import json

def generate_chart(chart_type: str, data: list, x_column: str,
                   y_column: str, title: str = "Chart") -> dict:
    try:
        if not data:
            return {"status": "error", "message": "No data to chart"}
        x = [row.get(x_column, "") for row in data]
        y = [row.get(y_column, 0)  for row in data]
        if chart_type == "bar":
            fig = px.bar(x=x, y=y, title=title, labels={"x":x_column,"y":y_column})
        elif chart_type == "line":
            fig = px.line(x=x, y=y, title=title, labels={"x":x_column,"y":y_column})
        elif chart_type == "pie":
            fig = px.pie(names=x, values=y, title=title)
        elif chart_type == "scatter":
            fig = px.scatter(x=x, y=y, title=title, labels={"x":x_column,"y":y_column})
        else:
            fig = px.bar(x=x, y=y, title=title)
        fig.update_layout(template="plotly_white", height=400)
        return {
            "status": "success",
            "plotly_json": json.loads(fig.to_json()),
            "chart_type": chart_type,
            "title": title
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}