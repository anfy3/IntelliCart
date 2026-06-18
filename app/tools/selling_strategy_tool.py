def selling_strategy_tool(product_name: str, category: str = "", budget: float | None = None) -> dict:
    try:
        return {
            "upsell": f"Suggest a slightly better model than {product_name} if it gives better value within the user's budget.",
            "cross_sell": f"Suggest useful accessories related to {category}, such as case, charger, earbuds, or warranty plan.",
            "promotion": "Check for exchange offers, bank discounts, festival offers, and student discounts.",
            "note": "Suggestions should be relevant and not forced."
        }

    except Exception as e:
        return {"error": str(e)}