from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.inventory import (
    InventoryCreate,
    InventoryUpdate,
    InventoryResponse
)

from services.inventory_service import (
    get_inventory,
    get_inventory_item,
    create_inventory,
    update_inventory,
    delete_inventory
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get("/", response_model=list[InventoryResponse])
def read_inventory(
    db: Session = Depends(get_db)
):
    return get_inventory(db)


@router.get("/{inventory_id}", response_model=InventoryResponse)
def read_inventory_item(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    item = get_inventory_item(db, inventory_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    return item


@router.post("/", response_model=InventoryResponse)
def create(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    return create_inventory(db, inventory)


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update(
    inventory_id: int,
    inventory: InventoryUpdate,
    db: Session = Depends(get_db)
):
    item = update_inventory(
        db,
        inventory_id,
        inventory
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    return item


@router.delete("/{inventory_id}")
def delete(
    inventory_id: int,
    db: Session = Depends(get_db)
):
    result = delete_inventory(
        db,
        inventory_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    return {
        "message": "Inventory deleted successfully"
    }
