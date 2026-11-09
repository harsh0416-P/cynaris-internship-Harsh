
from pathlib import Path
from uuid import uuid4
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import User, UserResolver, RequestContext
from vanna.core.tool import ToolContext
from vanna.core.enhancer.default import DefaultLlmContextEnhancer

from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.tools import RunSqlTool

from sql_audit import AuditedSqlRunner
from training_data import TRAINING_DATA


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DB_PATH = (
    PROJECT_DIR
    / "week-6-day-5-nl-sql-dashboard"
    / "data"
    / "sales.db"
)

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")


# --------------------------------------------------
# USER RESOLVER
# --------------------------------------------------

class LocalUserResolver(UserResolver):

    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="local-user",
            username="local-user",
            group_memberships=["user"]
        )


# --------------------------------------------------
# Vanna SQL CONFIGURATION
# --------------------------------------------------

llm = OllamaLlmService(
    model="llama3.2:1b",
    host="http://localhost:11434",
    temperature=0.1
)

sql_runner = AuditedSqlRunner(database_path=str(DB_PATH))

registry = ToolRegistry()

registry.register_local_tool(
    RunSqlTool(
        sql_runner=sql_runner,
        custom_tool_description=(
            "Execute read-only SQL SELECT queries on the sales database. "
            "The sales table contains sale_id, customer_name, product, "
            "category, amount, city and quantity. "
            "Use SQLite SQL syntax. Never modify database records."
        )
    ),
    access_groups=["user"]
)


# --------------------------------------------------
# AGENT MEMORY
# --------------------------------------------------

agent_memory = DemoAgentMemory(max_items=1000)


# --------------------------------------------------
# LOAD FIVE TRAINING EXAMPLES
# --------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    user = User(
        id="local-user",
        username="local-user",
        group_memberships=["user"]
    )

    context = ToolContext(
        user=user,
        conversation_id="w7d4-training",
        request_id=str(uuid4()),
        agent_memory=agent_memory
    )

    for item in TRAINING_DATA:

        content = (
            f"Question: {item['question']}\n"
            f"SQL: {item['sql'].strip()}"
        )

        await agent_memory.save_text_memory(content, context)

    print(f"Loaded {len(TRAINING_DATA)} SQL examples into memory.")

    yield


# --------------------------------------------------
# VANNA AGENT
# --------------------------------------------------

agent = Agent(
    llm_service=llm,
    tool_registry=registry,
    user_resolver=LocalUserResolver(),
    agent_memory=agent_memory,
    llm_context_enhancer=DefaultLlmContextEnhancer(agent_memory)
)


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Cynaris W7D4 Vanna Integration",
    description="Natural Language SQL Analyst with SQL Audit Logging",
    version="2.0.0",
    lifespan=lifespan
)


# --------------------------------------------------
# REQUEST MODEL
# --------------------------------------------------

class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


# --------------------------------------------------
# API ROUTES
# --------------------------------------------------

@app.get("/")
async def home():

    return {
        "message": "Cynaris W7D4 Vanna SQL Analyst API running",
        "status": "running"
    }


@app.get("/health")
async def health():

    return {
        "status": "running",
        "database": "connected" if DB_PATH.exists() else "missing",
        "model": "llama3.2:1b",
        "audit_logging": "enabled"
    }


@app.post("/cia/sql-analyst")
async def sql_analyst(request: QueryRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    conversation_id = request.conversation_id or str(uuid4())

    request_context = RequestContext(metadata={})

    responses = []

    try:

        async for component in agent.send_message(
            request_context,
            request.question,
            conversation_id=conversation_id
        ):

            simple_component = getattr(
                component,
                "simple_component",
                None
            )

            if simple_component:

                text = getattr(simple_component, "text", None)

                if text:
                    responses.append(text)

        return {
            "success": True,
            "conversation_id": conversation_id,
            "question": request.question,
            "ai_answer": responses[-1] if responses else None,
            "responses": responses
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
