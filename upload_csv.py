import pandas as pd
from database.connection import get_engine

def upload_csv(file_path: str, table_name: str = None) -> dict:
    try:
        df = pd.read_csv(file_path)
        if not table_name:
            import os
            table_name = os.path.splitext(
                os.path.basename(file_path)
            )[0].lower().replace(" ", "_")
        df.to_sql(table_name, get_engine(), if_exists="replace", index=False)
        return {
            "status": "success",
            "table_name": table_name,
            "rows_imported": len(df),
            "columns": list(df.columns),
            "message": f"Uploaded {len(df)} rows to table '{table_name}'"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_uploaded_tables() -> dict:
    from sqlalchemy import inspect
    inspector = inspect(get_engine())
    return {"status": "success", "tables": inspector.get_table_names()}