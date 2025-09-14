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

async def fetch_all_records(params, headers):
    """Fetch all records using pagination."""
    all_records = []
    offset = 0
    limit = 100  # Maximum per request

    while True:
        current_params = params.copy()
        current_params.update({
            "offset": offset,
            "limit": limit
        })

        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params=current_params,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()

            if not data.get("success", False):
                break

            result = data.get("result", {})
            records = result.get("records", [])

            if not records:
                break

            all_records.extend(records)
            offset += len(records)

            # If we got fewer records than the limit, we've reached the end
            if len(records) < limit:
                break

    return all_records


def format_hawker_data(records):
    """Format hawker centre data for display."""
    if not records:
        return "No hawker centres found."

    formatted_results = []
    for record in records:
        name = record.get('name', 'N/A')
        address = record.get('address_my_env', 'N/A')

        result = f"📍 **{name}**"
        if address != 'N/A':
            result += f"\n   📍 Address: {address}"

        # Q1 Cleaning
        q1_start = record.get('q1_cleaningstartdate', '')
        q1_end = record.get('q1_cleaningenddate', '')
        q1_remarks = record.get('remarks_q1', '')
        if q1_start or q1_end:
            result += f"\n\n   🧹 **Q1 Cleaning:**"
            if q1_start:
                result += f"\n     Start: {q1_start}"
            if q1_end:
                result += f"\n     End: {q1_end}"
            if q1_remarks:
                result += f"\n     Notes: {q1_remarks}"

        # Q2 Cleaning
        q2_start = record.get('q2_cleaningstartdate', '')
        q2_end = record.get('q2_cleaningenddate', '')
        q2_remarks = record.get('remarks_q2', '')
        if q2_start or q2_end:
            result += f"\n\n   🧹 **Q2 Cleaning:**"
            if q2_start:
                result += f"\n     Start: {q2_start}"
            if q2_end:
                result += f"\n     End: {q2_end}"
            if q2_remarks:
                result += f"\n     Notes: {q2_remarks}"

        # Q3 Cleaning
        q3_start = record.get('q3_cleaningstartdate', '')
        q3_end = record.get('q3_cleaningenddate', '')
        q3_remarks = record.get('remarks_q3', '')
        if q3_start or q3_end:
            result += f"\n\n   🧹 **Q3 Cleaning:**"
            if q3_start:
                result += f"\n     Start: {q3_start}"
            if q3_end:
                result += f"\n     End: {q3_end}"
            if q3_remarks:
                result += f"\n     Notes: {q3_remarks}"

        # Q4 Cleaning
        q4_start = record.get('q4_cleaningstartdate', '')
        q4_end = record.get('q4_cleaningenddate', '')
        q4_remarks = record.get('remarks_q4', '')
        if q4_start or q4_end:
            result += f"\n\n   🧹 **Q4 Cleaning:**"
            if q4_start:
                result += f"\n     Start: {q4_start}"
            if q4_end:
                result += f"\n     End: {q4_end}"
            if q4_remarks:
                result += f"\n     Notes: {q4_remarks}"

        # Other Works
        other_start = record.get('other_works_startdate', '')
        other_end = record.get('other_works_enddate', '')
        other_remarks = record.get('remarks_other_works', '')
        if other_start or other_end:
            result += f"\n\n   🔧 **Other Works:**"
            if other_start:
                result += f"\n     Start: {other_start}"
            if other_end:
                result += f"\n     End: {other_end}"
            if other_remarks:
                result += f"\n     Notes: {other_remarks}"

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
async def search_hawker_centres_by_address(address: str = "") -> str:
    """Search for hawker centres by address using exact field filtering."""
    logger.info(f"Searching hawker centres by address: {address}")

    if not address.strip():
        return "❌ Error: Please provide an address to search for hawker centres"

    try:
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY

        # Use filters parameter for exact field matching
        params = {
            "resource_id": RESOURCE_ID,
            "filters": {"address_my_env": address.strip()}
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
                return f"🔍 No hawker centres found with address containing '{address}'"

            formatted_data = format_hawker_data(records)
            return f"📍 Found {total} hawker centre(s) with address '{address}':\n\n{formatted_data}"

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except httpx.TimeoutException:
        logger.error("Request timeout")
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        logger.error(f"Error searching by address: {e}")
        return f"❌ Error: {str(e)}"


@mcp.tool()
async def get_all_hawker_centres() -> str:
    """Get all hawker centre records with their cleaning schedules and other works using pagination."""
    logger.info("Getting all hawker centres with pagination")

    try:
        headers = {}
        if API_KEY:
            headers["x-api-key"] = API_KEY

        params = {
            "resource_id": RESOURCE_ID
        }

        # Fetch all records using pagination
        all_records = await fetch_all_records(params, headers)
        total = len(all_records)

        if total == 0:
            return "📋 No hawker centre records found"

        formatted_data = format_hawker_data(all_records)
        return f"📊 Found {total} hawker centres in Singapore:\n\n{formatted_data}"

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return f"❌ API Error: HTTP {e.response.status_code}"
    except httpx.TimeoutException:
        logger.error("Request timeout")
        return "⏱️ Request timed out. Please try again."
    except Exception as e:
        logger.error(f"Error getting all hawker centres: {e}")
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
