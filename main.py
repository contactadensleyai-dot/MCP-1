from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="MCP Cabinet Pro",
    description="Agent professionnel MCP pour cabinet, compatible Relevance AI",
    version="1.0"
)

# ====== CONFIGURATION DU TOKEN ======
API_KEY = "mon_secret_mcp"  # Change ce mot de passe si tu veux
HEADER_NAME = "x-api-key"

def verify_api_key(x_api_key: str = Header(...)):
    """Vérifie que la requête contient le bon token"""
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# ====== ROUTE RACINE ======
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur ton MCP professionnel !",
        "status": "opérationnel",
        "instructions": "Utilisez /mcp/context et /mcp/decision pour interagir avec l'agent."
    }

# ====== ROUTE CONTEXT ======
@app.get("/mcp/context")
def get_context(x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    return {
        "send_email_allowed": False,
        "strict_mode": True,
        "default_action": "create_draft_only"
    }

# ====== ROUTE DECISION ======
class DecisionPayload(BaseModel):
    email_category: str
    domain: str
    confidence_level: str

@app.post("/mcp/decision")
def decision(payload: DecisionPayload, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

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
