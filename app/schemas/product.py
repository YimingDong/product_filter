from pydantic import BaseModel, Field
from typing import Optional, List

from app.utils.enums import Refrigerant, RefrigerantSupplyType


class CoolerFilter(BaseModel):
    """产品过滤模型"""
    evaporating_temp: float = Field(None, description="蒸发温度")
    repo_temp: float = Field(None, description="库温")
    required_cooling_cap: float = Field(None, description="需求冷量")
    refrigerant: Optional[str] = Field(description="制冷剂", default=Refrigerant.R404A.value)
    refrigerant_supply_type: Optional[str] = Field(description="制冷剂类型", default=RefrigerantSupplyType.DIRECT.value)
    fan_distance: Optional[float] = Field(None, description="片距")

    class Config:
        schema_extra = {
            "example": {
                "evaporating_temp": 1,
                "repo_temp": 100,
                "required_cooling_cap": 1000,
                "refrigerant": 1,
                "fan_distance": 33
            }
        }