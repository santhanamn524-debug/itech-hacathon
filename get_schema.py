from database.connection import get_engine
from sqlalchemy import inspect

def get_schema(table_name: str = None) -> dict:
    try:
        inspector = inspect(get_engine())
        tables = inspector.get_table_names()
        if table_name:
            cols = inspector.get_columns(table_name)
            return {
                "status": "success",
                "table": table_name,
                "columns": [{"name":c["name"],"type":str(c["type"])} for c in cols]
            }
        schema = {}
        for t in tables:
            cols = inspector.get_columns(t)
            schema[t] = [{"name":c["name"],"type":str(c["type"])} for c in cols]
        return {"status": "success", "tables": tables, "schema": schema}
    except Exception as e:
        return {"status": "error", "message": str(e)}