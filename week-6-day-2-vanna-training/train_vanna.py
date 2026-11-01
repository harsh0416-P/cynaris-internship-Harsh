import asyncio
import json
import uuid
from pathlib import Path

from vanna.core.user.models import User
from vanna.core.tool import ToolContext
from vanna.integrations.local.agent_memory import DemoAgentMemory

from training.training_examples import training_examples


async def main():
    # Initialize Vanna memory
    memory = DemoAgentMemory()

    # Create a user
    user = User(
        id="cynaris-trainee",
        username="Harsh"
    )

    # Create tool context
    context = ToolContext(
        user=user,
        conversation_id=str(uuid.uuid4()),
        request_id=str(uuid.uuid4()),
        agent_memory=memory
    )

    # Store each question and SQL example
    for example in training_examples:
        content = (
            "SQL TRAINING EXAMPLE\n"
            f"Question: {example['question']}\n"
            f"SQL: {example['sql']}"
        )

        await memory.save_text_memory(content, context)

    print(f"Stored {len(training_examples)} SQL examples.")

    # Retrieve stored examples
    results = await memory.get_recent_text_memories(
        context,
        limit=10
    )

    print("\nRETRIEVED TRAINING EXAMPLES")

    for index, result in enumerate(results, start=1):
        print(f"\nExample {index}")
        print(result.content)


if __name__ == "__main__":
    asyncio.run(main())