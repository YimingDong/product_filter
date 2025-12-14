from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.schemas.equipment import (
    CondenserCreate, CondenserUpdate, CondenserResponse, CondenserFilter,
    PowerSupplyCreate, PowerSupplyUpdate, PowerSupplyResponse, PowerSupplyFilter,
    CompressorCreate, CompressorUpdate, CompressorResponse, CompressorFilter,
    FanCreate, FanUpdate, FanResponse, FanFilter,
    EvaporatorCreate, EvaporatorUpdate, EvaporatorResponse, EvaporatorFilter,
    ImageCreate, ImageUpdate, ImageResponse,
    PaginationParams
)
from app.schemas.response import BaseResponse
from app.services.equipment_service import (
    CondenserService,
    PowerSupplyService,
    CompressorService,
    FanService,
    EvaporatorService,
    ImageService
)

# 创建路由器
router = APIRouter()


# 冷凝机API
@router.post("/condensers/", response_model=BaseResponse[CondenserResponse], summary="创建冷凝机")
def create_condenser(condenser: CondenserCreate, db: Session = Depends(get_db)):
    """创建新的冷凝机"""
    try:
        return BaseResponse(data=CondenserService.create_condenser(db, condenser))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/condensers/{condenser_id}", response_model=BaseResponse[CondenserResponse], summary="获取冷凝机")
def get_condenser(condenser_id: int, db: Session = Depends(get_db)):
    """根据ID获取冷凝机"""
    condenser = CondenserService.get_condenser(db, condenser_id)
    if not condenser:
        raise HTTPException(status_code=404, detail="Condenser not found")
    return BaseResponse(data=condenser)


@router.put("/condensers/{condenser_id}", response_model=BaseResponse[CondenserResponse], summary="更新冷凝机")
def update_condenser(condenser_id: int, condenser: CondenserUpdate, db: Session = Depends(get_db)):
    """更新冷凝机信息"""
    updated_condenser = CondenserService.update_condenser(db, condenser_id, condenser)
    if not updated_condenser:
        raise HTTPException(status_code=404, detail="Condenser not found")
    return BaseResponse(data=updated_condenser)


@router.delete("/condensers/{condenser_id}", response_model=BaseResponse[dict], summary="删除冷凝机")
def delete_condenser(condenser_id: int, db: Session = Depends(get_db)):
    """删除冷凝机"""
    success = CondenserService.delete_condenser(db, condenser_id)
    if not success:
        raise HTTPException(status_code=404, detail="Condenser not found")
    return BaseResponse(data={"message": "Condenser deleted successfully"})


