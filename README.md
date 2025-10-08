# 💰 Expense Tracker MCP Server

An intelligent expense tracking system built with the Model Context Protocol (MCP), allowing Claude AI to manage your personal finances through natural conversation.

## 🌟 Features

- **User Management**: Register and manage multiple users with phone numbers
- **Expense Tracking**: Add, update, and delete expenses with detailed metadata
- **Smart Categorization**: Organize expenses by categories and subcategories
- **Date Range Queries**: Filter expenses by custom date ranges
- **Item Summaries**: Get detailed breakdowns of spending by category
- **Natural Language Interface**: Interact with your expense data through Claude AI

## 🚀 What is MCP?

The Model Context Protocol (MCP) is an open standard by Anthropic that enables AI assistants like Claude to securely connect with external data sources and tools. This project implements an MCP server that gives Claude the ability to manage expense data in real-time.

## 🛠️ Tech Stack

- **FastMCP**: MCP server implementation
- **PostgreSQL**: Robust database for expense data
- **SQLAlchemy**: Async ORM for database operations
- **Docker**: Containerized PostgreSQL deployment
- **Pydantic**: Data validation

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Claude Desktop App

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ArProvat/expense-tracker-mcp.git
cd expense-tracker-mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start PostgreSQL Database

```bash
docker-compose up -d
```

This will start a PostgreSQL container with:

- **Host**: localhost
- **Port**: 5432
- **Database**: expenses
- **User**: postgres
- **Password**: postgres

### 4. Run Database Migrations

```bash
alembic upgrade head
```

### 5. Configure Claude Desktop

Add the MCP server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "expense-tracker": {
      "command": "python",
      "args": ["/path/to/your/expense-tracker-mcp/main.py"]
    }
  }
}
```

### 6. Restart Claude Desktop

Close and reopen Claude Desktop to load the MCP server.

## 📖 Usage

Once connected, you can interact with Claude naturally:

### Register a User

```
"Register me as a user with phone number +1234567890"
```

### Add Expenses

```
"Add an expense of $50 for groceries today"
"I spent 1500 taka on transportation yesterday"
```

### View Expenses

```
"Show me all my expenses from last week"
"What did I spend in January 2025?"
```

### Get Summaries

```
"Give me a summary of my food expenses this month"
"How much did I spend on entertainment?"
```

### Update Expenses

```
"Update my last grocery expense to $45"
"Change the category of yesterday's expense to 'Shopping'"
```

### Delete Expenses

```
"Delete my last expense"
"Remove the expense with ID abc123"
```

## 🎯 Available MCP Functions
### Tool
- `add_user` - Register a new user
- `add_expense` - Add a new expense entry
- `get_list_expenses` - Retrieve expenses by date range
- `delete_expense` - Remove an expense
- `get_item_summary` - Get spending summary by category
- `update_expense` - Modify existing expense details
### Resource
- `categories.json`-Define all categories and subcategories 

## 📊 Database Schema

The system uses PostgreSQL to store:

- User profiles with contact information
- Expense records with amounts, categories, and dates
- Metadata for custom fields and tags

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for creating MCP and Claude
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- The open-source community for the amazing tools and libraries

## 📧 Contact

For questions or feedback, feel free to reach out or open an issue!

---

**Built with ❤️ using Model Context Protocol**
