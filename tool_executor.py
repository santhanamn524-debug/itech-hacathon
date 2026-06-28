import json
import re
from tools import TOOL_REGISTRY


def parse_tool_call(llm_response: str) -> dict | None:
    # 1. Remove thinking block to prevent parser confusion
    cleaned = re.sub(r"<think>[\s\S]*?</think>", "", llm_response).strip()
    
    # 2. Try parsing within <tool_call> tags
    pattern = r"<tool_call>\s*([\s\S]*?)\s*</tool_call>"
    match = re.search(pattern, cleaned, re.IGNORECASE)
    
    json_str = None
    if match:
        json_str = match.group(1).strip()
    else:
        # Fallback: Find any JSON-like block in the text
        json_pattern = r"(\{[\s\S]*?\})"
        all_blocks = re.findall(json_pattern, cleaned)
        for block in all_blocks:
            try:
                parsed = json.loads(block.strip())
                if isinstance(parsed, dict) and "tool" in parsed:
                    return parsed
            except Exception:
                continue
                
    if json_str:
        # Remove markdown code formatting blocks if present
        if json_str.startswith("```"):
            json_str = re.sub(r"^```(?:json)?\s*", "", json_str)
            json_str = re.sub(r"\s*```$", "", json_str)
            json_str = json_str.strip()
            
        try:
            return json.loads(json_str)
        except Exception:
            # Fallback regex search for JSON if there was trailing junk inside tags
            json_obj_match = re.search(r"\{[\s\S]*\}", json_str)
            if json_obj_match:
                try:
                    return json.loads(json_obj_match.group(0))
                except Exception:
                    pass
                    
    return None


def execute_tool(tool_call: dict) -> dict:
    tool_name = tool_call.get("tool")
    parameters = tool_call.get("parameters", {})

    if tool_name not in TOOL_REGISTRY:
        return {
            "status": "error",
            "message": f"Unknown tool '{tool_name}'"
        }

    try:
        return TOOL_REGISTRY[tool_name](**parameters)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


class ToolExecutor:
    def parse_tool_call(self, llm_response: str):
        return parse_tool_call(llm_response)

    def execute_tool(self, tool_call: dict):
        return execute_tool(tool_call)