from mcp.server.fastmcp import FastMCP
from tools.hotel_tools import register_hotel_tools
from tools.weather_tools import register_weather_tools
from tools.aviation_tools import register_aviation_tools

# Initialize the central MCP server
mcp = FastMCP("Multi-Agent Travel MCP Server")

# Register all domain-specific tool modules
register_hotel_tools(mcp)
register_weather_tools(mcp)
register_aviation_tools(mcp)

if __name__ == "__main__":
    mcp.run()