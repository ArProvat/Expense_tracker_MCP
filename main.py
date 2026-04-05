from MCP.Expense_tracker_mcp import mcp , middleware
from fastapi.middleware.cors import CORSMiddleware


# Use the private _app attribute to add middleware

if __name__ == "__main__":
    print("Expense tracker MCP is starting...")
    # FastMCP.run() starts uvicorn internally - host must be 0.0.0.0 for Docker
    mcp.run(transport="http", host="0.0.0.0", port=8888, middleware=middleware)
