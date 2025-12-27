from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Optional, List, Dict, Any
from datetime import datetime

# 导入所有模型
from app.models.dao import (
    Condenser,
    PowerSupply,
    Compressor,
    Fan,
    Evaporator,
    Image,
    Cooler,
    CoolingCapacity,
    SCQuant
)

# 创建泛型类型变量
ModelType = TypeVar('ModelType')


class BaseRepository(Generic[ModelType]):
    """基础仓库类，提供通用的CRUD方法"""
    
    def __init__(self, session: Session, model_class: type):
        self.session = session
        self.model_class = model_class
    
    def create(self, **kwargs) -> ModelType:
        """创建新记录"""
        instance = self.model_class(**kwargs)
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """根据ID获取记录"""
        return self.session.query(self.model_class).filter(
            self.model_class.id == id,
            self.model_class.is_deleted == 0
        ).first()
    
    def get_by_fields(self, **kwargs) -> Optional[ModelType]:
        """根据字段条件获取记录"""
        query = self.session.query(self.model_class).filter(
            self.model_class.is_deleted == 0
        )
        
        for field, value in kwargs.items():
            if hasattr(self.model_class, field):
                query = query.filter(getattr(self.model_class, field) == value)
        
        return query.first()
    
    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """更新记录"""
        instance = self.get_by_id(id)
        if not instance:
            return None
        
        for field, value in kwargs.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        
        self.session.commit()
        self.session.refresh(instance)
        return instance
    
    def delete(self, id: int) -> bool:
        """软删除记录"""
        instance = self.get_by_id(id)
        if not instance:
            return False
        
        instance.is_deleted = 1
        instance.deleted_at = datetime.now()
        self.session.commit()
        return True
    
    def count(self, **filters) -> int:
        """统计记录数量"""
        query = self.session.query(self.model_class).filter(
            self.model_class.is_deleted == 0
        )
        
        for field, value in filters.items():
            if hasattr(self.model_class, field):
                query = query.filter(getattr(self.model_class, field) == value)
        
        return query.count()
    
    def search(self, skip: int = 0, limit: int = 100, **filters) -> List[ModelType]:
        """搜索记录，支持分页和基本过滤"""
        query = self.session.query(self.model_class).filter(
            self.model_class.is_deleted == 0
        )
        
        for field, value in filters.items():
            if hasattr(self.model_class, field):
                # 如果是字符串类型，使用like查询
                if isinstance(value, str):
                    query = query.filter(getattr(self.model_class, field).like(f"%{value}%"))
                else:
                    query = query.filter(getattr(self.model_class, field) == value)
        
        return query.offset(skip).limit(limit).all()


class CondenserRepository(BaseRepository[Condenser]):
    """冷凝机仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, Condenser)
    
    def search(self, model_code: Optional[str] = None, min_temperature: Optional[int] = None, 
               max_temperature: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Condenser]:
        """搜索冷凝机，支持型号和温度范围过滤"""
        query = self.session.query(Condenser).filter(Condenser.is_deleted == 0)
        
        if model_code:
            query = query.filter(Condenser.model_code.like(f"%{model_code}%"))
        
        if min_temperature is not None:
            query = query.filter(Condenser.applicable_temperature >= min_temperature)
        
        if max_temperature is not None:
            query = query.filter(Condenser.applicable_temperature <= max_temperature)
        
        return query.offset(skip).limit(limit).all()


class PowerSupplyRepository(BaseRepository[PowerSupply]):
    """电源仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, PowerSupply)
    
    def search(self, model_code: Optional[str] = None, min_voltage: Optional[float] = None, 
               max_voltage: Optional[float] = None, skip: int = 0, limit: int = 100) -> List[PowerSupply]:
        """搜索电源，支持型号和电压范围过滤"""
        query = self.session.query(PowerSupply).filter(PowerSupply.is_deleted == 0)
        
        if model_code:
            query = query.filter(PowerSupply.model_code.like(f"%{model_code}%"))
        
        if min_voltage is not None:
            query = query.filter(PowerSupply.voltage >= min_voltage)
        
        if max_voltage is not None:
            query = query.filter(PowerSupply.voltage <= max_voltage)
        
        return query.offset(skip).limit(limit).all()


