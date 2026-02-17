from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

# Configuration CORS totale
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MANIFESTE MCP (Répond sur toutes les routes courantes) ---
@app.api_route("/", methods=["GET", "POST"])
@app.api_route("/mcp/manifest", methods=["GET", "POST"])
async def manifest(request: Request):
    # Log pour voir ce que Relevance envoie réellement
    print(f"DEBUG - Méthode: {request.method} | Headers: {dict(request.headers)}")
    
    return {
        "mcp_version": "1.0",
        "name": "Cabinet Pro",
        "version": "1.0.0",
        "description": "Agent de décision pour cabinet",
        "tools": [
            {
                "name": "decision_tool",
                "description": "Décide de l'action pour un email",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "email_category": {"type": "string"},
                        "domain": {"type": "string"},
                        "confidence_level": {"type": "string"}
                    },
                    "required": ["email_category", "domain", "confidence_level"]
                }
            }
        ]
    }

# --- EXÉCUTION (SANS AUTHENTIFICATION POUR TESTER) ---
class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

@app.post("/mcp/execute")
async def execute(payload: ToolCall, request: Request):
    # On affiche la clé reçue dans les logs pour vérifier
    print(f"DEBUG - Exécution Tool: {payload.name}")
    
    args = payload.arguments
    cat = args.get("email_category", "A").upper()
    
    # Logique ultra-simple pour le test
    action = "alert_manager" if cat == "C" else "create_draft_only"

    return {
        "content": [{"type": "text", "text": action}]
    }
