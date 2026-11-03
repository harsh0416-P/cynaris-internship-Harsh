
from typing import List, Optional

from vanna.core.system_prompt import SystemPromptBuilder
from vanna.core.user.models import User
from vanna.core.tool import ToolSchema


class SQLTrainingPromptBuilder(SystemPromptBuilder):

    def __init__(self, examples):
        self.examples = examples

    async def build_system_prompt(
        self,
        user: User,
        tools: List[ToolSchema]
    ) -> Optional[str]:

        tool_names = [tool.name for tool in tools]

        prompt = """
You are an AI SQL data analyst.

DATABASE:
- Database: SQLite
- Table: sales
- Columns: sale_id, customer_name, product,
  category, amount, city, quantity

RULES:
1. Generate SQL using SQLite syntax.
2. Use only the sales table and its known columns.
3. Use the provided SQL examples as guidance.
4. Check column names and aggregation logic carefully.
5. Never invent database values.
6. Execute only read-only SELECT queries.
7. Explain results using the actual database output.
"""

        prompt += "\n\nRELEVANT SQL TRAINING EXAMPLES:\n"

        for index, example in enumerate(self.examples, start=1):
            prompt += (
                f"\nExample {index}\n"
                f"Question: {example['question']}\n"
                f"SQL: {example['sql']}\n"
            )

        prompt += f"\nAVAILABLE TOOLS: {', '.join(tool_names)}"

        return prompt