class CompressorRepository(BaseRepository[Compressor]):
    """压缩机仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, Compressor)
    
    def search(self, model_code: Optional[str] = None, min_efficiency: Optional[float] = None, 
               skip: int = 0, limit: int = 100) -> List[Compressor]:
        """搜索压缩机，支持型号和效率过滤"""
        query = self.session.query(Compressor).filter(Compressor.is_deleted == 0)
        
        if model_code:
            query = query.filter(Compressor.model_code.like(f"%{model_code}%"))
        
        if min_efficiency is not None:
            query = query.filter(Compressor.working_efficiency >= min_efficiency)
        
        return query.offset(skip).limit(limit).all()


class FanRepository(BaseRepository[Fan]):
    """风机仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, Fan)
    
    def search(self, name: Optional[str] = None, model_code: Optional[str] = None, 
               fan_type: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Fan]:
        """搜索风机，支持名称、型号和类型过滤"""
        query = self.session.query(Fan).filter(Fan.is_deleted == 0)
        
        if name:
            query = query.filter(Fan.name.like(f"%{name}%"))
        
        if model_code:
            query = query.filter(Fan.model_code.like(f"%{model_code}%"))
        
        if fan_type is not None:
            query = query.filter(Fan.type == fan_type)
        
        return query.offset(skip).limit(limit).all()


class EvaporatorRepository(BaseRepository[Evaporator]):
    """蒸发器仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, Evaporator)
    
    def search(self, name: Optional[str] = None, model_code: Optional[str] = None, 
               evaporator_type: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Evaporator]:
        """搜索蒸发器，支持名称、型号和类型过滤"""
        query = self.session.query(Evaporator).filter(Evaporator.is_deleted == 0)
        
        if name:
            query = query.filter(Evaporator.name.like(f"%{name}%"))
        
        if model_code:
            query = query.filter(Evaporator.model_code.like(f"%{model_code}%"))
        
        if evaporator_type is not None:
            query = query.filter(Evaporator.type == evaporator_type)
        
        return query.offset(skip).limit(limit).all()


class ImageRepository(BaseRepository[Image]):
    """图片仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, Image)
    
    def get_by_related_id(self, related_id: str, skip: int = 0, limit: int = 100) -> List[Image]:
        """根据关联ID获取图片"""
        return self.search(related_id=related_id, skip=skip, limit=limit)
    
    def delete_by_related_id(self, related_id: str) -> bool:
        """删除指定关联ID的所有图片"""
        query = self.session.query(Image).filter(
            Image.related_id == related_id,
            Image.is_deleted == 0
        )
        
        count = query.update({
            Image.is_deleted: 1,
            Image.deleted_at: datetime.now()
        })
        
        self.session.commit()
        return count > 0


