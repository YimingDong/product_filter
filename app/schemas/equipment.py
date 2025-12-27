from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 冷凝机模型
class CondenserBase(BaseModel):
    """冷凝机基础模型"""
    model_code: str = Field(..., min_length=1, max_length=100, description="型号编码")
    applicable_temperature: int = Field(..., description="适用库温")
    compressor_count: int = Field(..., description="压缩机数量")
    fan_count: int = Field(..., description="风机数量")
    suction_inlet: float = Field(..., description="吸气进口")
    liquid_supply_interface: float = Field(..., description="液供接口")
    length: float = Field(..., description="长")
    width: float = Field(..., description="宽")
    height: float = Field(..., description="高")
    installation_height: float = Field(..., description="安装尺寸高")
    installation_width: float = Field(..., description="安装尺寸宽")
    range: float = Field(..., description="射程")
    coil_defrost_power: float = Field(..., description="盘管化霜功率")
    water_pan_defrost_power: float = Field(..., description="水盘化霜功率")
    refrigeration_capacity: float = Field(..., description="制冷量")
    weight: float = Field(..., description="重量")


class CondenserCreate(CondenserBase):
    """创建冷凝机模型"""
    pass


class CondenserUpdate(BaseModel):
    """更新冷凝机模型"""
    model_code: Optional[str] = Field(None, min_length=1, max_length=100, description="型号编码")
    applicable_temperature: Optional[int] = Field(None, description="适用库温")
    compressor_count: Optional[int] = Field(None, description="压缩机数量")
    fan_count: Optional[int] = Field(None, description="风机数量")
    suction_inlet: Optional[float] = Field(None, description="吸气进口")
    liquid_supply_interface: Optional[float] = Field(None, description="液供接口")
    length: Optional[float] = Field(None, description="长")
    width: Optional[float] = Field(None, description="宽")
    height: Optional[float] = Field(None, description="高")
    installation_height: Optional[float] = Field(None, description="安装尺寸高")
    installation_width: Optional[float] = Field(None, description="安装尺寸宽")
    range: Optional[float] = Field(None, description="射程")
    coil_defrost_power: Optional[float] = Field(None, description="盘管化霜功率")
    water_pan_defrost_power: Optional[float] = Field(None, description="水盘化霜功率")
    refrigeration_capacity: Optional[float] = Field(None, description="制冷量")
    weight: Optional[float] = Field(None, description="重量")


class CondenserResponse(CondenserBase):
    """冷凝机响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: int
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# 电源模型
class PowerSupplyBase(BaseModel):
    """电源基础模型"""
    model_code: str = Field(..., min_length=1, max_length=100, description="型号编码")
    voltage: float = Field(..., description="电压")
    current: float = Field(..., description="电流")
    power: float = Field(..., description="功率")
    plug_type: int = Field(..., description="插头类型")
    weight: float = Field(..., description="重量")


class PowerSupplyCreate(PowerSupplyBase):
    """创建电源模型"""
    pass


class PowerSupplyUpdate(BaseModel):
    """更新电源模型"""
    model_code: Optional[str] = Field(None, min_length=1, max_length=100, description="型号编码")
    voltage: Optional[float] = Field(None, description="电压")
    current: Optional[float] = Field(None, description="电流")
    power: Optional[float] = Field(None, description="功率")
    plug_type: Optional[int] = Field(None, description="插头类型")
    weight: Optional[float] = Field(None, description="重量")


class PowerSupplyResponse(PowerSupplyBase):
    """电源响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: int
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# 压缩机模型
class CompressorBase(BaseModel):
    """压缩机基础模型"""
    model_code: str = Field(..., min_length=1, max_length=100, description="型号编码")
    type: int = Field(..., description="类型")
    compression_ratio: float = Field(..., description="压缩比")
    working_pressure: float = Field(..., description="工作压力")
    working_flow: float = Field(..., description="工作流量")
    working_efficiency: float = Field(..., description="工作效率")
    installation_height: float = Field(..., description="安装尺寸高")
    installation_width: float = Field(..., description="安装尺寸宽")
    installation_depth: float = Field(..., description="安装尺寸深")
    weight: float = Field(..., description="重量")


