def recommendation_tool(products: list, reviews: dict, user_message: str) -> str:
    return f"""
Choose the best product for this user.

User request:
{user_message}

Products:
{products}

Review summary:
{reviews}

Return:
- top recommendation
- runner-up
- reasons
- pros and cons
- confidence score
"""