from sqlalchemy import Column, Integer, String, Float, DateTime, Index, BigInteger
from datetime import datetime

# 导入基础模型类
from app.models.database import Base


# class Image(Base):
#     """图片模型"""
#     __tablename__ = "image"
#     __table_args__ = {
#         'comment': '图片'
#     }
#
#     id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
#     related_id = Column(String(255), nullable=False, comment='关联id')
#     image_url = Column(String(255), nullable=False, comment='图片URL')
#     created_at = Column(DateTime, default=datetime.now, comment='创建时间')
#     updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
#     is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
#     deleted_at = Column(DateTime, nullable=True, comment='删除时间')
#
#     def to_pydantic(self):
#         """转换为Pydantic模型实例"""
#         from app.schemas.equipment import ImageResponse
#         return ImageResponse(
#             id=self.id,
#             related_id=self.related_id,
#             image_url=self.image_url,
#             created_at=self.created_at,
#             updated_at=self.updated_at,
#             is_deleted=self.is_deleted,
#             deleted_at=self.deleted_at
#         )


class Cooler(Base):
    """冷风机模型"""
    __tablename__ = "cooler"
    __table_args__ = {
        'comment': '冷风机'
    }

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    heat_exchange_area = Column(Float, nullable=False, comment='换热面积')
    tube_volumn = Column(Float, nullable=True, comment='管容(dm³)')
    air_flow_rate = Column(Float, nullable=True, comment='风量(m³/h)')
    total_fan_power = Column(String(100), nullable=True, comment='电机总功率')
    total_fan_current = Column(String(100), nullable=True, comment='电机总电流')
    air_flow = Column(String(255), nullable=True, comment='射程')
    defrost_power = Column(Float, nullable=True, comment='化霜总功率')
    pipe_dia = Column(String(100), nullable=True, comment='接口管径(进/出Φmm）')
    noise = Column(Float, nullable=True, comment='噪音(dB)(5米)')
    weight = Column(Float, nullable=True, comment='重量')
    model = Column(String(100), nullable=True, comment='型号')
    fin_spacing = Column(String(100), nullable=True, comment='翅片间距')
    series = Column(String(100), nullable=True, comment='系列')
    create_time = Column(DateTime, default=datetime.now, nullable=False, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    is_deleted = Column(Integer, default=0, nullable=True, comment='逻辑删除')
    comment = Column(String(255), nullable=True, comment='参数注释')

    def to_pydantic(self):
        """转换为Pydantic模型实例"""
        from app.schemas.equipment import CoolerResponse
        return CoolerResponse(
            id=self.id,
            heat_exchange_area=self.heat_exchange_area,
            tube_volumn=self.tube_volumn,
            air_flow_rate=self.air_flow_rate,
            total_fan_power=self.total_fan_power,
            total_fan_current=self.total_fan_current,
            air_flow=self.air_flow,
            defrost_water_flow_rate=self.defrost_power,
            pipe_dia=self.pipe_dia,
            noise=self.noise,
            weight=self.weight,
            model=self.model,
            fin_spacing=self.fin_spacing,
            series=self.series,
            comment=self.comment,
            is_deleted=self.is_deleted
        )


class CoolingCapacity(Base):
    """冷量映射表模型"""
    __tablename__ = "cooling_capacity"
    __table_args__ = {
        'comment': '冷量映射表'
    }

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    cooler_id = Column(String(255), nullable=False, comment='冷风机的id')
    working_status = Column(String(100), nullable=False, comment='工况：SC1;SC2;SC3;SC4;SC5')
    refrigerant = Column(String(100), nullable=False, comment='制冷剂')
    capacity = Column(Float, nullable=False, comment='制冷量（KW）')
    created_time = Column(DateTime, default=datetime.now, nullable=True, comment='创建时间')
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True, comment='更新时间')
    is_deleted = Column(Integer, default=0, nullable=True, comment='逻辑删除')

    def to_pydantic(self):
        """转换为Pydantic模型实例"""
        from app.schemas.equipment import CoolingCapacityResponse
        return CoolingCapacityResponse(
            id=self.id,
            cooler_id=self.cooler_id,
            working_status=self.working_status,
            capacity=self.capacity,
            created_time=self.created_time,
            updated_time=self.updated_time,
            is_deleted=self.is_deleted
        )


class SCQuant(Base):
    """工况修正系数模型"""
    __tablename__ = "sc_quant"
    __table_args__ = {
        'comment': '工况修正系数'
    }

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='自增主键')
    evaporating_temp = Column(Float, nullable=False, comment='蒸发温度')
    delta_t = Column(Float, nullable=False, comment='温差')
    quant = Column(Float, nullable=True, comment='修正系数')
    create_time = Column(DateTime, default=datetime.now, nullable=False, comment='创建时间')
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False, comment='更新时间')
    is_deleted = Column(Integer, default=0, nullable=True, comment='逻辑删除')

    def to_pydantic(self):
        """转换为Pydantic模型实例"""
        from app.schemas.equipment import SCQuantResponse
        return SCQuantResponse(
            id=self.id,
            evaporating_temp=self.evaporating_temp,
            delta_t=self.delta_t,
            quant=self.quant,
            create_time=self.create_time,
            update_time=self.update_time,
            is_deleted=self.is_deleted
        )
