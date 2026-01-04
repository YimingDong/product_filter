from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 冷风机模型
class CoolerBase(BaseModel):
    """冷风机基础模型"""
    heat_exchange_area: float = Field(..., description="换热面积")
    tube_volumn: Optional[float] = Field(None, description="管容(dm³)")
    air_flow_rate: Optional[float] = Field(None, description="风量(m³/h)")
    total_fan_power: Optional[str] = Field(None, max_length=100, description="电机总功率")
    total_fan_current: Optional[str] = Field(None, max_length=100, description="电机总电流")
    air_flow: Optional[str] = Field(None, description="射程")
    defrost_power: Optional[float] = Field(None, description="化霜总功率")
    pipe_dia: Optional[str] = Field(None, max_length=100, description="接口管径(进/出Φmm）")
    noise: Optional[float] = Field(None, description="噪音(dB)(5米)")
    weight: Optional[float] = Field(None, description="重量")
    model: Optional[str] = Field(None, max_length=100, description="型号")
    fin_spacing: Optional[str] = Field(None, max_length=100, description="翅片间距")
    series: Optional[str] = Field(None, max_length=100, description="系列")
    comment: Optional[str] = Field(None, max_length=255, description="参数注释")


# class CoolerCreate(CoolerBase):
#     """创建冷风机模型"""
#     pass
#
#
# class CoolerUpdate(BaseModel):
#     """更新冷风机模型"""
#     heat_exchange_area: Optional[float] = Field(None, description="换热面积")
#     tube_volumn: Optional[float] = Field(None, description="管容(dm³)")
#     air_flow_rate: Optional[float] = Field(None, description="风量(m³/h)")
#     total_fan_power: Optional[str] = Field(None, max_length=100, description="电机总功率")
#     total_fan_current: Optional[str] = Field(None, max_length=100, description="电机总电流")
#     air_flow: Optional[float] = Field(None, description="射程")
#     defrost_water_flow_rate: Optional[float] = Field(None, description="冲霜水量(m³/h)")
#     pipe_dia: Optional[str] = Field(None, max_length=100, description="接口管径(进/出Φmm）")
#     noise: Optional[float] = Field(None, description="噪音(dB)(5米)")
#     weight: Optional[float] = Field(None, description="重量")
#     model: Optional[str] = Field(None, max_length=100, description="型号")
#     fin_spacing: Optional[str] = Field(None, max_length=100, description="翅片间距")
#     series: Optional[str] = Field(None, max_length=100, description="系列")
#     comment: Optional[str] = Field(None, max_length=255, description="参数注释")


class CoolerResponse(CoolerBase):
    """冷风机响应模型"""
    id: int
    is_deleted: int

    class Config:
        from_attributes = True


# 冷量映射表模型
class CoolingCapacityBase(BaseModel):
    """冷量映射表基础模型"""
    cooler_id: str = Field(..., description="冷风机的id")
    working_status: str = Field(..., max_length=100, description="工况：SC1;SC2;SC3;SC4;SC5")
    capacity: float = Field(..., description="制冷量（KW）")


class CoolingCapacityCreate(CoolingCapacityBase):
    """创建冷量映射表模型"""
    pass


class CoolingCapacityUpdate(BaseModel):
    """更新冷量映射表模型"""
    cooler_id: Optional[int] = Field(None, description="冷风机的id")
    working_status: Optional[str] = Field(None, max_length=100, description="工况：SC1;SC2;SC3;SC4;SC5")
    capacity: Optional[float] = Field(None, description="制冷量（KW）")


class CoolingCapacityResponse(CoolingCapacityBase):
    """冷量映射表响应模型"""
    id: int
    created_time: datetime
    updated_time: datetime
    is_deleted: int

    class Config:
        from_attributes = True


# 工况修正系数模型
class SCQuantBase(BaseModel):
    """工况修正系数基础模型"""
    evaporating_temp: float = Field(..., description="蒸发温度")
    delta_t: float = Field(..., description="温差")
    quant: Optional[float] = Field(None, description="修正系数")


class SCQuantCreate(SCQuantBase):
    """创建工况修正系数模型"""
    pass


class SCQuantUpdate(BaseModel):
    """更新工况修正系数模型"""
    evaporating_temp: Optional[float] = Field(None, description="蒸发温度")
    delta_t: Optional[float] = Field(None, description="温差")
    quant: Optional[float] = Field(None, description="修正系数")


class SCQuantResponse(SCQuantBase):
    """工况修正系数响应模型"""
    id: int
    create_time: datetime
    update_time: datetime
    is_deleted: int

    class Config:
        from_attributes = True


# 冷风机过滤模型
class CoolerFilter(BaseModel):
    """冷风机过滤模型"""
    model: Optional[str] = Field(None, description="型号")
    series: Optional[str] = Field(None, description="系列")
    min_heat_exchange_area: Optional[float] = Field(None, description="最小换热面积")
    max_heat_exchange_area: Optional[float] = Field(None, description="最大换热面积")


# 工况修正系数过滤模型
class SCQuantFilter(BaseModel):
    """工况修正系数过滤模型"""
    min_evaporating_temp: Optional[float] = Field(None, description="最小蒸发温度")
    max_evaporating_temp: Optional[float] = Field(None, description="最大蒸发温度")
    min_delta_t: Optional[float] = Field(None, description="最小温差")
    max_delta_t: Optional[float] = Field(None, description="最大温差")
