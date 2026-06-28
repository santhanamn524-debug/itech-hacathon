from database.connection import execute_raw_sql

def execute_query(sql: str) -> dict:
    try:
        result = execute_raw_sql(sql)
        if "error" in result:
            return {
                "status": "error",
                "message": result["error"],
                "sql_executed": sql,
                "columns": [],
                "rows": [],
                "row_count": 0
            }
        return {
            "status": "success",
            "columns": result["columns"],
            "rows": result["rows"],
            "row_count": result["row_count"],
            "sql_executed": sql,
            "message": f"Query returned {result['row_count']} rows"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "sql_executed": sql,
            "columns": [],
            "rows": [],
            "row_count": 0
        }