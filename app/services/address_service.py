from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from geopy.distance import geodesic
from typing import List

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate
import logging

logger = logging.getLogger(__name__)

def create_address(db: Session, address_data: AddressCreate) -> Address:
    try:
        address = Address(**address_data.model_dump())
        db.add(address)
        db.commit()
        db.refresh(address)

        logger.info(f"Address created with ID {address.id}")
        return address

    except SQLAlchemyError:
        db.rollback()
        logger.error("Database error during address creation", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create address")
    
def update_address(db: Session, address_id: int, update_data: AddressUpdate) -> Address:
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Attempt to update non-existing address ID {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")

    try:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)

        logger.info(f"Address updated with ID {address.id}")
        return address

    except SQLAlchemyError:
        db.rollback()
        logger.error("Database error during address update", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update address")
    
def delete_address(db: Session, address_id: int) -> None:
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Attempt to delete non-existing address ID {address_id}")
        raise HTTPException(status_code=404, detail="Address not found")

    try:
        db.delete(address)
        db.commit()

        logger.info(f"Address deleted with ID {address_id}")

    except SQLAlchemyError:
        db.rollback()
        logger.error("Database error during address deletion", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete address")
    
def get_addresses_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    distance_km: float
) -> List[Address]:

    origin = (latitude, longitude)

    addresses = db.query(Address).all()
    nearby_addresses = []

    for address in addresses:
        target = (address.latitude, address.longitude)
        distance = geodesic(origin, target).km

        if distance <= distance_km:
            nearby_addresses.append(address)

    logger.info(
        f"Nearby search performed at ({latitude}, {longitude}) within {distance_km} km"
    )

    return nearby_addresses