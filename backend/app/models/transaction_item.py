from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False,
        default=1
    )

    unit_price = Column(
        Float,
        nullable=False,
        default=0
    )

    subtotal = Column(
        Float,
        nullable=False,
        default=0
    )

    transaction = relationship(
        "Transaction",
        back_populates="items"
    )

    product = relationship("Product")
