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

    return {"action": "create_draft_only"}
