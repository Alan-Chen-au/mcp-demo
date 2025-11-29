import httpx
from mcp.server.fastmcp import FastMCP


# Create the MCP Server
# We verify this works with Python 3.12+
mcp = FastMCP("Weather Demo Service")


@mcp.tool()
async def get_weather(city: str) -> str:
    """
    Get the current weather forecast for a specified city.
    Wrapper for the free Open-Meteo Public API.
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. Geocoding: Convert city name to coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_res = await client.get(geo_url, params={"name": city, "count": 1, "language": "en", "format": "json"})
            geo_data = geo_res.json()

            if not geo_data.get("results"):
                return f"Error: City '{city}' not found."

            lat = geo_data["results"][0]["latitude"]
            lng = geo_data["results"][0]["longitude"]

            # 2. Weather: Get forecast
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_res = await client.get(weather_url, params={
                "latitude": lat,
                "longitude": lng,
                "current_weather": "true"
            })
            weather_data = weather_res.json()

            current = weather_data.get("current_weather", {})
            print("weather_data: ", current)
            temp = current.get("temperature")
            wind = current.get("windspeed")

            return f"Weather in {city}: {temp}°C, Wind Speed: {wind} km/h."

        except Exception as e:
            return f"API Error: {str(e)}"


if __name__ == "__main__":
    # Runs on stdio by default, compatible with MCP clients
    mcp.run()