@router.get("/condensers/", response_model=BaseResponse[dict], summary="搜索冷凝机")
def search_condensers(
    model_code: Optional[str] = Query(None, description="型号编码"),
    min_temperature: Optional[int] = Query(None, description="最低适用库温"),
    max_temperature: Optional[int] = Query(None, description="最高适用库温"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """搜索冷凝机列表"""
    filter_params = CondenserFilter(
        model_code=model_code,
        min_temperature=min_temperature,
        max_temperature=max_temperature
    )
    pagination = PaginationParams(page=page, size=size)
    return BaseResponse(data=CondenserService.search_condensers(db, filter_params, pagination))


# 电源API
@router.post("/power-supplies/", response_model=BaseResponse[PowerSupplyResponse], summary="创建电源")
def create_power_supply(power_supply: PowerSupplyCreate, db: Session = Depends(get_db)):
    """创建新的电源"""
    try:
        return BaseResponse(data=PowerSupplyService.create_power_supply(db, power_supply))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/power-supplies/{power_supply_id}", response_model=BaseResponse[PowerSupplyResponse], summary="获取电源")
def get_power_supply(power_supply_id: int, db: Session = Depends(get_db)):
    """根据ID获取电源"""
    power_supply = PowerSupplyService.get_power_supply(db, power_supply_id)
    if not power_supply:
        raise HTTPException(status_code=404, detail="PowerSupply not found")
    return BaseResponse(data=power_supply)


@router.put("/power-supplies/{power_supply_id}", response_model=BaseResponse[PowerSupplyResponse], summary="更新电源")
def update_power_supply(power_supply_id: int, power_supply: PowerSupplyUpdate, db: Session = Depends(get_db)):
    """更新电源信息"""
    updated_power_supply = PowerSupplyService.update_power_supply(db, power_supply_id, power_supply)
    if not updated_power_supply:
        raise HTTPException(status_code=404, detail="PowerSupply not found")
    return BaseResponse(data=updated_power_supply)


@router.delete("/power-supplies/{power_supply_id}", response_model=BaseResponse[dict], summary="删除电源")
def delete_power_supply(power_supply_id: int, db: Session = Depends(get_db)):
    """删除电源"""
    success = PowerSupplyService.delete_power_supply(db, power_supply_id)
    if not success:
        raise HTTPException(status_code=404, detail="PowerSupply not found")
    return BaseResponse(data={"message": "PowerSupply deleted successfully"})


@router.get("/power-supplies/", response_model=BaseResponse[dict], summary="搜索电源")
def search_power_supplies(
    model_code: Optional[str] = Query(None, description="型号编码"),
    min_voltage: Optional[float] = Query(None, description="最低电压"),
    max_voltage: Optional[float] = Query(None, description="最高电压"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """搜索电源列表"""
    filter_params = PowerSupplyFilter(
        model_code=model_code,
        min_voltage=min_voltage,
        max_voltage=max_voltage
    )
    pagination = PaginationParams(page=page, size=size)
    return BaseResponse(data=PowerSupplyService.search_power_supplies(db, filter_params, pagination))


# 压缩机API
@router.post("/compressors/", response_model=BaseResponse[CompressorResponse], summary="创建压缩机")
def create_compressor(compressor: CompressorCreate, db: Session = Depends(get_db)):
    """创建新的压缩机"""
    try:
        return BaseResponse(data=CompressorService.create_compressor(db, compressor))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/compressors/{compressor_id}", response_model=BaseResponse[CompressorResponse], summary="获取压缩机")
def get_compressor(compressor_id: int, db: Session = Depends(get_db)):
    """根据ID获取压缩机"""
    compressor = CompressorService.get_compressor(db, compressor_id)
    if not compressor:
        raise HTTPException(status_code=404, detail="Compressor not found")
    return BaseResponse(data=compressor)


@router.put("/compressors/{compressor_id}", response_model=BaseResponse[CompressorResponse], summary="更新压缩机")
def update_compressor(compressor_id: int, compressor: CompressorUpdate, db: Session = Depends(get_db)):
    """更新压缩机信息"""
    updated_compressor = CompressorService.update_compressor(db, compressor_id, compressor)
    if not updated_compressor:
        raise HTTPException(status_code=404, detail="Compressor not found")
    return BaseResponse(data=updated_compressor)


@router.delete("/compressors/{compressor_id}", response_model=BaseResponse[dict], summary="删除压缩机")
def delete_compressor(compressor_id: int, db: Session = Depends(get_db)):
    """删除压缩机"""
    success = CompressorService.delete_compressor(db, compressor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Compressor not found")
    return BaseResponse(data={"message": "Compressor deleted successfully"})


@router.get("/compressors/", response_model=BaseResponse[dict], summary="搜索压缩机")
def search_compressors(
    model_code: Optional[str] = Query(None, description="型号编码"),
    min_efficiency: Optional[float] = Query(None, description="最低工作效率"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """搜索压缩机列表"""
    filter_params = CompressorFilter(
        model_code=model_code,
        min_efficiency=min_efficiency
    )
    pagination = PaginationParams(page=page, size=size)
    return BaseResponse(data=CompressorService.search_compressors(db, filter_params, pagination))


# 风机API
@router.post("/fans/", response_model=BaseResponse[FanResponse], summary="创建风机")
def create_fan(fan: FanCreate, db: Session = Depends(get_db)):
    """创建新的风机"""
    try:
        return BaseResponse(data=FanService.create_fan(db, fan))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/fans/{fan_id}", response_model=BaseResponse[FanResponse], summary="获取风机")
def get_fan(fan_id: int, db: Session = Depends(get_db)):
    """根据ID获取风机"""
    fan = FanService.get_fan(db, fan_id)
    if not fan:
        raise HTTPException(status_code=404, detail="Fan not found")
    return BaseResponse(data=fan)


@router.put("/fans/{fan_id}", response_model=BaseResponse[FanResponse], summary="更新风机")
def update_fan(fan_id: int, fan: FanUpdate, db: Session = Depends(get_db)):
    """更新风机信息"""
    updated_fan = FanService.update_fan(db, fan_id, fan)
    if not updated_fan:
        raise HTTPException(status_code=404, detail="Fan not found")
    return BaseResponse(data=updated_fan)


@router.delete("/fans/{fan_id}", response_model=BaseResponse[dict], summary="删除风机")
def delete_fan(fan_id: int, db: Session = Depends(get_db)):
    """删除风机"""
    success = FanService.delete_fan(db, fan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fan not found")
    return BaseResponse(data={"message": "Fan deleted successfully"})


@router.get("/fans/", response_model=BaseResponse[dict], summary="搜索风机")
def search_fans(
    name: Optional[str] = Query(None, description="名称"),
    model_code: Optional[str] = Query(None, description="型号编码"),
    type: Optional[int] = Query(None, description="类型"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """搜索风机列表"""
    filter_params = FanFilter(
        name=name,
        model_code=model_code,
        type=type
    )
    pagination = PaginationParams(page=page, size=size)
    return BaseResponse(data=FanService.search_fans(db, filter_params, pagination))


# 蒸发器API
@router.post("/evaporators/", response_model=BaseResponse[EvaporatorResponse], summary="创建蒸发器")
def create_evaporator(evaporator: EvaporatorCreate, db: Session = Depends(get_db)):
    """创建新的蒸发器"""
    try:
        return BaseResponse(data=EvaporatorService.create_evaporator(db, evaporator))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/evaporators/{evaporator_id}", response_model=BaseResponse[EvaporatorResponse], summary="获取蒸发器")
def get_evaporator(evaporator_id: int, db: Session = Depends(get_db)):
    """根据ID获取蒸发器"""
    evaporator = EvaporatorService.get_evaporator(db, evaporator_id)
    if not evaporator:
        raise HTTPException(status_code=404, detail="Evaporator not found")
    return BaseResponse(data=evaporator)


@router.put("/evaporators/{evaporator_id}", response_model=BaseResponse[EvaporatorResponse], summary="更新蒸发器")
def update_evaporator(evaporator_id: int, evaporator: EvaporatorUpdate, db: Session = Depends(get_db)):
    """更新蒸发器信息"""
    updated_evaporator = EvaporatorService.update_evaporator(db, evaporator_id, evaporator)
    if not updated_evaporator:
        raise HTTPException(status_code=404, detail="Evaporator not found")
    return BaseResponse(data=updated_evaporator)


@router.delete("/evaporators/{evaporator_id}", response_model=BaseResponse[dict], summary="删除蒸发器")
def delete_evaporator(evaporator_id: int, db: Session = Depends(get_db)):
    """删除蒸发器"""
    success = EvaporatorService.delete_evaporator(db, evaporator_id)
    if not success:
        raise HTTPException(status_code=404, detail="Evaporator not found")
    return BaseResponse(data={"message": "Evaporator deleted successfully"})


@router.get("/evaporators/", response_model=BaseResponse[dict], summary="搜索蒸发器")
def search_evaporators(
    name: Optional[str] = Query(None, description="名称"),
    model_code: Optional[str] = Query(None, description="型号编码"),
    type: Optional[int] = Query(None, description="类型"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """搜索蒸发器列表"""
    filter_params = EvaporatorFilter(
        name=name,
        model_code=model_code,
        type=type
    )
    pagination = PaginationParams(page=page, size=size)
    return BaseResponse(data=EvaporatorService.search_evaporators(db, filter_params, pagination))


# 图片API
@router.post("/images/", response_model=BaseResponse[ImageResponse], summary="创建图片")
def create_image(image: ImageCreate, db: Session = Depends(get_db)):
    """创建新的图片"""
    try:
        return BaseResponse(data=ImageService.create_image(db, image))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/images/{image_id}", response_model=BaseResponse[ImageResponse], summary="获取图片")
def get_image(image_id: int, db: Session = Depends(get_db)):
    """根据ID获取图片"""
    image = ImageService.get_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return BaseResponse(data=image)


@router.put("/images/{image_id}", response_model=BaseResponse[ImageResponse], summary="更新图片")
def update_image(image_id: int, image: ImageUpdate, db: Session = Depends(get_db)):
    """更新图片信息"""
    updated_image = ImageService.update_image(db, image_id, image)
    if not updated_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return BaseResponse(data=updated_image)


@router.delete("/images/{image_id}", response_model=BaseResponse[dict], summary="删除图片")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    """删除图片"""
    success = ImageService.delete_image(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return BaseResponse(data={"message": "Image deleted successfully"})


@router.get("/images/", response_model=BaseResponse[dict], summary="获取图片列表")
def get_images(
    related_id: Optional[str] = Query(None, description="关联ID"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """根据关联ID获取图片列表"""
    if related_id:
        pagination = PaginationParams(page=page, size=size)
        return BaseResponse(data=ImageService.get_images_by_related_id(db, related_id, pagination))
    else:
        # 如果没有提供related_id，可以返回所有图片的分页列表
        # 注意：这里需要在ImageService中添加对应的方法
        raise HTTPException(status_code=400, detail="related_id is required")


@router.delete("/images/related/{related_id}", response_model=BaseResponse[dict], summary="删除关联图片")
def delete_images_by_related_id(related_id: str, db: Session = Depends(get_db)):
    """删除指定关联ID的所有图片"""
    success = ImageService.delete_images_by_related_id(db, related_id)
    if not success:
        raise HTTPException(status_code=404, detail="No images found for this related_id")
    return BaseResponse(data={"message": f"All images with related_id {related_id} deleted successfully"})