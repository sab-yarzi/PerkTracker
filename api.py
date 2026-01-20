from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import List
from database import get_all_perks, init_db
from models import SingularPerk
from pydantic import BaseModel

app = FastAPI(title="Perk Tracker API", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class PerkResponse(BaseModel):
    id: int
    company_name: str
    offer_text: str
    expiry_text: str | None
    conditions_text: str | None
    percentage_value: float | None
    minimum_spend: float | None
    money_back: float | None
    cap_amount: float | None
    confidence: float
    source: str | None
    created_at: str
    updated_at: str

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main UI"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/perks", response_model=List[PerkResponse])
async def get_perks():
    """Retrieve all perks from database"""
    try:
        perks = get_all_perks()
        return perks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/perks/{perk_id}", response_model=PerkResponse)
async def get_perk(perk_id: int):
    """Get a specific perk by ID"""
    try:
        perks = get_all_perks()
        perk = next((p for p in perks if p['id'] == perk_id), None)

        if not perk:
            raise HTTPException(status_code=404, detail=f"Perk {perk_id} not found")

        return perk
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/perks/company/{company_name}")
async def get_perks_by_company(company_name: str):
    """Get all perks for a specific company"""
    try:
        all_perks = get_all_perks()
        filtered = [p for p in all_perks if company_name.lower() in p['company_name'].lower()]
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get database statistics"""
    try:
        perks = get_all_perks()
        companies = set(p['company_name'] for p in perks)

        return {
            "total_perks": len(perks),
            "unique_companies": len(companies),
            "companies": sorted(companies)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
