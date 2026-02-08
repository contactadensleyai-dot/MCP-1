from fastapi import FastAPI

app = FastAPI(title="MCP Cabinet Pro")

@app.get("/mcp/context")
def get_context():
    return {
        "send_email_allowed": False,
        "strict_mode": True,
        "default_action": "create_draft_only"
    }

@app.post("/mcp/decision")
def decision(payload: dict):
    category = payload.get("email_category")
    domain = payload.get("domain")
    confidence = payload.get("confidence_level")

    if category == "C":
        return {"action": "alert_manager"}

    if domain in ["fiscal", "juridique"] and confidence != "suffisant":
        return {"action": "create_draft_only"}

    if category == "A":
        return {"action": "send_allowed"}

    return {"action": "create_draft_only"}   from fastapi import FastAPI 
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MCP Cabinet Pro", description="Agent professionnel MCP pour cabinet", version="1.0")

# Route racine pour vérifier que le MCP fonctionne
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur ton MCP professionnel !",
        "status": "opérationnel",
        "instructions": "Utilisez /predict pour interagir avec l'agent."
    }

# Modèle pour la requête /predict
class PredictRequest(BaseModel):
    query: str

# Exemple d'endpoint pour prédiction ou interaction avec ton agent
@app.post("/predict")
def predict(request: PredictRequest):
    # Ici tu peux ajouter ta logique IA ou réponse de ton agent
    response_text = f"Réponse simulée pour : '{request.query}'"
    return {
        "query": request.query,
        "response": response_text
    }

# Tu peux ajouter d'autres endpoints pour ton MCP ici
# Exemple: /ask, /chat, /status, etc.
app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur ton MCP professionnel !",
        "status": "opérationnel",
        "instructions": "Utilisez /predict pour interagir avec l'agent."
    }
