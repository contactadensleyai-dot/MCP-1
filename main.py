from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

app = FastAPI()

# Autoriser tout pour éviter les blocages de sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY_VALUE = "CHANGE_MOI_API_KEY_123"

# --- MANIFESTE (Ce que Relevance AI lit pour se connecter) ---
@app.api_route("/", methods=["GET", "POST"])
@app.api_route("/mcp/manifest", methods=["GET", "POST"])
async def manifest(request: Request):
    return {
        "mcp_version": "1.0",
        "name": "Cabinet Pro Agent",
        "version": "1.0.0",
        "tools": [
            {
                "name": "decision_tool",
                "description": "Analyse un email pour décider de l'action à prendre",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "email_category": {"type": "string", "description": "Catégorie A, B ou C"},
                        "domain": {"type": "string", "description": "Ex: fiscal, juridique"},
                        "confidence_level": {"type": "string", "description": "Niveau de confiance"}
                    },
                    "required": ["email_category", "domain", "confidence_level"]
                }
            }
        ]
    }

# --- MODÈLE DE DONNÉES ---
class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

# --- EXÉCUTION (L'action de l'outil) ---
@app.post("/mcp/execute")
async def execute(payload: ToolCall, request: Request):
    # On vérifie la clé API dans tous les formats possibles
    api_key = request.headers.get("API_KEY") or request.headers.get("X-API-KEY") or request.headers.get("api-key")
    
    if api_key != API_KEY_VALUE:
        raise HTTPException(status_code=401, detail="Clé API invalide")

    args = payload.arguments
    cat = args.get("email_category", "").upper()
    dom = args.get("domain", "").lower()
    conf = args.get("confidence_level", "").lower()

    # Logique simplifiée
    if cat == "C":
        action = "alert_manager"
    elif dom in ["fiscal", "juridique"] and conf != "suffisant":
        action = "create_draft_only"
    elif cat == "A":
        action = "send_allowed"
    else:
        action = "create_draft_only"

    # Format de retour standard MCP
    return {
        "content": [{"type": "text", "text": action}]
    }
