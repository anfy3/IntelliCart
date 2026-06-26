import logging

from app.agents.intent_agent import run_intent_agent
from app.agents.product_retrieval_agent import run_product_retrieval_agent
from app.agents.review_analysis_agent import run_review_analysis_agent
from app.agents.recommendation_agent import run_recommendation_agent
from app.agents.memory_agent import run_memory_agent

from app.tools.guardrail_tool import validate_user_query
from app.telemetry import tracer

logger = logging.getLogger("IntelliCart")
logger.setLevel(logging.INFO)


def run_orchestrator(user_message: str, session_id: str = "default", db=None):

    logger.info("Workflow started")

    logger.info("Starting Guardrail Validation")
    with tracer.start_as_current_span("Guardrail Validation"):
        guardrail_result = validate_user_query(user_message)

    if not guardrail_result["is_valid"]:
        logger.warning(f"Request blocked by guardrails: {guardrail_result['error']}")
        return {
            "status": "blocked",
            "user_message": user_message,
            "error": guardrail_result["error"]
        }

    try:
        logger.info("Starting Intent Agent")
        with tracer.start_as_current_span("Intent Agent"):
            intent_result = run_intent_agent(user_message)
        logger.info("Intent Agent completed")
    except Exception as e:
        logger.error(f"Intent Agent failed: {str(e)}")
        intent_result = {"error": str(e)}

    try:
        logger.info("Starting Product Retrieval Agent")
        with tracer.start_as_current_span("Product Retrieval Agent"):
            product_result = run_product_retrieval_agent(
                user_message=user_message,
                intent=intent_result,
                db=db
            )
        logger.info("Product Retrieval Agent completed")
    except Exception as e:
        logger.error(f"Product Retrieval Agent failed: {str(e)}")
        product_result = {"error": str(e)}

    extracted_products = product_result.get("extracted_products", [])
    logger.info(f"Extracted product count: {len(extracted_products)}")

    try:
        logger.info("Starting Review Analysis Agent")
        with tracer.start_as_current_span("Review Analysis Agent"):
            review_result = run_review_analysis_agent(
                products=extracted_products,
                db=db
            )
        logger.info("Review Analysis Agent completed")
    except Exception as e:
        logger.error(f"Review Analysis Agent failed: {str(e)}")
        review_result = {"error": str(e)}

    try:
        logger.info("Starting Recommendation Agent")
        with tracer.start_as_current_span("Recommendation Agent"):
            recommendation_result = run_recommendation_agent(
                user_message=user_message,
                products=extracted_products,
                reviews=review_result,
                db=db
            )
        logger.info("Recommendation Agent completed")
    except Exception as e:
        logger.error(f"Recommendation Agent failed: {str(e)}")
        recommendation_result = {
            "error": str(e),
            "fallback_response": "Recommendation could not be generated because the model provider failed."
        }

    try:
        logger.info("Starting Memory Agent")
        with tracer.start_as_current_span("Memory Agent"):
            memory_result = run_memory_agent(
                db=db,
                session_id=str(session_id),
                user_message=user_message,
                bot_response=str(recommendation_result)
            )
        logger.info("Memory Agent completed")
    except Exception as e:
        logger.error(f"Memory Agent failed: {str(e)}")
        memory_result = {"error": str(e)}

    logger.info("Workflow completed successfully")

    return {
        "status": "success",
        "user_message": user_message,
        "workflow": {
            "step_1_intent_understanding": intent_result,
            "step_2_product_retrieval": product_result,
            "step_3_review_analysis": review_result,
            "step_4_recommendation": recommendation_result,
            "step_5_memory_update": memory_result
        },
        "final_response": recommendation_result
    }