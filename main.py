from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

# =========================
# CONFIG
# =========================
API_KEY = "CHANGE_MOI_API_KEY_123"

app = FastAPI(
    title="MCP Cabinet Pro",
    description="MCP professionnel conforme au standard MCP pour Relevance AI",
    version="1.0"
)

# =========================
# AUTH
# =========================
def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Clé API invalide")

# =========================
# ROOT (OBLIGATOIRE POUR RENDER)
# =========================
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {
        "status": "ok",
        "message": "MCP Cabinet Pro opérationnel"
    }

# =========================
# MCP MANIFEST (CRITIQUE)
# DOIT SUPPORTER HEAD
# =========================
@app.api_route("/mcp/manifest", methods=["GET", "HEAD"])
def mcp_manifest():
    return {
        "name": "mcp-cabinet-pro",
        "description": "MCP professionnel pour cabinet (emails, décisions, conformité)",
        "version": "1.0",
        "auth": {
            "type": "header",
            "header": "x-api-key"
        },
        "endpoints": {
            "context": {
                "path": "/mcp/context",
                "method": "GET"
            },
            "decision": {
                "path": "/mcp/decision",
                "method": "POST"
            }
        }
    }

# =========================
# MCP CONTEXT
# =========================
@app.get("/mcp/context")
def get_context(x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)
    return {
        "send_email_allowed": False,
        "strict_mode": True,
        "default_action": "create_draft_only"
    }

# =========================
# DATA MODEL
# =========================
class DecisionPayload(BaseModel):
    email_category: str
    domain: str
    confidence_level: str

# =========================
# MCP DECISION
# =========================
@app.post("/mcp/decision")
def decision(
    payload: DecisionPayload,
    x_api_key: Optional[str] = Header(None)
):
    verify_api_key(x_api_key)

    if payload.email_category == "C":
        return {"action": "alert_manager"}

    if payload.domain in ["fiscal", "juridique"] and payload.confidence_level != "suffisant":
        return {"action": "create_draft_only"}

    if payload.email_category == "A":
        return {"action": "send_allowed"}

    return {"action": "create_draft_only"}