class CoolerRepository(BaseRepository[Cooler]):
    """冷风机仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, Cooler)
    
    def search(self, model: Optional[str] = None, series: Optional[str] = None, 
               min_heat_exchange_area: Optional[float] = None, 
               max_heat_exchange_area: Optional[float] = None,
               skip: int = 0, limit: int = 100) -> List[Cooler]:
        """搜索冷风机，支持型号、系列和换热面积范围过滤"""
        query = self.session.query(Cooler).filter(Cooler.is_deleted == 0)
        
        if model:
            query = query.filter(Cooler.model.like(f"%{model}%"))
        
        if series:
            query = query.filter(Cooler.series.like(f"%{series}%"))
        
        if min_heat_exchange_area is not None:
            query = query.filter(Cooler.heat_exchange_area >= min_heat_exchange_area)
        
        if max_heat_exchange_area is not None:
            query = query.filter(Cooler.heat_exchange_area <= max_heat_exchange_area)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_cooler_id(self, cooler_id: int) -> Optional[Cooler]:
        """根据冷风机ID获取记录"""
        return self.session.query(Cooler).filter(
            Cooler.id == cooler_id,
            Cooler.is_deleted == 0
        ).first()

    def get_by_cooler_ids(self, cooler_id: List[int]) -> List[Cooler]:
        """根据冷风机ID获取记录"""
        return self.session.query(Cooler).filter(
            Cooler.id.in_(cooler_id),
            Cooler.is_deleted == 0
        ).all()


class CoolingCapacityRepository(BaseRepository[CoolingCapacity]):
    """冷量映射表仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, CoolingCapacity)
    
    def get_by_cooler_id(self, cooler_id: int, skip: int = 0, limit: int = 100) -> List[CoolingCapacity]:
        """根据冷风机ID获取所有冷量映射记录"""
        query = self.session.query(CoolingCapacity).filter(
            CoolingCapacity.cooler_id == cooler_id,
            CoolingCapacity.is_deleted == 0
        )
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_working_status(self, working_status: str) -> List[CoolingCapacity]:
        """根据冷风机ID和工况获取冷量映射记录"""
        return self.session.query(CoolingCapacity).filter(
            CoolingCapacity.working_status == working_status,
            CoolingCapacity.is_deleted == 0
        ).all()

    # def get_by_working_status_and_cap(self, capacity: float, working_status: str) -> Optional[CoolingCapacity]:
    #     """根据冷风机ID和工况获取冷量映射记录"""
    #     return self.session.query(CoolingCapacity).filter(
    #         CoolingCapacity.capacity  cooler_id,
    #         CoolingCapacity.working_status == working_status,
    #         CoolingCapacity.is_deleted == 0
    #     ).first()
    
    def delete_by_cooler_id(self, cooler_id: int) -> bool:
        """删除指定冷风机ID的所有冷量映射记录"""
        query = self.session.query(CoolingCapacity).filter(
            CoolingCapacity.cooler_id == cooler_id,
            CoolingCapacity.is_deleted == 0
        )
        
        count = query.update({
            CoolingCapacity.is_deleted: 1
        })
        
        self.session.commit()
        return count > 0


class SCQuantRepository(BaseRepository[SCQuant]):
    """工况修正系数仓库类"""
    
    def __init__(self, session: Session):
        super().__init__(session, SCQuant)
    
    def get_by_evaporating_temp_and_delta_t(
        self, 
        evaporating_temp: float, 
        delta_t: float
    ) -> Optional[SCQuant]:
        """根据蒸发温度和温差获取工况修正系数"""
        return self.session.query(SCQuant).filter(
            SCQuant.evaporating_temp == evaporating_temp,
            SCQuant.delta_t == delta_t,
            SCQuant.is_deleted == 0
        ).first()
    
    def search(
        self, 
        min_evaporating_temp: Optional[float] = None, 
        max_evaporating_temp: Optional[float] = None,
        min_delta_t: Optional[float] = None, 
        max_delta_t: Optional[float] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[SCQuant]:
        """搜索工况修正系数，支持蒸发温度和温差范围过滤"""
        query = self.session.query(SCQuant).filter(SCQuant.is_deleted == 0)
        
        if min_evaporating_temp is not None:
            query = query.filter(SCQuant.evaporating_temp >= min_evaporating_temp)
        
        if max_evaporating_temp is not None:
            query = query.filter(SCQuant.evaporating_temp <= max_evaporating_temp)
        
        if min_delta_t is not None:
            query = query.filter(SCQuant.delta_t >= min_delta_t)
        
        if max_delta_t is not None:
            query = query.filter(SCQuant.delta_t <= max_delta_t)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_evaporating_temp_range(
        self, 
        min_temp: float, 
        max_temp: float,
        skip: int = 0, 
        limit: int = 100
    ) -> List[SCQuant]:
        """根据蒸发温度范围获取工况修正系数"""
        query = self.session.query(SCQuant).filter(
            SCQuant.evaporating_temp >= min_temp,
            SCQuant.evaporating_temp <= max_temp,
            SCQuant.is_deleted == 0
        )
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_delta_t_range(
        self, 
        min_delta_t: float, 
        max_delta_t: float,
        skip: int = 0, 
        limit: int = 100
    ) -> List[SCQuant]:
        """根据温差范围获取工况修正系数"""
        query = self.session.query(SCQuant).filter(
            SCQuant.delta_t >= min_delta_t,
            SCQuant.delta_t <= max_delta_t,
            SCQuant.is_deleted == 0
        )
        
        return query.offset(skip).limit(limit).all()