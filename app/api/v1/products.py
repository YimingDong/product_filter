from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models import get_db
from app.schemas.product import CoolerFilter
from app.schemas.response import BaseResponse, PaginationParams
from app.services.cooler_service import CoolerService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/cooler/filter", response_model=BaseResponse[dict])
def filter_coolers(
    filter_params: CoolerFilter,
    db: Session = Depends(get_db)
):
    """过滤产品"""
    try:
        result = CoolerService.filter_cooler(db, filter_params)
        return BaseResponse(
            message="Products filtered successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error filtering products: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# http://localhost:8080/api/v1/products/cooler/filter/-30/-25/150/R404A/direct/4.5
# evaporating_temp: float,
#     repo_temp: float,
#     required_cooling_cap: float,
#     refrigerant: str,
#     refrigerant_supply_type: str,
#     fan_distance: float,
@router.get("/cooler/filter", response_model=BaseResponse[dict])
def filter_coolers_get(
        evaporating_temp: float,
        repo_temp: float,
        required_cooling_cap: float,
        refrigerant: str,
        refrigerant_supply_type: str,
        db: Session = Depends(get_db)
):
    """过滤冷风机（GET请求）"""
    try:
        filter_params = CoolerFilter(
            evaporating_temp=evaporating_temp,
            repo_temp=repo_temp,
            required_cooling_cap=required_cooling_cap,
            refrigerant=refrigerant,
            refrigerant_supply_type=refrigerant_supply_type,
            fan_distance=0
        )
        result = CoolerService.filter_cooler(db, filter_params)
        return BaseResponse(
            message="Coolers filtered successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error filtering coolers: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")