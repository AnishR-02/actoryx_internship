import os
from dotenv import load_dotenv
from groq import Groq
import json
from app.domain import DGInput, calculate_dg_size

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------- Tool definition ----------

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_dg_size",
            "description": (
                "Calculate the required solar panel system size. "
                "Use this whenever the user asks about solar panel sizing, "
                "DG sizing, or how many panels they need."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "daily_consumption_kwh": {
                        "type": "number",
                        "description": "Daily energy consumption in kWh"
                    },
                    "peak_sun_hours": {
                        "type": "number",
                        "description": "Peak sun hours for the location per day"
                    },
                    "system_efficiency": {
                        "type": "number",
                        "description": "System efficiency between 0 and 1, default 0.8"
                    },
                    "safety_margin": {
                        "type": "number",
                        "description": "Safety margin multiplier, default 1.1"
                    },
                    "panel_wattage": {
                        "type": "number",
                        "description": "Wattage of each solar panel, default 400W"
                    },
                },
                "required": ["daily_consumption_kwh", "peak_sun_hours"]
            }
        }
    }
]

# ---------- Peak sun hours lookup by city ----------

CITY_SUN_HOURS = {
    "mumbai": 5.0, "delhi": 5.5, "chennai": 5.5,
    "bangalore": 5.5, "hyderabad": 5.5, "kolkata": 4.5,
    "pune": 5.5, "ahmedabad": 6.0, "jaipur": 6.5,
}

def get_sun_hours_hint(user_message: str) -> str:
    msg = user_message.lower()
    for city, hours in CITY_SUN_HOURS.items():
        if city in msg:
            return f"Note: {city.title()} gets approximately {hours} peak sun hours per day."
    return ""

# ---------- Main agent function ----------

def run_agent(user_message: str) -> dict:
    sun_hint = get_sun_hours_hint(user_message)
    full_message = f"{user_message}\n{sun_hint}" if sun_hint else user_message

    messages = [
        {
            "role": "system",
            "content": (
                "You are a solar energy expert assistant. "
                "Help users calculate the solar panel system size they need. "
                "When a user describes their energy needs, always call the calculate_dg_size tool. "
                "If system_efficiency, safety_margin, or panel_wattage are not mentioned, use defaults: 0.8, 1.1, 400. "
                "After getting the result, explain it in simple, friendly language."
            )
        },
        {
            "role": "user",
            "content": full_message
        }
    ]

    # First call — model decides to call the tool
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message

    # Check if model wants to call our tool
    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        # Fill in defaults if not provided
        args.setdefault("system_efficiency", 0.8)
        args.setdefault("safety_margin", 1.1)
        args.setdefault("panel_wattage", 400.0)

        # Call our domain function
        result = calculate_dg_size(DGInput(**args))

        result_data = {
            "dg_size_kw": result.dg_size_kw,
            "panel_count": result.panel_count,
            "daily_generation_kwh": result.daily_generation_kwh,
            "monthly_generation_kwh": result.monthly_generation_kwh,
            "annual_generation_kwh": result.annual_generation_kwh,
        }

        # Send result back to model for natural language response
        messages.append(response_message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result_data)
        })

        follow_up = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
        )

        return {
            "reply": follow_up.choices[0].message.content,
            "data": result_data
        }

    # Model responded with text only
    return {"reply": response_message.content, "data": None}