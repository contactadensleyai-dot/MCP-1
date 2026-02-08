from fastapi import FastAPI
from pydantic import BaseModel

# ✅ Une seule instance FastAPI
app = FastAPI(
    title="MCP Cabinet Pro",
    description="Agent professionnel MCP pour cabinet",
    version="1.0"
)

# -----------------------
# ROUTE RACINE
# -----------------------
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur ton MCP professionnel !",
        "status": "opérationnel",
        "instructions": "Utilisez /mcp/context et /mcp/decision pour interagir avec l'agent."
    }

# -----------------------
# ROUTE CONTEXTE
# -----------------------
@app.get("/mcp/context")
def get_context():
    return {
        "send_email_allowed": False,
        "strict_mode": True,
        "default_action": "create_draft_only"
    }

# -----------------------
# ROUTE DECISION
# -----------------------
class DecisionRequest(BaseModel):
    email_category: str
    domain: str
    confidence_level: str

@app.post("/mcp/decision")
def decision(payload: DecisionRequest):
    category = payload.email_category
    domain = payload.domain
    confidence = payload.confidence_level

    if category == "C":
        return {"action": "alert_manager"}

    if domain in ["fiscal", "juridique"] and confidence != "suffisant":
        return {"action": "create_draft_only"}

    if category == "A":
        return {"action": "send_allowed"}

    return {"action": "create_draft_only"}
