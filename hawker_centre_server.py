"""
Simple Hawker Centre Closure Tracker MCP Server - Track hawker centre closures in Singapore
"""
import os
import sys
import logging
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("hawker-server")

# Initialize MCP server
mcp = FastMCP("hawker-centre-tracker")

# Configuration
API_KEY = os.environ.get("DATA_GOV_SG_API_KEY", "")
BASE_URL = "https://data.gov.sg/api/action/datastore_search"
RESOURCE_ID = "b80cb643-a732-480d-86b5-e03957bc82aa"

# === UTILITY FUNCTIONS ===

def format_hawker_data(records):
    """Format hawker centre data for display."""
    if not records:
        return "No hawker centres found."

    formatted_results = []
    for record in records:
        name = record.get('name', 'N/A')
        address = record.get('address', 'N/A')


        closure_date = record.get('closure_date', 'N/A')
        reopening_date = record.get('reopening_date', 'N/A')
        reason = record.get('description', 'N/A')

        result = f"📍 **{name}**"
        if address != 'N/A':
            result += f"\n   Address: {address}"
        if closure_date != 'N/A':
            result += f"\n   🚫 Closure Date: {closure_date}"
        if reopening_date != 'N/A':
            result += f"\n   ✅ Reopening Date: {reopening_date}"
        if reason != 'N/A':
            result += f"\n   📋 Reason: {reason}"

        formatted_results.append(result)

    return "\n\n".join(formatted_results)

# === MCP TOOLS ===

@mcp.tool()
async def search_hawker_centres(keyword: str = "") -> str:
    """Search for hawker centre closure information by keyword."""
    logger.info(f"Searching hawker centres with keyword: {keyword}")

    if not keyword.strip():
        return "❌ Error: Please provide a keyword to search for hawker centres"

    try:
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY

        params = {
            "resource_id": RESOURCE_ID,
            "q": keyword.strip()
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            if not data.get("success", False):
                return f"❌ API Error: {data.get('error', 'Unknown error')}"

            result = data.get("result", {})
            records = result.get("records", [])
            total = result.get("total", 0)

            if total == 0:
                return f"🔍 No hawker centres found matching '{keyword}'"

            formatted_data = format_hawker_data(records)
            return f"🏪 Found {total} hawker centre(s) matching '{keyword}':\n\n{formatted_data}"

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except httpx.TimeoutException:
        logger.error("Request timeout")
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        logger.error(f"Error searching hawker centres: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_all_closures(limit: str = "50") -> str:
    """Get all current hawker centre closures with optional limit."""
    logger.info(f"Getting all hawker centre closures with limit: {limit}")

    try:
        # Convert string limit to integer
        try:
            limit_int = int(limit) if limit.strip() else 50
            if limit_int <= 0:
                limit_int = 50
        except ValueError:
            limit_int = 50

        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY

        params = {
            "resource_id": RESOURCE_ID,
            "limit": limit_int
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params=params,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()

            if not data.get("success", False):
                return f"❌ API Error: {data.get('error', 'Unknown error')}"

            result = data.get("result", {})
            records = result.get("records", [])
            total = result.get("total", 0)

            if total == 0:
                return "📋 No hawker centre closure records found"

            formatted_data = format_hawker_data(records[:limit_int])
            return f"📊 Showing {len(records)} of {total} hawker centre closure records:\n\n{formatted_data}"

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except httpx.TimeoutException:
        logger.error("Request timeout")
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        logger.error(f"Error getting all closures: {e}")
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===

if __name__ == "__main__":
    logger.info("Starting Hawker Centre Closure Tracker MCP server...")

    if not API_KEY:
        logger.warning("DATA_GOV_SG_API_KEY not set - API requests may be limited")

    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)