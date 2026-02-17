from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- STRUCTURE MCP OFFICIELLE ---
@app.api_route("/", methods=["GET", "POST"])
async def root(request: Request):
    # Si c'est un POST, on traite ça comme une demande JSON-RPC
    if request.method == "POST":
        body = await request.json()
        method = body.get("method")
        msg_id = body.get("id")

        # 1. Relevance demande la liste des outils
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "decision_tool",
                            "description": "Analyse un email pour cabinet",
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

        # 2. Relevance demande d'exécuter l'outil
        if method == "tools/call":
            params = body.get("params", {})
            arguments = params.get("arguments", {})
            cat = arguments.get("email_category", "A").upper()
            
            action = "alert_manager" if cat == "C" else "create_draft_only"
            
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": action}]
                }
            }

    # Si c'est un GET (navigateur), on renvoie une info simple
    return {"status": "MCP Server Running", "protocol": "JSON-RPC 2.0"}

# Route secondaire au cas où
@app.post("/mcp/execute")
async def execute_legacy(request: Request):
    return {"message": "Please use the root URL for JSON-RPC MCP"}
