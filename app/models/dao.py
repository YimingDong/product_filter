from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 导入基础模型类
from app.models.database import Base


class Condenser(Base):
    """冷凝机模型"""
    __tablename__ = "condenser"
    __table_args__ = {
        'comment': '冷凝机'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    model_code = Column(String(100), nullable=False, unique=True, comment='型号编码')
    applicable_temperature = Column(Integer, nullable=False, comment='适用库温')
    compressor_count = Column(Integer, nullable=False, comment='压缩机数量')
    fan_count = Column(Integer, nullable=False, comment='风机数量')
    suction_inlet = Column(Float, nullable=False, comment='吸气进口')
    liquid_supply_interface = Column(Float, nullable=False, comment='液供接口')
    length = Column(Float, nullable=False, comment='长')
    width = Column(Float, nullable=False, comment='宽')
    height = Column(Float, nullable=False, comment='高')
    installation_height = Column(Float, nullable=False, comment='安装尺寸高')
    installation_width = Column(Float, nullable=False, comment='安装尺寸宽')
    range = Column(Float, nullable=False, comment='射程')
    coil_defrost_power = Column(Float, nullable=False, comment='盘管化霜功率')
    water_pan_defrost_power = Column(Float, nullable=False, comment='水盘化霜功率')
    refrigeration_capacity = Column(Float, nullable=False, comment='制冷量')
    weight = Column(Float, nullable=False, comment='重量')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')


class PowerSupply(Base):
    """电源模型"""
    __tablename__ = "power_supply"
    __table_args__ = {
        'comment': '电源'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    model_code = Column(String(100), nullable=False, unique=True, comment='型号编码')
    voltage = Column(Float, nullable=False, comment='电压')
    current = Column(Float, nullable=False, comment='电流')
    power = Column(Float, nullable=False, comment='功率')
    plug_type = Column(Integer, nullable=False, comment='插头类型')
    weight = Column(Float, nullable=False, comment='重量')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')


class Compressor(Base):
    """压缩机模型"""
    __tablename__ = "compressor"
    __table_args__ = {
        'comment': '压缩机'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    model_code = Column(String(100), nullable=False, unique=True, comment='型号编码')
    type = Column(Integer, nullable=False, comment='类型')
    compression_ratio = Column(Float, nullable=False, comment='压缩比')
    working_pressure = Column(Float, nullable=False, comment='工作压力')
    working_flow = Column(Float, nullable=False, comment='工作流量')
    working_efficiency = Column(Float, nullable=False, comment='工作效率')
    installation_height = Column(Float, nullable=False, comment='安装尺寸高')
    installation_width = Column(Float, nullable=False, comment='安装尺寸宽')
    installation_depth = Column(Float, nullable=False, comment='安装尺寸深')
    weight = Column(Float, nullable=False, comment='重量')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')


class Fan(Base):
    """风机模型"""
    __tablename__ = "fan"
    __table_args__ = {
        'comment': '风机'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    name = Column(String(100), nullable=False, comment='名称')
    model_code = Column(String(100), nullable=False, unique=True, comment='型号编码')
    type = Column(Integer, nullable=False, comment='类型')
    working_voltage = Column(Float, nullable=False, comment='工作电压')
    working_power = Column(Float, nullable=False, comment='工作功率')
    installation_height = Column(Float, nullable=False, comment='安装尺寸高')
    installation_width = Column(Float, nullable=False, comment='安装尺寸宽')
    installation_depth = Column(Float, nullable=False, comment='安装尺寸深')
    weight = Column(Float, nullable=False, comment='重量')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')


class Evaporator(Base):
    """蒸发器模型"""
    __tablename__ = "evaporator"
    __table_args__ = {
        'comment': '蒸发器'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    name = Column(String(100), nullable=False, comment='名称')
    model_code = Column(String(100), nullable=False, unique=True, comment='型号编码')
    type = Column(Integer, nullable=False, comment='类型')
    working_voltage = Column(Float, nullable=False, comment='工作电压')
    working_power = Column(Float, nullable=False, comment='工作功率')
    installation_height = Column(Float, nullable=False, comment='安装尺寸高')
    installation_width = Column(Float, nullable=False, comment='安装尺寸宽')
    installation_depth = Column(Float, nullable=False, comment='安装尺寸深')
    weight = Column(Float, nullable=False, comment='重量')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')


class Image(Base):
    """图片模型"""
    __tablename__ = "image"
    __table_args__ = {
        'comment': '图片'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增主键')
    related_id = Column(String(255), nullable=False, comment='关联id')
    image_url = Column(String(255), nullable=False, comment='图片URL')
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    is_deleted = Column(Integer, default=0, comment='是否逻辑删除')
    deleted_at = Column(DateTime, nullable=True, comment='删除时间')
