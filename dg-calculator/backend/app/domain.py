from dataclasses import dataclass

# ---------- Input ----------

@dataclass
class DGInput:
    daily_consumption_kwh: float   # how much electricity the site uses per day
    peak_sun_hours: float          # effective sunny hours for the location
    system_efficiency: float       # how much energy is kept (0.0 to 1.0)
    safety_margin: float           # extra buffer on top (e.g. 1.1 = 10% extra)
    panel_wattage: float           # wattage of each individual panel (e.g. 400W)


# ---------- Output ----------

@dataclass
class DGResult:
    dg_size_kw: float              # total solar capacity needed
    panel_count: int               # number of panels required
    annual_generation_kwh: float   # estimated yearly output
    monthly_generation_kwh: float  # estimated monthly output
    daily_generation_kwh: float    # estimated daily output


# ---------- Calculation ----------

def calculate_dg_size(inp: DGInput) -> DGResult:
    # Step 1: raw capacity needed before safety margin
    raw_kw = inp.daily_consumption_kwh / (inp.peak_sun_hours * inp.system_efficiency)

    # Step 2: apply safety margin
    dg_size_kw = raw_kw * inp.safety_margin

    # Step 3: how many panels to hit that capacity
    panel_count = int((dg_size_kw * 1000) / inp.panel_wattage) + 1

    # Step 4: estimate generation (what the system will actually produce)
    daily_generation_kwh = panel_count * (inp.panel_wattage / 1000) * inp.peak_sun_hours * inp.system_efficiency
    monthly_generation_kwh = daily_generation_kwh * 30
    annual_generation_kwh = daily_generation_kwh * 365

    return DGResult(
        dg_size_kw=round(dg_size_kw, 2),
        panel_count=panel_count,
        annual_generation_kwh=round(annual_generation_kwh, 2),
        monthly_generation_kwh=round(monthly_generation_kwh, 2),
        daily_generation_kwh=round(daily_generation_kwh, 2),
    )