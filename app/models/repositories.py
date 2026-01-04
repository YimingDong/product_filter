from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Optional, List, Dict, Any
from datetime import datetime

# 导入所有模型
from app.models.dao import (
    Cooler,
    CoolingCapacity,
    SCQuant
)
from app.utils.enums import Refrigerant

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


# class ImageRepository(BaseRepository[Image]):
#     """图片仓库类"""
#
#     def __init__(self, session: Session):
#         super().__init__(session, Image)
#
#     def get_by_related_id(self, related_id: str, skip: int = 0, limit: int = 100) -> List[Image]:
#         """根据关联ID获取图片"""
#         return self.search(related_id=related_id, skip=skip, limit=limit)
#
#     def delete_by_related_id(self, related_id: str) -> bool:
#         """删除指定关联ID的所有图片"""
#         query = self.session.query(Image).filter(
#             Image.related_id == related_id,
#             Image.is_deleted == 0
#         )
#
#         count = query.update({
#             Image.is_deleted: 1,
#             Image.deleted_at: datetime.now()
#         })
#
#         self.session.commit()
#         return count > 0


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

    def get_by_cooler_ids(self, cooler_id: List[str]) -> List[Cooler]:
        """根据冷风机ID获取记录"""
        return self.session.query(Cooler).filter(
            Cooler.model.in_(cooler_id),
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
    
    def get_by_working_status_and_refrigerant(self, working_status: str, refrigerant: str = Refrigerant.R404A.value) -> List[CoolingCapacity]:
        """根据冷风机ID和工况获取冷量映射记录"""
        return self.session.query(CoolingCapacity).filter(
            CoolingCapacity.working_status == working_status,
            CoolingCapacity.refrigerant == refrigerant,
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