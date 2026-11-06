
from pathlib import Path
from uuid import uuid4
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import User, UserResolver, RequestContext
from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.tools import RunSqlTool


# ----------------------------------------
# 1. Project paths
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "sales.db"
STATIC_DIR = BASE_DIR / "static"

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

if not STATIC_DIR.exists():
    raise FileNotFoundError(f"Static directory not found: {STATIC_DIR}")


# ----------------------------------------
# 2. Local user authentication
# ----------------------------------------

class LocalUserResolver(UserResolver):

    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="local-user",
            username="local-user",
            group_memberships=["user"]
        )


# ----------------------------------------
# 3. Ollama LLM configuration
# ----------------------------------------

llm = OllamaLlmService(
    model="llama3.2:1b",
    host="http://localhost:11434",
    temperature=0.1
)


# ----------------------------------------
# 4. SQLite database connection
# ----------------------------------------

sql_runner = SqliteRunner(
    database_path=str(DB_PATH)
)


# ----------------------------------------
# 5. Register SQL tool
# ----------------------------------------

registry = ToolRegistry()

registry.register_local_tool(
    RunSqlTool(
        sql_runner=sql_runner,
        custom_tool_description=(
            "Execute read-only SQL SELECT queries on the sales database. "
            "The sales table contains: sale_id, customer_name, "
            "product, category, amount, city, quantity. "
            "Use SQLite SQL syntax. Never modify database records."
        )
    ),
    access_groups=["user"]
)


# ----------------------------------------
# 6. Agent memory
# ----------------------------------------

agent_memory = DemoAgentMemory(max_items=1000)


# ----------------------------------------
# 7. Create Vanna agent
# ----------------------------------------

agent = Agent(
    llm_service=llm,
    tool_registry=registry,
    user_resolver=LocalUserResolver(),
    agent_memory=agent_memory
)


# ----------------------------------------
# 8. FastAPI application
# ----------------------------------------

app = FastAPI(
    title="Cynaris NL SQL Dashboard",
    description="Natural Language SQL Dashboard using Vanna, Ollama and SQLite",
    version="1.0.0"
)


# Serve static frontend files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ----------------------------------------
# 9. Request model
# ----------------------------------------

class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


# ----------------------------------------
# 10. Dashboard homepage
# ----------------------------------------

@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")


# ----------------------------------------
# 11. Health check
# ----------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "running",
        "database": "connected" if DB_PATH.exists() else "missing",
        "model": "llama3.2:1b"
    }


# ----------------------------------------
# 12. Natural Language SQL endpoint
# ----------------------------------------

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
                text = getattr(
                    simple_component,
                    "text",
                    None
                )

                if text:
                    responses.append(text)

        return {
            "success": True,
            "conversation_id": conversation_id,
            "question": request.question,
            "ai_answer": responses[-1] if responses else None,
            "database_result": responses[0] if responses else None,
            "responses": responses
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ----------------------------------------
# 13. Application information
# ----------------------------------------

@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")