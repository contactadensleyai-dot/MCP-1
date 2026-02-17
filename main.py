from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

# =========================
# CONFIG
# =========================
API_KEY = "CHANGE_MOI_API_KEY_123"

app = FastAPI(
    title="MCP Cabinet Pro",
    version="1.0"
)

# =========================
# AUTH
# =========================
def verify_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# =========================
# ROOT
# =========================
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok"}

# =========================
# MCP MANIFEST
# =========================
@app.api_route("/mcp/manifest", methods=["GET", "HEAD"])
def manifest():
    return {
        "name": "mcp-cabinet-pro",
        "description": "MCP professionnel pour cabinet",
        "version": "1.0",
        "auth": {
            "type": "header",
            "header": "x-api-key"
        },
        "tools": [
            {
                "id": "decision",
                "name": "Decision Tool",
                "description": "Décide quelle action appliquer à un email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "email_category": {"type": "string"},
                        "domain": {"type": "string"},
                        "confidence_level": {"type": "string"}
                    },
                    "required": ["email_category", "domain", "confidence_level"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string"}
                    }
                }
            }
        ]
    }

# =========================
# TOOL EXECUTION MODEL
# =========================
class ToolExecution(BaseModel):
    tool_id: str
    input: Dict[str, Any]

# =========================
# TOOL EXECUTION ENDPOINT
# =========================
@app.post("/mcp/execute")
def execute_tool(
    payload: ToolExecution,
    x_api_key: Optional[str] = Header(None)
):
    verify_api_key(x_api_key)

    if payload.tool_id != "decision":
        raise HTTPException(status_code=400, detail="Unknown tool")

    data = payload.input

    email_category = data.get("email_category")
    domain = data.get("domain")
    confidence_level = data.get("confidence_level")

    if email_category == "C":
        action = "alert_manager"

    elif domain in ["fiscal", "juridique"] and confidence_level != "suffisant":
        action = "create_draft_only"

    elif email_category == "A":
        action = "send_allowed"

    else:
        action = "create_draft_only"

    return {
        "output": {
            "action": action
        }
    }
