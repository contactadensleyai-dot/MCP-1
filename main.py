from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "POST"])
async def mcp_gateway(request: Request):
    # Pour le navigateur ou le test de Render
    if request.method == "GET":
        return {"status": "MCP Server Ready", "message": "Connect with Relevance AI"}

    # Pour Relevance AI (POST)
    body = await request.json()
    method = body.get("method")
    msg_id = body.get("id")

    # 1. ÉTAPE D'INITIALISATION (Crucial pour Relevance)
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "CabinetPro",
                    "version": "1.0.0"
                }
            }
        }

    # 2. LISTE DES OUTILS
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "decision_tool",
                        "description": "Décide de l'action pour un email (A, B ou C)",
                        "inputSchema": {
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
        }

    # 3. APPEL DE L'OUTIL
    if method == "tools/call":
        params = body.get("params", {})
        args = params.get("arguments", {})
        cat = args.get("email_category", "A").upper()
        
        # Logique simplifiée
        action = "alert_manager" if cat == "C" else "create_draft_only"
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "content": [{"type": "text", "text": action}]
            }
        }

    # Réponse par défaut pour les pings
    return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
