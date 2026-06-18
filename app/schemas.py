from pydantic import BaseModel
from typing import Optional, Any


class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    specs: Optional[str] = None
    source_url: Optional[str] = None
    availability: Optional[str] = "Available"


class ProductResponse(ProductCreate):
    id: int


class ReviewCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    review_text: str
    rating: Optional[float] = None
    sentiment: Optional[str] = None
    source: Optional[str] = None
    suspicious_flag: Optional[str] = "No"


class ReviewResponse(ReviewCreate):
    id: int


class RecommendationCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    recommendation_reason: str
    confidence_score: Optional[float] = None
    alternative_option: Optional[str] = None


class RecommendationResponse(RecommendationCreate):
    id: int


class PromotionCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    offer_title: str
    discount: Optional[str] = None
    valid_until: Optional[str] = None


class PromotionResponse(PromotionCreate):
    id: int


class CrossSellCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    suggested_product: str
    reason: Optional[str] = None


class CrossSellResponse(CrossSellCreate):
    id: int


class UpsellCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    better_product: str
    reason: Optional[str] = None
    price_difference: Optional[float] = None


class UpsellResponse(UpsellCreate):
    id: int


class SessionCreate(BaseModel):
    session_code: str
    user_preference: Optional[str] = None


class SessionResponse(SessionCreate):
    id: int


class SearchHistoryCreate(BaseModel):
    session_id: Optional[int] = None
    query: str


class SearchHistoryResponse(SearchHistoryCreate):
    id: int


class ConversationHistoryCreate(BaseModel):
    session_id: Optional[int] = None
    user_message: str
    bot_response: Optional[str] = None


class ConversationHistoryResponse(ConversationHistoryCreate):
    id: int


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None


class ChatResponse(BaseModel):
    status: str
    user_message: str
    workflow: Optional[dict[str, Any]] = None
    final_response: Any

# ---------------- Agent Schemas ----------------

class IntentAgentOutput(BaseModel):
    category: Optional[str] = None
    brand: Optional[str] = None
    budget: Optional[float] = None
    usage: Optional[str] = None
    priorities: Optional[str] = None
    deal_breakers: Optional[str] = None


class ProductRetrievalOutput(BaseModel):
    product_name: str
    price: Optional[float] = None
    features: Optional[str] = None
    availability: Optional[str] = None
    source_url: Optional[str] = None


class ReviewAnalysisOutput(BaseModel):
    product_name: str
    positive_points: Optional[str] = None
    negative_points: Optional[str] = None
    sentiment: Optional[str] = None
    suspicious_review_flag: Optional[str] = "No"


class RecommendationAgentOutput(BaseModel):
    top_recommendation: Optional[str] = None
    runner_up: Optional[str] = None
    reasoning: Optional[str] = None
    confidence_score: Optional[float] = None
    upsell_suggestion: Optional[str] = None
    cross_sell_suggestion: Optional[str] = None
    promotion_suggestion: Optional[str] = None


class MemoryAgentOutput(BaseModel):
    session_id: Optional[str] = None
    last_query: Optional[str] = None


class OrchestratorOutput(BaseModel):
    status: str
    user_message: str
    intent: Optional[Any] = None
    products: Optional[Any] = None
    reviews: Optional[Any] = None
    recommendation: Optional[Any] = None
    memory: Optional[Any] = None
    final_response: Optional[Any] = None


# ---------------- Tool Schemas ----------------

class WebSearchToolInput(BaseModel):
    query: str


class WebSearchToolOutput(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    snippet: Optional[str] = None


class ProductComparisonToolInput(BaseModel):
    products: list[Any]
    user_priority: Optional[str] = None


class ReviewAnalysisToolInput(BaseModel):
    product_name: str


class RecommendationToolInput(BaseModel):
    user_message: str
    products: list[Any]
    reviews: Optional[Any] = None


class MemoryToolInput(BaseModel):
    session_id: str
    key: str
    value: str


class DatabaseRetrievalToolInput(BaseModel):
    category: Optional[str] = None
    brand: Optional[str] = None