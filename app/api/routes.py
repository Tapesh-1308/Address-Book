from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from app.db.session import get_db
from app.schemas.address import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
)
from app.services import address_service

router = APIRouter(prefix="/addresses", tags=["Addresses"])

logger = logging.getLogger(__name__)

@router.post("/", response_model=AddressResponse, status_code=201)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
):
    logger.info("Create address request received")
    return address_service.create_address(db, address)

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(
    address_id: int,
    address: AddressUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"Update request received for address ID {address_id}")
    return address_service.update_address(db, address_id, address)

@router.delete("/{address_id}", status_code=204)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
):
    logger.info(f"Delete request received for address ID {address_id}")
    address_service.delete_address(db, address_id)
    return

@router.get("/nearby", response_model=List[AddressResponse])
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    distance_km: float = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    logger.info("Nearby search request received")

    return address_service.get_addresses_within_distance(
        db=db,
        latitude=latitude,
        longitude=longitude,
        distance_km=distance_km,
    )