class CompressorCreate(CompressorBase):
    """创建压缩机模型"""
    pass


class CompressorUpdate(BaseModel):
    """更新压缩机模型"""
    model_code: Optional[str] = Field(None, min_length=1, max_length=100, description="型号编码")
    type: Optional[int] = Field(None, description="类型")
    compression_ratio: Optional[float] = Field(None, description="压缩比")
    working_pressure: Optional[float] = Field(None, description="工作压力")
    working_flow: Optional[float] = Field(None, description="工作流量")
    working_efficiency: Optional[float] = Field(None, description="工作效率")
    installation_height: Optional[float] = Field(None, description="安装尺寸高")
    installation_width: Optional[float] = Field(None, description="安装尺寸宽")
    installation_depth: Optional[float] = Field(None, description="安装尺寸深")
    weight: Optional[float] = Field(None, description="重量")


class CompressorResponse(CompressorBase):
    """压缩机响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: int
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# 风机模型
class FanBase(BaseModel):
    """风机基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="名称")
    model_code: str = Field(..., min_length=1, max_length=100, description="型号编码")
    type: int = Field(..., description="类型")
    working_voltage: float = Field(..., description="工作电压")
    working_power: float = Field(..., description="工作功率")
    installation_height: float = Field(..., description="安装尺寸高")
    installation_width: float = Field(..., description="安装尺寸宽")
    installation_depth: float = Field(..., description="安装尺寸深")
    weight: float = Field(..., description="重量")


class FanCreate(FanBase):
    """创建风机模型"""
    pass


class FanUpdate(BaseModel):
    """更新风机模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="名称")
    model_code: Optional[str] = Field(None, min_length=1, max_length=100, description="型号编码")
    type: Optional[int] = Field(None, description="类型")
    working_voltage: Optional[float] = Field(None, description="工作电压")
    working_power: Optional[float] = Field(None, description="工作功率")
    installation_height: Optional[float] = Field(None, description="安装尺寸高")
    installation_width: Optional[float] = Field(None, description="安装尺寸宽")
    installation_depth: Optional[float] = Field(None, description="安装尺寸深")
    weight: Optional[float] = Field(None, description="重量")


class FanResponse(FanBase):
    """风机响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: int
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# 蒸发器模型
class EvaporatorBase(BaseModel):
    """蒸发器基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="名称")
    model_code: str = Field(..., min_length=1, max_length=100, description="型号编码")
    type: int = Field(..., description="类型")
    working_voltage: float = Field(..., description="工作电压")
    working_power: float = Field(..., description="工作功率")
    installation_height: float = Field(..., description="安装尺寸高")
    installation_width: float = Field(..., description="安装尺寸宽")
    installation_depth: float = Field(..., description="安装尺寸深")
    weight: float = Field(..., description="重量")


class EvaporatorCreate(EvaporatorBase):
    """创建蒸发器模型"""
    pass


class EvaporatorUpdate(BaseModel):
    """更新蒸发器模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="名称")
    model_code: Optional[str] = Field(None, min_length=1, max_length=100, description="型号编码")
    type: Optional[int] = Field(None, description="类型")
    working_voltage: Optional[float] = Field(None, description="工作电压")
    working_power: Optional[float] = Field(None, description="工作功率")
    installation_height: Optional[float] = Field(None, description="安装尺寸高")
    installation_width: Optional[float] = Field(None, description="安装尺寸宽")
    installation_depth: Optional[float] = Field(None, description="安装尺寸深")
    weight: Optional[float] = Field(None, description="重量")


class EvaporatorResponse(EvaporatorBase):
    """蒸发器响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: int
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# 图片模型
class ImageBase(BaseModel):
    """图片基础模型"""
    related_id: str = Field(..., min_length=1, max_length=255, description="关联id")
    image_url: str = Field(..., min_length=1, max_length=255, description="图片URL")


class ImageCreate(ImageBase):
    """创建图片模型"""
    pass


class ImageUpdate(BaseModel):
    """更新图片模型"""
    related_id: Optional[str] = Field(None, min_length=1, max_length=255, description="关联id")
    image_url: Optional[str] = Field(None, min_length=1, max_length=255, description="图片URL")


class ImageResponse(ImageBase):
    """图片响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: int
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


