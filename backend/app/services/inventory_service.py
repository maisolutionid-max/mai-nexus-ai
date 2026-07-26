from sqlalchemy.orm import Session

from models.inventory import Inventory
from schemas.inventory import InventoryCreate, InventoryUpdate


def get_inventory(db: Session):
    return db.query(Inventory).all()


def get_inventory_item(db: Session, inventory_id: int):
    return db.query(Inventory).filter(
        Inventory.id == inventory_id
    ).first()


def create_inventory(
    db: Session,
    inventory: InventoryCreate
):
    db_inventory = Inventory(**inventory.model_dump())

    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)

    return db_inventory


def update_inventory(
    db: Session,
    inventory_id: int,
    inventory: InventoryUpdate
):
    item = get_inventory_item(db, inventory_id)

    if not item:
        return None

    update_data = inventory.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


def delete_inventory(
    db: Session,
    inventory_id: int
):
    item = get_inventory_item(db, inventory_id)

    if not item:
        return False

    db.delete(item)
    db.commit()

    return True
