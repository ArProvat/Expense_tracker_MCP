from fastmcp import FastMCP
import os
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from typing import List, Optional
from .models import Base, User, Expense
import datetime

user=User
expense=Expense
# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  
print(f"Using database URL: {DATABASE_URL}")
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(expire_on_commit=False, class_=AsyncSession, bind=engine)

# Initialize DB
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield

mcp = FastMCP("Expense Tracker MCP", lifespan=lifespan)

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mcp = FastMCP("MyServer")

# Configure CORS for browser-based clients
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins; use specific origins for security
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=[
            "mcp-protocol-version",
            "mcp-session-id",
            "Authorization",
            "Content-Type",
        ],
        expose_headers=["mcp-session-id"],
    )
]
# ------------------- MCP Tools -------------------

@mcp.tool
async def add_user(username: str, phone_number: str, Extra_metadata: Optional[dict] = None) -> dict:
    """Register a new user"""
    async with SessionLocal() as session:
        new_user = user(username=username, phone_number=phone_number, Extra_metadata=Extra_metadata)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return {
            "id": new_user.id,
            "username": new_user.username,
            "phone_number": new_user.phone_number
        }

@mcp.tool
async def add_expense(user_id: str, amount: int, category: Optional[str] = None,
                      subcategory: Optional[str] = None, description: Optional[str] = None,
                      date: Optional[datetime.datetime] = None,
                      Extra_metadata: Optional[dict] = None) -> dict:
    """Add a new expense for a user"""
    async with SessionLocal() as session:
        new_expense = expense(
            user_id=user_id,
            amount=amount,
            category=category,
            subcategory=subcategory,
            description=description,
            date=date or datetime.datetime.utcnow(),
            Extra_metadata=Extra_metadata
        )
        session.add(new_expense)
        await session.commit()
        await session.refresh(new_expense)
        return {
            "message": "Expense added successfully",
            "data": {
                "id": new_expense.id,
                "amount": new_expense.amount,
                "category": new_expense.category,
                "subcategory": new_expense.subcategory,
                "description": new_expense.description,
                "date": new_expense.date.isoformat(),
            }
        }

@mcp.tool
async def get_list_expenses(user_id: str, start_date: datetime.datetime, end_date: datetime.datetime) -> List[dict]:
    """Get all expenses for a user within a date range"""
    async with SessionLocal() as session:
        result = await session.execute(
            select(
                expense.id,
                expense.amount,
                expense.category,
                expense.subcategory,
                expense.description,
                expense.date,
            ).where(
                (expense.user_id == user_id) &
                (expense.date >= start_date) &
                (expense.date <= end_date)
            )
        )
        expenses = result.fetchall()
        return [dict(row._mapping) for row in expenses]

@mcp.tool
async def delete_expense(expense_id: str, user_id: str) -> dict:
    """Delete an expense by its ID"""
    async with SessionLocal() as session:
        exp = await session.get(expense, expense_id)
        if exp and exp.user_id == user_id:
            await session.delete(exp)
            await session.commit()
            return {"message": "Expense deleted successfully"}
        return {"message": "Expense not found"}

@mcp.tool
async def get_item_summary(user_id: str, category: str, start_date: datetime.datetime, end_date: datetime.datetime) -> dict:
    """Get item summary for a user within a date range"""
    async with SessionLocal() as session:
        result = await session.execute(
            select(
                expense.id,
                expense.category,
                expense.subcategory,
                expense.amount,
                expense.date,
            ).where(
                (expense.user_id == user_id) &
                (expense.category == category) &
                (expense.date >= start_date) &
                (expense.date <= end_date)
            )
        )
        expenses = result.fetchall()
        total_amount = sum(row._mapping["amount"] for row in expenses)
        return {
            "expenses": [dict(row._mapping) for row in expenses],
            "total_amount": total_amount,
        }

@mcp.tool
async def update_expense(
    user_id: str,
    expense_id: Optional[str] = None,
    amount: Optional[int] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    description: Optional[str] = None,
    date: Optional[datetime.datetime] = None,
    start_date: Optional[datetime.datetime] = None,
    end_date: Optional[datetime.datetime] = None,
) -> dict:
    """Update an expense by ID or filters; updates even if new data matches existing"""
    async with SessionLocal() as session:
        query = select(expense).where(expense.user_id == user_id)
        if expense_id:
            query = query.where(expense.id == expense_id)
        if start_date and end_date:
            query = query.where(expense.date >= start_date, expense.date <= end_date)
        if category:
            query = query.where(expense.category == category)

        result = await session.execute(query)
        exp = result.scalars().first()

        if not exp:
            return {"message": "Expense not found"}

        # Update all fields even if values are the same
        exp.amount = amount if amount is not None else exp.amount
        exp.category = category if category is not None else exp.category
        exp.subcategory = subcategory if subcategory is not None else exp.subcategory
        exp.description = description if description is not None else exp.description
        exp.date = date if date is not None else exp.date

        await session.commit()
        await session.refresh(exp)

        return {
            "message": "Expense updated successfully",
            "data": {
                "id": exp.id,
                "amount": exp.amount,
                "category": exp.category,
                "subcategory": exp.subcategory,
                "description": exp.description,
                "date": exp.date.isoformat(),
            },
        }

# ------------------- Resources -------------------

categories_path = os.path.join(os.path.dirname(__file__), "categories.json")
@mcp.resource("expense://categories", mime_type="application/json")
async def get_categories():
    """Get all categories"""
    with open(categories_path, "r", encoding="utf-8") as f:
        return f.read()
