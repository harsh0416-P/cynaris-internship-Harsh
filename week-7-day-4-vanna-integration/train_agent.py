import asyncio
import uuid

from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.core.tool import ToolContext
from vanna.core.user import User

from training_data import TRAINING_DATA


async def main():
    memory = DemoAgentMemory(max_items=1000)

    user = User(
        id="local-user",
        username="local-user",
        group_memberships=["user"]
    )

    context = ToolContext(
        user=user,
        conversation_id="w7d4-training",
        request_id=str(uuid.uuid4()),
        agent_memory=memory
    )

    # Store five question-SQL examples
    for item in TRAINING_DATA:
        content = (
            f"Question: {item['question']}\n"
            f"SQL: {item['sql'].strip()}"
        )

        await memory.save_text_memory(content, context)

    print("Stored examples:", len(TRAINING_DATA))

    # Verify memory retrieval
    results = await memory.search_text_memories(
        query="Show total sales revenue by city",
        context=context,
        limit=5,
        similarity_threshold=0.0
    )

    print("\nRetrieved examples:")
    for result in results:
        print(result.memory.content)
        print("-" * 40)


if __name__ == "__main__":
    asyncio.run(main())