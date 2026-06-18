from app.models import Product, Review, Recommendation


def save_products_to_db(db, products: list):
    saved_products = []

    for item in products:
        existing_product = db.query(Product).filter(
            Product.name == item.get("name")
        ).first()

        if existing_product:
            saved_products.append(existing_product)
            continue
        
        product = Product(
            name=item.get("name"),
            category=item.get("category"),
            brand=item.get("brand"),
            price=item.get("price"),
            rating=item.get("rating"),
            specs=item.get("specs"),
            source_url=item.get("source_url"),
            availability=item.get("availability", "Available")
        )

        db.add(product)
        db.commit()
        db.refresh(product)
        saved_products.append(product)

    return saved_products


def save_review_to_db(db, product_id: int, review_summary: str, sentiment: str = "Positive"):
    review = Review(
        product_id=product_id,
        review_text=review_summary,
        sentiment=sentiment,
        source="AI review summary",
        suspicious_flag="No"
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def save_recommendation_to_db(db, product_id: int, reason: str, confidence_score: float):
    recommendation = Recommendation(
        product_id=product_id,
        reason=reason,
        confidence_score=confidence_score
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation

def save_recommendation_output(
    db,
    product_id,
    recommendation_text,
    confidence_score
):
    recommendation = Recommendation(
        product_id=product_id,
        reason=recommendation_text,
        confidence_score=confidence_score
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation