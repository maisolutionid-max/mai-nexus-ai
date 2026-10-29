
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.services import order_service
from app.services.pricing import calculate_price

router = APIRouter()


@router.get("/orders", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return order_service.get_orders(db)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order(db, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order tidak ditemukan",
        )

    return order


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_data = order.model_dump()

    # Harga dihitung dari jenis layanan dan berat.
    order_data["total_price"] = calculate_price(
        order_data["service_type"],
        order_data["weight"],
    )

    order_to_create = OrderCreate(**order_data)
    return order_service.create_order(db, order_to_create)


@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
):
    updated = order_service.update_order(db, order_id, order)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order tidak ditemukan",
        )

    return updated


@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    deleted = order_service.delete_order(db, order_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order tidak ditemukan",
        )

    return None

   
