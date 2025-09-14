# Claude Integration Guide - Hawker Centre Closure Tracker

> **Disclaimer**: This is an unofficial MCP server project that was entirely generated using Claude AI. While functional, please review and test thoroughly before production use.

## Overview

This MCP server provides Claude with access to Singapore's official hawker centre closure data via data.gov.sg API. It enables real-time queries about hawker centre closures, reopening dates, and closure reasons.

## Available Tools

### 1. search_hawker_centres(keyword)
- **Purpose**: Search for hawker centre closure information by keyword (full text search)
- **Parameters**: `keyword` (string) - Search term (hawker centre name, location, etc.)
- **Returns**: Formatted list of matching hawker centres with closure details
- **Example**: `search_hawker_centres("Bedok")`

### 2. search_hawker_centres_by_address(address)
- **Purpose**: Search for hawker centres by exact address matching
- **Parameters**: `address` (string) - Full or partial address to search for
- **Returns**: Formatted list of hawker centres with matching addresses
- **Example**: `search_hawker_centres_by_address("Ang Mo Kio Avenue 10")`

### 3. get_all_closures(limit)
- **Purpose**: Retrieve all current hawker centre closure records
- **Parameters**: `limit` (string, default "50") - Maximum number of records to return
- **Returns**: Formatted list of hawker centre closures
- **Example**: `get_all_closures("20")`

## Data Structure

Each hawker centre record includes:
- **Name**: Official hawker centre name
- **Address**: Full address of the hawker centre (address_my_env)
- **Q1 Cleaning**: Start date, end date, and remarks for Q1 cleaning period
- **Q2 Cleaning**: Start date, end date, and remarks for Q2 cleaning period
- **Q3 Cleaning**: Start date, end date, and remarks for Q3 cleaning period
- **Q4 Cleaning**: Start date, end date, and remarks for Q4 cleaning period
- **Other Works**: Start date, end date, and remarks for other maintenance works

## Usage Guidelines for Claude

### Natural Language Processing
Claude can understand these types of queries:
- "Find hawker centres closed in Tampines"
- "Show me recent hawker centre closures"
- "Is [Hawker Centre Name] currently closed?"
- "What hawker centres are closing for renovation?"

### Response Formatting
The tools return formatted text with:
- 📍 Location markers for hawker centre names
- 🚫 Closure date indicators
- ✅ Reopening date indicators
- 📋 Reason descriptions
- 🔍 Search status messages
- ❌ Error indicators

### Error Handling
The tools handle various error scenarios:
- Empty search keywords
- API connectivity issues
- Invalid limit values
- Authentication problems
- Timeout errors

### Best Practices

1. **Keyword Selection**: Use location names, hawker centre names, or partial matches
2. **Limit Management**: Default to 50 records, adjust based on user needs
3. **Error Communication**: Relay error messages clearly to users
4. **Data Freshness**: Data comes directly from government sources

## Authentication

- **Optional**: API key can be provided via DATA_GOV_SG_API_KEY secret
- **Benefits**: Higher rate limits and more reliable access
- **Fallback**: Works without API key but may have limitations

## Integration Notes

- All responses are formatted for human readability
- Emojis provide visual context for different data types
- Error messages are user-friendly and actionable
- Logging is directed to stderr for debugging

## Development Considerations

- Server runs in Docker container for security
- Non-root user execution
- Environment variables for configuration
- Comprehensive error handling
- Timeout protection for API calls

This server enables Claude to provide accurate, real-time information about Singapore hawker centre closures, helping users plan visits and understand closure schedules.