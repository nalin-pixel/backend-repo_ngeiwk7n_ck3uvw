import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Lead, VideoIdea, Script

app = FastAPI(title="YT Real Estate Growth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "yt-re-real-estate", "status": "ok"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# ---------- Lead capture ----------

@app.post("/api/leads")
def create_lead(lead: Lead):
    try:
        lead_id = create_document("lead", lead)
        return {"id": lead_id, "message": "Lead captured"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------- Idea generation (simple rule-based for MVP) ----------
class IdeaRequest(BaseModel):
    market: str
    niche: Optional[str] = None
    goal: Optional[str] = "leads"

@app.post("/api/ideas", response_model=List[VideoIdea])
def generate_ideas(payload: IdeaRequest):
    market = payload.market.strip()
    niche = (payload.niche or "buyers").strip()
    goal = (payload.goal or "leads").strip()

    hooks = [
        "Avoid These Costly Mistakes",
        "Ultimate Guide",
        "Pros & Cons No One Tells You",
        "What $500k Buys You",
        "Top Neighborhoods Ranked",
    ]

    ideas: List[VideoIdea] = []
    for h in hooks:
        title = f"{h} When Buying in {market}" if "What $" not in h else f"{h} in {market}"
        angle = f"{niche.title()} in {market}: {h}"
        ideas.append(VideoIdea(market=market, niche=niche, title=title, angle=angle, goal=goal))

    return ideas

# ---------- Script outline (template-based) ----------
class ScriptRequest(BaseModel):
    title: str
    market: str
    angle: str
    niche: Optional[str] = None

@app.post("/api/script", response_model=Script)
def generate_script(payload: ScriptRequest):
    cta = "Thinking about moving? Schedule a free 15‑min call in the link below."
    outline = [
        "Hook (5-7s): Bold claim referencing the market and pain point",
        "Pattern interrupt: quick b-roll of neighborhoods / skyline",
        "Authority: who you are and why to trust you",
        "Value chunk #1: actionable tip with concrete example",
        "Value chunk #2: local insight only a realtor knows",
        "Soft CTA: mention free relocation guide",
        "Value chunk #3: address common misconception",
        "CTA: invite to book a call / download guide",
    ]

    return Script(
        title=payload.title,
        market=payload.market,
        angle=payload.angle,
        call_to_action=cta,
        outline=outline,
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
