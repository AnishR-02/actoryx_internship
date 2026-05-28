import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from app.domain import DGInput, DGResult, calculate_dg_size
from app.database import save_calculation, get_recent_calculations

# ---------- MCP Server ----------

mcp = FastMCP(name="dg-calculator", json_response=True)

@mcp.tool(description=(
    "Calculate the required solar panel system size for a location. "
    "Use this when the user provides their daily energy consumption, location sun hours, "
    "system efficiency, safety margin, and panel wattage."
))
def mcp_calculate_dg(
    daily_consumption_kwh: float,
    peak_sun_hours: float,
    system_efficiency: float,
    safety_margin: float,
    panel_wattage: float
) -> dict:
    result = calculate_dg_size(DGInput(
        daily_consumption_kwh=daily_consumption_kwh,
        peak_sun_hours=peak_sun_hours,
        system_efficiency=system_efficiency,
        safety_margin=safety_margin,
        panel_wattage=panel_wattage
    ))
    return {
        "dg_size_kw": result.dg_size_kw,
        "panel_count": result.panel_count,
        "annual_generation_kwh": result.annual_generation_kwh,
        "monthly_generation_kwh": result.monthly_generation_kwh,
        "daily_generation_kwh": result.daily_generation_kwh,
    }

_mcp_app = mcp.streamable_http_app()

# ---------- Lifespan ----------

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with _mcp_app.router.lifespan_context(app):
        yield

# ---------- FastAPI App ----------

fastapi_app = FastAPI(
    title="DG Size Calculator",
    description="Solar panel sizing API — REST + MCP",
    version="1.0.0",
    lifespan=lifespan
)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Model ----------

class CalcRequest(BaseModel):
    daily_consumption_kwh: float
    peak_sun_hours: float
    system_efficiency: float = 0.8
    safety_margin: float = 1.1
    panel_wattage: float = 400.0

# ---------- REST Endpoints ----------

@fastapi_app.post("/calculate", response_model=DGResult)
def calculate(req: CalcRequest):
    inp = DGInput(
        daily_consumption_kwh=req.daily_consumption_kwh,
        peak_sun_hours=req.peak_sun_hours,
        system_efficiency=req.system_efficiency,
        safety_margin=req.safety_margin,
        panel_wattage=req.panel_wattage
    )
    result = calculate_dg_size(inp)
    save_calculation(req.model_dump(), {
        "dg_size_kw": result.dg_size_kw,
        "panel_count": result.panel_count,
        "daily_generation_kwh": result.daily_generation_kwh,
        "monthly_generation_kwh": result.monthly_generation_kwh,
        "annual_generation_kwh": result.annual_generation_kwh,
    })
    return result

@fastapi_app.get("/history")
def history():
    return get_recent_calculations()

@fastapi_app.get("/health")
def health():
    return {"status": "ok", "interfaces": ["REST /docs", "MCP /mcp"]}

# ---------- Agent Endpoint ----------

from app.agent import run_agent

class AgentRequest(BaseModel):
    message: str

@fastapi_app.post("/agent")
def agent(req: AgentRequest):
    return run_agent(req.message)

# ---------- ASGI Dispatcher ----------

class CombinedApp:
    def __init__(self, rest_app, mcp_asgi_app):
        self._rest = rest_app
        self._mcp = mcp_asgi_app

    async def __call__(self, scope, receive, send):
        path = scope.get("path", "")
        if path == "/mcp" or path.startswith("/mcp/"):
            await self._mcp(scope, receive, send)
        else:
            await self._rest(scope, receive, send)

app = CombinedApp(fastapi_app, _mcp_app)

# ---------- Run ----------

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)