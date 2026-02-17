from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

# ==============================
# CONFIGURATION
# ==============================
# IMPORTANT : C'est cette valeur que tu dois mettre dans Relevance AI
API_KEY_VALUE = "CHANGE_MOI_API_KEY_123" 

app = FastAPI(title="MCP Cabinet Pro", version="1.0")

# ==============================
# AUTH VERIFICATION
# ==============================
def verify_api_key(api_key: Optional[str]):
    # On compare avec le header "API_KEY" tel que configuré dans ton image
    if api_key != API_KEY_VALUE:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# ==============================
# MANIFEST (Fusionné avec la racine pour Relevance AI)
# ==============================
@app.get("/")
@app.post("/") # On ajoute POST car Relevance AI semble tester la racine en POST
def mcp_manifest():
    return {
        "mcp_version": "1.0",
        "name": "mcp-cabinet-pro",
        "description": "MCP professionnel pour cabinet",
        "tools": [
            {
                "name": "decision_tool",
                "description": "Décide quelle action appliquer à un email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "email_category": {"type": "string", "description": "Catégorie A, B ou C"},
                        "domain": {"type": "string", "description": "fiscal ou juridique"},
                        "confidence_level": {"type": "string"}
                    },
                    "required": ["email_category", "domain", "confidence_level"]
                }
            }
        ]
    }

# ==============================
# TOOL EXECUTION
# ==============================
class ToolExecution(BaseModel):
    name: str
    arguments: Dict[str, Any]

@app.post("/mcp/execute")
def execute_tool(
    payload: ToolExecution, 
    api_key: Optional[str] = Header(None, alias="API-KEY") # On force le nom du header ici
):
    verify_api_key(api_key)

    if payload.name != "decision_tool":
        raise HTTPException(status_code=400, detail="Unknown tool")

    data = payload.arguments
    email_category = data.get("email_category")
    domain = data.get("domain")
    confidence_level = data.get("confidence_level")

    # Logique décisionnelle
    if email_category == "C":
        action = "alert_manager"
    elif domain in ["fiscal", "juridique"] and confidence_level != "suffisant":
        action = "create_draft_only"
    elif email_category == "A":
        action = "send_allowed"
    else:
        action = "create_draft_only"

    return {
        "content": [
            {
                "type": "text",
                "text": f"L'action décidée est : {action}"
            }
        ]
    }