# 通用过滤和分页模型
class PaginationParams(BaseModel):
    """分页参数模型"""
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(10, ge=1, le=100, description="每页数量")


class CondenserFilter(BaseModel):
    """冷凝机过滤模型"""
    model_code: Optional[str] = Field(None, description="型号编码")
    min_temperature: Optional[int] = Field(None, description="最低适用库温")
    max_temperature: Optional[int] = Field(None, description="最高适用库温")


class PowerSupplyFilter(BaseModel):
    """电源过滤模型"""
    model_code: Optional[str] = Field(None, description="型号编码")
    min_voltage: Optional[float] = Field(None, description="最低电压")
    max_voltage: Optional[float] = Field(None, description="最高电压")


class CompressorFilter(BaseModel):
    """压缩机过滤模型"""
    model_code: Optional[str] = Field(None, description="型号编码")
    min_efficiency: Optional[float] = Field(None, description="最低工作效率")


class FanFilter(BaseModel):
    """风机过滤模型"""
    name: Optional[str] = Field(None, description="名称")
    model_code: Optional[str] = Field(None, description="型号编码")
    type: Optional[int] = Field(None, description="类型")


class EvaporatorFilter(BaseModel):
    """蒸发器过滤模型"""
    name: Optional[str] = Field(None, description="名称")
    model_code: Optional[str] = Field(None, description="型号编码")
    type: Optional[int] = Field(None, description="类型")


# 冷风机模型
class CoolerBase(BaseModel):
    """冷风机基础模型"""
    heat_exchange_area: float = Field(..., description="换热面积")
    tube_volumn: Optional[float] = Field(None, description="管容(dm³)")
    air_flow_rate: Optional[float] = Field(None, description="风量(m³/h)")
    total_fan_power: Optional[str] = Field(None, max_length=100, description="电机总功率")
    total_fan_current: Optional[str] = Field(None, max_length=100, description="电机总电流")
    air_flow: Optional[float] = Field(None, description="射程")
    defrost_water_flow_rate: Optional[float] = Field(None, description="冲霜水量(m³/h)")
    pipe_dia: Optional[str] = Field(None, max_length=100, description="接口管径(进/出Φmm）")
    noise: Optional[float] = Field(None, description="噪音(dB)(5米)")
    weight: Optional[float] = Field(None, description="重量")
    model: Optional[str] = Field(None, max_length=100, description="型号")
    fin_spacing: Optional[str] = Field(None, max_length=100, description="翅片间距")
    series: Optional[str] = Field(None, max_length=100, description="系列")
    comment: Optional[str] = Field(None, max_length=255, description="参数注释")


class CoolerCreate(CoolerBase):
    """创建冷风机模型"""
    pass


class CoolerUpdate(BaseModel):
    """更新冷风机模型"""
    heat_exchange_area: Optional[float] = Field(None, description="换热面积")
    tube_volumn: Optional[float] = Field(None, description="管容(dm³)")
    air_flow_rate: Optional[float] = Field(None, description="风量(m³/h)")
    total_fan_power: Optional[str] = Field(None, max_length=100, description="电机总功率")
    total_fan_current: Optional[str] = Field(None, max_length=100, description="电机总电流")
    air_flow: Optional[float] = Field(None, description="射程")
    defrost_water_flow_rate: Optional[float] = Field(None, description="冲霜水量(m³/h)")
    pipe_dia: Optional[str] = Field(None, max_length=100, description="接口管径(进/出Φmm）")
    noise: Optional[float] = Field(None, description="噪音(dB)(5米)")
    weight: Optional[float] = Field(None, description="重量")
    model: Optional[str] = Field(None, max_length=100, description="型号")
    fin_spacing: Optional[str] = Field(None, max_length=100, description="翅片间距")
    series: Optional[str] = Field(None, max_length=100, description="系列")
    comment: Optional[str] = Field(None, max_length=255, description="参数注释")


class CoolerResponse(CoolerBase):
    """冷风机响应模型"""
    id: int
    is_deleted: int

    class Config:
        from_attributes = True


# 冷量映射表模型
class CoolingCapacityBase(BaseModel):
    """冷量映射表基础模型"""
    cooler_id: int = Field(..., description="冷风机的id")
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
