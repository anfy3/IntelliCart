from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String)
    brand = Column(String)
    price = Column(Float)
    rating = Column(Float)
    specs = Column(Text)
    source_url = Column(String)
    availability = Column(String, default="Available")

    reviews = relationship("Review", back_populates="product")
    recommendations = relationship("Recommendation", back_populates="product")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    review_text = Column(Text)
    rating = Column(Float)
    sentiment = Column(String)
    source = Column(String)
    suspicious_flag = Column(String, default="No")

    product = relationship("Product", back_populates="reviews")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    reason = Column(Text)
    confidence_score = Column(Float)

    product = relationship("Product", back_populates="recommendations")


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    offer_title = Column(String)
    discount = Column(String)
    valid_until = Column(String)


class CrossSell(Base):
    __tablename__ = "cross_sells"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    suggested_product = Column(String)
    reason = Column(Text)


class Upsell(Base):
    __tablename__ = "upsells"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    better_product = Column(String)
    reason = Column(Text)
    price_difference = Column(Float)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, unique=True)
    user_preference = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    query = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConversationHistory(Base):
    __tablename__ = "conversation_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    user_message = Column(Text)
    bot_response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)