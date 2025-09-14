# Hawker Centre Closure Tracker MCP Server

A **Model Context Protocol (MCP)** server that provides real-time information on hawker centre closures in Singapore,
powered by data from [data.gov.sg](https://data.gov.sg).

> **Disclaimer**:
> This is an **unofficial** MCP server project, generated with Claude AI. While it is functional, please **review and
test thoroughly before using in production**.

---

## Purpose

This MCP server offers a secure interface for AI assistants to access official Singapore government data about hawker
centre closures.
It includes details such as closure dates, reopening dates, and reasons for closure.

---

## Features

### Implemented Tools

* **`search_hawker_centres`** – Search closure information by keyword (name, location, etc.)
* **`search_hawker_centres_by_address`** – Search for closures by street address
* **`get_all_hawker_centres`** – Retrieve all current hawker centre closure records (with configurable limits)

---

## Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) with MCP Toolkit enabled
* Docker MCP CLI plugin (`docker mcp` command)
* *(Optional but recommended)*: A [data.gov.sg API key](https://data.gov.sg/developer) for higher rate limits

---

## Usage Examples

In Claude Desktop, you can try prompts such as:

* "Search for hawker centres with 'Bedok' in the name"
* "Find hawker centre closures in Jurong"
* "Search for hawker centres by address on Ang Mo Kio Avenue 10"
* "Find hawker centres at Block 123 Toa Payoh Lorong 1"
* "Show me all hawker centres in Singapore"
* "Get all hawker centre cleaning schedules"
* "Is Ang Mo Kio hawker centre closed?"

---

## Installation

### Step 1: Build the Docker Image

```bash
docker build -t [MCP_SERVER_NAME] .
```

### Step 2: Create a Catalog Directory

```bash
mkdir -p ~/.docker/mcp/catalogs
```

### Step 3: Create a Catalog YAML File

Create a file named `hawker-centre-closure.yaml` (or any custom name) inside the catalogs directory:

> **Note**: Ensure the entry is placed under the `registry:` key, not at the root.

```yaml
version: 2
name: custom
displayName: Hawker Centre Closure Tracker
registry:
  hawker-centre-tracker:
    description: "Track hawker centre closures in Singapore using official data.gov.sg API"
    title: "Hawker Centre Closure Tracker"
    type: server
    dateAdded: "2025-01-15T00:00:00Z"
    image: hawker-mcp-server:latest
    tools:
      - name: search_hawker_centres
    # Uncomment the following section if you have a data.gov.sg API key
    # secrets:
    #   - name: DATA_GOV_SG_API_KEY
    #     env: DATA_GOV_SG_API_KEY
    #     example: "your-api-key-from-data-gov-sg"
    metadata:
      category: integration
      tags:
        - singapore
        - government-data
        - hawker-centres
        - food
      license: MIT
      owner: local
```

### Step 4: Configure Claude Desktop

Locate your Claude Desktop config file:

* **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
* **Linux**: `~/.config/Claude/claude_desktop_config.json`

Add your catalog under the `args` array. Example:

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v",
        "/var/run/docker.sock:/var/run/docker.sock",
        "-v",
        "[YOUR_HOME]/mcp:/mcp",
        "docker/mcp-gateway",
        "--catalog=/mcp/catalogs/docker-mcp.yaml",
        "--catalog=/mcp/catalogs/hawker-centre-mcp.yaml",
        "--config=/mcp/config.yaml",
        "--registry=/mcp/registry.yaml",
        "--tools-config=/mcp/tools.yaml",
        "--transport=stdio"
      ]
    }
  }
}
```

Replace `[YOUR_HOME]` with:

* macOS: `/Users/your_username/.docker/mcp`
* Windows: `C:\\Users\\your_username\\.docker\\mcp` (double backslashes required)
* Linux: `/home/your_username/.docker/mcp`

### Step 5: Restart Claude Desktop

Quit and restart Claude Desktop. The tools should now appear in the interface.

### Step 6: Verify Installation

* Check the server list:

```bash
docker mcp server list
```

* If your server does not appear, check logs:

    * **macOS**: `~/Library/Application Support/Claude/logs`
    * **Windows**: `%APPDATA%\Claude\logs`
    * **Linux**: `~/.config/Claude/logs`

---

## Architecture

```
Claude Desktop → MCP Gateway → Hawker Centre MCP Server → data.gov.sg API
                                         ↓
                              Docker Desktop Secrets
                              (DATA_GOV_SG_API_KEY)
```

---

## Development

### Local Testing

```bash
# Set environment variables
export DATA_GOV_SG_API_KEY="your-api-key"

# Run server directly
python hawker_server.py

# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python hawker_server.py
```

### Adding New Tools

1. Add the function in `hawker_server.py`
2. Decorate it with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

---

## Troubleshooting

### Tools Not Appearing

* Confirm Docker image built successfully
* Verify catalog and registry files
* Ensure Claude config includes your catalog
* Restart Claude Desktop

### Authentication Errors

* Check secrets with `docker mcp secret list`
* Ensure environment variable names match in both code and catalog
* Without an API key, the server works but may be rate-limited

### API Errors

* Verify [data.gov.sg API](https://data.gov.sg) is online
* Check the correct `resource_id` is used
* Confirm API key validity

---

## Security Considerations

* Store all secrets in Docker Desktop Secrets
* Never hardcode credentials in code
* Run server as a non-root user
* Avoid logging sensitive data
* API key is optional but recommended for production use

---

## License

MIT License