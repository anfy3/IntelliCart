from dotenv import load_dotenv
load_dotenv()

from agno.agent import Agent
from agno.models.nvidia import Nvidia

from app.tools.review_tool import review_analysis_tool
from app.tools.review_scraper_tool import review_scraper_tool
from app.tools.database_tool import save_review_to_db


review_analysis_agent = Agent(
    name="Review Analysis Agent",
    model=Nvidia(id="meta/llama-3.3-70b-instruct"),
    instructions=[
        "Analyze review information.",
        "Summarize positives, negatives, sentiment, and suspicious review patterns.",
        "Be honest if review data is limited.",
        "Do not invent customer reviews."
    ],
    markdown=True
)


def run_review_analysis_agent(products, db=None):
    try:
        # For now we are using the main shortlisted product.
        # Later this can be made dynamic from extracted products.
        product_name = "Samsung Galaxy A55 5G"
        product_id = 1

        review_data = review_scraper_tool(product_name)

        basic_review = review_analysis_tool(product_name)

        response = review_analysis_agent.run(f"""
Analyze these review search results:

{review_data}

Product:
{product_name}

Return:
- overall sentiment
- positive points
- negative points
- review summary
- suspicious review warning if any
""")

        if db:
            save_review_to_db(
                db=db,
                product_id=product_id,
                review_summary=response.content,
                sentiment="Positive"
            )

        return {
            "product_name": product_name,
            "review_search_results": review_data,
            "basic_review": basic_review,
            "saved_to_db": True if db else False,
            "agent_output": response.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }