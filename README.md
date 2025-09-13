# Hawker Centre Closure Tracker MCP Server

A Model Context Protocol (MCP) server that provides real-time information about hawker centre closures in Singapore using data from data.gov.sg.

## Purpose

This MCP server provides a secure interface for AI assistants to access official Singapore government data about hawker centre closures, including closure dates, reopening dates, and reasons for closure.

## Features

### Current Implementation

- **`search_hawker_centres`** - Search for specific hawker centre closure information by keyword (name, location, etc.)
- **`get_all_closures`** - Retrieve all current hawker centre closure records with configurable limit

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- Optional: data.gov.sg API key for higher rate limits (recommended)

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop, you can ask:

- "Search for hawker centres with 'Bedok' in the name"
- "Find hawker centre closures in Jurong"
- "Show me all current hawker centre closures"
- "Get the latest 20 hawker centre closure records"
- "Is Ang Mo Kio hawker centre closed?"

## Architecture

```
Claude Desktop → MCP Gateway → Hawker Centre MCP Server → data.gov.sg API
                                         ↓
                              Docker Desktop Secrets
                              (DATA_GOV_SG_API_KEY)
```

## Development

### Local Testing

```bash
# Set environment variables for testing
export DATA_GOV_SG_API_KEY="your-api-key"

# Run directly
python hawker_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python hawker_server.py
```

### Adding New Tools

1. Add the function to `hawker_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing

- Verify Docker image built successfully
- Check catalog and registry files
- Ensure Claude Desktop config includes custom catalog
- Restart Claude Desktop

### Authentication Errors

- Verify secrets with `docker mcp secret list`
- Ensure secret names match in code and catalog
- Note: The server works without API key but may have rate limits

### API Errors

- Check if data.gov.sg API is accessible
- Verify the resource_id is correct
- Check API key validity if using one

## Security Considerations

- All secrets stored in Docker Desktop secrets
- Never hardcode credentials
- Running as non-root user
- Sensitive data never logged
- API key is optional but recommended for production use

## License

MIT License