from pydantic import BaseModel, Field, model_validator
from typing import Optional, List

from app.utils.enums import Refrigerant, RefrigerantSupplyType


class CoolerFilter(BaseModel):
    """产品过滤模型"""
    evaporating_temp: float = Field(None, description="蒸发温度")
    repo_temp: float = Field(None, description="库温")
    required_cooling_cap: float = Field(None, description="需求冷量")
    refrigerant: Optional[str] = Field(Refrigerant.R404A.value, description="制冷剂")
    refrigerant_supply_type: Optional[str] = Field(RefrigerantSupplyType.DIRECT.value, description="制冷剂类型")
    fan_distance: Optional[float] = Field(None, description="片距")

    @model_validator(mode='before')
    @classmethod
    def set_defaults(cls, data):
        """当字段值为None时，使用默认值"""
        if isinstance(data, dict):
            # 如果refrigerant为None或未提供，使用默认值
            if data.get('refrigerant') is None:
                data['refrigerant'] = Refrigerant.R404A.value
            # 如果refrigerant_supply_type为None或未提供，使用默认值
            if data.get('refrigerant_supply_type') is None:
                data['refrigerant_supply_type'] = RefrigerantSupplyType.DIRECT.value
        return data

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