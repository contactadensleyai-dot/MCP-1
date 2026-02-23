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
    if request.method == "GET":
        return {"status": "MCP Server Ready"}

    body = await request.json()
    method = body.get("method")
    msg_id = body.get("id")

    # 1. INITIALISATION
    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "CabinetPro", "version": "1.0.0"}
            }
        }

    # 2. LISTE DES OUTILS (On change le nom ici pour la recherche)
    if method == "tools/list":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "tools": [
                    {
                        "name": "outil_de_decision",  # Pas d'espaces, utilise des underscores
                        "description": "Analyse la catégorie de l'email pour décider de l'action.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "email_category": {
                                    "type": "string", 
                                    "description": "La catégorie extraite (A, B ou C)"
                                },
                                "domain": {
                                    "type": "string", 
                                    "description": "Le domaine (fiscal, juridique, etc.)"
                                },
                                "confidence_level": {
                                    "type": "string", 
                                    "description": "Niveau de confiance de l'IA"
                                }
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
        action = "alert_manager" if cat == "C" else "create_draft_only"
        
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {"content": [{"type": "text", "text": action}]}
        }

    return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
