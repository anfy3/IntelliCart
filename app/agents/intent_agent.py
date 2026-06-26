import logging
logger = logging.getLogger("IntelliCart")
logger.info("Starting Intent Agent")

from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.nvidia import Nvidia

intent_agent = Agent(
    name="Intent Understanding Agent",
    model=Nvidia(id="meta/llama-3.3-70b-instruct"),
    instructions=[
        "Extract the user's shopping intent.",
        "Find product category, brand, budget, usage, priorities, and deal breakers.",
        "Return the result clearly."
    ],
    markdown=True
)


def run_intent_agent(user_message: str):
    response = intent_agent.run(f"""
Extract intent from this user query:

{user_message}

Return:
- category
- brand
- budget
- usage
- priorities
- deal_breakers
""")
    return response.content

logger.info("Workflow completed successfully")