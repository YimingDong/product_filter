from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.repositories import (
    CondenserRepository,
    PowerSupplyRepository,
    CompressorRepository,
    FanRepository,
    EvaporatorRepository,
    ImageRepository
)
from app.schemas.equipment import (
    CondenserCreate, CondenserUpdate, CondenserFilter, PaginationParams,
    PowerSupplyCreate, PowerSupplyUpdate, PowerSupplyFilter,
    CompressorCreate, CompressorUpdate, CompressorFilter,
    FanCreate, FanUpdate, FanFilter,
    EvaporatorCreate, EvaporatorUpdate, EvaporatorFilter,
    ImageCreate, ImageUpdate
)


class CondenserService:
    """冷凝机服务类"""

    @staticmethod
    def create_condenser(db: Session, condenser_data: CondenserCreate):
        """创建冷凝机"""
        condenser_repo = CondenserRepository(db)
        return condenser_repo.create(**condenser_data.model_dump())

    @staticmethod
    def get_condenser(db: Session, condenser_id: int):
        """根据ID获取冷凝机"""
        condenser_repo = CondenserRepository(db)
        return condenser_repo.get_by_id(condenser_id)

    @staticmethod
    def update_condenser(db: Session, condenser_id: int, condenser_data: CondenserUpdate):
        """更新冷凝机"""
        condenser_repo = CondenserRepository(db)
        return condenser_repo.update(condenser_id, **condenser_data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_condenser(db: Session, condenser_id: int):
        """删除冷凝机"""
        condenser_repo = CondenserRepository(db)
        return condenser_repo.delete(condenser_id)

    @staticmethod
    def search_condensers(db: Session, filter_params: CondenserFilter, pagination: PaginationParams):
        """搜索冷凝机"""
        condenser_repo = CondenserRepository(db)
        skip = (pagination.page - 1) * pagination.size
        condensers = condenser_repo.search(
            model_code=filter_params.model_code,
            min_temperature=filter_params.min_temperature,
            max_temperature=filter_params.max_temperature,
            skip=skip,
            limit=pagination.size
        )
        total = condenser_repo.count(
            model_code=filter_params.model_code,
            applicable_temperature=filter_params.min_temperature if filter_params.min_temperature == filter_params.max_temperature else None
        )
        pages = (total + pagination.size - 1) // pagination.size

        return {
            "items": condensers,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }


class PowerSupplyService:
    """电源服务类"""

    @staticmethod
    def create_power_supply(db: Session, power_supply_data: PowerSupplyCreate):
        """创建电源"""
        power_supply_repo = PowerSupplyRepository(db)
        return power_supply_repo.create(**power_supply_data.model_dump())

    @staticmethod
    def get_power_supply(db: Session, power_supply_id: int):
        """根据ID获取电源"""
        power_supply_repo = PowerSupplyRepository(db)
        return power_supply_repo.get_by_id(power_supply_id)

    @staticmethod
    def update_power_supply(db: Session, power_supply_id: int, power_supply_data: PowerSupplyUpdate):
        """更新电源"""
        power_supply_repo = PowerSupplyRepository(db)
        return power_supply_repo.update(power_supply_id, **power_supply_data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_power_supply(db: Session, power_supply_id: int):
        """删除电源"""
        power_supply_repo = PowerSupplyRepository(db)
        return power_supply_repo.delete(power_supply_id)

    @staticmethod
    def search_power_supplies(db: Session, filter_params: PowerSupplyFilter, pagination: PaginationParams):
        """搜索电源"""
        power_supply_repo = PowerSupplyRepository(db)
        skip = (pagination.page - 1) * pagination.size
        power_supplies = power_supply_repo.search(
            model_code=filter_params.model_code,
            min_voltage=filter_params.min_voltage,
            max_voltage=filter_params.max_voltage,
            skip=skip,
            limit=pagination.size
        )
        total = power_supply_repo.count(
            model_code=filter_params.model_code,
            voltage=filter_params.min_voltage if filter_params.min_voltage == filter_params.max_voltage else None
        )
        pages = (total + pagination.size - 1) // pagination.size

        return {
            "items": power_supplies,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }


class CompressorService:
    """压缩机服务类"""

    @staticmethod
    def create_compressor(db: Session, compressor_data: CompressorCreate):
        """创建压缩机"""
        compressor_repo = CompressorRepository(db)
        return compressor_repo.create(**compressor_data.model_dump())

    @staticmethod
    def get_compressor(db: Session, compressor_id: int):
        """根据ID获取压缩机"""
        compressor_repo = CompressorRepository(db)
        return compressor_repo.get_by_id(compressor_id)

    @staticmethod
    def update_compressor(db: Session, compressor_id: int, compressor_data: CompressorUpdate):
        """更新压缩机"""
        compressor_repo = CompressorRepository(db)
        return compressor_repo.update(compressor_id, **compressor_data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_compressor(db: Session, compressor_id: int):
        """删除压缩机"""
        compressor_repo = CompressorRepository(db)
        return compressor_repo.delete(compressor_id)

    @staticmethod
    def search_compressors(db: Session, filter_params: CompressorFilter, pagination: PaginationParams):
        """搜索压缩机"""
        compressor_repo = CompressorRepository(db)
        skip = (pagination.page - 1) * pagination.size
        compressors = compressor_repo.search(
            model_code=filter_params.model_code,
            min_efficiency=filter_params.min_efficiency,
            skip=skip,
            limit=pagination.size
        )
        total = compressor_repo.count(
            model_code=filter_params.model_code
        )
        pages = (total + pagination.size - 1) // pagination.size

        return {
            "items": compressors,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }


class FanService:
    """风机服务类"""

    @staticmethod
    def create_fan(db: Session, fan_data: FanCreate):
        """创建风机"""
        fan_repo = FanRepository(db)
        return fan_repo.create(**fan_data.model_dump())

    @staticmethod
    def get_fan(db: Session, fan_id: int):
        """根据ID获取风机"""
        fan_repo = FanRepository(db)
        return fan_repo.get_by_id(fan_id)

    @staticmethod
    def update_fan(db: Session, fan_id: int, fan_data: FanUpdate):
        """更新风机"""
        fan_repo = FanRepository(db)
        return fan_repo.update(fan_id, **fan_data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_fan(db: Session, fan_id: int):
        """删除风机"""
        fan_repo = FanRepository(db)
        return fan_repo.delete(fan_id)

    @staticmethod
    def search_fans(db: Session, filter_params: FanFilter, pagination: PaginationParams):
        """搜索风机"""
        fan_repo = FanRepository(db)
        skip = (pagination.page - 1) * pagination.size
        fans = fan_repo.search(
            name=filter_params.name,
            model_code=filter_params.model_code,
            fan_type=filter_params.type,
            skip=skip,
            limit=pagination.size
        )
        total = fan_repo.count(
            name=filter_params.name,
            model_code=filter_params.model_code,
            type=filter_params.type
        )
        pages = (total + pagination.size - 1) // pagination.size

        return {
            "items": fans,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }


class EvaporatorService:
    """蒸发器服务类"""

    @staticmethod
    def create_evaporator(db: Session, evaporator_data: EvaporatorCreate):
        """创建蒸发器"""
        evaporator_repo = EvaporatorRepository(db)
        return evaporator_repo.create(**evaporator_data.model_dump())

    @staticmethod
    def get_evaporator(db: Session, evaporator_id: int):
        """根据ID获取蒸发器"""
        evaporator_repo = EvaporatorRepository(db)
        return evaporator_repo.get_by_id(evaporator_id)

    @staticmethod
    def update_evaporator(db: Session, evaporator_id: int, evaporator_data: EvaporatorUpdate):
        """更新蒸发器"""
        evaporator_repo = EvaporatorRepository(db)
        return evaporator_repo.update(evaporator_id, **evaporator_data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_evaporator(db: Session, evaporator_id: int):
        """删除蒸发器"""
        evaporator_repo = EvaporatorRepository(db)
        return evaporator_repo.delete(evaporator_id)

    @staticmethod
    def search_evaporators(db: Session, filter_params: EvaporatorFilter, pagination: PaginationParams):
        """搜索蒸发器"""
        evaporator_repo = EvaporatorRepository(db)
        skip = (pagination.page - 1) * pagination.size
        evaporators = evaporator_repo.search(
            name=filter_params.name,
            model_code=filter_params.model_code,
            evaporator_type=filter_params.type,
            skip=skip,
            limit=pagination.size
        )
        total = evaporator_repo.count(
            name=filter_params.name,
            model_code=filter_params.model_code,
            type=filter_params.type
        )
        pages = (total + pagination.size - 1) // pagination.size

        return {
            "items": evaporators,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }


class ImageService:
    """图片服务类"""

    @staticmethod
    def create_image(db: Session, image_data: ImageCreate):
        """创建图片"""
        image_repo = ImageRepository(db)
        return image_repo.create(**image_data.model_dump())

    @staticmethod
    def get_image(db: Session, image_id: int):
        """根据ID获取图片"""
        image_repo = ImageRepository(db)
        return image_repo.get_by_id(image_id)

    @staticmethod
    def update_image(db: Session, image_id: int, image_data: ImageUpdate):
        """更新图片"""
        image_repo = ImageRepository(db)
        return image_repo.update(image_id, **image_data.model_dump(exclude_unset=True))

    @staticmethod
    def delete_image(db: Session, image_id: int):
        """删除图片"""
        image_repo = ImageRepository(db)
        return image_repo.delete(image_id)

    @staticmethod
    def get_images_by_related_id(db: Session, related_id: str, pagination: PaginationParams):
        """根据关联ID获取图片列表"""
        image_repo = ImageRepository(db)
        skip = (pagination.page - 1) * pagination.size
        images = image_repo.get_by_related_id(related_id, skip=skip, limit=pagination.size)
        total = image_repo.count(related_id=related_id)
        pages = (total + pagination.size - 1) // pagination.size

        return {
            "items": images,
            "total": total,
            "page": pagination.page,
            "size": pagination.size,
            "pages": pages
        }

    @staticmethod
    def delete_images_by_related_id(db: Session, related_id: str):
        """根据关联ID删除图片"""
        image_repo = ImageRepository(db)
        return image_repo.delete_by_related_id(related_id)