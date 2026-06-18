def product_comparison_tool(products: list, user_priority: str = "") -> str:
    return f"""
Compare these products fairly based on the user's priority.

User priority:
{user_priority}

Products:
{products}
"""