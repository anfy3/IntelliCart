from app.agents.intent_agent import run_intent_agent
from app.agents.product_retrieval_agent import run_product_retrieval_agent
from app.agents.review_analysis_agent import run_review_analysis_agent
from app.agents.recommendation_agent import run_recommendation_agent
from app.agents.memory_agent import run_memory_agent


def run_orchestrator(user_message: str, session_id: str = "default", db=None):
    try:
        intent_result = run_intent_agent(user_message)
    except Exception as e:
        intent_result = {"error": str(e)}

    try:
        product_result = run_product_retrieval_agent(
            user_message=user_message,
            intent=intent_result,
            db=db
        )
    except Exception as e:
        product_result = {"error": str(e)}

    try:
        review_result = run_review_analysis_agent(
        products=product_result,
        db=db
)
    except Exception as e:
        review_result = {"error": str(e)}

    try:
        recommendation_result = run_recommendation_agent(
            user_message=user_message,
            products=product_result,
            reviews=review_result,
            db=db
)
    except Exception as e:
        recommendation_result = {
            "error": str(e),
            "fallback_response": "Recommendation could not be generated because the model provider failed."
        }

    try:
        memory_result = run_memory_agent(
            db=db,
            session_id=str(session_id),
            user_message=user_message,
            bot_response=recommendation_result
        )
    except Exception as e:
        memory_result = {"error": str(e)}

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