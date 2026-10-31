
from pathlib import Path
from uuid import uuid4
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import User, UserResolver, RequestContext
from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.tools import RunSqlTool

from training.training_examples import training_examples
from training.custom_prompt import SQLTrainingPromptBuilder


class LocalUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="local-user",
            username="Harsh",
            group_memberships=["user"]
        )


# Reuse the W6D1 database without copying it
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "week-6-day-1-vanna"
    / "data"
    / "sales.db"
)

if not DATABASE_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DATABASE_PATH}")


llm = OllamaLlmService(
    model="llama3.2:1b",
    host="http://localhost:11434",
    temperature=0.1
)

sql_runner = SqliteRunner(database_path=str(DATABASE_PATH))

registry = ToolRegistry()

registry.register_local_tool(
    RunSqlTool(
        sql_runner=sql_runner,
        custom_tool_description=(
            "Execute read-only SELECT queries on the sales database. "
            "The sales table contains sale_id, customer_name, product, "
            "category, amount, city, and quantity. Use SQLite syntax."
        )
    ),
    access_groups=["user"]
)

agent_memory = DemoAgentMemory(max_items=1000)

prompt_builder = SQLTrainingPromptBuilder(training_examples)

agent = Agent(
    llm_service=llm,
    tool_registry=registry,
    user_resolver=LocalUserResolver(),
    agent_memory=agent_memory,
    system_prompt_builder=prompt_builder
)

app = FastAPI(
    title="Cynaris W6D2 Trained SQL Analyst",
    description="SQL analyst using domain-specific question-SQL examples",
    version="2.0.0"
)


class QueryRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


@app.get("/")
async def home():
    return {
        "status": "running",
        "project": "Cynaris W6D2",
        "training_examples": len(training_examples)
    }


@app.post("/cia/sql-analyst")
async def sql_analyst(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    conversation_id = request.conversation_id or str(uuid4())
    request_context = RequestContext(metadata={})
    responses = []

    try:
        async for component in agent.send_message(
            request_context,
            request.question,
            conversation_id=conversation_id
        ):
            simple_component = getattr(component, "simple_component", None)

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
        raise HTTPException(status_code=500, detail=str(error))
