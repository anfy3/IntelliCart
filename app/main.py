from fastapi import FastAPI

from app.database import engine, Base
import app.models

from app.routes import (
    product_routes,
    review_routes,
    recommendation_routes,
    promotion_routes,
    cross_sell_routes,
    upsell_routes,
    session_routes,
    search_history_routes,
    conversation_history_routes,
    chat_routes
)

app = FastAPI(
    title="IntelliCart API",
    description="Agentic AI Shopping Assistant Backend",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Home"])
def home():
    return {"message": "Welcome to IntelliCart Backend"}


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "service": "IntelliCart Backend",
        "version": "1.0.0"
    }


app.include_router(product_routes.router)
app.include_router(review_routes.router)
app.include_router(recommendation_routes.router)
app.include_router(promotion_routes.router)
app.include_router(cross_sell_routes.router)
app.include_router(upsell_routes.router)
app.include_router(session_routes.router)
app.include_router(search_history_routes.router)
app.include_router(conversation_history_routes.router)
app.include_router(chat_routes.router)